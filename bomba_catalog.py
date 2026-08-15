"""Acertijos familiares para Alerta Bomba."""

RAW = {
"facil": """
mapa|mapamundi|Tengo ciudades sin casas, montañas sin árboles y agua sin peces.|Sirvo para orientarse;Represento lugares;Puedo doblarme;Tengo países y caminos;Soy un mapa
reloj|reloj de pared|Tengo agujas y números, pero no sé coser ni contar.|Suele estar a la vista;Mide algo invisible;Puede hacer tic tac;Marca horas;Soy un reloj
esponja||Tengo muchos agujeros y aun así puedo guardar agua.|Soy liviana;Vivo cerca del agua;Ayudo a limpiar;Me aprietan para escurrirme;Soy una esponja
peine||Tengo dientes, pero no muerdo.|Soy un objeto;Se usa con una mano;Ordeno algo de la cabeza;Paso entre el cabello;Soy un peine
botella||Tengo cuello, pero no tengo cabeza.|Soy un recipiente;Puedo ser de vidrio o plástico;Guardo líquidos;Tengo tapa;Soy una botella
mesa||Tengo cuatro patas, pero no puedo caminar.|Estoy en muchas casas;Sostengo objetos;La familia puede reunirse alrededor mío;No soy una silla;Soy una mesa
zapato|calzado|Tengo lengua, pero no hablo; tengo suela, pero no camino solo.|Se usa de a pares;Protejo una parte del cuerpo;Voy cerca del suelo;Me atan con cordones;Soy un zapato
libro||Tengo hojas, pero no soy un árbol.|Puedo abrirme y cerrarme;Guardo historias;Tengo páginas;Se me puede leer;Soy un libro
paraguas||Cuando llueve subo y cuando deja de llover bajo.|Se lleva con una mano;Puedo plegarme;Protejo del agua;Me abro sobre la cabeza;Soy un paraguas
vela||Cuanto más trabajo, más pequeña me vuelvo.|Doy luz;Puedo perfumar;Tengo una mecha;Me derrite el fuego;Soy una vela
eco||Te respondo aunque nunca te hago una pregunta.|No tengo cuerpo;Necesito un sonido;Se escucha en montañas o lugares vacíos;Repito lo que oigo;Soy el eco
sombra||Te sigo durante el día, pero desaparezco en la oscuridad.|No puedo tocarse;Dependo de la luz;Copio tu silueta;Estoy en el suelo o la pared;Soy una sombra
huevo||Tengo una casa blanca sin puertas ni ventanas y dentro vive algo amarillo.|Es alimento;Tengo cáscara;Puede cocinarse;Lo ponen las gallinas;Soy un huevo
nube||Viajo sin piernas y lloro sin ojos.|Estoy en el cielo;Cambio de forma;Estoy hecha de gotas;Puedo traer lluvia;Soy una nube
toalla||Cuanto más seco, más mojada quedo.|Soy de tela;Estoy en el baño;Absorbo agua;Sirvo después de bañarse;Soy una toalla
globo||Me inflan para crecer y una punta puede terminar conmigo.|Soy liviano;Puedo decorar fiestas;Tengo aire dentro;Puedo explotar;Soy un globo
llave||Soy pequeña, de metal y abro cosas grandes.|Entro en una cerradura;Suele llevarse en un llavero;Abro puertas;Tengo dientes de metal;Soy una llave
semáforo||Tengo tres ojos y nunca puedo ver.|Estoy en la calle;Organizo el tránsito;Uso luces;Mis colores son rojo amarillo y verde;Soy un semáforo
lápiz||Dejo una huella gris y pierdo la cabeza cuando trabajo.|Se usa con la mano;Puede sacarse punta;Sirvo para escribir;Tengo grafito;Soy un lápiz
guitarra||Tengo seis cuerdas y una boca que no habla.|Soy instrumento musical;Se toca con ambas manos;Tengo un mástil;Puedo rasguearse;Soy una guitarra
""",
"medio": """
silencio||Si dices mi nombre, dejo de existir.|No soy un objeto;Puede llenar una habitación;Se rompe con un sonido;Es ausencia de ruido;Soy el silencio
mañana||Siempre está por venir, pero cuando llega cambia de nombre.|Se relaciona con el tiempo;Nadie puede vivir en mí todavía;Sigo al día de hoy;Cuando llego soy presente;Soy mañana
secreto||Si me tienes quieres compartirlo, pero si lo compartes dejas de tenerlo.|No es material;Puede pasar entre personas;Conviene guardarlo;Deja de ser privado al contarlo;Soy un secreto
edad||Aumenta todos los años y nunca puede disminuir.|Todos tenemos una;Se mide con números;Cambia en los cumpleaños;Indica cuánto tiempo viviste;Es la edad
promesa||Se puede romper sin tocarla.|Se hace con palabras;Implica compromiso;Depende de la confianza;Debe cumplirse;Soy una promesa
agujero||Cuanto más me quitas, más grande me hago.|Soy un espacio vacío;Puedo estar en el suelo;Se agrando al cavar;No soy una montaña;Soy un agujero
escalera||Subo y bajo, pero siempre permanezco en el mismo lugar.|Tiene peldaños;Une alturas;Se usa con los pies;Puede apoyarse en una pared;Soy una escalera
nombre||Me pertenece, pero los demás me usan más que yo.|No es un objeto;Identifica a una persona;Se dice para llamarte;Te lo dieron al nacer;Soy tu nombre
diccionario||Tengo miles de palabras, pero nunca digo ninguna.|Es un libro;Sirvo para consultar;Ordeno contenido alfabéticamente;Explico significados;Soy un diccionario
huella||Cuanto más camino, más dejo atrás.|Es una marca;Puede ayudar a identificar;La producen pies o zapatos;Queda en suelo blando;Soy una huella
ascensor||Subo lleno y bajo vacío, aunque a veces hago exactamente lo contrario.|Estoy en edificios;Tengo puertas;Transporto personas entre pisos;Uso botones;Soy un ascensor
calendario||Tengo muchos días, pero nunca puedo vivir ninguno.|Organizo el tiempo;Tengo meses;Suele colgarse o estar en el celular;Marca fechas;Soy un calendario
moneda||Tengo cara y cruz, pero no tengo brazos ni piernas.|Soy pequeña;Puedo ser metálica;Sirvo para pagar;Se me lanza para decidir;Soy una moneda
teclado||Tengo muchas teclas y ninguna abre una puerta.|Se usa con dedos;Permito escribir;Estoy frente a una pantalla;Pertenezco a una computadora;Soy un teclado
ancla||Cuando me usan bajo, cuando no me usan subo.|Soy pesada;Trabajo en el agua;Detengo algo grande;Estoy unida a un barco;Soy un ancla
estampilla|sello postal|Viajo por todo el mundo pegada en una esquina.|Soy pequeña y de papel;Tengo una imagen;Voy sobre sobres;Pago el envío postal;Soy una estampilla
respiración|aliento|Entra y sale todo el día sin usar puertas.|Es indispensable para vivir;No suele verse;Usa los pulmones;Incluye aire;Es la respiración
fotografía|foto|Guardo un instante sin detener el tiempo.|Puedo estar en papel o pantalla;Muestro una imagen;Se obtiene con una cámara;Conservo recuerdos;Soy una fotografía
brújula||Siempre señala un lugar aunque nunca se mueve hasta allí.|Sirvo para orientarse;Tengo una aguja;Uso el campo magnético;Señalo el norte;Soy una brújula
cremallera|cierre|Tengo muchos dientes que se juntan al subir.|Estoy en ropa y bolsos;Abro y cierro;Tengo un pequeño tirador;Mis dientes encajan;Soy un cierre
""",
"dificil": """
nada||¿Qué es aquello que, si lo nombras, ya estás diciendo algo?|No puede sostenerse;Representa ausencia;Es menos que vacío;Su nombre contradice su significado;La respuesta es nada
segundo lugar|segundo|En una carrera adelantas a quien va segundo. ¿En qué posición quedas?|Es un problema lógico;No llegas primero;Ocupas el lugar de quien superaste;Adelantaste al segundo;Quedas segundo
viernes||Un hombre llega un viernes, permanece tres días y se va un viernes. ¿Cómo es posible?|No hay viaje en el tiempo;La palabra tiene dos significados;Uno de los viernes no es un día;Puede ser nombre de animal;Su caballo se llama Viernes
dos|2|Dos padres y dos hijos comen tres manzanas y cada uno come una. ¿Cuántas personas hay?|No son cuatro personas;Hay tres generaciones;Uno es padre e hijo;Son abuelo padre e hijo;Hay tres personas
ninguno|ningún mes|¿Cuántos meses tienen exactamente veintiocho días?|La formulación es importante;No pregunta al menos;Los meses tienen más días;Ninguno tiene exactamente 28 siempre;La respuesta es ninguno
uno|1|¿Cuántas veces puedes restar diez de cien?|Después de hacerlo cambia el número;La segunda resta ya no sería de cien;Sólo la primera cumple;No son diez veces;Una vez
su hija|hija|Una médica mira a una niña y dice: es mi hija, pero la médica no es su padre. ¿Quién es?|No hay contradicción;Evita una suposición;La profesión no indica género;Es uno de sus progenitores;Es su madre
blanco||Una casa tiene cuatro paredes orientadas al sur y un oso pasa cerca. ¿De qué color es?|Importa la ubicación;Sólo ocurre cerca de un polo;Es el Polo Norte;Allí viven osos polares;Es blanco
una hora|60 minutos|Tienes dos cuerdas que tardan una hora en quemarse de forma irregular. ¿Cuánto tarda una sola completa?|La velocidad irregular no importa para una cuerda entera;La pregunta no pide medir media hora;Se quema de punta a punta;El dato ya está incluido;Una hora
ocho|8|¿Qué número sigue: 1, 1, 2, 3, 5…?|Es una secuencia famosa;Cada término suma los dos anteriores;Después de 3 y 5;Es Fibonacci;Sigue el 8
letra m|m|Aparece una vez en minuto, dos en momento y ninguna en siglo. ¿Qué es?|No es una cantidad de tiempo;Observa las palabras;Es una letra;Está al inicio de minuto;Es la letra M
incorrectamente||¿Qué palabra está escrita incorrectamente en todos los diccionarios?|Es un juego de lenguaje;No es un error editorial;La propia palabra lo afirma;Está escrita así de manera correcta;Es incorrectamente
futuro||No puedes verlo ni tocarlo, pero siempre está delante de ti.|No es un objeto;Está relacionado con el tiempo;Todavía no ocurrió;Se convierte en presente;Es el futuro
imaginación||Puede llevarte a cualquier lugar sin mover tu cuerpo.|No es un vehículo;Ocurre en la mente;Crea mundos;Es esencial para inventar;Es la imaginación
memoria||Guarda cosas sin cajones y a veces las pierde sin moverlas.|No es una computadora;Forma parte de la mente;Conserva experiencias;Puede fallar con el tiempo;Es la memoria
pregunta||Puede tener muchas respuestas y aun así seguir siendo la misma.|Está hecha de palabras;Busca información;Suele terminar con un signo;Puede ser difícil o fácil;Es una pregunta
reflejo||Hace todo lo que haces, pero nunca comienza primero.|Necesita una superficie;No tiene voluntad;Puede verse en agua;Aparece en un espejo;Es tu reflejo
tiempo||Todos lo gastan, nadie puede guardarlo y jamás regresa.|No es dinero;Se mide;Avanza constantemente;Los relojes lo indican;Es el tiempo
mentira||Puede viajar muy rápido aunque no tenga piernas y crece al repetirse.|No es material;Se transmite hablando;No es verdad;Puede engañar a muchos;Es una mentira
conocimiento||Cuanto más compartes, más tienen los demás y tú no pierdes nada.|No es un objeto;Se obtiene aprendiendo;Puede enseñarse;Crece al estudiar;Es el conocimiento
""",
}

