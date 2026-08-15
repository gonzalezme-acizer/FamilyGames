"""API multissala de Familia en Juego Cloud sobre Supabase."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import time
from http.server import BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import server as game  # noqa: E402

# El motor local no debe escribir archivos ni mantener conexiones SSE en Vercel.
game.save_state = lambda: None
game.notify = lambda: None

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "")
PUBLIC_APP_URL = os.environ.get("PUBLIC_APP_URL", "").rstrip("/")
SUPPORTED_LOCALES = {"es", "pt-BR", "en"}
BASE_CONTENT = game.CONTENT
CONTENT_CACHE = {}
PLAYER_ACTIONS = {
    "answer", "passPrompt", "requestHint", "chooseWhoSaidPhrase",
    "guessWhoSaid", "requestWhoAmIHint", "answerLie", "answerSong",
    "bombAction", "guessBomb", "buzzMystery", "guessMystery",
}


class ApiError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def token_hash(value):
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def db_request(method, path, payload=None, prefer=None):
    if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
        raise ApiError("Falta configurar SUPABASE_SECRET_KEY en el backend de Vercel.", 503)
    raw = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"apikey": SUPABASE_SECRET_KEY, "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    request = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{path}", data=raw, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            body = response.read()
            return json.loads(body) if body else []
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise ApiError(f"Supabase rechazó la operación: {detail[:300]}", 502) from exc
    except urllib.error.URLError as exc:
        raise ApiError("No se pudo conectar con Supabase.", 502) from exc


def room_by_code(code):
    safe = urllib.parse.quote(str(code or "").strip().upper())
    rows = db_request("GET", f"rooms?code=eq.{safe}&select=id,code,host_secret_hash,status,locale")
    if not rows:
        raise ApiError("La sala no existe o ya venció.", 404)
    return rows[0]


def state_row(room_id):
    rows = db_request("GET", f"room_states?room_id=eq.{room_id}&select=version,state")
    if not rows:
        raise ApiError("La sala todavía no tiene estado de juego.", 404)
    return rows[0]


def verify_host(room, token):
    return bool(token) and secrets.compare_digest(room["host_secret_hash"], token_hash(token))


def verify_player(room_id, player_id, token):
    if not player_id or not token:
        return False
    pid = urllib.parse.quote(str(player_id))
    rows = db_request("GET", f"players?id=eq.{pid}&room_id=eq.{room_id}&select=connection_token_hash")
    return bool(rows) and secrets.compare_digest(rows[0]["connection_token_hash"], token_hash(token))


def set_engine_state(state):
    game.STATE = json.loads(json.dumps(state))
    return game.STATE


def paged_rows(table, query, page_size=1000):
    rows, offset = [], 0
    while True:
        separator = "&" if "?" in query else "?"
        page = db_request("GET", f"{table}{query}{separator}limit={page_size}&offset={offset}")
        rows.extend(page)
        if len(page) < page_size:
            return rows
        offset += page_size


def content_for_locale(locale):
    locale = locale if locale in SUPPORTED_LOCALES else "es"
    cached = CONTENT_CACHE.get(locale)
    if cached and time.time() - cached[0] < 300:
        return cached[1]
    cards = paged_rows("content_cards", "?active=eq.true&select=id,game,difficulty,category,payload")
    translations = paged_rows(
        "content_card_translations",
        f"?locale=eq.{urllib.parse.quote(locale)}&select=card_id,category,payload",
    )
    if locale != "es" and not translations:
        translations = paged_rows(
            "content_card_translations", "?locale=eq.es&select=card_id,category,payload"
        )
    translated = {item["card_id"]: item for item in translations}
    result = {}
    for card in cards:
        translation = translated.get(card["id"])
        payload = dict((translation or {}).get("payload") or card.get("payload") or {})
        payload.setdefault("difficulty", card.get("difficulty"))
        payload.setdefault("category", (translation or {}).get("category") or card.get("category"))
        result.setdefault(card["game"], []).append(payload)
    if not result:
        result = BASE_CONTENT
    CONTENT_CACHE[locale] = (time.time(), result)
    return result


def public_payload(state, player_id=None):
    set_engine_state(state)
    return game.public_state(player_id)


def mutate_room(room, action, attempts=4):
    for _ in range(attempts):
        current = state_row(room["id"])
        set_engine_state(current["state"])
        game.CONTENT = content_for_locale(room.get("locale", "es"))
        game.handle_action(action)
        next_state = game.STATE
        next_version = int(current["version"]) + 1
        rows = db_request(
            "PATCH",
            f"room_states?room_id=eq.{room['id']}&version=eq.{current['version']}&select=version,state",
            {"version": next_version, "state": next_state},
            "return=representation",
        )
        if rows:
            return rows[0]["state"]
    raise ApiError("La sala recibió acciones simultáneas. Intentá nuevamente.", 409)


def create_room(locale="es"):
    locale = locale if locale in SUPPORTED_LOCALES else "es"
    host_token = secrets.token_urlsafe(32)
    for _ in range(12):
        code = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        try:
            rows = db_request(
                "POST", "rooms?select=id,code",
                {"code": code, "host_secret_hash": token_hash(host_token), "locale": locale},
                "return=representation",
            )
            room = rows[0]
            state = game.fresh_state()
            state["room"] = code
            state["locale"] = locale
            db_request("POST", "room_states", {"room_id": room["id"], "version": 1, "state": state})
            return room, state, host_token
        except ApiError as exc:
            if "duplicate" not in str(exc).lower():
                raise
    raise ApiError("No se pudo generar un código de sala único.", 503)


class handler(BaseHTTPRequestHandler):
    def _json(self, payload, status=200):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _body(self):
        try:
            return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except (ValueError, json.JSONDecodeError) as exc:
            raise ApiError("JSON inválido.") from exc

    def _base_url(self):
        if PUBLIC_APP_URL:
            return PUBLIC_APP_URL
        host = self.headers.get("x-forwarded-host") or self.headers.get("host") or "localhost"
        proto = self.headers.get("x-forwarded-proto") or "https"
        return f"{proto}://{host}"

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            if parsed.path == "/api/health":
                return self._json({"ok": True, "project": "familia-en-juego-cloud", "database": bool(SUPABASE_SECRET_KEY)})
            if parsed.path != "/api/state":
                raise ApiError("Ruta inexistente.", 404)
            room = room_by_code(query.get("room", [""])[0])
            player_id = query.get("player", [None])[0]
            player_token = self.headers.get("x-player-token")
            authorized_player = player_id if verify_player(room["id"], player_id, player_token) else None
            host_ok = verify_host(room, self.headers.get("x-host-token"))
            state = state_row(room["id"])["state"]
            locale = room.get("locale", state.get("locale", "es"))
            state["locale"] = locale
            localized_content = content_for_locale(locale)
            base = self._base_url()
            return self._json({
                "ok": True,
                "state": public_payload(state, authorized_player if authorized_player else None if host_ok else "__spectator__"),
                "contentStats": {key: len(value) for key, value in localized_content.items()},
                "joinUrl": f"{base}/?join=1&room={room['code']}",
            })
        except ApiError as exc:
            return self._json({"ok": False, "error": str(exc)}, exc.status)

    def do_POST(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/api/rooms":
                body = self._body()
                room, state, host_token = create_room(body.get("locale", "es"))
                return self._json({"ok": True, "room": room["code"], "hostToken": host_token, "state": public_payload(state)}, 201)
            if parsed.path != "/api/action":
                raise ApiError("Ruta inexistente.", 404)
            body = self._body()
            room = room_by_code(body.get("room"))
            action = body.get("action") or {}
            kind = action.get("type")
            host_ok = verify_host(room, self.headers.get("x-host-token"))
            player_ok = verify_player(room["id"], action.get("playerId"), self.headers.get("x-player-token"))
            new_player_token = None
            if kind == "join":
                new_player_token = secrets.token_urlsafe(28)
                action["playerId"] = str(uuid.uuid4())
            elif kind in PLAYER_ACTIONS:
                if not player_ok:
                    raise ApiError("El celular perdió su autorización. Volvé a entrar a la sala.", 401)
            elif not host_ok:
                raise ApiError("Esta acción requiere autorización del anfitrión.", 401)
            state = mutate_room(room, action)
            if kind == "join":
                joined = next((item for item in state.get("players", []) if item.get("id") == action["playerId"]), None)
                if not joined:
                    raise ApiError("No se pudo registrar al participante.", 500)
                db_request(
                    "POST", "players?on_conflict=id",
                    {
                        "id": joined["id"], "room_id": room["id"], "name": joined["name"],
                        "team_id": joined.get("teamId"), "connection_token_hash": token_hash(new_player_token),
                    },
                    "resolution=merge-duplicates",
                )
                return self._json({"ok": True, "state": public_payload(state, joined["id"]), "playerId": joined["id"], "playerToken": new_player_token})
            return self._json({"ok": True, "state": public_payload(state, action.get("playerId") if player_ok else None)})
        except ApiError as exc:
            return self._json({"ok": False, "error": str(exc)}, exc.status)
        except Exception as exc:
            return self._json({"ok": False, "error": f"Error inesperado: {type(exc).__name__}"}, 500)
