"""60 personajes para Personaje Incógnito, con 20 pistas progresivas."""

ROWS = {
"facil": """
Albert Einstein|Einstein|Ciencia|real|Alemania|siglo XX|Fue físico;Formuló la relatividad;Su apellido es sinónimo popular de genio
Lionel Messi|Messi;Leo Messi|Fútbol|real|Argentina|actualidad|Nació en Rosario;Fue campeón mundial en 2022;Usó el número 10
Diego Maradona|Maradona;Diego|Fútbol|real|Argentina|siglo XX|Fue campeón mundial en 1986;Jugó en Napoli;Fue apodado Pelusa
Shakira|Shakira Mebarak|Música|real|Colombia|actualidad|Nació en Barranquilla;Canta en español e inglés;Popularizó un baile de caderas
Michael Jackson|Jackson;Michael|Música|real|Estados Unidos|siglo XX|Integró Jackson 5;Publicó Thriller;Fue llamado Rey del Pop
Taylor Swift|Taylor|Música|real|Estados Unidos|actualidad|Es cantautora;Regrabó varios álbumes;Sus seguidores son llamados swifties
Superman|Clark Kent;Kal-El|Superhéroes|ficticio|Krypton|cómics|Vuela;Usa una capa roja;La kryptonita lo debilita
Batman|Bruce Wayne|Superhéroes|ficticio|Ciudad Gótica|cómics|No tiene poderes permanentes;Conduce el Batimóvil;Su símbolo es un murciélago
Spider-Man|Peter Parker;Hombre Araña|Superhéroes|ficticio|Nueva York|cómics|Trepa paredes;Lanza telarañas;Fue mordido por una araña
Mujer Maravilla|Wonder Woman;Diana|Superhéroes|ficticio|Themyscira|cómics|Usa el Lazo de la Verdad;Es una amazona;También se llama Diana
Mickey Mouse|Mickey|Disney y Pixar|ficticio|Disney|animación|Es un ratón;Su pareja es Minnie;Usa guantes blancos
Elsa|Reina Elsa|Disney y Pixar|ficticio|Arendelle|animación|Es hermana de Anna;Controla hielo y nieve;Canta Libre soy
Simba|Rey Simba|Disney y Pixar|ficticio|África|animación|Es un león;Su padre es Mufasa;Protagoniza El rey león
Woody|Sheriff Woody|Disney y Pixar|ficticio|Toy Story|animación|Es un vaquero de juguete;Perteneció a Andy;Es amigo de Buzz
Buzz Lightyear|Buzz|Disney y Pixar|ficticio|Toy Story|animación|Es un guardián espacial de juguete;Dice al infinito y más allá;Es amigo de Woody
José de San Martín|San Martín|Historia|real|Argentina|siglo XIX|Nació en Yapeyú;Cruzó los Andes;Fue libertador de Argentina Chile y Perú
Cleopatra|Cleopatra VII|Historia|real|Egipto|Antigüedad|Fue reina de Egipto;Se vinculó con Julio César;Perteneció a la dinastía ptolemaica
Mahatma Gandhi|Gandhi|Historia|real|India|siglo XX|Defendió la resistencia no violenta;Estudió Derecho;Ayudó a la independencia de India
Elvis Presley|Elvis|Música|real|Estados Unidos|siglo XX|Fue llamado Rey del Rock;Vivió en Graceland;Popularizó Jailhouse Rock
Cristiano Ronaldo|Cristiano;CR7|Fútbol|real|Portugal|actualidad|Fue capitán de Portugal;Usa el número 7;Jugó en Real Madrid
""",
"medio": """
Marie Curie|Curie|Ciencia|real|Polonia y Francia|siglos XIX y XX|Investigó la radiactividad;Ganó dos premios Nobel;Descubrió radio y polonio
Napoleón Bonaparte|Napoleón|Historia|real|Francia|siglo XIX|Nació en Córcega;Fue emperador;Fue derrotado en Waterloo
Frida Kahlo|Frida|Arte|real|México|siglo XX|Pintó muchos autorretratos;Estuvo casada con Diego Rivera;Vivió en la Casa Azul
Freddie Mercury|Freddie|Música|real|Reino Unido|siglo XX|Fue cantante de Queen;Nació en Zanzíbar;Compuso Bohemian Rhapsody
Charly García|Charly|Música|real|Argentina|actualidad|Integró Sui Generis;Es pianista y compositor;Grabó Clics modernos
Beyoncé|Beyoncé Knowles|Música|real|Estados Unidos|actualidad|Integró Destiny's Child;Es cantante y bailarina;Grabó Single Ladies
Pantera Negra|T'Challa;Black Panther|Superhéroes|ficticio|Wakanda|cómics|Es rey;Su traje usa vibranium;Protege una nación africana ficticia
Doctor Strange|Stephen Strange|Superhéroes|ficticio|Marvel|cómics|Fue cirujano;Practica magia;Usa el Ojo de Agamotto
Mulán|Fa Mulán|Disney y Pixar|ficticio|China|animación|Se disfraza de soldado;La acompaña Mushu;Su historia proviene de una antigua balada
Moana|Vaiana|Disney y Pixar|ficticio|Polinesia|animación|Navega por el océano;Conoce a Maui;Devuelve el corazón de Te Fiti
Stitch|Experimento 626|Disney y Pixar|ficticio|espacio exterior|animación|Es un extraterrestre azul;También se llama Experimento 626;Forma una familia con Lilo
Harry Potter|Harry|Cine y literatura|ficticio|Reino Unido|fantasía|Estudia en Hogwarts;Tiene una cicatriz en la frente;Enfrenta a Voldemort
Darth Vader|Anakin Skywalker|Cine|ficticio|Star Wars|ciencia ficción|Antes fue Anakin Skywalker;Usa sable láser rojo;Es padre de Luke
Michael Jordan|Jordan|Deportes|real|Estados Unidos|siglo XX|Ganó seis títulos NBA;Jugó en Chicago Bulls;Usó el número 23
Serena Williams|Serena|Deportes|real|Estados Unidos|actualidad|Ganó 23 Grand Slam individuales;Su hermana es Venus;Fue campeona olímpica
Usain Bolt|Bolt|Deportes|real|Jamaica|actualidad|Fue velocista;Tiene el récord de 100 metros;Celebraba con pose de rayo
Jorge Luis Borges|Borges|Literatura|real|Argentina|siglo XX|Escribió El Aleph;Fue director de la Biblioteca Nacional;Perdió progresivamente la vista
Abraham Lincoln|Lincoln|Historia|real|Estados Unidos|siglo XIX|Fue presidente;Lideró durante la Guerra Civil;Impulsó la abolición de la esclavitud
Charles Darwin|Darwin|Ciencia|real|Reino Unido|siglo XIX|Viajó en el Beagle;Explicó la selección natural;Publicó El origen de las especies
Pelé|Edson Arantes do Nascimento|Fútbol|real|Brasil|siglo XX|Ganó tres mundiales;Jugó en Santos;Fue llamado O Rei
""",
"dificil": """
Ada Lovelace|Augusta Ada King|Ciencia|real|Reino Unido|siglo XIX|Trabajó sobre la máquina analítica;Fue hija de Lord Byron;Escribió un algoritmo para números de Bernoulli
Mansa Musa|Musa I|Historia|real|Imperio de Malí|Edad Media|Gobernó Malí;Peregrinó a La Meca;Fue célebre por repartir oro
Olympe de Gouges|Marie Gouze|Historia|real|Francia|siglo XVIII|Escribió sobre derechos de la mujer;Vivió la Revolución francesa;Murió guillotinada
Emmy Noether|Noether|Ciencia|real|Alemania|siglo XX|Fue matemática;Relacionó simetrías y conservación;Aportó al álgebra abstracta
Srinivasa Ramanujan|Ramanujan|Ciencia|real|India|siglo XX|Fue matemático autodidacta;Colaboró con Hardy;Trabajó en teoría de números
Vera Rubin|Rubin|Ciencia|real|Estados Unidos|siglo XX|Estudió galaxias;Aportó evidencia de materia oscura;Fue astrónoma
Juan Manuel Fangio|Fangio|Deportes|real|Argentina|siglo XX|Nació en Balcarce;Ganó cinco títulos de Fórmula 1;Fue campeón con cuatro escuderías
Nadia Comăneci|Comăneci;Nadia|Deportes|real|Rumania|siglo XX|Fue gimnasta;Logró el primer 10 olímpico perfecto;Ganó cinco oros olímpicos
Billie Jean King|Billie Jean|Deportes|real|Estados Unidos|siglo XX|Fue tenista;Jugó la Batalla de los Sexos;Impulsó premios deportivos iguales
David Bowie|Bowie;Ziggy Stardust|Música|real|Reino Unido|siglo XX|Creó a Ziggy Stardust;Actuó en Labyrinth;Su apellido artístico era Bowie
Nina Simone|Eunice Waymon|Música|real|Estados Unidos|siglo XX|Fue pianista y cantante;Su nombre real era Eunice Waymon;Cantó por los derechos civiles
Akira Kurosawa|Kurosawa|Cine|real|Japón|siglo XX|Dirigió Los siete samuráis;Influyó en cineastas occidentales;Trabajó con Toshiro Mifune
Moon Knight|Marc Spector|Superhéroes|ficticio|Marvel|cómics|Una identidad es Marc Spector;Está ligado a Khonshu;Viste principalmente de blanco
Zatanna|Zatanna Zatara|Superhéroes|ficticio|DC Comics|cómics|Es hechicera;Pronuncia conjuros al revés;Su padre es Zatara
Yzma|Consejera Yzma|Disney y Pixar|ficticio|Imperio de Kuzco|animación|Es enemiga de Kuzco;Su ayudante es Kronk;Usa pociones
Edna Moda|Edna|Disney y Pixar|ficticio|Los Increíbles|animación|Diseña trajes de superhéroes;No permite capas;Es muy pequeña y autoritaria
Lotso|Lotso Abrazos|Disney y Pixar|ficticio|Toy Story|animación|Es un oso rosado;Huele a frutillas;Controla Sunnyside
Violeta Parra|Violeta|Música|real|Chile|siglo XX|Compuso Gracias a la vida;Investigó folclore chileno;También creó obras visuales
Ernest Shackleton|Shackleton|Exploración|real|Irlanda y Reino Unido|siglo XX|Exploró la Antártida;Comandó el Endurance;Rescató a toda su tripulación
Avicena|Ibn Sina|Ciencia e historia|real|Persia|Edad Media|Fue médico y filósofo;Escribió El canon de medicina;También es conocido como Ibn Sina
""",
}

