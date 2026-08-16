"""Primera expansión canónica: tarjetas nuevas, sin variantes de redacción."""

import re


def _level(index, total):
    return "facil" if index < total / 3 else "medio" if index < total * 2 / 3 else "dificil"


MIME = {
    "Cosas": "Máquina de coser|Detector de humo|Molino de viento|Silla plegable|Control remoto|Bomba de aire",
    "Sentimientos": "Euforia|Culpa|Admiración|Desorientación|Valentía|Desilusión",
    "Acciones": "Cambiar pañal|Armar carpa|Hacer malabares|Buscar señal|Batir huevos|Domar caballo",
    "Películas": "Volver al futuro|Escuela de rock|El gran showman|Buscando a Nemo|Mi villano favorito|Una noche museo",
    "Superhéroes": "Linterna Verde|Doctor Fate|Silver Surfer|Kate Bishop|Blue Beetle|Caballero Luna",
    "Libros": "El principito|Drácula|Matilda|La historia interminable|El nombre rosa|Crónica anunciada",
    "Animales": "Panda rojo|Cangrejo ermitaño|Pez globo|Mantis religiosa|Mono araña|Dragón de Komodo",
    "Personajes históricos": "Juana de Arco|Nikola Tesla|Amelia Earhart|Simón Bolívar|Marie Antoinette|Winston Churchill",
    "Canciones": "La cucaracha|We Will Rock You|Twist and Shout|El baile sapito|La Macarena|Stayin Alive",
    "Juegos": "Piedra papel tijera|Carrera de postas|Sopa de letras|Teléfono descompuesto|Búsqueda del tesoro|Simón dice",
}


DRAWING = """Un pulpo chef|Un castillo inflable|Un robot jardinero|Una jirafa en ascensor|Un fantasma tímido|Una ciudad submarina|Un dragón bibliotecario|Una nave de cartón|Un volcán de helado|Un tren volador|Una tortuga astronauta|Un piano con patas|Un museo encantado|Una plaza futurista|Un gato detective|Una isla flotante|Un monstruo resfriado|Una bicicleta acuática|Un faro en tormenta|Una casa diminuta|Un dinosaurio oficinista|Una heladera parlante|Un árbol con zapatos|Una escuela de magia|Un caracol de carreras|Una luna de queso|Un perro fotógrafo|Un laberinto vegetal|Un pez con paraguas|Una montaña rusa casera""".split("|")


CHALLENGES = """Imitá a un director de orquesta que pierde la batuta|Cantá Feliz cumpleaños como cantante de ópera|Actuá una escena de acción en cámara ultralenta|Hacé una publicidad dramática de una cuchara|Caminá como robot sobre un piso imaginariamente pegajoso|Explicá cómo hacer una tostada como científico loco|Bailá tango con una escoba invisible|Imitá tres animales sin repetir movimientos|Representá un gol sin usar la palabra gol|Hacé percusión corporal durante veinte segundos|Actuá como detective que descubre una media perdida|Cantá una canción infantil con voz de villano|Construí una estatua humana con dos compañeros|Mantené un libro en la cabeza mientras saludás al público|Imitá a un superhéroe cuyo poder no funciona|Narrá una carrera de caracoles con máxima emoción|Representá cinco emociones en quince segundos|Inventá un rap con tres nombres de la familia|Hacé una coreografía usando sólo brazos|Actuá como turista perdido dentro de su propia casa|Imitá una escena de película sin sonidos|Pasá de anciano a bebé en diez segundos|Hacé reír sin hablar ni tocar a nadie|Cantá el estribillo de una canción cambiando todas las vocales|Representá una tormenta usando únicamente el cuerpo|Actuá como chef que prueba una comida extremadamente ácida|Caminá diez pasos sosteniendo una pose de flamenco|Improvisá un discurso de premio para una tarea doméstica|Imitá a un comentarista de un partido de piedra papel tijera|Creá con tu equipo una máquina humana durante veinte segundos""".split("|")


