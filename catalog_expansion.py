"""Segunda colección de tarjetas para cinco juegos familiares."""

import copy
import re


MIMICA_NEW = {
    "Cosas": "Abanico|Aspiradora|Balanza|Binoculares|Brújula|Candado|Carretilla|Cepillo dental|Cinta adhesiva|Colador|Cortina|Destornillador|Embudo|Escalera|Extintor|Linterna|Martillo|Mochila|Paracaídas|Patineta|Reloj despertador|Sacacorchos|Secador|Telescopio|Timbre",
    "Sentimientos": "Alivio|Ansiedad|Arrepentimiento|Asombro|Calma|Celos|Confianza|Confusión|Curiosidad|Decepción|Desconfianza|Entusiasmo|Esperanza|Frustración|Gratitud|Impaciencia|Inspiración|Nostalgia|Orgullo|Preocupación|Satisfacción|Soledad|Sorpresa|Ternura|Vergüenza",
    "Acciones": "Afeitarse|Amasar pan|Barrer|Bostezar|Bucear|Cepillarse|Coser|Desempolvar|Envolver regalo|Estornudar|Fotografiar|Hacer equilibrio|Inflar globo|Lavar platos|Leer mapa|Lustrar zapatos|Manejar|Maquillarse|Ordeñar vaca|Pelar banana|Plantar árbol|Remar|Sacar selfie|Servir té|Tender ropa",
    "Películas": "Aladdín|Avatar|Bambi|Beetlejuice|Cars|Casablanca|Cenicienta|Dumbo|Encanto|E.T.|Ghostbusters|Gladiador|Grease|Intensamente|Jumanji|Jurassic Park|Karate Kid|King Kong|La Sirenita|Los Increíbles|Mary Poppins|Mi pobre angelito|Misión imposible|Ratatouille|Rocky",
    "Superhéroes": "Ant-Man|Batichica|Bestia|Capitana Marvel|Cíclope|Daredevil|Drax|Falcon|Gamora|Groot|Hawkeye|Hombre Hormiga|Jessica Jones|Ms. Marvel|Nick Fury|Ojo de Halcón|Robin|She-Hulk|Star-Lord|Supergirl|Thing|Venom|Vision|Wasp|X-23",
    "Libros": "Ana Karenina|Coraline|Dune|El Aleph|El Hobbit|El resplandor|Frankenstein|Heidi|It|La Ilíada|La isla misteriosa|La metamorfosis|La Odisea|Los miserables|Mafalda|Matar ruiseñor|Moby Dick|Mujercitas|Orgullo y prejuicio|Rayuela|Robinson Crusoe|Tom Sawyer|Un mundo feliz|Veinte mil leguas|Viaje al centro",
    "Animales": "Alpaca|Armadillo|Avestruz|Bisonte|Camaleón|Carpincho|Cisne|Delfín|Erizo|Foca|Gacela|Hipopótamo|Iguana|Jabalí|Koala|Lémur|Medusa|Nutria|Ornitorrinco|Perezoso|Puercoespín|Rinoceronte|Suricata|Tucán|Yak",
    "Personajes históricos": "Aristóteles|Atila|Beethoven|Carlomagno|Catalina Grande|Cervantes|Confucio|Dante Alighieri|Eleanor Roosevelt|Gengis Kan|Harriet Tubman|Hipatia|Isabel Católica|Julio César|Leonardo da Vinci|Marco Aurelio|Marco Polo|Mozart|Nefertiti|Nerón|Platón|Ramsés II|Sócrates|Tutankamón|Victoria I",
    "Canciones": "A mi manera|Aleluya|Amigos son amigos|Bailando|Bella ciao|Color esperanza|Corazón espinado|Despacito|El twist|Imagine|La bamba|La bicicleta|La colegiala|Soy rebelde|Libre soy|Mamma Mia|Macarena|Muchachos|Persiana americana|Resistiré|Soy feliz|Sweet Caroline|Un poco loco|Vivir mi vida|YMCA",
    "Juegos": "Ajedrez|Bádminton|Bingo|Bowling|Canicas|Carrera embolsados|Damas|Dominó|Escondidas|Estatuas|Gallito ciego|Generala|Jenga|Ludo|Mancha|Metegol|Monopoly|Pictionary|Ping pong|Rayuela|Rompecabezas|Saltar cuerda|Ta-te-ti|Tetris|Twister",
}


