"""Banco de 300 personajes para ¿Quién soy?"""

CATEGORY_HINTS = {
    "Disney y Pixar": "Es un personaje de Disney o Pixar.",
    "Superhéroes": "Es un superhéroe, villano o personaje de cómics.",
    "Cine y series": "Es un personaje o figura muy relacionada con el cine o las series.",
    "Historia": "Es una figura histórica.",
    "Deportes": "Es una figura del deporte.",
    "Música": "Es cantante, músico o compositor.",
    "Literatura": "Es un personaje o autor relacionado con la literatura.",
    "Animación y juegos": "Es un personaje animado, de anime o de videojuegos.",
    "Ciencia y exploración": "Es una figura de la ciencia, la invención o la exploración.",
    "Argentina y Latinoamérica": "Es una personalidad de Argentina o Latinoamérica.",
}


CATALOG = {
    "facil": {
        "Disney y Pixar": "Mickey Mouse|Minnie Mouse|Pato Donald|Goofy|Elsa|Simba|Woody|Buzz Lightyear|Stitch|Moana",
        "Superhéroes": "Superman|Batman|Spider-Man|Mujer Maravilla|Hulk|Iron Man|Capitán América|Thor|Pantera Negra|Flash",
        "Cine y series": "Harry Potter|Darth Vader|Shrek|Merlina Addams|Homero Simpson|Indiana Jones|Mr. Bean|Rocky Balboa|Jack Sparrow|Barbie",
        "Historia": "José de San Martín|Manuel Belgrano|Domingo F. Sarmiento|Napoleón Bonaparte|Cleopatra|Cristóbal Colón|Mahatma Gandhi|Abraham Lincoln|Juana de Arco|Reina Isabel II",
        "Deportes": "Lionel Messi|Diego Maradona|Pelé|Kylian Mbappé|Cristiano Ronaldo|Manu Ginóbili|Serena Williams|Rafael Nadal|Usain Bolt|Michael Phelps",
        "Música": "Michael Jackson|Shakira|Taylor Swift|Madonna|Freddie Mercury|Elvis Presley|Beyoncé|Bad Bunny|Lali Espósito|Fito Páez",
        "Literatura": "El Principito|Don Quijote|Sherlock Holmes|Pinocho|Peter Pan|Alicia en el País de las Maravillas|Drácula|Monstruo de Frankenstein|Caperucita Roja|Robin Hood",
        "Animación y juegos": "Bob Esponja|Peppa Pig|Pikachu|Mario Bros.|Luigi|Sonic|Goku|Naruto|Scooby-Doo|Tom de Tom y Jerry",
        "Ciencia y exploración": "Albert Einstein|Neil Armstrong|Marie Curie|Charles Darwin|Galileo Galilei|Isaac Newton|Nikola Tesla|Jane Goodall|Stephen Hawking|Amelia Earhart",
        "Argentina y Latinoamérica": "Papa Francisco|Mirtha Legrand|Susana Giménez|Ricardo Darín|Mafalda|Quino|Jorge Luis Borges|Mercedes Sosa|Gustavo Cerati|Frida Kahlo"
    },
    "medio": {
        "Disney y Pixar": "Mulán|Tiana|Rapunzel|Mérida|Miguel de Coco|Alegría de Intensamente|Remy de Ratatouille|WALL-E|Maléfica|Hércules de Disney",
        "Superhéroes": "Doctor Strange|Bruja Escarlata|Aquaman|Linterna Verde|Wolverine|Deadpool|Viuda Negra|Loki|Profesor X|Harley Quinn",
        "Cine y series": "Forrest Gump|Hannibal Lecter|E.T.|Marty McFly|Neo de Matrix|Katniss Everdeen|Eleven de Stranger Things|Walter White|El Zorro|Mary Poppins",
        "Historia": "Julio César|Marco Polo|Alejandro Magno|Winston Churchill|Simón Bolívar|Tutankamón|Ana Frank|Martin Luther King Jr.|Catalina la Grande|Nelson Mandela",
        "Deportes": "Roger Federer|Novak Djokovic|Michael Jordan|LeBron James|Simone Biles|Lewis Hamilton|Ayrton Senna|Marta Vieira|Tiger Woods|Muhammad Ali",
        "Música": "Adele|Bruno Mars|Lady Gaga|Sting|Paul McCartney|John Lennon|Bob Marley|Luis Miguel|Karol G|Charly García",
        "Literatura": "Romeo|Julieta Capuleto|Hércules Poirot|Matilda Wormwood|Huckleberry Finn|Dorian Gray|Capitán Nemo|Willy Wonka|Gregor Samsa|Mary Poppins de los libros",
        "Animación y juegos": "Ash Ketchum|Sailor Moon|Vegeta|Aang|Shrek Gato con Botas|Crash Bandicoot|Link de Zelda|Kirby|Donkey Kong|Dora la Exploradora",
        "Ciencia y exploración": "Ada Lovelace|Alan Turing|Louis Pasteur|Sigmund Freud|Carl Sagan|Jacques Cousteau|Valentina Tereshkova|Alexander Fleming|Johannes Kepler|Rosalind Franklin",
        "Argentina y Latinoamérica": "Julio Cortázar|Gabriel García Márquez|Diego Rivera|Celia Cruz|Chabuca Granda|Astor Piazzolla|Sandro|Tita Merello|René Favaloro|César Milstein"
    },
    "dificil": {
        "Disney y Pixar": "Yzma|Kuzco|Edna Moda|Úrsula|Jafar|Hades de Hércules|Randall de Monsters Inc.|Lotso|Pepita de Coco|Madame Mim",
        "Superhéroes": "Moon Knight|Shuri|Zatanna|Nightwing|Gambito|Raven|Magneto|Mística|Hellboy|Doctor Doom",
        "Cine y series": "Travis Bickle|Norma Desmond|Atticus Finch|Amélie Poulain|Don Draper|Saul Goodman|Fleabag|Dale Cooper|Ellen Ripley|Rick Blaine",
        "Historia": "Boudica|Avicena|Leonor de Aquitania|Mansa Musa|Suleimán el Magnífico|Olympe de Gouges|Toussaint Louverture|Otto von Bismarck|Emmeline Pankhurst|Haile Selassie",
        "Deportes": "Nadia Comăneci|Jesse Owens|Billie Jean King|Garry Kasparov|Juan Manuel Fangio|Eddy Merckx|Martina Navratilova|Haile Gebrselassie|Teófilo Stevenson|Birgit Fischer",
        "Música": "Nina Simone|David Bowie|Kate Bush|Joni Mitchell|Caetano Veloso|Chico Buarque|Björn Ulvaeus|Ella Fitzgerald|Ennio Morricone|Joan Manuel Serrat",
        "Literatura": "Leopold Bloom|Raskólnikov|Emma Bovary|Aureliano Buendía|Sethe de Beloved|Ignatius Reilly|Meursault|Clarissa Dalloway|Funes el memorioso|Pedro Páramo",
        "Animación y juegos": "Spike Spiegel|Totoro|Lupin III|Samus Aran|Solid Snake|Chun-Li|Guybrush Threepwood|Saitama|Inuyasha|Leela de Futurama",
        "Ciencia y exploración": "Emmy Noether|Srinivasa Ramanujan|Lise Meitner|Niels Bohr|Rachel Carson|Edwin Hubble|Vera Rubin|Ernest Shackleton|Ibn Battuta|Gertrude Bell",
        "Argentina y Latinoamérica": "Alfonsina Storni|Roberto Arlt|Violeta Parra|João Gilberto|Chavela Vargas|Oswaldo Guayasamín|María Elena Walsh|Atahualpa Yupanqui|Lola Mora|Victoria Ocampo"
    }
}


def build_who_am_i():
    cards = []
    for difficulty, categories in CATALOG.items():
        for category, names in categories.items():
            for name in names.split("|"):
                clean = name.strip()
                letters = sum(character.isalpha() for character in clean)
                words = len(clean.split())
                hints = [
                    CATEGORY_HINTS[category],
                    f"Su nombre empieza con «{clean[0].upper()}» y tiene {words} palabra{'s' if words != 1 else ''}.",
                    f"Su nombre completo tiene {letters} letras y termina en «{clean[-1].upper()}».",
                ]
                cards.append({"category": category, "difficulty": difficulty, "prompt": clean, "hints": hints})
    return cards
