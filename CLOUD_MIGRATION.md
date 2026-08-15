# Migración de Familia en Juego a la nube

Este proyecto es una copia independiente. Ningún cambio realizado aquí modifica
la aplicación local ubicada en la carpeta superior.

## Arquitectura objetivo

- Vercel sirve la interfaz, la PWA y las funciones de API.
- Redis conserva el estado activo de cada sala, los relojes y los turnos.
- Supabase PostgreSQL conserva salas, jugadores, preguntas y partidas.
- Un canal de tiempo real sincroniza el tablero, el SmartTV y los celulares.
- El servidor nunca envía respuestas o identidades secretas a clientes que no
  deban conocerlas.

## Etapas

1. Separar el motor de juego del servidor HTTP actual.
2. Reemplazar el estado global por repositorios de sala respaldados por Redis.
3. Crear endpoints con identificador de sala y autorización de anfitrión.
4. Migrar la actualización en vivo y la reconexión de participantes.
5. Guardar contenido y resultados persistentes en PostgreSQL.
6. Ejecutar pruebas simultáneas con tablero, SmartTV y varios celulares.
7. Desplegar una vista previa privada y, después de validarla, producción.

## Estado actual

- Copia completa de interfaz, contenido, música, imágenes y aplicación local.
- Configuración inicial de Vercel.
- Endpoint de diagnóstico `/api/health`.
- Variables de entorno documentadas, todavía sin credenciales.
- URL y clave publicable de Supabase configuradas solamente en `.env.local`.
- Esquema inicial disponible en `supabase/schema.sql`, todavía sin aplicar.
- Falta incorporar una nueva clave `sb_secret_...` exclusiva del backend.
- API multissala implementada con códigos de sala y estado JSON versionado.
- Credenciales independientes para anfitrión y participantes.
- Sincronización cloud por consulta incremental y recuperación automática.
- Filtrado probado de consignas e identidades secretas según el dispositivo.
- La conexión pública confirmó que Supabase reconoce las tablas del esquema.
- Falta configurar el secreto backend y ejecutar las pruebas integrales contra
  la base real antes de publicar una vista previa.