CONFESSIONS = """Practiqué una discusión frente al espejo y perdí.|Abrí la heladera tres veces esperando que apareciera algo nuevo.|Saludé con entusiasmo a alguien que no me estaba saludando.|Mandé un mensaje sobre una persona a esa misma persona.|Busqué mis anteojos mientras los tenía puestos.|Puse una alarma y después me enojé cuando sonó.|Ensayé cómo pedir pizza antes de llamar.|Le pedí perdón a un mueble después de chocarlo.|Inventé una excusa y olvidé cuál era a mitad de contarla.|Guardé algo tan bien que nunca volví a encontrarlo.|Fingí entender una película y después busqué la explicación.|Apreté más fuerte el control remoto para que funcionara.|Entré a una habitación y olvidé completamente para qué.|Canté una letra inventada con total seguridad.|Me reí de un chiste varios segundos tarde.|Usé la calculadora para una cuenta que sabía hacer.|Miré el celular para ver la hora y olvidé mirar la hora.|Respondí igualmente cuando llamaron a alguien con otro nombre.|Probé una pose seria para una foto y terminé estornudando.|Dije «ya voy» antes de empezar a prepararme.|Abrí un paquete por abajo porque no encontré la apertura.|Hablé con una mascota esperando una respuesta concreta.|Me escondí para comer el último postre sin compartir.|Busqué una receta y terminé mirando videos de animales.|Aplaudí cuando nadie más estaba aplaudiendo.|Puse una contraseña tan segura que no pude entrar.|Me quedé quieto para que una puerta automática me detectara.|Ordené un cajón y ahora encuentro menos cosas que antes.|Inventé un baile porque no conocía la coreografía.|Dije que recordaba a alguien y todavía no sé quién era.""".split("|")


WHO_AM_I = [
    ("Paddington", "Cine y literatura"), ("Merlina Addams", "Cine y TV"), ("Gandalf", "Literatura y cine"),
    ("Hermione Granger", "Literatura y cine"), ("Indiana Jones", "Cine"), ("Dora la Exploradora", "Infantil"),
    ("Sonic", "Videojuegos"), ("Princesa Peach", "Videojuegos"), ("Ahsoka Tano", "Cine y TV"),
    ("Willy Wonka", "Literatura y cine"), ("Sherlock Holmes", "Literatura"), ("Katniss Everdeen", "Literatura y cine"),
    ("Don Quijote", "Literatura"), ("Pippi Calzaslargas", "Literatura"), ("Tintín", "Historietas"),
    ("Mafalda", "Historietas"), ("Condorito", "Historietas"), ("Astérix", "Historietas"),
    ("Rosalía", "Música"), ("Dua Lipa", "Música"), ("Ed Sheeran", "Música"),
    ("Carlos Gardel", "Música"), ("Mercedes Sosa", "Música"), ("Astor Piazzolla", "Música"),
    ("Manu Ginóbili", "Deportes"), ("Paula Pareto", "Deportes"), ("Luciana Aymar", "Deportes"),
    ("René Favaloro", "Ciencia"), ("Cecilia Grierson", "Historia"), ("Julio Cortázar", "Literatura"),
]


