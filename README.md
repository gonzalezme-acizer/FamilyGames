# Familia en Juego — versión Cloud

> Proyecto independiente en preparación para Vercel. La versión local original
> permanece en la carpeta superior y no es modificada por este proyecto.

La estrategia y el estado de la migración están documentados en
[`CLOUD_MIGRATION.md`](CLOUD_MIGRATION.md).

Una experiencia de juegos familiares para una pantalla principal y celulares conectados en la misma red Wi-Fi.

Incluye bancos amplios de tarjetas en español, distribuidos entre los niveles Fácil, Medio y Difícil.

Cada partida permite elegir dificultad y duración, comienza con una cuenta regresiva, explica y narra las reglas, mantiene turno y tanteador visibles, incluye música regulable y evita repetir tarjetas hasta agotar el mazo. Desde “Familia y equipos” se pueden crear y borrar equipos, agregar, mover o quitar participantes.

Carrera de Mente cuenta con 600 preguntas —100 para cada una de sus seis categorías—, con un banco especialmente reforzado en los niveles medio y difícil, dos dados, un tablero de 100 casillas, doce casillas especiales, estrellas por categoría y duelos entre equipos. La pregunta se muestra y puede responderse tanto en el celular como en la pantalla principal; el sistema la evalúa automáticamente, sin confirmación del anfitrión. Al llegar a la meta, las preguntas corresponden a las estrellas que todavía falten y, al completar las seis, aparece un festejo con el nombre del equipo ganador. Mímica contiene 250 consignas de hasta tres palabras —25 en cada una de sus diez categorías—, una pista definida para cada tarjeta, tiempo por turno configurable, entre una y cinco rondas, tres pases y tres pedidos de ayuda por turno, y una rotación intercalada para que cada participante actúe una vez por ronda; Dibujo Relámpago contiene 70 consignas. Reto Show Familiar contiene 300 retos —100 por dificultad— de imitación, canciones, actuación, humor, destreza segura, improvisación y coordinación. ¿Quién dijo qué? contiene 134 confesiones cómicas: entrega dos al azar a cada celular, concede 60 segundos para elegir y luego muestra todas las frases simultáneamente con un selector de participante junto a cada una. ¿Quién soy? contiene 300 personajes —100 por dificultad—: entrega uno distinto a cada celular para colocarlo en la frente, nunca muestra las identidades en la pantalla principal y permite que el anfitrión marque qué participantes adivinaron durante la ronda. Tres verdades y una mentira contiene 60 figuras y cuatro datos por tarjeta, elige un representante rotativo por equipo, concede 90 segundos y puntúa 3 por victoria exclusiva, 1 por empate y 0 por derrota. Los modos secretos conceden cinco segundos de preparación sin consumir el reloj general.

## Iniciar

En macOS, abrí `Familia en Juego.app`. La aplicación inicia el servidor y muestra el juego en su propia ventana, sin abrir Chrome, Safari ni otro navegador. Al cerrar la aplicación también se apaga el servidor.

Si modificás el proyecto, hacé doble clic en `crear_app.command` para reconstruir la aplicación con los últimos cambios.

También podés usar el modo tradicional: hacé doble clic en `iniciar.command` y luego abrí `http://localhost:8765` en la laptop. La terminal mostrará la dirección para los celulares.

Alternativa desde Terminal:

```bash
python3 server.py
```

No requiere instalar paquetes. El estado se guarda en `game-state.json`.

## Celulares y QR

La pantalla de Sala muestra un QR generado a partir de la dirección local. Todos los dispositivos deben estar conectados a la misma red. Si la red o el navegador bloquean la imagen QR, se puede escribir en el celular la dirección que aparece debajo.

## Actualizar contenido

En Configuración se puede importar un JSON publicado en una URL. Debe tener una o más claves `trivia`, `mimica`, `dibujo`, `rapido`, cada una con una lista de elementos. El contenido importado se agrega a `content.json`.
