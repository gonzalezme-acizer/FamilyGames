"""Banco familiar de 300 canciones para Just Sing (sin letras)."""

RAW = {
"facil": """
Libre soy|Idina Menzel|2013|Disney y Pixar
No se habla de Bruno|Reparto de Encanto|2021|Disney y Pixar
Un mundo ideal|Brad Kane y Lea Salonga|1992|Disney y Pixar
Hakuna Matata|Nathan Lane y Ernie Sabella|1994|Disney y Pixar
Recuérdame|Benjamin Bratt|2017|Disney y Pixar
Cuán lejos voy|Auli'i Cravalho|2016|Disney y Pixar
Bajo el mar|Samuel E. Wright|1989|Disney y Pixar
Hay un amigo en mí|Randy Newman|1995|Disney y Pixar
Colores en el viento|Judy Kuhn|1995|Disney y Pixar
Parte de él|Jodi Benson|1989|Disney y Pixar
Yo voy a ser Rey León|Jason Weaver|1994|Disney y Pixar
Supercalifragilisticoespialidoso|Julie Andrews y Dick Van Dyke|1964|Películas familiares
Un poco loco|Anthony Gonzalez y Gael García Bernal|2017|Disney y Pixar
De nada|Dwayne Johnson|2016|Disney y Pixar
Mucho más allá|Idina Menzel|2019|Disney y Pixar
En mi corazón vivirás|Phil Collins|1999|Disney y Pixar
Busca lo más vital|Phil Harris y Bruce Reitherman|1967|Disney y Pixar
La familia Madrigal|Stephanie Beatriz|2021|Disney y Pixar
Qué hay más allá|Auli'i Cravalho|2024|Disney y Pixar
Bella y Bestia|Angela Lansbury|1991|Disney y Pixar
El reino del revés|María Elena Walsh|1964|Infantil
Manuelita la tortuga|María Elena Walsh|1962|Infantil
La reina Batata|María Elena Walsh|1966|Infantil
El twist del Mono Liso|María Elena Walsh|1962|Infantil
Canción de tomar el té|María Elena Walsh|1963|Infantil
La vaca estudiosa|María Elena Walsh|1963|Infantil
Arroz con leche|Tradicional|1900|Infantil
El patio de mi casa|Tradicional|1900|Infantil
Estrellita dónde estás|Tradicional|1806|Infantil
Los elefantes|Tradicional|1900|Infantil
La farolera|Tradicional|1900|Infantil
Que llueva|Tradicional|1900|Infantil
El payaso Plim Plim|El Reino Infantil|2011|Infantil
La gallina Turuleca|Gaby, Fofó y Miliki|1971|Infantil
Susanita tiene un ratón|Gaby, Fofó y Miliki|1974|Infantil
Hola Don Pepito|Los Payasos de la Tele|1971|Infantil
El auto de papá|Pipo Pescador|1972|Infantil
La batalla del movimiento|El Reino Infantil|2014|Infantil
Soy una taza|CantaJuego|2005|Infantil
Baby Shark|Pinkfong|2016|Infantil
Happy Birthday to You|Tradicional|1893|Clásico familiar
Color Esperanza|Diego Torres|2001|Clásico familiar
Vivir mi vida|Marc Anthony|2013|Latino familiar
La bicicleta|Carlos Vives y Shakira|2016|Latino familiar
Despacito|Luis Fonsi y Daddy Yankee|2017|Pop familiar
La vida es un carnaval|Celia Cruz|1998|Latino familiar
Waka Waka|Shakira|2010|Pop familiar
Muchachos, ahora nos volvimos a ilusionar|La Mosca|2022|Popular
Soy cordobés|Rodrigo|2000|Popular
La mano de Dios|Rodrigo|2000|Popular
De música ligera|Soda Stereo|1990|Rock familiar
Persiana americana|Soda Stereo|1986|Rock familiar
Lamento boliviano|Enanitos Verdes|1994|Rock familiar
Mil horas|Los Abuelos de la Nada|1983|Rock familiar
Flaca|Andrés Calamaro|1997|Rock familiar
Me gustas tú|Manu Chao|2001|Pop familiar
Corazón partío|Alejandro Sanz|1997|Pop familiar
La camisa negra|Juanes|2005|Pop familiar
Limón y sal|Julieta Venegas|2006|Pop familiar
Bonito|Jarabe de Palo|2003|Pop familiar
Shake It Off|Taylor Swift|2014|Pop internacional
Happy|Pharrell Williams|2013|Pop internacional
Roar|Katy Perry|2013|Pop internacional
Firework|Katy Perry|2010|Pop internacional
Uptown Funk|Mark Ronson y Bruno Mars|2014|Pop internacional
Count on Me|Bruno Mars|2010|Pop internacional
What Makes You Beautiful|One Direction|2011|Pop internacional
Can't Stop the Feeling!|Justin Timberlake|2016|Pop internacional
Dance Monkey|Tones and I|2019|Pop internacional
Flowers|Miley Cyrus|2023|Pop internacional
As It Was|Harry Styles|2022|Pop internacional
Blinding Lights|The Weeknd|2019|Pop internacional
Old Town Road|Lil Nas X|2019|Pop internacional
Believer|Imagine Dragons|2017|Pop internacional
Thunder|Imagine Dragons|2017|Pop internacional
We Will Rock You|Queen|1977|Clásico familiar
We Are the Champions|Queen|1977|Clásico familiar
Don't Stop Me Now|Queen|1978|Clásico familiar
I Want to Break Free|Queen|1984|Clásico familiar
Yellow Submarine|The Beatles|1966|Clásico familiar
Ob-La-Di, Ob-La-Da|The Beatles|1968|Clásico familiar
Here Comes the Sun|The Beatles|1969|Clásico familiar
Imagine|John Lennon|1971|Clásico familiar
Dancing Queen|ABBA|1976|Clásico familiar
Mamma Mia|ABBA|1975|Clásico familiar
I Will Survive|Gloria Gaynor|1978|Clásico familiar
YMCA|Village People|1978|Clásico familiar
September|Earth, Wind & Fire|1978|Clásico familiar
Take on Me|a-ha|1985|Clásico familiar
Girls Just Want to Have Fun|Cyndi Lauper|1983|Clásico familiar
Wake Me Up Before You Go-Go|Wham!|1984|Clásico familiar
Never Gonna Give You Up|Rick Astley|1987|Clásico familiar
Livin' on a Prayer|Bon Jovi|1986|Clásico familiar
Walking on Sunshine|Katrina and the Waves|1985|Clásico familiar
I Gotta Feeling|The Black Eyed Peas|2009|Pop familiar
Best Day of My Life|American Authors|2013|Pop familiar
Try Everything|Shakira|2016|Películas familiares
You're Welcome|Dwayne Johnson|2016|Disney y Pixar
Let It Go|Idina Menzel|2013|Disney y Pixar
We Don't Talk About Bruno|Reparto de Encanto|2021|Disney y Pixar
""",
"medio": """
Ji ji ji|Patricio Rey y sus Redonditos de Ricota|1986|Rock argentino
Seminare|Serú Girán|1978|Rock argentino|…Esas motos que van a mi…
Nos siguen pegando abajo|Charly García|1983|Rock argentino
11 y 6|Fito Páez|1985|Rock argentino
Mariposa Tecknicolor|Fito Páez|1994|Rock argentino
Cuando pase el temblor|Soda Stereo|1985|Rock argentino
Crimen|Gustavo Cerati|2006|Rock argentino
Seguir viviendo sin tu amor|Luis Alberto Spinetta|1991|Rock argentino
El amor después del amor|Fito Páez|1992|Rock argentino
Trátame suavemente|Soda Stereo|1984|Rock argentino
Costumbres argentinas|Los Abuelos de la Nada|1985|Rock argentino
Tirá para arriba|Miguel Mateos|1984|Rock argentino
La muralla verde|Enanitos Verdes|1986|Rock argentino
El extraño de pelo largo|La Joven Guardia|1968|Rock argentino
Sólo le pido a Dios|León Gieco|1978|Canción latinoamericana
Inconsciente colectivo|Charly García|1982|Rock argentino
Rasguña las piedras|Sui Generis|1973|Rock argentino
El oso|Moris|1970|Rock argentino
Una luna de miel en la mano|Virus|1985|Rock argentino
Imágenes paganas|Virus|1986|Rock argentino
Matador|Los Fabulosos Cadillacs|1993|Rock latino
Siguiendo la luna|Los Fabulosos Cadillacs|1992|Rock latino
El satánico Dr. Cadillac|Los Fabulosos Cadillacs|1989|Rock latino
La flaca|Jarabe de Palo|1996|Rock latino
Rayando el sol|Maná|1990|Rock latino
En el muelle de San Blas|Maná|1997|Rock latino
Oye mi amor|Maná|1992|Rock latino
Eres|Café Tacvba|2003|Rock latino
La ingrata|Café Tacvba|1994|Rock latino
Clavado en un bar|Maná|1997|Rock latino
La célula que explota|Caifanes|1990|Rock latino
Devuélveme a mi chica|Hombres G|1985|Rock español
La chica de ayer|Nacha Pop|1980|Rock español
Entre dos tierras|Héroes del Silencio|1990|Rock español
20 de abril|Celtas Cortos|1991|Rock español
Resistiré|Dúo Dinámico|1988|Pop español
A quién le importa|Alaska y Dinarama|1986|Pop español
Hijo de la luna|Mecano|1986|Pop español
Cruz de navajas|Mecano|1986|Pop español
La fuerza del destino|Mecano|1988|Pop español
Bailando|Enrique Iglesias|2014|Pop latino
Suerte|Shakira|2001|Pop latino
Antología|Shakira|1995|Pop latino
A Dios le pido|Juanes|2002|Pop latino
Es por ti|Juanes|2002|Pop latino
Andar conmigo|Julieta Venegas|2003|Pop latino
Me voy|Julieta Venegas|2006|Pop latino
Colgando en tus manos|Carlos Baute y Marta Sánchez|2008|Pop latino
Robarte un beso|Carlos Vives y Sebastián Yatra|2017|Pop latino
La gozadera|Gente de Zona y Marc Anthony|2015|Pop latino
Rolling in the Deep|Adele|2010|Pop internacional
Someone Like You|Adele|2011|Pop internacional
Just the Way You Are|Bruno Mars|2010|Pop internacional
Locked Out of Heaven|Bruno Mars|2012|Pop internacional
Poker Face|Lady Gaga|2008|Pop internacional
Bad Romance|Lady Gaga|2009|Pop internacional
Teenage Dream|Katy Perry|2010|Pop internacional
Since U Been Gone|Kelly Clarkson|2004|Pop internacional
Complicated|Avril Lavigne|2002|Pop internacional
Sk8er Boi|Avril Lavigne|2002|Pop internacional
Viva la Vida|Coldplay|2008|Pop internacional
Clocks|Coldplay|2002|Pop internacional
Somebody Told Me|The Killers|2004|Rock internacional
Mr. Brightside|The Killers|2003|Rock internacional
Use Somebody|Kings of Leon|2008|Rock internacional
Sex on Fire|Kings of Leon|2008|Rock internacional
Wonderwall|Oasis|1995|Rock internacional
Don't Look Back in Anger|Oasis|1996|Rock internacional
Zombie|The Cranberries|1994|Rock internacional
Linger|The Cranberries|1993|Rock internacional
Iris|Goo Goo Dolls|1998|Rock internacional
What's Up?|4 Non Blondes|1993|Rock internacional
Torn|Natalie Imbruglia|1997|Pop internacional
No Scrubs|TLC|1999|Pop internacional
Genie in a Bottle|Christina Aguilera|1999|Pop internacional
...Baby One More Time|Britney Spears|1998|Pop internacional
Bye Bye Bye|NSYNC|2000|Pop internacional
Everybody|Backstreet Boys|1997|Pop internacional
Wannabe|Spice Girls|1996|Pop internacional
Losing My Religion|R.E.M.|1991|Rock internacional
Under the Bridge|Red Hot Chili Peppers|1991|Rock internacional
Californication|Red Hot Chili Peppers|1999|Rock internacional
Basket Case|Green Day|1994|Rock internacional
In the End|Linkin Park|2000|Rock internacional
Bring Me to Life|Evanescence|2003|Rock internacional
Sweet Child o' Mine|Guns N' Roses|1987|Rock internacional
Every Breath You Take|The Police|1983|Rock internacional
With or Without You|U2|1987|Rock internacional
Africa|Toto|1982|Clásico internacional
Footloose|Kenny Loggins|1984|Películas
Ghostbusters|Ray Parker Jr.|1984|Películas
Eye of the Tiger|Survivor|1982|Películas
(I've Had) The Time of My Life|Bill Medley y Jennifer Warnes|1987|Películas
My Heart Will Go On|Celine Dion|1997|Películas
I Don't Want to Miss a Thing|Aerosmith|1998|Películas
Shallow|Lady Gaga y Bradley Cooper|2018|Películas
City of Stars|Ryan Gosling y Emma Stone|2016|Películas
This Is Me|Keala Settle|2017|Películas
Can't Fight the Moonlight|LeAnn Rimes|2000|Películas
Man! I Feel Like a Woman!|Shania Twain|1997|Pop internacional
""",
"dificil": """
Viernes 3 AM|Serú Girán|1979|Rock argentino
Desarma y sangra|Serú Girán|1980|Rock argentino
Canción para mi muerte|Sui Generis|1972|Rock argentino
Los dinosaurios|Charly García|1983|Rock argentino
Rezo por vos|Charly García y Luis Alberto Spinetta|1985|Rock argentino
Bajan|Pescado Rabioso|1973|Rock argentino
Muchacha ojos de papel|Almendra|1969|Rock argentino
Post-crucifixión|Pescado Rabioso|1973|Rock argentino
Barro tal vez|Luis Alberto Spinetta|1982|Rock argentino
Cantata de puentes amarillos|Pescado Rabioso|1973|Rock argentino
Presente|Vox Dei|1970|Rock argentino
Mañana campestre|Arco Iris|1971|Rock argentino
Jugo de tomate frío|Manal|1970|Rock argentino
Avellaneda blues|Manal|1970|Rock argentino
La grasa de las capitales|Serú Girán|1979|Rock argentino
Ruta 66|Pappo's Blues|1971|Rock argentino
Sucio y desprolijo|Pappo's Blues|1973|Rock argentino
El anillo del Capitán Beto|Invisible|1976|Rock argentino
Todas las hojas son del viento|Pescado Rabioso|1973|Rock argentino
Yo vengo a ofrecer mi corazón|Fito Páez|1985|Rock argentino
Todo cambia|Mercedes Sosa|1984|Folclore latinoamericano
Gracias a la vida|Violeta Parra|1966|Folclore latinoamericano
Alfonsina y el mar|Mercedes Sosa|1969|Folclore argentino
Zamba de mi esperanza|Jorge Cafrune|1964|Folclore argentino
Luna tucumana|Atahualpa Yupanqui|1949|Folclore argentino
Balderrama|Mercedes Sosa|1971|Folclore argentino
Tonada de un viejo amor|Eduardo Falú|1956|Folclore argentino
El cosechero|Ramón Ayala|1963|Folclore argentino
Ojalá|Silvio Rodríguez|1978|Trova
Unicornio|Silvio Rodríguez|1982|Trova
Yolanda|Pablo Milanés|1970|Trova
Te recuerdo Amanda|Víctor Jara|1969|Canción latinoamericana
Construção|Chico Buarque|1971|Música brasileña
Águas de Março|Elis Regina y Tom Jobim|1974|Música brasileña
Chega de Saudade|João Gilberto|1959|Música brasileña
Garota de Ipanema|Astrud Gilberto y Stan Getz|1964|Música brasileña
Eu sei que vou te amar|Tom Jobim y Vinicius de Moraes|1959|Música brasileña
Mediterráneo|Joan Manuel Serrat|1971|Canción española
Aquellas pequeñas cosas|Joan Manuel Serrat|1971|Canción española
Al alba|Luis Eduardo Aute|1975|Canción española
Pongamos que hablo de Madrid|Joaquín Sabina|1980|Canción española
19 días y 500 noches|Joaquín Sabina|1999|Canción española
Insurrección|El Último de la Fila|1986|Rock español
Lucha de gigantes|Nacha Pop|1987|Rock español
Escuela de calor|Radio Futura|1984|Rock español
Maldito duende|Héroes del Silencio|1990|Rock español
En algún lugar|Duncan Dhu|1987|Rock español
Déjame|Los Secretos|1980|Rock español
Cadillac solitario|Loquillo y Los Trogloditas|1983|Rock español
Santa Lucía|Miguel Ríos|1980|Rock español
A Day in the Life|The Beatles|1967|Clásico internacional
Strawberry Fields Forever|The Beatles|1967|Clásico internacional
While My Guitar Gently Weeps|The Beatles|1968|Clásico internacional
God Only Knows|The Beach Boys|1966|Clásico internacional
Good Vibrations|The Beach Boys|1966|Clásico internacional
The Sound of Silence|Simon & Garfunkel|1964|Clásico internacional
Mrs. Robinson|Simon & Garfunkel|1968|Clásico internacional
Space Oddity|David Bowie|1969|Clásico internacional
Life on Mars?|David Bowie|1971|Clásico internacional
Heroes|David Bowie|1977|Clásico internacional
Tiny Dancer|Elton John|1971|Clásico internacional
Rocket Man|Elton John|1972|Clásico internacional
Dreams|Fleetwood Mac|1977|Clásico internacional
Go Your Own Way|Fleetwood Mac|1976|Clásico internacional
The Chain|Fleetwood Mac|1977|Clásico internacional
Wish You Were Here|Pink Floyd|1975|Rock internacional
Time|Pink Floyd|1973|Rock internacional
Comfortably Numb|Pink Floyd|1979|Rock internacional
Baba O'Riley|The Who|1971|Rock internacional
Won't Get Fooled Again|The Who|1971|Rock internacional
Riders on the Storm|The Doors|1971|Rock internacional
People Are Strange|The Doors|1967|Rock internacional
White Rabbit|Jefferson Airplane|1967|Rock internacional
Piece of My Heart|Big Brother and the Holding Company|1968|Rock internacional
Fortunate Son|Creedence Clearwater Revival|1969|Rock internacional
Gimme Shelter|The Rolling Stones|1969|Rock internacional
Paint It, Black|The Rolling Stones|1966|Rock internacional
You Can't Always Get What You Want|The Rolling Stones|1969|Rock internacional
The Boxer|Simon & Garfunkel|1969|Clásico internacional
American Pie|Don McLean|1971|Clásico internacional
Vincent|Don McLean|1971|Clásico internacional
Me and Bobby McGee|Janis Joplin|1971|Clásico internacional
Both Sides, Now|Joni Mitchell|1969|Clásico internacional
Big Yellow Taxi|Joni Mitchell|1970|Clásico internacional
River|Joni Mitchell|1971|Clásico internacional
Wild World|Cat Stevens|1970|Clásico internacional
Father and Son|Cat Stevens|1970|Clásico internacional
Superstition|Stevie Wonder|1972|Soul
Sir Duke|Stevie Wonder|1976|Soul
What's Going On|Marvin Gaye|1971|Soul
Let's Stay Together|Al Green|1971|Soul
Ain't No Sunshine|Bill Withers|1971|Soul
Lean on Me|Bill Withers|1972|Soul
Respect|Aretha Franklin|1967|Soul
(You Make Me Feel Like) A Natural Woman|Aretha Franklin|1967|Soul
Son of a Preacher Man|Dusty Springfield|1968|Soul
At Last|Etta James|1960|Soul
Feeling Good|Nina Simone|1965|Jazz y soul
My Way|Frank Sinatra|1969|Clásico internacional
What a Wonderful World|Louis Armstrong|1967|Clásico internacional
"""
}

def build_just_sing():
    cards = []
    for difficulty, raw in RAW.items():
        rows = [line.strip().split("|") for line in raw.strip().splitlines() if line.strip()]
        if len(rows) != 100:
            raise ValueError(f"Just Sing requiere 100 canciones {difficulty}; hay {len(rows)}")
        for row in rows:
            title, artist, year, audience, *excerpt_parts = row
            excerpt = excerpt_parts[0].strip() if excerpt_parts else ""
            if excerpt and len(excerpt.split()) > 10:
                raise ValueError(f"El fragmento de {title} supera las 10 palabras")
            cards.append({
                "difficulty": difficulty,
                "title": title,
                "artist": artist,
                "year": int(year),
                "era": f"Década de {(int(year) // 10) * 10}",
                "audience": audience,
                "excerpt": excerpt,
                "clue": excerpt,
            })
    return cards