THREE_TRUTHS = [
    ("René Favaloro", "Ciencia", ["Nació en La Plata.", "Desarrolló la técnica del bypass coronario.", "Trabajó como médico rural en La Pampa."], "Recibió el Premio Nobel de Medicina."),
    ("Amelia Earhart", "Historia", ["Fue pionera de la aviación.", "Cruzó sola el Atlántico en avión.", "Desapareció durante un vuelo alrededor del mundo."], "Fue la primera persona en llegar a la Luna."),
    ("Nikola Tesla", "Ciencia", ["Nació en el actual territorio de Croacia.", "Trabajó con sistemas de corriente alterna.", "Una unidad del campo magnético lleva su apellido."], "Inventó el teléfono móvil."),
    ("Frida Kahlo", "Arte", ["Nació en México.", "Pintó numerosos autorretratos.", "Estuvo casada con Diego Rivera."], "Fue escultora oficial de la Torre Eiffel."),
    ("Manu Ginóbili", "Deportes", ["Nació en Bahía Blanca.", "Jugó en San Antonio Spurs.", "Ganó una medalla de oro olímpica con Argentina."], "Fue arquero de la selección argentina de fútbol."),
    ("Jane Goodall", "Ciencia", ["Estudió chimpancés en Tanzania.", "Nació en Londres.", "Fundó un instituto dedicado a conservación."], "Descubrió la penicilina."),
    ("Julio Cortázar", "Literatura", ["Nació en Bruselas.", "Escribió Rayuela.", "Vivió gran parte de su vida en París."], "Escribió Cien años de soledad."),
    ("Valentina Tereshkova", "Historia", ["Fue la primera mujer en viajar al espacio.", "Era soviética.", "Su misión espacial fue Vostok 6."], "Caminó sobre la Luna en 1969."),
    ("Hedy Lamarr", "Ciencia y arte", ["Fue actriz de cine.", "Coconcebió un sistema de salto de frecuencia.", "Nació en Austria."], "Dirigió la primera misión a Marte."),
    ("Pelé", "Deportes", ["Nació en Brasil.", "Ganó tres Copas del Mundo.", "Jugó gran parte de su carrera en Santos."], "Fue campeón mundial con Argentina."),
    ("Ada Lovelace", "Ciencia", ["Fue hija del poeta Lord Byron.", "Escribió notas sobre la máquina analítica.", "Vivió en el siglo XIX."], "Diseñó el primer teléfono inteligente."),
    ("Violeta Parra", "Música", ["Nació en Chile.", "Compuso Gracias a la vida.", "También produjo obra visual."], "Fue integrante de ABBA."),
    ("Jacques Cousteau", "Exploración", ["Fue explorador oceanográfico.", "Codiseñó el regulador Aqua-Lung.", "Realizó documentales sobre el mar."], "Fue el primer ser humano en Marte."),
    ("Serena Williams", "Deportes", ["Fue número uno del tenis mundial.", "Su hermana Venus también es tenista.", "Ganó 23 títulos individuales de Grand Slam."], "Ganó el Mundial de fútbol de 2014."),
    ("Hayao Miyazaki", "Cine", ["Cofundó Studio Ghibli.", "Dirigió El viaje de Chihiro.", "Nació en Japón."], "Creó al personaje Mickey Mouse."),
]


SONGS = [
    ("A rodar mi vida", "Fito Páez", 1992), ("El tesoro", "El Mató a un Policía Motorizado", 2017),
    ("Brillante sobre el mic", "Fito Páez", 1992), ("Puente", "Gustavo Cerati", 1999),
    ("Zona de promesas", "Soda Stereo", 1993), ("Zamba para olvidar", "Daniel Toro", 1968),
    ("Alfonsina y el mar", "Mercedes Sosa", 1969), ("Todo cambia", "Mercedes Sosa", 1984),
    ("Universos paralelos", "Jorge Drexler y Ana Tijoux", 2014), ("Hasta la raíz", "Natalia Lafourcade", 2015),
    ("Viva la Vida", "Coldplay", 2008), ("Somewhere Only We Know", "Keane", 2004),
    ("Dog Days Are Over", "Florence + The Machine", 2008), ("Mr. Brightside", "The Killers", 2003),
    ("Watermelon Sugar", "Harry Styles", 2019), ("Levitating", "Dua Lipa", 2020),
    ("Good as Hell", "Lizzo", 2016), ("Adventure of a Lifetime", "Coldplay", 2015),
    ("Surface Pressure", "Jessica Darrow", 2021), ("Nobody Like U", "4*TOWN", 2022),
]


