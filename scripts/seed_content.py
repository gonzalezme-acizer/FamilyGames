#!/usr/bin/env python3
"""Carga idempotente del catálogo español en Supabase.

Uso:
  python3 scripts/seed_content.py          # muestra cantidades
  python3 scripts/seed_content.py --apply  # escribe en Supabase
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_local_env():
    path = ROOT / ".env.local"
    if not path.exists():
        return
    for line in path.read_text("utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_local_env()
sys.path.insert(0, str(ROOT))
import server as game  # noqa: E402

URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SECRET = os.environ.get("SUPABASE_SECRET_KEY", "")


def request(method, path, payload=None, prefer=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"apikey": SECRET, "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    req = urllib.request.Request(f"{URL}/rest/v1/{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
            return json.loads(body) if body else []
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8", "replace")) from exc


def stable_key(game_id, payload):
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{game_id}:{canonical}".encode("utf-8")).hexdigest()


def chunks(items, size=100):
    for index in range(0, len(items), size):
        yield items[index:index + size]


def all_rows(path, page_size=1000):
    rows, offset = [], 0
    while True:
        separator = "&" if "?" in path else "?"
        batch = request("GET", f"{path}{separator}limit={page_size}&offset={offset}")
        rows.extend(batch)
        if len(batch) < page_size:
            return rows
        offset += page_size


def main():
    cards = []
    for game_id, entries in game.CONTENT.items():
        for payload in entries:
            cards.append({
                "game": game_id,
                "difficulty": payload.get("difficulty", "medio"),
                "category": payload.get("category"),
                "content_key": stable_key(game_id, payload),
                "source_locale": "es",
                "payload": payload,
                "active": True,
            })
    by_game = {game_id: len(entries) for game_id, entries in game.CONTENT.items()}
    print(json.dumps({"total": len(cards), "games": by_game}, ensure_ascii=False, indent=2))
    if "--apply" not in sys.argv:
        print("Vista previa solamente. Agregá --apply para escribir en Supabase.")
        return
    if not URL or not SECRET.startswith("sb_secret_"):
        raise SystemExit("Configurá SUPABASE_URL y una SUPABASE_SECRET_KEY nueva en .env.local")
    imported = 0
    wanted_keys = {item["content_key"] for item in cards}
    for batch in chunks(cards):
        rows = request(
            "POST", "content_cards?on_conflict=content_key&select=id,content_key",
            batch, "resolution=merge-duplicates,return=representation",
        )
        payload_by_key = {item["content_key"]: item["payload"] for item in batch}
        translations = [{
            "card_id": row["id"], "locale": "es", "payload": payload_by_key[row["content_key"]],
            "category": next(item["category"] for item in batch if item["content_key"] == row["content_key"]),
            "reviewed": True,
        } for row in rows]
        request(
            "POST", "content_card_translations?on_conflict=card_id,locale",
            translations, "resolution=merge-duplicates",
        )
        imported += len(rows)
        print(f"Importadas {imported}/{len(cards)}")
    if "--sync" in sys.argv:
        stored = all_rows("content_cards?source_locale=eq.es&select=id,content_key")
        obsolete = [row["id"] for row in stored if row["content_key"] not in wanted_keys]
        for batch in chunks(obsolete):
            encoded = ",".join(batch)
            request("DELETE", f"content_cards?id=in.({encoded})")
        print(f"Eliminadas {len(obsolete)} tarjetas obsoletas o variantes repetidas.")
    print("Catálogo español cargado correctamente.")


if __name__ == "__main__":
    main()
