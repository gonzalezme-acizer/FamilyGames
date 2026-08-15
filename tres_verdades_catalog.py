"""Banco factual para Tres verdades y una mentira."""

CARDS = [
    # Personajes históricos
    ("José de San Martín","Historia","facil",["Nació en Yapeyú.","Cruzó los Andes al frente del Ejército de los Andes.","Participó en las independencias de Argentina, Chile y Perú."],"Fue presidente de Argentina durante dos mandatos."),
    ("Cleopatra VII","Historia","facil",["Fue la última gobernante activa del Egipto ptolemaico.","Tuvo alianzas con Julio César y Marco Antonio.","Pertenecía a una dinastía de origen macedonio-griego."],"Mandó construir la Gran Pirámide de Guiza."),
    ("Mahatma Gandhi","Historia","facil",["Impulsó la resistencia no violenta.","Estudió Derecho en Londres.","Trabajó durante años en Sudáfrica."],"Recibió el Premio Nobel de la Paz en 1947."),
    ("Napoleón Bonaparte","Historia","medio",["Nació en Córcega.","Fue coronado emperador de los franceses.","Fue derrotado definitivamente en Waterloo."],"Murió exiliado en la isla de Elba."),
    ("Juana de Arco","Historia","medio",["Participó en la Guerra de los Cien Años.","Fue condenada y quemada en Ruan.","La Iglesia católica la canonizó siglos después."],"Llegó a ser reina de Francia."),
    ("Nelson Mandela","Historia","medio",["Pasó 27 años encarcelado.","Fue presidente de Sudáfrica.","Compartió el Nobel de la Paz de 1993."],"Nació en Ciudad del Cabo en 1925."),
    ("Leonardo da Vinci","Historia","dificil",["Pintó La última cena.","Escribía muchas notas con escritura especular.","Diseccionó cuerpos para estudiar anatomía."],"Construyó y voló con éxito un helicóptero de tamaño real."),
    ("Ada Lovelace","Historia","dificil",["Fue hija del poeta Lord Byron.","Trabajó sobre la máquina analítica de Charles Babbage.","Describió un algoritmo para calcular números de Bernoulli."],"Construyó la primera computadora electrónica en su casa."),
    ("Mansa Musa","Historia","dificil",["Gobernó el Imperio de Malí.","Realizó una célebre peregrinación a La Meca.","Su viaje distribuyó enormes cantidades de oro."],"Conquistó personalmente el Imperio romano de Oriente."),
    ("Olympe de Gouges","Historia","dificil",["Escribió la Declaración de los Derechos de la Mujer y de la Ciudadana.","Vivió durante la Revolución francesa.","Murió guillotinada en 1793."],"Fue la primera mujer elegida presidenta de Francia."),
    # Deportes
    ("Lionel Messi","Deportes","facil",["Nació en Rosario.","Ganó el Mundial de 2022 con Argentina.","Jugó más de veinte temporadas en el primer equipo del Barcelona."],"Ganó una medalla olímpica de oro en natación."),
    ("Michael Jordan","Deportes","facil",["Ganó seis campeonatos de la NBA con Chicago Bulls.","Usó principalmente el número 23.","Jugó béisbol profesional durante su primera retirada."],"Fue elegido número uno del draft de la NBA de 1984."),
    ("Serena Williams","Deportes","facil",["Ganó 23 títulos individuales de Grand Slam.","Su hermana Venus también fue campeona de tenis.","Ganó oros olímpicos en singles y dobles."],"Representó deportivamente a Canadá."),
    ("Usain Bolt","Deportes","medio",["Nació en Jamaica.","Posee el récord mundial de 100 metros con 9,58 segundos.","Ganó ocho medallas olímpicas de oro."],"Compitió en salto con garrocha en tres Juegos Olímpicos."),
    ("Manu Ginóbili","Deportes","medio",["Ganó cuatro campeonatos de la NBA.","Fue campeón olímpico con Argentina en 2004.","Jugó toda su carrera NBA en San Antonio Spurs."],"Fue seleccionado con la primera elección del draft de la NBA."),
    ("Nadia Comăneci","Deportes","medio",["Logró el primer 10 perfecto de la gimnasia olímpica.","Nació en Rumania.","Consiguió cinco oros olímpicos."],"Su primer 10 perfecto ocurrió en los Juegos de Moscú 1980."),
    ("Juan Manuel Fangio","Deportes","dificil",["Ganó cinco campeonatos mundiales de Fórmula 1.","Fue campeón con cuatro escuderías diferentes.","Nació en Balcarce."],"Obtuvo todos sus títulos después de cumplir 50 años."),
    ("Billie Jean King","Deportes","dificil",["Ganó 39 títulos de Grand Slam contando todas las modalidades.","Venció a Bobby Riggs en la Batalla de los Sexos.","Impulsó la igualdad de premios en el tenis."],"Nunca ganó el torneo de Wimbledon."),
    ("Garry Kasparov","Deportes","dificil",["Fue campeón mundial de ajedrez a los 22 años.","Disputó partidas famosas contra la computadora Deep Blue.","Nació en Bakú."],"Conservó el título mundial sin interrupción hasta 2010."),
    ("Jutta Kleinschmidt","Deportes","dificil",["Ganó la clasificación general del Rally Dakar.","Es ingeniera de formación.","Compitió tanto en motocicletas como en automóviles."],"Fue la primera mujer campeona mundial de Fórmula 1."),
    # Artistas
    ("Shakira","Arte y música","facil",["Nació en Barranquilla.","Grabó canciones en español e inglés.","Participó en el espectáculo de medio tiempo del Super Bowl 2020."],"Ganó un Premio Óscar como mejor actriz."),
    ("Michael Jackson","Arte y música","facil",["Integró The Jackson 5.","Publicó el álbum Thriller.","Popularizó el paso de baile moonwalk."],"Compuso la banda sonora completa de Titanic."),
    ("Frida Kahlo","Arte y música","facil",["Nació en Coyoacán, México.","Realizó numerosos autorretratos.","Estuvo casada con Diego Rivera."],"Fue una destacada escultora nacida en España."),
    ("Freddie Mercury","Arte y música","medio",["Fue cantante principal de Queen.","Nació en Zanzíbar.","Escribió Bohemian Rhapsody."],"Su nombre de nacimiento era David Robert Jones."),
    ("Mercedes Sosa","Arte y música","medio",["Nació en Tucumán.","Fue conocida como La Negra.","Integró el Movimiento del Nuevo Cancionero."],"Fue la voz principal de Soda Stereo."),
    ("Hayao Miyazaki","Arte y música","medio",["Cofundó Studio Ghibli.","Dirigió El viaje de Chihiro.","También trabajó como animador y guionista."],"Creó la serie Los Simpson."),
    ("David Bowie","Arte y música","dificil",["Interpretó al personaje Ziggy Stardust.","Actuó en la película Labyrinth.","Su apellido artístico no era su apellido de nacimiento."],"Nació con el nombre Freddie Mercury."),
    ("Nina Simone","Arte y música","dificil",["Fue pianista y cantante.","Su nombre de nacimiento era Eunice Waymon.","Su obra estuvo ligada al movimiento por los derechos civiles."],"Ganó fama inicialmente como baterista de jazz."),
    ("Akira Kurosawa","Arte y música","dificil",["Dirigió Los siete samuráis.","Fue cineasta japonés.","Su obra influyó en directores occidentales."],"Dirigió la trilogía original de El Padrino."),
    ("Toni Morrison","Arte y música","dificil",["Escribió Beloved.","Recibió el Nobel de Literatura.","Fue editora antes de dedicarse plenamente a escribir."],"Escribió originalmente sus novelas en francés."),
    # Científicos
    ("Albert Einstein","Ciencia","facil",["Desarrolló la teoría de la relatividad especial.","Recibió el Nobel de Física por el efecto fotoeléctrico.","Nació en Alemania."],"Recibió el Nobel por descubrir la penicilina."),
    ("Marie Curie","Ciencia","facil",["Ganó dos premios Nobel.","Investigó la radiactividad.","Descubrió junto con Pierre Curie los elementos polonio y radio."],"Fue la primera persona en caminar sobre la Luna."),
    ("Charles Darwin","Ciencia","facil",["Viajó en el HMS Beagle.","Publicó El origen de las especies.","Desarrolló la idea de selección natural."],"Formuló las tres leyes del movimiento planetario."),
    ("Nikola Tesla","Ciencia","medio",["Trabajó con sistemas de corriente alterna.","Nació en Smiljan, en el actual territorio de Croacia.","Una unidad de campo magnético lleva su apellido."],"Inventó y comercializó el primer teléfono inteligente."),
    ("Jane Goodall","Ciencia","medio",["Estudió chimpancés en Gombe.","Nació en Londres.","Documentó que los chimpancés fabrican y usan herramientas."],"Realizó su investigación principal con osos polares en Canadá."),
    ("Alan Turing","Ciencia","medio",["Contribuyó al descifrado de Enigma.","Propuso una prueba sobre inteligencia de máquinas.","Fue matemático británico."],"Dirigió la misión Apolo 11."),
    ("Emmy Noether","Ciencia","dificil",["Realizó aportes fundamentales al álgebra abstracta.","Un teorema suyo vincula simetrías y leyes de conservación.","Enseñó durante un tiempo sin salario ni cargo oficial."],"Descubrió la estructura de doble hélice del ADN."),
    ("Rosalind Franklin","Ciencia","dificil",["Trabajó con difracción de rayos X.","La Fotografía 51 fue clave para estudiar el ADN.","También investigó virus y carbón."],"Compartió el Nobel de 1962 con Watson, Crick y Wilkins."),
    ("Srinivasa Ramanujan","Ciencia","dificil",["Fue un matemático indio.","Colaboró con G. H. Hardy en Cambridge.","Realizó importantes aportes a la teoría de números."],"Recibió formación doctoral en física nuclear en París."),
    ("Vera Rubin","Ciencia","dificil",["Estudió la rotación de galaxias.","Su trabajo aportó evidencia de materia oscura.","Fue astrónoma estadounidense."],"Descubrió el planeta Neptuno mediante observación directa."),
    # Superhéroes
    ("Superman","Superhéroes","facil",["Su nombre kryptoniano es Kal-El.","Creció en Smallville.","Trabaja como periodista bajo la identidad de Clark Kent."],"Nació en Ciudad Gótica como Bruce Wayne."),
    ("Batman","Superhéroes","facil",["Su identidad es Bruce Wayne.","Protege Ciudad Gótica.","No posee superpoderes sobrehumanos permanentes."],"Fue enviado a la Tierra desde el planeta Krypton."),
    ("Spider-Man","Superhéroes","facil",["Su identidad más conocida es Peter Parker.","Fue criado por sus tíos Ben y May.","Trabaja como fotógrafo en varias de sus historias."],"Su escudo está hecho de vibranium."),
    ("Mujer Maravilla","Superhéroes","medio",["También es conocida como Diana.","Procede de Themyscira.","Utiliza el Lazo de la Verdad."],"Es hermana biológica de Batman."),
    ("Pantera Negra","Superhéroes","medio",["T'Challa es rey de Wakanda.","Su traje utiliza vibranium.","Debutó en un cómic de Los Cuatro Fantásticos."],"Obtuvo sus poderes tras ser mordido por una araña radiactiva."),
    ("Doctor Strange","Superhéroes","medio",["Fue cirujano antes de estudiar magia.","Su nombre es Stephen Strange.","Está asociado con el Ojo de Agamotto."],"Es el gobernante hereditario de Asgard."),
    ("Moon Knight","Superhéroes","dificil",["Una de sus identidades es Marc Spector.","Está vinculado al dios egipcio Khonshu.","Ha trabajado como mercenario."],"Es originario del planeta Marte."),
    ("Zatanna","Superhéroes","dificil",["Es una hechicera de DC Comics.","Suele lanzar conjuros pronunciando palabras al revés.","Su padre es el mago Zatara."],"Es prima de Diana de Themyscira."),
    ("Magneto","Superhéroes","dificil",["Puede controlar campos magnéticos.","Es un personaje central de las historias de X-Men.","Sobrevivió al Holocausto en muchas versiones."],"Su identidad civil más conocida es Norman Osborn."),
    ("Hellboy","Superhéroes","dificil",["Fue creado por Mike Mignola.","Trabaja con una agencia dedicada a lo paranormal.","Posee una gran mano de piedra llamada Mano Derecha del Destino."],"Fue creado originalmente como compañero de Superman."),
    # Disney y Pixar
    ("Mickey Mouse","Disney y Pixar","facil",["Debutó en Steamboat Willie en 1928.","Su pareja es Minnie Mouse.","Pluto es su perro."],"Fue creado como villano principal de Blancanieves."),
    ("Elsa","Disney y Pixar","facil",["Es reina de Arendelle.","Tiene poderes relacionados con el hielo.","Anna es su hermana."],"Es hija del rey Tritón y vive bajo el mar."),
    ("Woody","Disney y Pixar","facil",["Es un muñeco vaquero.","Pertenece originalmente a Andy.","Es amigo de Buzz Lightyear."],"Es el villano que gobierna la ciudad de Monstruópolis."),
    ("Mulán","Disney y Pixar","medio",["Se disfraza de soldado.","Mushu la acompaña en la película animada.","Su historia está inspirada en una antigua balada china."],"Nació como princesa de Arendelle."),
    ("Remy","Disney y Pixar","medio",["Es una rata con talento para cocinar.","Protagoniza Ratatouille.","Ayuda a Linguini en un restaurante parisino."],"Es el dueño humano del restaurante Gusteau's."),
    ("WALL-E","Disney y Pixar","medio",["Es un robot compactador de basura.","Conoce a un robot llamado EVA.","Permanece inicialmente en una Tierra abandonada."],"Fue diseñado para gobernar la nave Axiom como capitán."),
    ("Yzma","Disney y Pixar","dificil",["Es la antagonista de Las locuras del emperador.","Tiene un ayudante llamado Kronk.","Intenta convertir a Kuzco mediante una poción."],"Es la madre de la princesa Rapunzel."),
    ("Edna Moda","Disney y Pixar","dificil",["Diseña trajes para superhéroes.","Aparece en Los Increíbles.","Se opone firmemente a usar capas."],"Posee el poder de volverse invisible."),
    ("Lotso","Disney y Pixar","dificil",["Es un oso de peluche rosado.","Huele a frutillas.","Controla la guardería Sunnyside."],"Es el juguete favorito de Andy desde la primera Toy Story."),
    ("Madame Mim","Disney y Pixar","dificil",["Aparece en La espada en la piedra.","Compite en un duelo mágico con Merlín.","Puede transformarse en distintos animales."],"Es el hada madrina de Cenicienta.")
]


def build_three_truths():
    cards=[]
    for name,category,difficulty,truths,lie in CARDS:
        statements=[{"text":text,"lie":False} for text in truths]+[{"text":lie,"lie":True}]
        cards.append({"category":category,"difficulty":difficulty,"prompt":name,"statements":statements})
    return cards