INCOGNITO = [
    ("René Favaloro", "Ciencia", "Argentina", "siglo XX", ["Fue médico rural", "Desarrolló el bypass coronario", "Nació en La Plata"]),
    ("Amelia Earhart", "Aviación", "Estados Unidos", "siglo XX", ["Fue piloto", "Cruzó sola el Atlántico", "Desapareció sobre el Pacífico"]),
    ("Gandalf", "Fantasía", "Tierra Media", "ficción", ["Es un mago", "Lleva un bastón", "Acompaña a la Comunidad del Anillo"]),
    ("Mafalda", "Historietas", "Argentina", "siglo XX", ["Es una niña de historieta", "Odia la sopa", "Fue creada por Quino"]),
    ("Manu Ginóbili", "Básquet", "Argentina", "actualidad", ["Nació en Bahía Blanca", "Jugó en la NBA", "Ganó oro olímpico"]),
    ("Hayao Miyazaki", "Cine", "Japón", "actualidad", ["Es director de animación", "Cofundó Studio Ghibli", "Dirigió El viaje de Chihiro"]),
    ("Dua Lipa", "Música", "Reino Unido", "actualidad", ["Es cantante pop", "Tiene ascendencia kosovar", "Grabó Levitating"]),
    ("Sherlock Holmes", "Literatura", "Londres", "ficción", ["Es detective", "Vive en Baker Street", "Su compañero es Watson"]),
    ("Valentina Tereshkova", "Espacio", "Unión Soviética", "siglo XX", ["Fue cosmonauta", "Viajó en Vostok 6", "Fue la primera mujer en el espacio"]),
    ("Sonic", "Videojuegos", "SEGA", "ficción", ["Es azul", "Corre a enorme velocidad", "Es un erizo"]),
    ("Mercedes Sosa", "Música", "Argentina", "siglo XX", ["Nació en Tucumán", "Fue cantante folclórica", "Fue llamada La Negra"]),
    ("Paddington", "Literatura y cine", "Londres", "ficción", ["Llegó desde Perú", "Usa sombrero rojo", "Es un oso"]),
    ("Jane Goodall", "Ciencia", "Reino Unido", "actualidad", ["Es primatóloga", "Trabajó en Tanzania", "Estudió chimpancés"]),
    ("Willy Wonka", "Literatura y cine", "una fábrica", "ficción", ["Es excéntrico", "Organiza una visita con boletos dorados", "Fabrica chocolate"]),
    ("Paula Pareto", "Deportes", "Argentina", "actualidad", ["También es médica", "Ganó oro olímpico", "Compite en judo"]),
]


BOMB = [
    ("reloj", "Tengo manos y cara, pero no brazos ni ojos.", ["Mido algo", "Puedo estar en una pared", "Tengo números", "Marco horas"]),
    ("libro", "Tengo hojas y lomo, pero no soy árbol ni animal.", ["Guardo historias", "Se abre", "Se lee", "Estoy en bibliotecas"]),
    ("aguja", "Tengo un ojo, pero no puedo ver.", ["Soy pequeña", "Puedo pinchar", "Trabajo con hilo", "Sirvo para coser"]),
    ("botella", "Tengo cuello, pero no cabeza.", ["Soy un recipiente", "Puedo ser de vidrio", "Guardo líquidos", "Tengo tapa"]),
    ("peine", "Tengo muchos dientes, pero nunca muerdo.", ["Cabe en una mano", "Se usa frente al espejo", "Ordeno algo", "Trabajo con cabello"]),
    ("mesa", "Tengo cuatro patas, pero no puedo caminar.", ["Soy un mueble", "Sostengo objetos", "Se come sobre mí", "Tengo una superficie plana"]),
    ("zapato", "Tengo lengua y suela, pero no puedo hablar ni nadar.", ["Se usa de a dos", "Va en el suelo", "Protejo una parte del cuerpo", "Voy en los pies"]),
    ("repollo", "Tengo muchas capas y ninguna es ropa.", ["Soy alimento", "Crezco en la tierra", "Soy una verdura", "Tengo hojas apretadas"]),
    ("esponja", "Estoy llena de agujeros y aun así puedo guardar agua.", ["Soy liviana", "Se usa para limpiar", "Absorbo", "Estoy en cocina o baño"]),
    ("fuego", "Si me alimentas vivo; si me das de beber muero.", ["Doy calor", "Necesito oxígeno", "Consumo combustible", "El agua me apaga"]),
    ("piano", "Tengo muchas llaves, pero ninguna abre puertas.", ["Soy grande", "Produzco música", "Uso teclas blancas y negras", "Soy un instrumento"]),
    ("correo", "Puedo recorrer el mundo sin moverme de mi sobre.", ["Llevo un mensaje", "Tengo destinatario", "Uso estampilla", "Lo entrega un cartero"]),
    ("nariz", "Estoy entre dos ojos y encima de una boca.", ["Soy parte del cuerpo", "Permito respirar", "Detecto olores", "Estoy en la cara"]),
    ("camino", "Todos pasan sobre mí, pero yo nunca voy a ningún lado.", ["Uno lugares", "Puedo ser de tierra", "Me recorren vehículos", "Soy una vía"]),
    ("burbuja", "Nazco redonda, vuelo liviana y muero con un toque.", ["Tengo aire", "Puedo salir del jabón", "Soy transparente", "Exploto fácilmente"]),
    ("invierno", "Llego después del otoño y me voy antes de la primavera.", ["Soy una estación", "Traigo frío", "Los días son cortos", "Puedo traer nieve"]),
    ("ascensor", "Tengo puertas, pero no soy casa; subo y bajo sin piernas.", ["Estoy en edificios", "Uso botones", "Transporto personas", "Voy entre pisos"]),
    ("túnel", "Tengo entrada y salida, pero casi nunca ventanas.", ["Es un paso", "Puedo atravesar montañas", "Suele ser oscuro", "Circulan trenes o autos"]),
    ("paraguas", "Me abro cuando el cielo se cierra.", ["Se lleva con una mano", "Tengo varillas", "Protejo la cabeza", "Se usa cuando llueve"]),
    ("palomitas", "Somos pequeñas, blancas y explotamos de alegría con calor.", ["Somos comida", "Venimos del maíz", "Acompañamos películas", "También nos llaman pochoclo"]),
]