EXTRA_ROWS = {
"facil": """
Ariel|La Sirenita|Disney y Pixar|ficticio|Atlántica|animación|Es una princesa sirena;Su padre es el rey Tritón;Sueña con vivir en la superficie
Hulk|Bruce Banner|Superhéroes|ficticio|Marvel|cómics|Su identidad es Bruce Banner;Tiene enorme fuerza;Su piel suele ser verde
Mario Bros.|Mario;Super Mario|Videojuegos|ficticio|Reino Champiñón|videojuegos|Es plomero;Usa gorra roja;Rescata a la princesa Peach
Madonna|Reina del Pop|Música|real|Estados Unidos|actualidad|Es cantante y actriz;Grabó Like a Virgin;Fue llamada Reina del Pop
Kylian Mbappé|Mbappé;Kylian|Fútbol|real|Francia|actualidad|Fue campeón mundial en 2018;Es delantero;Jugó en Paris Saint-Germain
""",
"medio": """
Loki|Dios del Engaño|Superhéroes|ficticio|Asgard|cómics|Es hermano adoptivo de Thor;Es conocido por sus engaños;Usa magia
Rapunzel|Princesa Rapunzel|Disney y Pixar|ficticio|Corona|animación|Tiene cabello extremadamente largo;Vive encerrada en una torre;La acompaña Pascal
Roger Federer|Federer|Deportes|real|Suiza|actualidad|Fue tenista profesional;Ganó veinte Grand Slam individuales;Destacó sobre césped
Adele|Adele Adkins|Música|real|Reino Unido|actualidad|Es cantante;Grabó Hello;Sus álbumes suelen tener títulos numéricos
Galileo Galilei|Galileo|Ciencia|real|Italia|siglos XVI y XVII|Mejoró el telescopio;Estudió lunas de Júpiter;Defendió el heliocentrismo
""",
"dificil": """
Hades|Hades de Hércules|Disney y Pixar|ficticio|Inframundo|animación|Es villano en Hércules;Tiene cabello de fuego azul;Gobierna el inframundo
Gambito|Remy LeBeau|Superhéroes|ficticio|Marvel|cómics|Es miembro de X-Men;Carga objetos con energía;Suele usar cartas de juego
Rachel Carson|Carson|Ciencia|real|Estados Unidos|siglo XX|Fue bióloga marina;Escribió Primavera silenciosa;Impulsó el movimiento ambiental moderno
Atahualpa Yupanqui|Yupanqui|Música|real|Argentina|siglo XX|Fue cantor y guitarrista;Investigó música popular;Compuso El arriero
Boudica|Boudicca|Historia|real|Britania|Antigüedad|Fue reina de los icenos;Lideró una rebelión contra Roma;Vivió en el siglo I
""",
}