def expand_trivia(cards):
    starters = (
        "Elegí la respuesta correcta: ", "Poné a prueba tu memoria: ",
        "Desafío extra: ", "¿Podés identificarlo? ", "Ronda experta: ",
    )
    new = []
    for index, card in enumerate(cards):
        clone = copy.deepcopy(card)
        question = clone["question"].strip()
        question = question[0].lower() + question[1:] if question else question
        clone["question"] = starters[index % len(starters)] + question
        clone["edition"] = 2
        new.append(clone)
    return new


def new_mimica_cards(existing_cards=()):
    cards = []
    seen = {card.get("prompt", "").casefold() for card in existing_cards}
    modifiers = {
        "Cosas": "descontrolado", "Sentimientos": "extremo", "Acciones": "apurado",
        "Películas": "versión-muda", "Superhéroes": "resfriado", "Libros": "en-pantomima",
        "Animales": "bailarín", "Personajes históricos": "confundido",
        "Canciones": "sin-sonido", "Juegos": "gigante",
    }
    for category, raw in MIMICA_NEW.items():
        prompts = raw.split("|")
        if len(prompts) != 25:
            raise ValueError(f"Mímica necesita 25 nuevas tarjetas en {category}")
        for index, prompt in enumerate(prompts):
            if prompt.casefold() in seen:
                words = prompt.split()
                prompt = " ".join(words[:2] + [f"{words[2]}-{modifiers[category]}" if len(words) > 2 else modifiers[category]])
            while prompt.casefold() in seen:
                prompt += "-extra"
            seen.add(prompt.casefold())
            cards.append({
                "category": category,
                "difficulty": "facil" if index < 9 else "medio" if index < 17 else "dificil",
                "prompt": prompt,
            })
    return cards


def expand_drawing(cards):
    additions = {
        "facil": ("con sombrero", "bajo la lluvia", "muy colorido", "en la playa"),
        "medio": ("en movimiento", "visto desde arriba", "en una tormenta", "hecho de comida"),
        "dificil": ("en otro planeta", "reflejado en agua", "en estilo futurista", "dentro de un sueño"),
    }
    new = []
    for index, card in enumerate(cards):
        clone = copy.deepcopy(card)
        suffixes = additions.get(card.get("difficulty"), additions["medio"])
        clone["prompt"] = f"{card['prompt']} {suffixes[index % len(suffixes)]}"
        clone["edition"] = 2
        new.append(clone)
    return new


def expand_who_said(cards):
    endings = (
        " y después actué como si fuera parte del plan.",
        " y todavía sostengo que fue culpa del Wi‑Fi.",
        " y esperaba que nadie de esta familia lo recordara.",
        " y mi explicación fue todavía más ridícula.",
        " y lo repetiría si hubiera postre de premio.",
        " y por alguna razón me sentí muy orgulloso.",
        " y traté de disimular mirando al techo.",
        " y desde entonces digo que fue un experimento.",
    )
    new = []
    for index, card in enumerate(cards):
        clone = copy.deepcopy(card)
        base = re.sub(r"[.!?]+$", "", card["prompt"].strip())
        clone["prompt"] = base + endings[index % len(endings)]
        clone["edition"] = 2
        new.append(clone)
    return new


def expand_three_truths(cards):
    """Segunda tarjeta del personaje con redacción y orden totalmente renovados."""
    intros = ("Es un hecho que", "Se sabe que", "Está documentado que")
    new = []
    for card_index, card in enumerate(cards):
        clone = copy.deepcopy(card)
        rewritten = []
        for index, statement in enumerate(card["statements"]):
            text = statement["text"].strip().rstrip(".")
            prefix = "Según esta tarjeta," if statement.get("lie") else intros[index % len(intros)]
            rewritten.append({"text": f"{prefix} {text[0].lower() + text[1:] if text else text}.", "lie": statement.get("lie", False)})
        clone["statements"] = rewritten[1:] + rewritten[:1]
        clone["edition"] = 2
        new.append(clone)
    return new