def build_expansion():
    result = {key: [] for key in ("mimica", "dibujo", "rapido", "quien_dijo", "quien_soy", "tres_verdades", "just_sing", "incognito", "bomba")}
    for category, raw in MIME.items():
        prompts = raw.split("|")
        result["mimica"] += [{"category": category, "difficulty": _level(i, len(prompts)), "prompt": p} for i, p in enumerate(prompts)]
    result["dibujo"] = [{"category": "Escenas", "difficulty": _level(i, len(DRAWING)), "prompt": p} for i, p in enumerate(DRAWING)]
    result["rapido"] = [{"category": "Reto nuevo", "difficulty": _level(i, len(CHALLENGES)), "prompt": p} for i, p in enumerate(CHALLENGES)]
    result["quien_dijo"] = [{"category": "Confesiones", "difficulty": _level(i, len(CONFESSIONS)), "prompt": p} for i, p in enumerate(CONFESSIONS)]
    for i, (name, category) in enumerate(WHO_AM_I):
        letters = sum(ch.isalpha() for ch in name)
        result["quien_soy"].append({"category": category, "difficulty": _level(i, len(WHO_AM_I)), "prompt": name,
            "hints": [f"Se relaciona con {category.lower()}.", f"Su nombre comienza con {name[0]}.", f"Su nombre tiene {letters} letras."]})
    for i, (name, category, truths, lie) in enumerate(THREE_TRUTHS):
        statements = [{"text": text, "lie": False} for text in truths] + [{"text": lie, "lie": True}]
        result["tres_verdades"].append({"category": category, "difficulty": _level(i, len(THREE_TRUTHS)), "prompt": name, "statements": statements})
    for i, (title, artist, year) in enumerate(SONGS):
        result["just_sing"].append({"difficulty": _level(i, len(SONGS)), "title": title, "artist": artist, "year": year,
            "era": f"Década de {(year // 10) * 10}", "audience": "Familiar", "excerpt": "", "clue": ""})
    for i, (name, category, origin, era, facts) in enumerate(INCOGNITO):
        letters = sum(ch.isalpha() for ch in name); words = name.split()
        clues = ["Puede ser una persona real o un personaje ficticio.", f"Se relaciona con {category.lower()}.", f"Tiene vínculo con {origin}.",
                 f"Su historia se ubica en {era}.", "Es conocido por distintas generaciones.", *[fact + "." for fact in facts],
                 f"Su nombre tiene {len(words)} palabra{'s' if len(words)>1 else ''}.", f"Empieza con {name[0]}.", f"Tiene {letters} letras."]
        while len(clues) < 19: clues.insert(-1, "Cada nueva pista acerca más a su identidad.")
        clues.append(f"La pista final: {facts[-1]}.")
        result["incognito"].append({"difficulty": _level(i, len(INCOGNITO)), "category": category, "prompt": name, "aliases": [name], "clues": clues[:20]})
    for i, (answer, prompt, hints) in enumerate(BOMB):
        result["bomba"].append({"difficulty": _level(i, len(BOMB)), "category": "Acertijo", "prompt": prompt, "answer": answer,
            "aliases": [answer], "hints": [*hints, f"La respuesta es {answer}"]})
    return result
