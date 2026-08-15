#!/usr/bin/env python3
"""Familia en Juego: tiny dependency-free LAN server."""

from __future__ import annotations

import json
import mimetypes
import os
import queue
import random
import re
import socket
import ssl
import string
import threading
import time
import unicodedata
import urllib.parse
import urllib.request
import shutil
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
DATA_DIR = Path(os.environ.get("FAMILIA_DATA_DIR", ROOT))
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = DATA_DIR / "game-state.json"
CONTENT_FILE = DATA_DIR / "content.json"
SING_EXCERPTS_FILE = DATA_DIR / "just-sing-excerpts.json"
if DATA_DIR != ROOT and not CONTENT_FILE.exists():
    shutil.copy2(ROOT / "content.json", CONTENT_FILE)
LOCK = threading.RLock()
SUBSCRIBERS: list[queue.Queue] = []

TRIVIA_CATEGORIES = [
    "Entretenimiento y Música", "Historia", "Geografía",
    "Literatura", "Deportes", "Conocimientos generales",
]
TRIVIA_FINISH = 100
TRIVIA_SPECIALS = {
    8: "back4", 15: "forward4", 22: "joker",
    31: "back4", 38: "forward4", 45: "joker",
    54: "back4", 61: "forward4", 68: "joker",
    77: "back4", 84: "forward4", 91: "joker",
}


def fresh_state():
    return {
        "room": "".join(random.choice(string.ascii_uppercase) for _ in range(4)),
        "players": [],
        "teams": [
            {"id": "sol", "name": "Los Rayos", "color": "#ffca3a", "score": 0, "position": 0, "stars": {}, "finished": False},
            {"id": "luna", "name": "Los Cometas", "color": "#7b61ff", "score": 0, "position": 0, "stars": {}, "finished": False},
        ],
        "game": None,
        "round": 0,
        "activeTeam": "sol",
        "activePlayer": None,
        "prompt": None,
        "answer": None,
        "timerEnds": None,
        "status": "lobby",
        "usedPrompts": {},
        "roundCategory": None,
        "lastRoll": None,
        "battle": None,
        "passesUsed": 0,
        "helpsUsed": 0,
        "revealedHint": None,
        "turnCorrect": 0,
        "turnRemainingMs": None,
        "lastTriviaPlayer": {},
        "mimicaOrder": [],
        "mimicaTurnIndex": 0,
        "mimicaCurrentRound": 1,
        "challengePlayerIndex": {},
        "whoSaidPlayers": [],
        "whoSaidChoices": {},
        "whoSaidSelected": {},
        "whoSaidOrder": [],
        "whoSaidIndex": 0,
        "whoSaidGuesses": {},
        "whoSaidTeamPoints": {},
        "whoSaidCurrentRound": 1,
        "whoAmIOrder": [],
        "whoAmIIndex": 0,
        "whoAmICurrentRound": 1,
        "whoAmIMaxRounds": 10,
        "whoAmIHintsUsed": 0,
        "whoAmIPoints": {},
        "whoAmIAssignments": {},
        "whoAmIGuessed": [],
        "truthRepresentatives": {},
        "truthAnswers": {},
        "truthPlayerIndex": {},
        "truthOutcome": None,
        "singPhase": None,
        "singOptions": [],
        "singCorrect": None,
        "singAnswers": {},
        "singPhaseWins": {},
        "singWinnerOrder": [],
        "singFinalistTeam": None,
        "singCard": None,
        "singAward": 0,
        "singMatchPoints": {},
        "mysteryCard": None,
        "mysteryClueIndex": 0,
        "mysteryLockedPlayers": [],
        "mysteryBuzzPlayer": None,
        "mysteryRoundWinner": None,
        "bombCard": None, "bombOrder": [], "bombIndex": 0, "bombHolder": None,
        "bombEliminated": [], "bombPowerUsed": {}, "bombHints": [],
        "bombRoundWins": {}, "bombRoundWinner": None, "bombGuessPlayer": None,
        "lastAnswerCorrect": None,
        "winnerTeam": None,
        "activity": ["¡Sala lista para recibir a la familia!"],
    }


