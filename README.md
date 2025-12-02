HUB de juego – Proyecto Pac-Man (Rama pacman)
Este repositorio contiene el desarrollo del juego Pac-Man como parte del proyecto HUB de juego ITSSMT 7A 2224. A continuación se incluyen las instrucciones completas para clonar y abrir el proyecto utilizando Xcode en una Mac.
Requisitos previos:
Mac con macOS actualizado.
Xcode instalado desde App Store o desde la página oficial de Apple.
Conexión a internet para clonar el repositorio y descargar dependencias.
Clonar el proyecto en Xcode
Repositorio principal:
https://github.com/0raven04/HUB-de-juego-ITSSMT-7A-2224.git
La rama correspondiente al juego Pac-Man es:
pacman
Instrucciones para clonar desde Xcode en macOS
1. Abrir Xcode
Iniciar Xcode desde Launchpad o Spotlight.
2. Seleccionar Clone Git Repository
Si Xcode muestra la pantalla de bienvenida, seleccionar Clone Git Repository.
Si Xcode ya está abierto, usar: Source Control → Clone…
3. Pegar la URL del repositorio
Introducir la siguiente URL en el campo correspondiente:
https://github.com/0raven04/HUB-de-juego-ITSSMT-7A-2224.git
Continuar con Next o Clone.
4. Seleccionar la ubicación local
Elegir la carpeta donde se guardará el proyecto, por ejemplo:
~/Documents/Projects/
Xcode descargará los archivos del repositorio en esa ubicación.
5. Esperar a que finalice la clonación
Xcode mostrará el proceso de descarga. Una vez terminado, abrirá el proyecto automáticamente o mostrará la opción para abrirlo.
6. Abrir el archivo adecuado
Dependiendo de lo que incluya el repositorio:
Abrir el archivo .xcworkspace si existe.
Si no existe, abrir el archivo .xcodeproj.
En caso de necesitarlo, usar File → Open… para seleccionar el archivo correcto.
7. Cambiar a la rama pacman
El código del juego Pac-Man se encuentra en la rama pacman. Para cambiar a esta rama:
Método A: Desde la barra superior de Xcode.
Seleccionar el menú de ramas ubicado cerca del botón Run y elegir la rama:
pacman
Método B: Desde el menú de Source Control.
Ir a Source Control → Branches…, buscar pacman y seleccionarla.
Si la rama no aparece, usar Source Control → Pull… o Source Control → Remote → Fetch para traer las ramas remotas y luego seleccionarla.
8. Resolver dependencias
Si el proyecto utiliza Swift Package Manager, Xcode descargará las dependencias automáticamente. Esperar a que finalice la resolución de paquetes antes de compilar.
9. Seleccionar scheme y dispositivo
En la barra superior izquierda seleccionar el scheme correspondiente al juego y elegir el dispositivo o simulador donde se ejecutará.
10. Ejecutar el proyecto
Presionar el botón Run o usar el atajo:
Cmd + R
Si aparece un aviso sobre Signing & Capabilities, iniciar sesión en Xcode mediante:
Xcode → Settings → Accounts
Luego seleccionar un equipo de desarrollo en la configuración del proyecto.
Contenido de la rama pacman
La rama pacman contiene el código fuente del juego Pac-Man, los recursos visuales y la implementación del módulo dentro del HUB de juegos utilizando SwiftUI.
Información del desarrollador
Proyecto desarrollado por Ricardo (Lou), estudiante de Ingeniería en Sistemas del ITSSMT.