GENERIC = {
    "real": ["Es una persona real.", "Su nombre aparece en libros y registros.", "Alcanzó reconocimiento internacional."],
    "ficticio": ["Es un personaje ficticio.", "Aparece en historias conocidas.", "Tiene una imagen muy reconocible."],
}


def build_incognito():
    cards = []
    for difficulty, raw in ROWS.items():
        combined = raw.strip() + "\n" + EXTRA_ROWS[difficulty].strip()
        rows = [line.strip().split("|") for line in combined.splitlines() if line.strip()]
        if len(rows) != 25:
            raise ValueError(f"Incógnito requiere 25 personajes {difficulty}")
        for name, aliases, category, kind, origin, era, facts_raw in rows:
            facts = facts_raw.split(";")
            words = name.split()
            letters = sum(ch.isalpha() for ch in name)
            clues = [
                "Puede ser una figura real o un personaje de ficción.",
                f"Pertenece al mundo de {category.lower()}.",
                GENERIC[kind][0], GENERIC[kind][1],
                f"Se relaciona con {origin}.", f"Su historia se ubica principalmente en {era}.",
                GENERIC[kind][2], f"Su nivel en este juego es {difficulty}.",
                "Es conocido por personas de distintas generaciones.",
                f"Una pista importante está vinculada con {category.lower()}.",
                *[fact + "." for fact in facts],
                f"Su nombre tiene {len(words)} palabra{'s' if len(words) != 1 else ''}.",
                f"Su nombre comienza con la letra {name[0].upper()}.",
                f"Su nombre completo tiene {letters} letras.",
                f"La última letra de su nombre es {name[-1].upper()}.",
                f"Sus iniciales son {'.'.join(word[0].upper() for word in words)}.",
                f"Una forma alternativa de nombrarlo es {aliases.split(';')[0]}.",
                f"La pista decisiva: {facts[-1]}.",
            ]
            cards.append({"difficulty": difficulty, "category": category, "prompt": name,
                          "aliases": [name, *aliases.split(";")], "clues": clues[:20]})
    return cards