EXTRA = {
"facil": """
tijera||Tengo dos hojas, pero no soy un árbol.|Soy una herramienta;Trabajo con los dedos;Puedo cortar papel;Tengo dos aros;Soy una tijera
campana||Tengo boca y cuerpo, pero para hablar tienen que golpearme.|Soy de metal;Produzco sonido;Puedo estar en una torre;Tengo badajo;Soy una campana
caracol||Llevo mi casa encima y camino sin pies.|Soy un animal;Me muevo lentamente;Dejo un rastro;Tengo caparazón;Soy un caracol
heladera|refrigerador;nevera|Soy una caja grande donde el invierno vive todo el año.|Estoy en la cocina;Uso electricidad;Conservo alimentos;Mantengo todo frío;Soy una heladera
pelota|balón|Me patean, me lanzan y nunca me enojo.|Soy redonda;Participo en deportes;Puedo rebotar;Entro en arcos o aros;Soy una pelota
""",
"medio": """
cero|0|Si me sumas no cambio nada, pero si multiplicas conmigo lo convierto todo en mí.|Soy un número;Soy par;Represento ausencia;En multiplicaciones domino el resultado;Soy cero
río||Nací sin vida, corro sin piernas y termino dentro de algo mayor.|Soy parte de la naturaleza;Tengo corriente;Cruzo tierras;Desemboco en mar o lago;Soy un río
espejo||No tengo memoria, pero te devuelvo instantáneamente todo lo que veas en mí.|Tengo superficie lisa;Puedo romperme;Reflejo luz;Muestra tu rostro;Soy un espejo
contraseña|clave|Me inventan para dejar entrar y me esconden para impedirlo.|No soy una llave física;Protejo información;Uso letras o números;Se escribe para acceder;Soy una contraseña
semilla||Parezco pequeña y dormida, pero puedo convertirme en algo mucho más alto.|Pertenezco a una planta;Necesito agua;Se coloca en tierra;Puede germinar;Soy una semilla
""",
"dificil": """
once|11|Un reloj marca las doce. ¿Qué hora era exactamente una hora antes?|No requiere calendario;Debes retroceder una hora;No es medianoche necesariamente;Antes de doce viene once;Son las once
cinco|5|Tengo cinco velas encendidas y apago dos. ¿Cuántas velas quedan?|Pregunta cuántas quedan, no cuántas siguen encendidas;Las apagadas no desaparecen;Todas permanecen allí;Había cinco objetos;Quedan cinco
el fósforo|fósforo;cerilla|En una habitación oscura tienes una vela, una lámpara y una chimenea. ¿Qué enciendes primero?|No es ninguno de los tres objetos grandes;Necesitas iniciar el fuego;Cabe en una mano;Se frota para encender;El fósforo
ningún lado|ninguno;ningun lado|Un gallo pone un huevo en el techo inclinado. ¿Hacia qué lado cae?|Hay una trampa anterior a la dirección;No necesitas saber la pendiente;Los gallos son machos;No ponen huevos;No cae hacia ningún lado
Ana||La madre de Ana tiene tres hijas: Lila, Lola y… ¿quién falta?|La respuesta está en la pregunta;No busques otro nombre con L;Se menciona al principio;Es hija de esa madre;Ana
""",
}

def build_bomb_riddles():
    cards=[]
    for difficulty,raw in RAW.items():
        combined=raw.strip()+"\n"+EXTRA[difficulty].strip()
        rows=[line.strip().split("|") for line in combined.splitlines() if line.strip()]
        if len(rows)!=25: raise ValueError(f"Se esperaban 25 acertijos {difficulty}")
        for answer,aliases,prompt,hints in rows:
            cards.append({"difficulty":difficulty,"category":"Acertijo","prompt":prompt,"answer":answer,
                          "aliases":[answer,*[a for a in aliases.split(';') if a]],"hints":hints.split(';')})
    return cards
