#!/usr/bin/env python3
"""Build 1,800 Spanish trivia cards from verifiable Wikidata facts (CC0)."""

from __future__ import annotations

import json
import random
import re
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "FamiliaEnJuego/2.0 (family trivia catalog; contact: gonzalezme@gmail.com)"


def query(sparql):
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql, "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = json.load(response)
    return [{key: value["value"] for key, value in row.items()} for row in payload["results"]["bindings"]]


def norm(value):
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def entity_metadata(ids):
    result = {}
    ids = sorted({value.rsplit("/", 1)[-1] for value in ids if value and "/entity/Q" in value})
    for offset in range(0, len(ids), 50):
        params = urllib.parse.urlencode({
            "action": "wbgetentities", "ids": "|".join(ids[offset:offset + 50]),
            "props": "labels|sitelinks", "languages": "es|en", "languagefallback": 1,
            "format": "json", "origin": "*",
        })
        request = urllib.request.Request(f"https://www.wikidata.org/w/api.php?{params}", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            entities = json.load(response)["entities"]
        for qid, entity in entities.items():
            labels = entity.get("labels", {})
            label = (labels.get("es") or labels.get("en") or {}).get("value")
            if label:
                result[qid] = {"label": label, "popularity": len(entity.get("sitelinks", {}))}
    return result


def enrich(rows, entity_fields):
    metadata = entity_metadata(row.get(field) for row in rows for field in entity_fields)
    enriched = []
    for row in rows:
        clone = dict(row)
        popularity = []
        valid = True
        for field in entity_fields:
            qid = row.get(field, "").rsplit("/", 1)[-1]
            item = metadata.get(qid)
            if not item:
                valid = False
                break
            clone[field + "Label"] = item["label"]
            popularity.append(item["popularity"])
        if valid:
            clone["popularity"] = min(popularity)
            enriched.append(clone)
    return sorted(enriched, key=lambda item: item["popularity"], reverse=True)


def difficulty(index, total):
    ratio = index / max(1, total)
    return "facil" if ratio < .34 else "medio" if ratio < .68 else "dificil"


def options(rows, index, key, correct, seed):
    pool = []
    for jump in range(1, len(rows)):
        value = rows[(index + jump * 17) % len(rows)][key]
        if norm(value) != norm(correct) and norm(value) not in {norm(item) for item in pool}:
            pool.append(value)
        if len(pool) == 3:
            break
    values = [correct, *pool]
    random.Random(seed).shuffle(values)
    return values, values.index(correct)


def fact_cards(category, rows, left, right, forward, source_key):
    clean, seen = [], set()
    for row in rows:
        signature = (norm(row.get(left)), norm(row.get(right)))
        if not all(signature) or signature in seen:
            continue
        seen.add(signature)
        clean.append(row)
    cards = []
    for index, row in enumerate(clean[:300]):
        level = difficulty(index, min(300, len(clean)))
        a, b = row[left], row[right]
        opts, correct = options(clean, index, right, b, f"{category}-f-{index}")
        cards.append({"category": category, "difficulty": level, "question": forward.format(a=a, b=b), "options": opts, "correct": correct,
                      "source": row.get(source_key), "sourceProvider": "Wikidata"})
    if len(cards) < 150:
        raise ValueError(f"{category}: sólo se generaron {len(cards)} hechos únicos")
    return cards


QUERIES = {
    "Geografía": """
      SELECT DISTINCT ?country ?capital WHERE {
        ?country wdt:P31 wd:Q3624078; wdt:P36 ?capital.
        FILTER NOT EXISTS { ?country wdt:P31 wd:Q3024240 }
      } LIMIT 220
    """,
    "Historia": """
      SELECT DISTINCT ?person (STR(YEAR(?born)) AS ?year) WHERE {
        ?person wdt:P31 wd:Q5; wdt:P569 ?born; wdt:P106 wd:Q82955.
        FILTER(YEAR(?born) >= 1000 && YEAR(?born) <= 2000)
      } LIMIT 1000
    """,
    "Literatura": """
      SELECT DISTINCT ?work ?author WHERE {
        VALUES ?type { wd:Q8261 wd:Q7725634 wd:Q571 }
        ?work wdt:P31 ?type; wdt:P50 ?author.
      } LIMIT 1000
    """,
    "Deportes": """
      SELECT DISTINCT ?person ?sport WHERE {
        ?person wdt:P31 wd:Q5; wdt:P106 wd:Q2066131; wdt:P641 ?sport.
      } LIMIT 1000
    """,
    "Entretenimiento y Música": """
      SELECT DISTINCT ?work ?performer WHERE {
        ?work wdt:P31 wd:Q7366; wdt:P175 ?performer.
      } LIMIT 1000
    """,
    "Conocimientos generales": """
      SELECT DISTINCT ?element ?symbol ?number WHERE {
        ?element wdt:P31 wd:Q11344; wdt:P246 ?symbol; wdt:P1086 ?number.
      } ORDER BY xsd:integer(?number)
    """,
}


def main():
    cards = []
    geo = enrich(query(QUERIES["Geografía"]), ("country", "capital"))
    cards += fact_cards("Geografía", geo, "countryLabel", "capitalLabel", "¿Cuál es la capital de {a}?", "country")
    history = enrich(query(QUERIES["Historia"]), ("person",))
    cards += fact_cards("Historia", history, "personLabel", "year", "¿En qué año nació {a}?", "person")
    literature = enrich(query(QUERIES["Literatura"]), ("work", "author"))
    cards += fact_cards("Literatura", literature, "workLabel", "authorLabel", "¿Quién escribió «{a}»?", "work")
    sports = enrich(query(QUERIES["Deportes"]), ("person", "sport"))
    cards += fact_cards("Deportes", sports, "personLabel", "sportLabel", "¿En qué deporte se destacó {a}?", "person")
    music = enrich(query(QUERIES["Entretenimiento y Música"]), ("work", "performer"))
    cards += fact_cards("Entretenimiento y Música", music, "workLabel", "performerLabel", "¿Quién interpretó principalmente «{a}»?", "work")

    elements = enrich(query(QUERIES["Conocimientos generales"]), ("element",))
    elements = elements[:75]
    for index, row in enumerate(elements):
        level = difficulty(index, 75)
        facts = [
            (f"¿Cuál es el símbolo químico de {row['elementLabel']}?", "symbol", row["symbol"]),
            (f"¿Qué elemento tiene el símbolo {row['symbol']}?", "elementLabel", row["elementLabel"]),
            (f"¿Cuál es el número atómico de {row['elementLabel']}?", "number", row["number"]),
            (f"¿Qué elemento tiene número atómico {row['number']}?", "elementLabel", row["elementLabel"]),
        ]
        for part, (question, key, answer) in enumerate(facts):
            opts, correct = options(elements, index, key, answer, f"general-{index}-{part}")
            cards.append({"category": "Conocimientos generales", "difficulty": level, "question": question, "options": opts, "correct": correct,
                          "source": row["element"], "sourceProvider": "Wikidata"})
    # Do not reintroduce questions already present in the hand-curated catalog.
    import server
    existing = {norm(card.get("question")) for card in server.CONTENT.get("trivia", []) if card.get("sourceProvider") != "Wikidata"}
    unique, seen = [], set(existing)
    for card in cards:
        fingerprint = norm(card["question"])
        if fingerprint and fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(card)
    cards = unique
    (ROOT / "wikidata-trivia.json").write_text(json.dumps(cards, ensure_ascii=False, indent=2), "utf-8")
    print(json.dumps({"cards": len(cards), "byCategory": {category: sum(c["category"] == category for c in cards) for category in QUERIES}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