def load_json(path, default):
    try:
        return json.loads(path.read_text("utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


SING_EXCERPTS = load_json(SING_EXCERPTS_FILE, {})


def lyric_key(card):
    return f"{card.get('artist', '').strip().casefold()}|{card.get('title', '').strip().casefold()}"


def normalized_words(value):
    value = unicodedata.normalize("NFKD", value or "")
    return re.sub(r"[^a-z0-9 ]", "", value.encode("ascii", "ignore").decode().lower()).split()


def choose_lyric_excerpt(lyrics, title):
    """Keep one recognizable, title-free microfragment; never persist full lyrics."""
    title_words = set(normalized_words(title))
    candidates = []
    counts = {}
    for raw_line in (lyrics or "").splitlines():
        line = re.sub(r"^\s*\[\d{1,2}:\d{2}(?:\.\d+)?\]\s*", "", raw_line).strip()
        line = re.sub(r"^\s*\[[^]]+\]\s*$", "", line).strip()
        words = line.split()
        if len(words) < 4:
            continue
        if title_words and title_words.issubset(set(normalized_words(line))):
            continue
        if len(words) > 10:
            line = " ".join(words[:10]).rstrip(",;:-")
        fingerprint = " ".join(normalized_words(line))
        if not fingerprint:
            continue
        counts[fingerprint] = counts.get(fingerprint, 0) + 1
        candidates.append((line, fingerprint))
    if not candidates:
        return ""
    # Repeated lines are normally part of the chorus and therefore easiest to recognize.
    line, _ = max(candidates, key=lambda item: (counts[item[1]], len(item[0].split())))
    return f"…{line.strip(' …')}…"


def fetch_lyric_excerpt(card):
    key = lyric_key(card)
    if key in SING_EXCERPTS:
        return SING_EXCERPTS[key]
    query = urllib.parse.urlencode({"track_name": card.get("title", ""), "artist_name": card.get("artist", "")})
    request = urllib.request.Request(
        f"https://lrclib.net/api/search?{query}",
        headers={"User-Agent": "FamiliaEnJuego/1.0 (local family game)"},
    )
    try:
        cert_file = Path("/etc/ssl/cert.pem")
        ssl_context = ssl.create_default_context(cafile=str(cert_file) if cert_file.exists() else None)
        with urllib.request.urlopen(request, timeout=7, context=ssl_context) as response:
            matches = json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return ""
    wanted_title = set(normalized_words(card.get("title")))
    wanted_artist = set(normalized_words(card.get("artist")))
    for match in matches[:8]:
        found_title = set(normalized_words(match.get("trackName")))
        found_artist = set(normalized_words(match.get("artistName")))
        if not wanted_title.intersection(found_title) or not wanted_artist.intersection(found_artist):
            continue
        excerpt = choose_lyric_excerpt(match.get("plainLyrics") or match.get("syncedLyrics"), card.get("title"))
        if excerpt:
            SING_EXCERPTS[key] = excerpt
            SING_EXCERPTS_FILE.write_text(json.dumps(SING_EXCERPTS, ensure_ascii=False, indent=2), "utf-8")
            return excerpt
    return ""


def expand_trivia_facts(catalog):
    """Convert each compact fact into two distinct multiple-choice questions."""
    templates = {
        "Entretenimiento y Música": ("¿Quién está principalmente asociado con «{a}»?", "¿Con cuál de estas obras está asociado {b}?"),
        "Historia": ("¿En qué año ocurrió {a}?", "¿Cuál de estos acontecimientos ocurrió en {b}?"),
        "Geografía": ("¿Qué ciudad funciona como capital de {a}?", "¿De qué país es capital {b}?"),
        "Literatura": ("¿Quién escribió «{a}»?", "¿Cuál de estas obras escribió {b}?"),
        "Deportes": ("¿Quién consiguió este logro: {a}?", "¿Qué logro corresponde a {b}?"),
        "Conocimientos generales": ("¿Qué concepto corresponde a esta definición: {b}?", "¿Cuál es la definición correcta de {a}?"),
    }
    questions = []
    for category, facts in catalog.items():
        forward, reverse = templates[category]
        for index, (a, b, difficulty) in enumerate(facts):
            peers = [facts[(index + jump) % len(facts)] for jump in (1, 7, 17)]
            if category == "Conocimientos generales":
                forward_options, reverse_options = [a] + [p[0] for p in peers], [b] + [p[1] for p in peers]
            else:
                forward_options, reverse_options = [b] + [p[1] for p in peers], [a] + [p[0] for p in peers]
            questions.extend([
                {"category": category, "difficulty": difficulty, "question": forward.format(a=a, b=b), "options": forward_options, "correct": 0},
                {"category": category, "difficulty": difficulty, "question": reverse.format(a=a, b=b), "options": reverse_options, "correct": 0},
            ])
    return questions


STATE = load_json(STATE_FILE, fresh_state())
CONTENT = load_json(CONTENT_FILE, {})
TRIVIA_FILE = ROOT / "trivia-120.json"
if TRIVIA_FILE.exists():
    CONTENT["trivia"] = load_json(TRIVIA_FILE, CONTENT.get("trivia", []))
TRIVIA_EXPANSION_FILE = ROOT / "trivia-expansion.json"
if TRIVIA_EXPANSION_FILE.exists():
    CONTENT["trivia"].extend(expand_trivia_facts(load_json(TRIVIA_EXPANSION_FILE, {})))
MIMICA_FILE = ROOT / "mimica-250.json"
if MIMICA_FILE.exists():
    mimica_catalog = load_json(MIMICA_FILE, {})
    CONTENT["mimica"] = [
        {
            "category": category,
            "difficulty": "facil" if index < 9 else "medio" if index < 17 else "dificil",
            "prompt": prompt,
        }
        for category, prompts in mimica_catalog.items()
        for index, prompt in enumerate(prompts)
    ]
EXTRA_FILE = ROOT / "extra-prompts.json"
if EXTRA_FILE.exists():
    for game, cards in load_json(EXTRA_FILE, {}).items():
        if game == "mimica" and MIMICA_FILE.exists():
            continue
        existing = {item.get("question") or item.get("prompt") for item in CONTENT.setdefault(game, [])}
        CONTENT[game].extend(item for item in cards if (item.get("question") or item.get("prompt")) not in existing)
try:
    from desafios_catalog import build_challenges
    CONTENT["rapido"] = build_challenges()
except ImportError:
    pass
try:
    from quien_dijo_catalog import build_who_said
    CONTENT["quien_dijo"] = build_who_said()
except ImportError:
    pass
try:
    from quien_soy_catalog import build_who_am_i
    CONTENT["quien_soy"] = build_who_am_i()
except ImportError:
    pass
try:
    from tres_verdades_catalog import build_three_truths
    CONTENT["tres_verdades"] = build_three_truths()
except ImportError:
    pass
try:
    from just_sing_catalog import build_just_sing
    CONTENT["just_sing"] = build_just_sing()
except (ImportError, ValueError):
    pass
try:
    from incognito_catalog import build_incognito
    CONTENT["incognito"] = build_incognito()
except (ImportError, ValueError):
    pass
try:
    from bomba_catalog import build_bomb_riddles
    CONTENT["bomba"] = build_bomb_riddles()
except (ImportError, ValueError):
    pass
try:
    from catalog_expansion import (
        expand_drawing, expand_three_truths, expand_trivia, expand_who_said,
        new_mimica_cards,
    )
    CONTENT["trivia"].extend(expand_trivia(CONTENT["trivia"]))
    CONTENT["mimica"].extend(new_mimica_cards(CONTENT["mimica"]))
    CONTENT["dibujo"].extend(expand_drawing(CONTENT["dibujo"]))
    CONTENT["quien_dijo"].extend(expand_who_said(CONTENT["quien_dijo"]))
    CONTENT["tres_verdades"].extend(expand_three_truths(CONTENT["tres_verdades"]))
except (ImportError, ValueError, KeyError):
    pass
for team in STATE.get("teams", []):
    team.setdefault("stars", {})
    team.setdefault("finished", False)
STATE.setdefault("mimicaOrder", [])
STATE.setdefault("mimicaTurnIndex", 0)
STATE.setdefault("mimicaCurrentRound", 1)
STATE.setdefault("challengePlayerIndex", {})
STATE.setdefault("whoSaidPlayers", [])
STATE.setdefault("whoSaidChoices", {})
STATE.setdefault("whoSaidSelected", {})
STATE.setdefault("whoSaidOrder", [])
STATE.setdefault("whoSaidIndex", 0)
STATE.setdefault("whoSaidGuesses", {})
STATE.setdefault("whoSaidTeamPoints", {})
STATE.setdefault("whoSaidCurrentRound", 1)
STATE.setdefault("whoAmIOrder", [])
STATE.setdefault("whoAmIIndex", 0)
STATE.setdefault("whoAmICurrentRound", 1)
STATE.setdefault("whoAmIMaxRounds", 10)
STATE.setdefault("whoAmIHintsUsed", 0)
STATE.setdefault("whoAmIPoints", {})
STATE.setdefault("whoAmIAssignments", {})
STATE.setdefault("whoAmIGuessed", [])
STATE.setdefault("truthRepresentatives", {})
STATE.setdefault("truthAnswers", {})
STATE.setdefault("truthPlayerIndex", {})
STATE.setdefault("singPhase", None)
STATE.setdefault("singOptions", [])
STATE.setdefault("singCorrect", None)
STATE.setdefault("singAnswers", {})
STATE.setdefault("singPhaseWins", {})
STATE.setdefault("singWinnerOrder", [])
STATE.setdefault("singFinalistTeam", None)
STATE.setdefault("singCard", None)
STATE.setdefault("singAward", 0)
STATE.setdefault("singMatchPoints", {})
STATE.setdefault("mysteryCard", None)
STATE.setdefault("mysteryClueIndex", 0)
STATE.setdefault("mysteryLockedPlayers", [])
STATE.setdefault("mysteryBuzzPlayer", None)
STATE.setdefault("mysteryRoundWinner", None)
for _key, _default in {"bombCard":None,"bombOrder":[],"bombIndex":0,"bombHolder":None,
    "bombEliminated":[],"bombPowerUsed":{},"bombHints":[],"bombRoundWins":{},
    "bombRoundWinner":None,"bombGuessPlayer":None}.items(): STATE.setdefault(_key, _default)
STATE.setdefault("truthOutcome", None)
STATE.setdefault("lastAnswerCorrect", None)
STATE.setdefault("winnerTeam", None)


def save_state():
    STATE_FILE.write_text(json.dumps(STATE, ensure_ascii=False, indent=2), "utf-8")


def public_state(for_player=None):
    snapshot = json.loads(json.dumps(STATE))
    if snapshot.get("prompt") and (snapshot.get("game") or {}).get("id") in ("mimica", "dibujo"):
        if not for_player or for_player != snapshot.get("activePlayer"):
            snapshot["prompt"] = "Contenido secreto en el celular del participante"
            snapshot["answer"] = None
    if snapshot.get("prompt") and (snapshot.get("game") or {}).get("id") == "trivia" and snapshot.get("status") in ("countdown", "playing"):
        snapshot["prompt"].pop("correct", None)
    if (snapshot.get("game") or {}).get("id") == "quien_dijo" and for_player:
        snapshot["whoSaidChoices"] = {for_player: snapshot.get("whoSaidChoices", {}).get(for_player, [])}
        if snapshot.get("status") == "who_said_choose":
            snapshot["whoSaidSelected"] = {player_id: True for player_id in snapshot.get("whoSaidSelected", {})}
        if snapshot.get("status") in ("who_said_guess", "who_said_reveal", "game_complete"):
            snapshot["whoSaidOrder"] = [item for item in snapshot.get("whoSaidOrder", []) if item.get("playerId") != for_player]
            snapshot["whoSaidPlayers"] = [player_id for player_id in snapshot.get("whoSaidPlayers", []) if player_id != for_player]
            snapshot["whoSaidGuesses"] = {for_player: snapshot.get("whoSaidGuesses", {}).get(for_player, {})}
    if (snapshot.get("game") or {}).get("id") == "quien_soy":
        assignments = snapshot.get("whoAmIAssignments", {})
        snapshot["whoAmIAssignments"] = {for_player: assignments.get(for_player)} if for_player and assignments.get(for_player) else {}
    if snapshot.get("prompt") and (snapshot.get("game") or {}).get("id") == "tres_verdades" and snapshot.get("status") == "playing":
        snapshot["prompt"].pop("correct", None)
        for statement in snapshot["prompt"].get("statements", []):
            statement.pop("lie", None)
    if (snapshot.get("game") or {}).get("id") == "just_sing":
        snapshot.pop("singCard", None)
        snapshot.pop("singCorrect", None)
        if for_player and snapshot.get("status") == "sing_question":
            snapshot["prompt"] = {}
    if (snapshot.get("game") or {}).get("id") == "incognito":
        snapshot.pop("mysteryCard", None)
        if snapshot.get("prompt") and snapshot.get("status") not in ("mystery_result", "game_complete"):
            snapshot["prompt"]["blurredName"] = "IDENTIDAD PROTEGIDA"
        if for_player and snapshot.get("prompt"):
            snapshot["prompt"].pop("blurredName", None)
    if (snapshot.get("game") or {}).get("id") == "bomba":
        snapshot.pop("bombCard", None)
    return snapshot


def notify():
    dead = []
    for channel in SUBSCRIBERS:
        try:
            channel.put_nowait(True)
        except queue.Full:
            dead.append(channel)
    for channel in dead:
        if channel in SUBSCRIBERS:
            SUBSCRIBERS.remove(channel)


def log(message):
    STATE.setdefault("activity", []).insert(0, message)
    STATE["activity"] = STATE["activity"][:8]


def find_team(team_id):
    return next((team for team in STATE["teams"] if team["id"] == team_id), None)


def find_player(player_id):
    return next((player for player in STATE["players"] if player["id"] == player_id), None)


def select_prompt(game, difficulty, category=None):
    options = CONTENT.get(game, [])
    if difficulty != "aleatorio":
        options = [item for item in options if item.get("difficulty") == difficulty]
    if category:
        options = [item for item in options if item.get("category") == category]
    if not options:
        return None
    used = STATE.setdefault("usedPrompts", {}).setdefault(game, [])
    def card_key(card):
        if card.get("edition"):
            return json.dumps(card, sort_keys=True, ensure_ascii=False)
        return card.get("question") or card.get("prompt") or json.dumps(card, sort_keys=True)
    available = [item for item in options if card_key(item) not in used]
    if not available:
        last = used[-1] if used else None
        used.clear()
        available = [item for item in options if card_key(item) != last] or options
    item = json.loads(json.dumps(random.choice(available)))
    if game == "mimica":
        item.setdefault("hint", make_mimica_hint(item.get("category", ""), item.get("prompt", "")))
    used.append(card_key(item))
    if game == "trivia" and item.get("options"):
        correct_text = item["options"][item.get("correct", 0)]
        random.shuffle(item["options"])
        item["correct"] = item["options"].index(correct_text)
    return item


def make_mimica_hint(category, prompt):
    introductions = {
        "Cosas": "Es un objeto",
        "Sentimientos": "Es algo que se siente",
        "Acciones": "Es algo que se hace",
        "Películas": "Es el título de una película",
        "Superhéroes": "Es un personaje con poderes",
        "Libros": "Es el título de un libro",
        "Animales": "Es un animal",
        "Personajes históricos": "Es una figura de la historia",
        "Canciones": "Es el título de una canción",
        "Juegos": "Es un juego",
    }
    clean_prompt = str(prompt).strip()
    words = clean_prompt.split()
    letters = sum(character.isalpha() for character in clean_prompt)
    first = clean_prompt[:1].upper() or "?"
    word_detail = f" y son {len(words)} palabras" if len(words) > 1 else ""
    return f"{introductions.get(category, 'Pensá en la categoría')}. Empieza con «{first}», tiene {letters} letras{word_detail}."


def next_team():
    if not STATE["teams"]:
        return
    playable = [t for t in STATE["teams"] if not t.get("finished")] or STATE["teams"]
    ids = [t["id"] for t in playable]
    try:
        idx = (ids.index(STATE["activeTeam"]) + 1) % len(ids)
    except ValueError:
        idx = 0
    STATE["activeTeam"] = ids[idx]


def build_mimica_order():
    """Intercala jugadores por equipo y conserva el orden de registro."""
    members = {
        team["id"]: [p["id"] for p in STATE["players"] if p.get("teamId") == team["id"]]
        for team in STATE["teams"]
    }
    longest_team = max((len(players) for players in members.values()), default=0)
    return [
        members[team["id"]][position]
        for position in range(longest_team)
        for team in STATE["teams"]
        if position < len(members[team["id"]])
    ]


def current_mimica_player():
    order = STATE.get("mimicaOrder", [])
    index = STATE.get("mimicaTurnIndex", 0)
    return find_player(order[index]) if 0 <= index < len(order) else None


def next_challenge_player():
    """Elige por orden de registro al próximo jugador del equipo activo."""
    if not STATE.get("teams"):
        return None
    for _ in STATE["teams"]:
        team_id = STATE.get("activeTeam")
        members = [p for p in STATE["players"] if p.get("teamId") == team_id]
        if members:
            indexes = STATE.setdefault("challengePlayerIndex", {})
            index = indexes.get(team_id, 0) % len(members)
            indexes[team_id] = index + 1
            return members[index]
        next_team()
    return None


def finish_game_by_points(label):
    """Finaliza una partida por rondas usando sólo los puntos de esta partida."""
    baseline = (STATE.get("game") or {}).get("startScores", {})
    points = {team["id"]: team.get("score", 0) - baseline.get(team["id"], 0) for team in STATE["teams"]}
    best = max(points.values(), default=0)
    winners = [team for team in STATE["teams"] if points.get(team["id"], 0) == best]
    STATE.update({"status": "game_complete", "prompt": None, "answer": None, "timerEnds": None})
    if len(winners) == 1:
        winner = winners[0]
        STATE["winnerTeam"] = {"id": winner["id"], "name": winner["name"], "celebrationId": str(time.time_ns())}
        log(f"🏆 ¡{winner['name']} ganó {label}!")
    else:
        STATE["winnerTeam"] = None
        log(f"🤝 {label} terminó en empate")


def start_who_said(new_match=True):
    players = [player for player in STATE["players"] if player.get("online")]
    STATE["whoSaidPlayers"] = [player["id"] for player in players]
    STATE["whoSaidChoices"] = {}
    STATE["whoSaidSelected"] = {}
    STATE["whoSaidOrder"] = []
    STATE["whoSaidIndex"] = 0
    STATE["whoSaidGuesses"] = {}
    if new_match:
        STATE["whoSaidTeamPoints"] = {team["id"]: 0 for team in STATE["teams"]}
        STATE["whoSaidCurrentRound"] = 1
        STATE["winnerTeam"] = None
    needed = len(players) * 2
    phrases = [card["prompt"] for card in CONTENT.get("quien_dijo", [])]
    if len(players) < 2 or len(phrases) < needed:
        STATE.update({"status": "who_said_needs_players", "prompt": None, "timerEnds": None})
        log("Se necesitan al menos dos participantes conectados para jugar ¿Quién dijo qué?")
        return
    chosen = random.sample(phrases, needed)
    for index, player in enumerate(players):
        STATE["whoSaidChoices"][player["id"]] = chosen[index * 2:index * 2 + 2]
    choose_ms = int((STATE.get("game") or {}).get("duration", 60)) * 1000
    STATE.update({"status": "who_said_choose", "prompt": None, "timerEnds": int(time.time() * 1000) + choose_ms, "activePlayer": None})
    log(f"🤭 Ronda {STATE.get('whoSaidCurrentRound', 1)}: cada participante recibió dos frases")


def begin_who_said_guessing():
    for player_id in STATE.get("whoSaidPlayers", []):
        if player_id not in STATE.get("whoSaidSelected", {}):
            choices = STATE.get("whoSaidChoices", {}).get(player_id, [])
            if choices:
                STATE["whoSaidSelected"][player_id] = random.choice(choices)
    order = [{"playerId": player_id, "prompt": prompt} for player_id, prompt in STATE["whoSaidSelected"].items()]
    random.shuffle(order)
    for index, item in enumerate(order):
        item["roundIndex"] = index
    STATE["whoSaidOrder"] = order
    STATE["whoSaidIndex"] = 0
    STATE["whoSaidGuesses"] = {}
    STATE["status"] = "who_said_guess"
    STATE["prompt"] = None
    STATE["timerEnds"] = None
    log("🔎 ¡Comienza la ronda de adivinanzas!")


def reveal_who_said():
    order = STATE.get("whoSaidOrder", [])
    for voter_id, guesses in STATE.get("whoSaidGuesses", {}).items():
        voter = find_player(voter_id)
        team = find_team((voter or {}).get("teamId"))
        for index, guessed_id in guesses.items():
            if int(index) < len(order) and order[int(index)].get("playerId") != voter_id and guessed_id == order[int(index)].get("playerId") and team:
                STATE["whoSaidTeamPoints"][team["id"]] = STATE["whoSaidTeamPoints"].get(team["id"], 0) + 1
                team["score"] += 100
    STATE["status"] = "who_said_reveal"
    log("🤭 ¡Se revelaron todas las frases y sus autores!")


def finish_who_said():
    points = STATE.get("whoSaidTeamPoints", {})
    best = max(points.values(), default=0)
    winners = [team for team in STATE["teams"] if points.get(team["id"], 0) == best]
    STATE.update({"status": "game_complete", "prompt": None, "timerEnds": None})
    if len(winners) == 1:
        winner = winners[0]
        STATE["winnerTeam"] = {"id": winner["id"], "name": winner["name"], "celebrationId": str(time.time_ns())}
        log(f"🏆 ¡{winner['name']} ganó ¿Quién dijo qué? con {best} aciertos!")
    else:
        log(f"🤝 ¡Empate en ¿Quién dijo qué? con {best} aciertos!")


def prepare_who_am_i():
    order = STATE.get("whoAmIOrder", [])
    index = STATE.get("whoAmIIndex", 0)
    actor = find_player(order[index]) if 0 <= index < len(order) else None
    if not actor:
        STATE["whoAmIIndex"] = 0
        STATE["whoAmICurrentRound"] = STATE.get("whoAmICurrentRound", 1) + 1
        if STATE["whoAmICurrentRound"] > STATE.get("whoAmIMaxRounds", 10):
            finish_who_am_i()
            return
        actor = find_player(order[0]) if order else None
        if not actor:
            finish_who_am_i()
            return
    game = STATE.get("game") or {}
    STATE["activePlayer"] = actor["id"]
    STATE["activeTeam"] = actor["teamId"]
    card = select_prompt("quien_soy", game.get("difficulty", "aleatorio"))
    STATE["prompt"] = None
    STATE["whoAmIAssignments"] = {actor["id"]: card} if card else {}
    STATE["whoAmIGuessed"] = []
    STATE["whoAmIHintsUsed"] = 0
    STATE["round"] = STATE.get("whoAmICurrentRound", 1)
    STATE["status"] = "countdown"
    STATE["turnRemainingMs"] = 120000
    STATE["timerEnds"] = int(time.time() * 1000) + 10000
    log(f"🎭 {actor['name']} se prepara para descubrir quién es")


def start_who_am_i_round():
    players = [player for player in STATE["players"] if player.get("online")]
    game = STATE.get("game") or {}
    difficulty = game.get("difficulty", "aleatorio")
    cards = CONTENT.get("quien_soy", [])
    if difficulty != "aleatorio":
        cards = [card for card in cards if card.get("difficulty") == difficulty]
    if not players or len(cards) < len(players):
        STATE.update({"status": "game_complete", "prompt": None, "timerEnds": None})
        log("Conectá participantes con sus celulares para jugar ¿Quién soy?")
        return
    STATE["whoAmIAssignments"] = {}
    STATE["whoAmIGuessed"] = []
    STATE["whoAmIPoints"] = {team["id"]: 0 for team in STATE["teams"]}
    STATE["whoAmIOrder"] = [player["id"] for player in players]
    STATE["whoAmIIndex"] = 0
    STATE["whoAmICurrentRound"] = 1
    STATE["whoAmIMaxRounds"] = max(1, int(game.get("rounds", 10)))
    STATE["activePlayer"] = None
    STATE["prompt"] = None
    STATE["winnerTeam"] = None
    prepare_who_am_i()
    log(f"🎭 Comienza ¿Quién soy?: {STATE['whoAmIMaxRounds']} rondas, un participante por vez")


def finish_who_am_i():
    points = STATE.get("whoAmIPoints", {})
    best = max(points.values(), default=0)
    winners = [team for team in STATE["teams"] if best > 0 and points.get(team["id"], 0) == best]
    STATE.update({"status": "game_complete", "prompt": None, "activePlayer": None, "timerEnds": None})
    if len(winners) == 1:
        winner = winners[0]
        STATE["winnerTeam"] = {"id": winner["id"], "name": winner["name"], "celebrationId": str(time.time_ns())}
        log(f"🏆 ¡{winner['name']} ganó ¿Quién soy? con {best} aciertos!")
    elif winners:
        log(f"🤝 ¡Empate en ¿Quién soy? con {best} aciertos!")
    else:
        STATE["winnerTeam"] = None
        log("🎭 ¿Quién soy? terminó sin aciertos: no hay equipo ganador")


def sing_phase_options(card, field):
    difficulty = card.get("difficulty", "facil")
    pool = [item.get(field) for item in CONTENT.get("just_sing", []) if item.get("difficulty") == difficulty and item.get(field) != card.get(field)]
    wrong = random.sample(list(dict.fromkeys(pool)), min(3, len(set(pool))))
    options = wrong + [card.get(field)]
    random.shuffle(options)
    return options


def set_sing_phase(phase):
    card = STATE.get("singCard") or {}
    field = {"title": "title", "artist": "artist", "era": "era"}[phase]
    options = sing_phase_options(card, field)
    STATE["singPhase"] = phase
    STATE["singOptions"] = options
    STATE["singCorrect"] = options.index(card.get(field))
    STATE["singAnswers"] = {}
    STATE["status"] = "sing_question"
    STATE["timerEnds"] = int(time.time() * 1000) + 45000


def start_just_sing(new_match=True):
    players = [player for player in STATE["players"] if player.get("online")]
    if not players:
        STATE.update({"status": "sing_needs_players", "prompt": None, "timerEnds": None})
        log("Conectá participantes con sus celulares para jugar Just Sing")
        return
    difficulty = (STATE.get("game") or {}).get("difficulty", "aleatorio")
    card = None
    excerpt = ""
    for _ in range(6):
        candidate = select_prompt("just_sing", difficulty)
        if not candidate:
            break
        candidate_excerpt = candidate.get("excerpt") or fetch_lyric_excerpt(candidate)
        if candidate_excerpt:
            card, excerpt = candidate, candidate_excerpt
            break
    if not card:
        STATE.update({"status": "sing_content_unavailable", "prompt": None, "timerEnds": None})
        log("No pude obtener un fragmento de letra. Revisá la conexión e intentá nuevamente")
        return
    STATE["singCard"] = card
    STATE["prompt"] = {"excerpt": excerpt}
    STATE["singPhaseWins"] = {team["id"]: 0 for team in STATE["teams"]}
    STATE["singWinnerOrder"] = []
    STATE["singFinalistTeam"] = None
    STATE["singAward"] = 0
    STATE["winnerTeam"] = None
    if new_match:
        STATE["round"] = 1
        STATE["singMatchPoints"] = {team["id"]: 0 for team in STATE["teams"]}
    set_sing_phase("title")
    log("🎤 Just Sing comenzó: primero hay que descubrir el título")


def advance_sing_phase(winner_team_id=None):
    if winner_team_id:
        STATE["singPhaseWins"][winner_team_id] = STATE["singPhaseWins"].get(winner_team_id, 0) + 1
        STATE.setdefault("singWinnerOrder", []).append(winner_team_id)
    phase = STATE.get("singPhase")
    if phase == "title":
        set_sing_phase("artist")
        log("🎙️ Título resuelto: ahora adivinen el intérprete")
    elif phase == "artist":
        set_sing_phase("era")
        log("📅 Intérprete resuelto: ahora adivinen la época")
    else:
        points = STATE.get("singPhaseWins", {})
        best = max(points.values(), default=0)
        if best <= 0:
            if STATE.get("round", 1) < (STATE.get("game") or {}).get("rounds", 1):
                STATE.update({"status": "sing_round_result", "timerEnds": None, "winnerTeam": None, "singAward": 0})
                log("🎤 Nadie acertó esta canción de Just Sing")
            else:
                finish_just_sing()
            return
        tied = [team_id for team_id, value in points.items() if value == best]
        finalist = next((team_id for team_id in STATE.get("singWinnerOrder", []) if team_id in tied), tied[0])
        STATE["singFinalistTeam"] = finalist
        card = STATE.get("singCard") or {}
        STATE["prompt"] = {"title": card.get("title"), "artist": card.get("artist"), "year": card.get("year"), "audience": card.get("audience")}
        STATE["status"] = "sing_perform"
        STATE["timerEnds"] = None
        log(f"🎶 {find_team(finalist)['name']} debe cantar para confirmar sus puntos")


def resolve_just_sing(sang):
    if STATE.get("status") != "sing_perform":
        return
    team = find_team(STATE.get("singFinalistTeam"))
    if not team:
        return
    earned = 3 if sang else 1
    team["score"] += earned * 100
    STATE.setdefault("singMatchPoints", {})[team["id"]] = STATE.get("singMatchPoints", {}).get(team["id"], 0) + earned
    STATE["singAward"] = earned
    if STATE.get("round", 1) < (STATE.get("game") or {}).get("rounds", 1):
        STATE["winnerTeam"] = None
        STATE["status"] = "sing_round_result"
    else:
        finish_just_sing()
    log(f"🎤 {team['name']} sumó {earned} punto{'s' if earned != 1 else ''} en Just Sing")


def finish_just_sing():
    points = STATE.get("singMatchPoints", {})
    best = max(points.values(), default=0)
    winners = [team for team in STATE["teams"] if best > 0 and points.get(team["id"], 0) == best]
    STATE.update({"status": "game_complete", "timerEnds": None})
    if len(winners) == 1:
        winner = winners[0]
        STATE["winnerTeam"] = {"id": winner["id"], "name": winner["name"], "celebrationId": str(time.time_ns())}
    else:
        STATE["winnerTeam"] = None


def prepare_incognito():
    card = select_prompt("incognito", (STATE.get("game") or {}).get("difficulty", "aleatorio"))
    players = [player for player in STATE["players"] if player.get("online")]
    if not card or not players:
        STATE.update({"status": "game_complete", "prompt": None, "timerEnds": None})
        log("Conectá participantes con sus celulares para jugar Personaje Incógnito")
        return
    STATE["round"] = STATE.get("round", 0) + 1
    STATE["mysteryCard"] = card
    STATE["mysteryClueIndex"] = 0
    STATE["mysteryLockedPlayers"] = []
    STATE["mysteryBuzzPlayer"] = None
    STATE["mysteryRoundWinner"] = None
    # Nunca enviamos el nombre real antes de la revelación. Un filtro CSS puede
    # llegar a ser legible en pantallas grandes o capturas con mucho contraste.
    STATE["prompt"] = {"clues": [card["clues"][0]], "blurredName": "IDENTIDAD PROTEGIDA"}
    STATE["status"] = "mystery_clues"
    STATE["timerEnds"] = int(time.time() * 1000) + 6000
    log(f"🕵️ Comienza la ronda {STATE['round']} de Personaje Incógnito")


def reveal_next_mystery_clue():
    if STATE.get("status") != "mystery_clues":
        return
    card = STATE.get("mysteryCard") or {}
    next_index = STATE.get("mysteryClueIndex", 0) + 1
    if next_index >= min(20, len(card.get("clues", []))):
        STATE["prompt"] = {"clues": card.get("clues", []), "answer": card.get("prompt")}
        STATE.update({"status": "mystery_result", "timerEnds": None, "mysteryRoundWinner": None})
        log(f"🔎 Nadie adivinó: era {card.get('prompt')}")
        return
    STATE["mysteryClueIndex"] = next_index
    STATE["prompt"] = {"clues": card.get("clues", [])[:next_index + 1], "blurredName": "IDENTIDAD PROTEGIDA"}
    STATE["timerEnds"] = int(time.time() * 1000) + 6000


def submit_mystery_guess(player_id, guess):
    player = find_player(player_id)
    card = STATE.get("mysteryCard") or {}
    if STATE.get("status") != "mystery_guess" or not player or STATE.get("mysteryBuzzPlayer") != player_id:
        return
    normalized = " ".join(normalized_words(str(guess)))
    aliases = {" ".join(normalized_words(alias)) for alias in card.get("aliases", [])}
    if normalized and normalized in aliases:
        clue_number = STATE.get("mysteryClueIndex", 0) + 1
        earned = 3 if clue_number <= 6 else 2 if clue_number <= 13 else 1
        team = find_team(player.get("teamId"))
        if team:
            team["score"] += earned * 100
        STATE["mysteryRoundWinner"] = {"player": player["name"], "teamId": player.get("teamId"), "points": earned}
        STATE["prompt"] = {"clues": card.get("clues", [])[:clue_number], "answer": card.get("prompt")}
        STATE.update({"status": "mystery_result", "timerEnds": None})
        log(f"🎉 {player['name']} adivinó a {card.get('prompt')} y sumó {earned} puntos")
    else:
        locked = STATE.setdefault("mysteryLockedPlayers", [])
        if player_id not in locked:
            locked.append(player_id)
        STATE["mysteryBuzzPlayer"] = None
        online_ids = {p["id"] for p in STATE["players"] if p.get("online")}
        if online_ids and online_ids.issubset(set(locked)):
            STATE["prompt"] = {"clues": card.get("clues", []), "answer": card.get("prompt")}
            STATE.update({"status": "mystery_result", "timerEnds": None})
        else:
            STATE["status"] = "mystery_clues"
            STATE["timerEnds"] = int(time.time() * 1000) + 6000
        log(f"😅 {player['name']} arriesgó y no acertó")


def build_bomb_order():
    members = {team["id"]: [p["id"] for p in STATE["players"] if p.get("teamId") == team["id"] and p.get("online")] for team in STATE["teams"]}
    longest = max((len(group) for group in members.values()), default=0)
    return [members[team["id"]][i] for i in range(longest) for team in STATE["teams"] if i < len(members[team["id"]])]


def bomb_active_order():
    eliminated = set(STATE.get("bombEliminated", []))
    return [pid for pid in STATE.get("bombOrder", []) if pid not in eliminated and find_player(pid)]


def move_bomb(direction=1):
    active = bomb_active_order()
    if not active:
        return
    current = STATE.get("bombHolder")
    full_order = STATE.get("bombOrder", [])
    try: index = full_order.index(current)
    except ValueError: index = -1 if direction > 0 else 0
    for step in range(1, len(full_order) + 1):
        candidate = full_order[(index + direction * step) % len(full_order)]
        if candidate in active:
            STATE["bombHolder"] = candidate
            break
    STATE["bombGuessPlayer"] = None
    STATE["status"] = "bomb_active"
    STATE["timerEnds"] = int(time.time() * 1000) + 15000


def prepare_bomb_round(new_match=False):
    order = build_bomb_order()
    active_teams = {find_player(pid).get("teamId") for pid in order if find_player(pid)}
    if len(active_teams) < 2:
        STATE.update({"status":"game_complete","prompt":None,"timerEnds":None})
        log("Alerta Bomba necesita participantes conectados en al menos dos equipos")
        return
    if new_match:
        STATE["round"] = 0
        STATE["bombPowerUsed"] = {pid: {"pass":False,"return":False,"pause":False} for pid in order}
        STATE["bombRoundWins"] = {team["id"]: 0 for team in STATE["teams"]}
    STATE["round"] += 1
    card = select_prompt("bomba", (STATE.get("game") or {}).get("difficulty", "aleatorio"))
    STATE["bombCard"], STATE["bombOrder"], STATE["bombEliminated"] = card, order, []
    STATE["bombHints"], STATE["bombRoundWinner"], STATE["bombGuessPlayer"] = [], None, None
    STATE["prompt"] = {"question": card["prompt"], "hints": []}
    STATE["bombHolder"] = order[(STATE["round"] - 1) % len(order)]
    STATE["status"] = "bomb_active"
    STATE["timerEnds"] = int(time.time() * 1000) + 15000
    log(f"💣 Comienza la ronda {STATE['round']} de Alerta Bomba")


def award_bomb_round(team_id, reason):
    team = find_team(team_id)
    if team:
        STATE["bombRoundWins"][team_id] = STATE.get("bombRoundWins", {}).get(team_id, 0) + 1
        team["score"] += 100
        STATE["bombRoundWinner"] = {"teamId":team_id,"name":team["name"],"reason":reason}
    card = STATE.get("bombCard") or {}
    STATE["prompt"] = {"question":card.get("prompt"),"hints":STATE.get("bombHints",[]),"answer":card.get("answer")}
    STATE.update({"status":"bomb_result","timerEnds":None,"bombGuessPlayer":None})


def explode_bomb():
    holder = find_player(STATE.get("bombHolder"))
    if not holder: return
    rivals = [team for team in STATE["teams"] if team["id"] != holder.get("teamId")]
    if rivals: award_bomb_round(rivals[0]["id"], f"La alerta explotó en {holder['name']}")


def submit_bomb_guess(player_id, guess):
    if STATE.get("status") != "bomb_guess" or STATE.get("bombGuessPlayer") != player_id: return
    player, card = find_player(player_id), STATE.get("bombCard") or {}
    normalized = " ".join(normalized_words(str(guess)))
    valid = {" ".join(normalized_words(a)) for a in card.get("aliases", [])}
    if normalized and normalized in valid:
        award_bomb_round(player.get("teamId"), f"{player['name']} resolvió el acertijo")
        return
    STATE.setdefault("bombEliminated", []).append(player_id)
    team_active = [pid for pid in bomb_active_order() if (find_player(pid) or {}).get("teamId") == player.get("teamId")]
    if not team_active:
        rivals = [team for team in STATE["teams"] if team["id"] != player.get("teamId")]
        if rivals: award_bomb_round(rivals[0]["id"], f"Todos los jugadores de {find_team(player.get('teamId'))['name']} fallaron")
    else:
        move_bomb(1)
        log(f"😅 {player['name']} falló y queda fuera de esta ronda")


def prepare_three_truths():
    game = STATE.get("game") or {}
    card = select_prompt("tres_verdades", game.get("difficulty", "aleatorio"))
    if not card:
        STATE.update({"status": "game_complete", "prompt": None, "timerEnds": None})
        return
    random.shuffle(card["statements"])
    card["correct"] = next(index for index, item in enumerate(card["statements"]) if item.get("lie"))
    representatives = {}
    indexes = STATE.setdefault("truthPlayerIndex", {})
    for team in STATE["teams"]:
        members = [player for player in STATE["players"] if player.get("teamId") == team["id"] and player.get("online")]
        if members:
            index = indexes.get(team["id"], 0) % len(members)
            representatives[team["id"]] = members[index]["id"]
            indexes[team["id"]] = index + 1
    if not representatives:
        STATE.update({"status": "game_complete", "prompt": None, "timerEnds": None})
        log("Conectá al menos un representante para jugar Tres verdades y una mentira")
        return
    STATE["truthRepresentatives"] = representatives
    STATE["truthAnswers"] = {}
    STATE["truthOutcome"] = None
    STATE["prompt"] = card
    STATE["round"] = STATE.get("round", 0) + 1
    STATE["status"] = "playing"
    STATE["timerEnds"] = int(time.time() * 1000) + 90000
    log(f"🧐 Tres verdades y una mentira: {card['prompt']}")


def resolve_three_truths():
    prompt = STATE.get("prompt") or {}
    correct_index = prompt.get("correct")
    correct_teams = [team_id for team_id, answer in STATE.get("truthAnswers", {}).items() if answer == correct_index]
    points = {}
    if len(correct_teams) == 1:
        points[correct_teams[0]] = 3
    elif len(correct_teams) > 1:
        points.update({team_id: 1 for team_id in correct_teams})
    for team in STATE["teams"]:
        earned = points.get(team["id"], 0)
        if earned:
            team["score"] += earned * 100
    STATE["truthOutcome"] = {"correctTeams": correct_teams, "points": points}
    STATE["status"] = "result"
    STATE["timerEnds"] = None
    if len(correct_teams) == 1:
        log(f"🏆 {find_team(correct_teams[0])['name']} gana la ronda y suma 3 puntos")
    elif correct_teams:
        log("🤝 Los equipos empatan y suman 1 punto cada uno")
    else:
        log("😜 Ningún equipo encontró la mentira")


def prepare_round(new_turn=True):
    game = STATE.get("game")
    difficulty = (game or {}).get("difficulty", "aleatorio")
    item = select_prompt((game or {}).get("id"), difficulty)
    if new_turn:
        STATE["round"] += 1
        STATE["passesUsed"] = 0
        STATE["helpsUsed"] = 0
        STATE["turnCorrect"] = 0
        STATE["turnRemainingMs"] = int((game or {}).get("duration", 45)) * 1000
    STATE["status"] = "countdown"
    STATE["answer"] = None
    STATE["prompt"] = item
    STATE["revealedHint"] = None
    think_seconds = 5 if (game or {}).get("id") in ("mimica", "dibujo") else 3
    STATE["timerEnds"] = int(time.time() * 1000) + think_seconds * 1000
    if new_turn or not STATE.get("activePlayer"):
        if (game or {}).get("id") == "mimica":
            chosen = current_mimica_player()
        elif (game or {}).get("id") == "rapido":
            chosen = next_challenge_player()
        else:
            candidates = [p for p in STATE["players"] if p.get("teamId") == STATE["activeTeam"]]
            chosen = random.choice(candidates) if candidates else None
        STATE["activePlayer"] = chosen["id"] if chosen else None
        if chosen:
            STATE["activeTeam"] = chosen["teamId"]


def trivia_category(position):
    return TRIVIA_CATEGORIES[(max(1, position) - 1) % len(TRIVIA_CATEGORIES)]


def prepare_trivia_question(category, battle=False):
    game = STATE.get("game") or {}
    STATE["roundCategory"] = category
    STATE["prompt"] = select_prompt("trivia", game.get("difficulty", "aleatorio"), category)
    STATE["answer"] = None
    STATE["status"] = "countdown"
    STATE["timerEnds"] = int(time.time() * 1000) + (5000 if battle else 3000)
    STATE["turnRemainingMs"] = int(game.get("duration", 45)) * 1000


def has_all_stars(team):
    return all(team.get("stars", {}).get(category, 0) > 0 for category in TRIVIA_CATEGORIES)


def missing_star_categories(team):
    return [category for category in TRIVIA_CATEGORIES if team.get("stars", {}).get(category, 0) < 1]


def choose_trivia_player(team_id):
    candidates = [p for p in STATE["players"] if p.get("teamId") == team_id and p.get("online")]
    if not candidates:
        return None
    last = STATE.setdefault("lastTriviaPlayer", {}).get(team_id)
    choices = [p for p in candidates if p["id"] != last] or candidates
    chosen = random.choice(choices)
    STATE["lastTriviaPlayer"][team_id] = chosen["id"]
    return chosen["id"]


def resolve_round(correct):
    game_id = (STATE.get("game") or {}).get("id")
    battle = STATE.get("battle")
    winner_player = find_player((STATE.get("answer") or {}).get("playerId")) if battle else None
    team = find_team(winner_player.get("teamId")) if winner_player else find_team(STATE.get("activeTeam"))
    STATE["lastAnswerCorrect"] = bool(correct)
    if team:
        points = {"facil": 100, "medio": 200, "dificil": 300}.get((STATE.get("prompt") or {}).get("difficulty"), 200)
        won_game = False
        if correct:
            team["score"] += points
            if game_id == "trivia":
                category = STATE.get("roundCategory")
                team.setdefault("stars", {})[category] = team.setdefault("stars", {}).get(category, 0) + 1
                if team.get("position", 0) >= TRIVIA_FINISH:
                    if has_all_stars(team):
                        team["finished"] = True
                        STATE["winnerTeam"] = {"id": team["id"], "name": team["name"], "celebrationId": str(time.time_ns())}
                        won_game = True
                    else:
                        pending = ", ".join(missing_star_categories(team))
                        log(f"{team['name']} permanece en la meta; todavía le falta: {pending}")
            elif game_id == "quien_soy":
                STATE["whoAmIPoints"][team["id"]] = STATE.get("whoAmIPoints", {}).get(team["id"], 0) + 1
            log(f"¡{team['name']} suma {points} puntos!")
            if won_game:
                log(f"🏆 ¡Ganó {team['name']}! Completó Carrera de Mente con todas las estrellas")
        else:
            log(f"{team['name']} no sumó esta ronda")
    if game_id == "mimica" and correct:
        STATE["turnCorrect"] = STATE.get("turnCorrect", 0) + 1
        STATE["turnRemainingMs"] = max(0, (STATE.get("timerEnds") or 0) - int(time.time() * 1000))
        if STATE["turnRemainingMs"] > 0:
            prepare_round(new_turn=False)
        else:
            STATE["status"] = "result"
            STATE["timerEnds"] = None
    else:
        STATE["status"] = "result"
        STATE["timerEnds"] = None


def handle_action(action):
    kind = action.get("type")
    if kind == "join":
        name = str(action.get("name", "")).strip()[:28]
        if not name:
            return
        requested_id = str(action.get("playerId") or "p" + os.urandom(4).hex())[:64]
        selected_team = find_team(action.get("teamId"))
        existing = find_player(requested_id)
        if not existing:
            # Permite que alguien agregado previamente por el anfitrión conecte
            # su celular sin crear un participante duplicado.
            existing = next((
                player for player in STATE["players"]
                if not player.get("online") and player.get("name", "").casefold() == name.casefold()
            ), None)
        if existing:
            existing["id"] = requested_id
            existing["online"] = True
            existing["name"] = name
            if selected_team:
                existing["teamId"] = selected_team["id"]
        else:
            smallest = min(STATE["teams"], key=lambda t: sum(p.get("teamId") == t["id"] for p in STATE["players"]))
            STATE["players"].append({"id": requested_id, "name": name, "teamId": selected_team["id"] if selected_team else smallest["id"], "online": True})
        joined_team = selected_team or find_team(existing.get("teamId")) if existing else selected_team or smallest
        log(f"{name} se unió a {joined_team['name']}")
    elif kind == "addPlayer":
        name = str(action.get("name", "")).strip()[:28]
        if name:
            team = action.get("teamId") or STATE["teams"][0]["id"]
            STATE["players"].append({"id": "p" + os.urandom(4).hex(), "name": name, "teamId": team, "online": False})
    elif kind == "movePlayer":
        player = find_player(action.get("playerId"))
        if player and find_team(action.get("teamId")):
            player["teamId"] = action["teamId"]
    elif kind == "removePlayer":
        player = find_player(action.get("playerId"))
        if player:
            STATE["players"].remove(player)
            log(f"{player['name']} salió de la sala")
    elif kind == "addTeam":
        colors = ["#00c2a8", "#ff6b6b", "#31a8ff", "#f97316"]
        name = str(action.get("name", "")).strip()[:24]
        if name and len(STATE["teams"]) < 6:
            STATE["teams"].append({"id": "t" + os.urandom(3).hex(), "name": name, "color": colors[len(STATE["teams"]) % len(colors)], "score": 0, "position": 0, "stars": {}, "finished": False})
    elif kind == "deleteTeam":
        team = find_team(action.get("teamId"))
        if team and len(STATE["teams"]) > 1:
            replacement = next(t for t in STATE["teams"] if t["id"] != team["id"])
            for player in STATE["players"]:
                if player.get("teamId") == team["id"]:
                    player["teamId"] = replacement["id"]
            STATE["teams"].remove(team)
            if STATE.get("activeTeam") == team["id"]:
                STATE["activeTeam"] = replacement["id"]
            log(f"Se eliminó el equipo {team['name']}")
    elif kind == "renameTeam":
        team = find_team(action.get("teamId"))
        if team and str(action.get("name", "")).strip():
            team["name"] = str(action["name"]).strip()[:24]
    elif kind == "startGame":
        duration = max(10, min(180, int(action.get("duration", 45))))
        game_rounds = max(1, min(50, int(action.get("rounds", 1))))
        STATE["game"] = {
            "id": action.get("game"), "difficulty": action.get("difficulty", "aleatorio"),
            "duration": duration, "rounds": game_rounds,
            "sessionId": action.get("sessionId"),
            "startScores": {team["id"]: team.get("score", 0) for team in STATE["teams"]},
        }
        if action.get("game") == "tres_verdades":
            STATE["game"]["duration"] = 90
        if action.get("game") == "quien_soy":
            STATE["game"]["duration"] = 120
        STATE["round"] = 0
        STATE["activeTeam"] = STATE["teams"][0]["id"]
        STATE["battle"] = None
        STATE["mimicaOrder"] = build_mimica_order() if action.get("game") == "mimica" else []
        STATE["mimicaTurnIndex"] = 0
        STATE["mimicaCurrentRound"] = 1
        STATE["challengePlayerIndex"] = {}
        STATE["activePlayer"] = None
        STATE["lastAnswerCorrect"] = None
        STATE["winnerTeam"] = None
        if action.get("game") == "tres_verdades":
            STATE["truthPlayerIndex"] = {}
            prepare_three_truths()
        elif action.get("game") == "quien_soy":
            start_who_am_i_round()
        elif action.get("game") == "quien_dijo":
            start_who_said()
        elif action.get("game") == "just_sing":
            start_just_sing()
        elif action.get("game") == "incognito":
            prepare_incognito()
        elif action.get("game") == "bomba":
            STATE["game"]["rounds"] = 3
            prepare_bomb_round(new_match=True)
        elif action.get("game") == "trivia":
            STATE.update({"round": 1, "status": "await_roll", "prompt": None, "answer": None, "timerEnds": None, "roundCategory": None, "lastRoll": None})
        elif action.get("game") == "mimica" and not STATE["mimicaOrder"]:
            STATE.update({"status": "game_complete", "prompt": None, "answer": None, "timerEnds": None})
            log("Agregá participantes a los equipos para jugar a la mímica")
        else:
            prepare_round()
        log("¡Comenzó una nueva partida!")
    elif kind == "rollDice":
        if STATE.get("status") == "await_roll" and (STATE.get("game") or {}).get("id") == "trivia":
            team = find_team(STATE.get("activeTeam"))
            chosen_player = choose_trivia_player(team["id"]) if team else None
            if team and chosen_player:
                STATE["activePlayer"] = chosen_player
                dice = [random.randint(1, 6), random.randint(1, 6)]
                start = team.get("position", 0)
                position = min(TRIVIA_FINISH, start + sum(dice))
                special = TRIVIA_SPECIALS.get(position)
                if special == "back4":
                    position = max(1, position - 4)
                elif special == "forward4":
                    position = min(TRIVIA_FINISH, position + 4)
                team["position"] = position
                STATE["lastRoll"] = {"dice": dice, "from": start, "to": position, "special": special}
                missing_categories = missing_star_categories(team) if position >= TRIVIA_FINISH else []
                category = random.choice(missing_categories) if missing_categories else trivia_category(position)
                STATE["roundCategory"] = category
                log(f"{team['name']} sacó {dice[0]} + {dice[1]} y avanzó hasta la casilla {position}")
                rival = next((t for t in STATE["teams"] if t["id"] != team["id"] and t.get("position") == position and position > 0), None)
                if position >= TRIVIA_FINISH and missing_categories:
                    log(f"⭐ En la meta, {team['name']} juega por una estrella pendiente: {category}")
                    prepare_trivia_question(category)
                elif rival:
                    STATE["activePlayer"] = None
                    STATE["battle"] = {"teams": [team["id"], rival["id"]], "category": category, "players": []}
                    STATE["status"] = "battle_setup"
                    STATE["prompt"] = None
                elif special == "joker":
                    STATE["status"] = "choose_category"
                    STATE["prompt"] = None
                else:
                    prepare_trivia_question(category)
    elif kind == "chooseCategory":
        category = action.get("category")
        if STATE.get("status") == "choose_category" and category in TRIVIA_CATEGORIES:
            prepare_trivia_question(category)
    elif kind == "startBattle":
        battle = STATE.get("battle")
        chosen = action.get("players") or []
        if STATE.get("status") == "battle_setup" and battle and len(chosen) == 2:
            valid = [find_player(pid) for pid in chosen]
            if all(valid) and {p["teamId"] for p in valid} == set(battle["teams"]):
                battle["players"] = chosen
                prepare_trivia_question(battle["category"], battle=True)
    elif kind == "beginRound":
        if STATE.get("status") == "countdown":
            STATE["status"] = "playing"
            remaining = STATE.get("turnRemainingMs") or int((STATE.get("game") or {}).get("duration", 45)) * 1000
            STATE["timerEnds"] = int(time.time() * 1000) + remaining
    elif kind == "answer":
        if STATE["status"] == "playing":
            player_id = action.get("playerId")
            battle_players = (STATE.get("battle") or {}).get("players", [])
            allowed = player_id in battle_players if battle_players else (find_player(player_id) or {}).get("teamId") == STATE.get("activeTeam")
            if allowed:
                STATE["answer"] = {"playerId": player_id, "value": action.get("value")}
                if (STATE.get("game") or {}).get("id") == "trivia":
                    resolve_round(action.get("value") == (STATE.get("prompt") or {}).get("correct"))
                else:
                    STATE["status"] = "review"
    elif kind == "passPrompt":
        if (STATE.get("game") or {}).get("id") == "mimica" and STATE.get("passesUsed", 0) < 3 and STATE.get("status") in ("countdown", "playing"):
            if STATE.get("status") == "playing":
                STATE["turnRemainingMs"] = max(0, (STATE.get("timerEnds") or 0) - int(time.time() * 1000))
            STATE["passesUsed"] = STATE.get("passesUsed", 0) + 1
            log(f"Pase {STATE['passesUsed']} de 3")
            prepare_round(new_turn=False)
    elif kind == "requestHint":
        if (
            (STATE.get("game") or {}).get("id") == "mimica"
            and STATE.get("helpsUsed", 0) < 3
            and not STATE.get("revealedHint")
            and STATE.get("status") in ("countdown", "playing")
            and action.get("playerId") == STATE.get("activePlayer")
        ):
            STATE["helpsUsed"] = STATE.get("helpsUsed", 0) + 1
            STATE["revealedHint"] = (STATE.get("prompt") or {}).get("hint") or make_mimica_hint(
                (STATE.get("prompt") or {}).get("category", ""),
                (STATE.get("prompt") or {}).get("prompt", ""),
            )
            actor = find_player(STATE.get("activePlayer"))
            log(f"💡 {actor['name'] if actor else 'El participante'} pidió una pista ({STATE['helpsUsed']} de 3)")
    elif kind == "chooseWhoSaidPhrase":
        player_id = action.get("playerId")
        phrase = action.get("phrase")
        choices = STATE.get("whoSaidChoices", {}).get(player_id, [])
        if STATE.get("status") == "who_said_choose" and phrase in choices and player_id not in STATE.get("whoSaidSelected", {}):
            STATE["whoSaidSelected"][player_id] = phrase
            player = find_player(player_id)
            log(f"✓ {player['name'] if player else 'Un participante'} ya eligió su frase")
    elif kind == "guessWhoSaid":
        voter_id = action.get("playerId")
        guessed_id = action.get("guessedPlayerId")
        phrase_index = int(action.get("phraseIndex", -1))
        order = STATE.get("whoSaidOrder", [])
        eligible = [player_id for player_id in STATE.get("whoSaidPlayers", []) if find_player(player_id)]
        if (
            STATE.get("status") == "who_said_guess"
            and voter_id in eligible
            and guessed_id in STATE.get("whoSaidPlayers", [])
            and guessed_id != voter_id
            and 0 <= phrase_index < len(order)
            and order[phrase_index].get("playerId") != voter_id
        ):
            guesses = STATE.setdefault("whoSaidGuesses", {}).setdefault(voter_id, {})
            for previous_index, previous_player in list(guesses.items()):
                if previous_player == guessed_id:
                    guesses.pop(previous_index, None)
            guesses[str(phrase_index)] = guessed_id
            required = max(0, len(order) - 1)
            if all(len(STATE["whoSaidGuesses"].get(player_id, {})) == required for player_id in eligible):
                reveal_who_said()
    elif kind == "requestWhoAmIHint":
        if (STATE.get("game") or {}).get("id") == "quien_soy" and STATE.get("status") in ("countdown", "playing") and STATE.get("whoAmIHintsUsed", 0) < 3:
            STATE["whoAmIHintsUsed"] = STATE.get("whoAmIHintsUsed", 0) + 1
            actor = find_player(STATE.get("activePlayer"))
            log(f"💡 {actor['name'] if actor else 'El participante'} recibió la pista {STATE['whoAmIHintsUsed']} de 3")
    elif kind == "markWhoAmIGuessed":
        player = find_player(action.get("playerId"))
        if (STATE.get("game") or {}).get("id") == "quien_soy" and STATE.get("status") == "playing" and player and player["id"] == STATE.get("activePlayer") and player["id"] in STATE.get("whoAmIAssignments", {}):
            guessed = STATE.setdefault("whoAmIGuessed", [])
            team = find_team(player.get("teamId"))
            value = {"facil": 100, "medio": 200, "dificil": 300}.get((STATE.get("game") or {}).get("difficulty"), 200)
            if player["id"] in guessed:
                guessed.remove(player["id"])
                if team:
                    STATE["whoAmIPoints"][team["id"]] = max(0, STATE["whoAmIPoints"].get(team["id"], 0) - 1)
                    team["score"] = max(0, team["score"] - value)
            else:
                guessed.append(player["id"])
                if team:
                    STATE["whoAmIPoints"][team["id"]] = STATE["whoAmIPoints"].get(team["id"], 0) + 1
                    team["score"] += value
                STATE["status"] = "result"
                STATE["timerEnds"] = None
    elif kind == "answerLie":
        player_id = action.get("playerId")
        player = find_player(player_id)
        team_id = (player or {}).get("teamId")
        value = int(action.get("value", -1))
        if (
            (STATE.get("game") or {}).get("id") == "tres_verdades"
            and STATE.get("status") == "playing"
            and STATE.get("truthRepresentatives", {}).get(team_id) == player_id
            and team_id not in STATE.get("truthAnswers", {})
            and 0 <= value < len((STATE.get("prompt") or {}).get("statements", []))
        ):
            STATE["truthAnswers"][team_id] = value
            if len(STATE["truthAnswers"]) == len(STATE.get("truthRepresentatives", {})):
                resolve_three_truths()
    elif kind == "answerSong":
        player = find_player(action.get("playerId"))
        value = int(action.get("value", -1))
        if (
            (STATE.get("game") or {}).get("id") == "just_sing"
            and STATE.get("status") == "sing_question"
            and player and player.get("online")
            and player["id"] not in STATE.get("singAnswers", {})
            and 0 <= value < len(STATE.get("singOptions", []))
        ):
            STATE["singAnswers"][player["id"]] = value
            if value == STATE.get("singCorrect"):
                advance_sing_phase(player.get("teamId"))
            elif len(STATE["singAnswers"]) >= len([p for p in STATE["players"] if p.get("online")]):
                advance_sing_phase()
    elif kind == "resolveSing":
        resolve_just_sing(bool(action.get("sang")))
    elif kind == "nextMysteryClue":
        reveal_next_mystery_clue()
    elif kind == "buzzMystery":
        player = find_player(action.get("playerId"))
        if (STATE.get("status") == "mystery_clues" and player and player.get("online")
                and player["id"] not in STATE.get("mysteryLockedPlayers", [])):
            STATE["mysteryBuzzPlayer"] = player["id"]
            STATE["status"] = "mystery_guess"
            STATE["timerEnds"] = None
            log(f"🔴 {player['name']} apretó el pulsador y va a arriesgar")
    elif kind == "guessMystery":
        submit_mystery_guess(action.get("playerId"), action.get("guess", ""))
    elif kind == "bombAction":
        player_id, move = action.get("playerId"), action.get("move")
        if STATE.get("status") == "bomb_active" and STATE.get("bombHolder") == player_id:
            used = STATE.setdefault("bombPowerUsed", {}).setdefault(player_id, {"pass":False,"return":False,"pause":False})
            if move == "hint":
                card = STATE.get("bombCard") or {}; hints = card.get("hints", [])
                if len(STATE.get("bombHints", [])) < len(hints): STATE.setdefault("bombHints", []).append(hints[len(STATE["bombHints"])])
                STATE["prompt"]["hints"] = STATE.get("bombHints", [])
                move_bomb(1)
            elif move in ("pass", "return") and not used[move]:
                used[move] = True; move_bomb(1 if move == "pass" else -1)
            elif move == "pause" and not used["pause"]:
                used["pause"] = True; STATE["timerEnds"] = (STATE.get("timerEnds") or int(time.time()*1000)) + 5000
            elif move == "risk":
                STATE["bombGuessPlayer"] = player_id; STATE["status"] = "bomb_guess"; STATE["timerEnds"] = None
    elif kind == "guessBomb":
        submit_bomb_guess(action.get("playerId"), action.get("guess", ""))
    elif kind == "bombExplode":
        if STATE.get("status") == "bomb_active": explode_bomb()
    elif kind == "timeUp":
        if (STATE.get("game") or {}).get("id") == "just_sing" and STATE.get("status") == "sing_question":
            advance_sing_phase()
        elif (STATE.get("game") or {}).get("id") == "tres_verdades" and STATE.get("status") == "playing":
            resolve_three_truths()
        elif (STATE.get("game") or {}).get("id") == "quien_dijo" and STATE.get("status") == "who_said_choose":
            begin_who_said_guessing()
        elif STATE.get("status") == "playing":
            STATE["status"] = "result"
            STATE["timerEnds"] = None
            log("¡Tiempo! Termina el turno")
    elif kind == "resolve":
        resolve_round(bool(action.get("correct")))
    elif kind == "next":
        STATE["battle"] = None
        if (STATE.get("game") or {}).get("id") == "tres_verdades":
            if STATE.get("round", 0) >= (STATE.get("game") or {}).get("rounds", 1):
                finish_game_by_points("Tres verdades y una mentira")
            else:
                prepare_three_truths()
        elif (STATE.get("game") or {}).get("id") == "quien_soy":
            if STATE.get("status") == "result":
                STATE["whoAmIIndex"] = STATE.get("whoAmIIndex", 0) + 1
                prepare_who_am_i()
        elif (STATE.get("game") or {}).get("id") == "quien_dijo":
            if STATE.get("status") == "who_said_reveal":
                if STATE.get("whoSaidCurrentRound", 1) < (STATE.get("game") or {}).get("rounds", 1):
                    STATE["whoSaidCurrentRound"] = STATE.get("whoSaidCurrentRound", 1) + 1
                    start_who_said(new_match=False)
                else:
                    finish_who_said()
        elif (STATE.get("game") or {}).get("id") == "just_sing" and STATE.get("status") == "sing_round_result":
            STATE["round"] = STATE.get("round", 1) + 1
            start_just_sing(new_match=False)
        elif (STATE.get("game") or {}).get("id") == "incognito" and STATE.get("status") == "mystery_result":
            if STATE.get("round", 0) >= (STATE.get("game") or {}).get("rounds", 1):
                finish_game_by_points("Personaje Incógnito")
            else:
                prepare_incognito()
        elif (STATE.get("game") or {}).get("id") == "bomba" and STATE.get("status") == "bomb_result":
            if STATE.get("round", 0) >= 3:
                wins=STATE.get("bombRoundWins",{}); best=max(wins.values(),default=0); winners=[t for t in STATE["teams"] if wins.get(t["id"],0)==best]
                STATE.update({"status":"game_complete","timerEnds":None,"winnerTeam":None})
                if len(winners)==1: STATE["winnerTeam"]={"id":winners[0]["id"],"name":winners[0]["name"],"celebrationId":str(time.time_ns())}
            else: prepare_bomb_round()
        elif (STATE.get("game") or {}).get("id") == "trivia":
            if STATE.get("round", 0) >= (STATE.get("game") or {}).get("rounds", 1):
                finish_game_by_points("Carrera de Mente")
            else:
                next_team()
                STATE.update({"round": STATE.get("round", 0) + 1, "status": "await_roll", "prompt": None, "answer": None, "timerEnds": None, "roundCategory": None, "lastRoll": None, "activePlayer": None})
        elif (STATE.get("game") or {}).get("id") == "mimica":
            STATE["mimicaTurnIndex"] = STATE.get("mimicaTurnIndex", 0) + 1
            STATE["activePlayer"] = None
            if current_mimica_player():
                prepare_round()
            elif STATE.get("mimicaCurrentRound", 1) < (STATE.get("game") or {}).get("rounds", 1):
                STATE["mimicaCurrentRound"] = STATE.get("mimicaCurrentRound", 1) + 1
                STATE["mimicaTurnIndex"] = 0
                log(f"🎭 Comienza la ronda {STATE['mimicaCurrentRound']} de mímica")
                prepare_round()
            else:
                STATE.update({"status": "game_complete", "prompt": None, "answer": None, "timerEnds": None})
                log("🎭 ¡Todos los participantes completaron todas las rondas de mímica!")
        else:
            if STATE.get("round", 0) >= (STATE.get("game") or {}).get("rounds", 1):
                finish_game_by_points((STATE.get("game") or {}).get("id", "Juego"))
            else:
                next_team()
                prepare_round()
    elif kind == "adjustScore":
        team = find_team(action.get("teamId"))
        if team:
            team["score"] = max(0, team["score"] + int(action.get("amount", 0)))
    elif kind == "lobby":
        STATE.update({"game": None, "prompt": None, "answer": None, "timerEnds": None, "status": "lobby", "activePlayer": None, "winnerTeam": None, "lastAnswerCorrect": None})
    elif kind == "reset":
        room, players, teams, used = STATE["room"], STATE["players"], STATE["teams"], STATE.get("usedPrompts", {})
        STATE.clear()
        STATE.update(fresh_state())
        STATE["room"], STATE["players"], STATE["teams"] = room, players, teams
        STATE["usedPrompts"] = used
        STATE["activeTeam"] = teams[0]["id"] if teams else None
        for team in STATE["teams"]:
            team["score"] = team["position"] = 0
            team["stars"] = {}
            team["finished"] = False
        log("🔄 Marcador y partida reiniciados")
    save_state()
    notify()


class Handler(BaseHTTPRequestHandler):
    server_version = "FamiliaEnJuego/1.0"

    def end_headers(self):
        self.send_header("Permissions-Policy", "screen-wake-lock=(self)")
        super().end_headers()

    def log_message(self, fmt, *args):
        if not self.path.startswith("/events"):
            super().log_message(fmt, *args)

    def send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/state":
            player = urllib.parse.parse_qs(parsed.query).get("player", [None])[0]
            return self.send_json({
                "state": public_state(player),
                "contentStats": {k: len(v) for k, v in CONTENT.items()},
                "joinUrl": f"http://{local_ip()}:{self.server.server_port}/?join=1",
            })
        if parsed.path == "/events":
            player = urllib.parse.parse_qs(parsed.query).get("player", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            channel = queue.Queue(maxsize=2)
            SUBSCRIBERS.append(channel)
            try:
                while True:
                    payload = json.dumps(public_state(player), ensure_ascii=False)
                    self.wfile.write(f"data: {payload}\n\n".encode())
                    self.wfile.flush()
                    try:
                        channel.get(timeout=20)
                    except queue.Empty:
                        pass
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                if channel in SUBSCRIBERS:
                    SUBSCRIBERS.remove(channel)
            return
        path = parsed.path
        if path == "/":
            path = "/index.html"
        target = (PUBLIC / path.lstrip("/")).resolve()
        if not str(target).startswith(str(PUBLIC.resolve())) or not target.is_file():
            target = PUBLIC / "index.html"
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self.send_json({"error": "JSON inválido"}, 400)
        if self.path == "/api/action":
            with LOCK:
                handle_action(body)
            return self.send_json({"ok": True, "state": public_state(body.get("playerId"))})
        if self.path == "/api/content/import":
            url = str(body.get("url", ""))
            if not url.startswith(("https://", "http://")):
                return self.send_json({"error": "URL inválida"}, 400)
            try:
                with urllib.request.urlopen(url, timeout=12) as response:
                    imported = json.load(response)
                if not isinstance(imported, dict):
                    raise ValueError("Formato incorrecto")
                for game in ("trivia", "mimica", "dibujo", "rapido"):
                    if isinstance(imported.get(game), list):
                        CONTENT.setdefault(game, []).extend(imported[game])
                CONTENT_FILE.write_text(json.dumps(CONTENT, ensure_ascii=False, indent=2), "utf-8")
                return self.send_json({"ok": True, "stats": {k: len(v) for k, v in CONTENT.items()}})
            except Exception as exc:
                return self.send_json({"error": f"No se pudo importar: {exc}"}, 400)
        self.send_error(404)


def local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "localhost"
    finally:
        sock.close()


if __name__ == "__main__":
    port = int(os.environ.get("FAMILIA_PORT", "8765"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("\n🎉 FAMILIA EN JUEGO está lista")
    print(f"   Pantalla principal: http://localhost:{port}")
    print(f"   Celulares (misma Wi-Fi): http://{local_ip()}:{port}/?join=1")
    print("   Para cerrar, presioná Ctrl+C\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n¡Hasta la próxima partida!")
