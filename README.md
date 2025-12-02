Instrucciones para clonar en Xcode en otra Mac (Necesario tener una Mac con Xcode instalado ya sea en App Store o web de Apple)

Abrir Xcode
Iniciar Xcode desde Launchpad o Spotlight.
Elegir “Clone Git Repository”
Si ves la pantalla de bienvenida, haz clic en Clone Git Repository.
Si ya tienes un proyecto abierto: en la barra de menús ve a Source Control → Clone…
Pegar la URL del repositorio
En el campo correspondiente pega la URL (terminada en .git):
https://github.com/0raven04/HUB-de-juego-ITSSMT-7A-2224.git
Después haz clic en Next / Clone.
Seleccionar la carpeta local donde guardar el proyecto
Escoge una ubicación organizada (por ejemplo ~/Documents/Projects/) y confirma. Xcode descargará el repositorio en esa carpeta.
Esperar a que Xcode termine de clonar
Verás una barra de progreso. Cuando termine, Xcode abrirá el proyecto automáticamente (o te dará la opción de abrirlo).
Abrir el archivo de proyecto correcto
Si el repo contiene ProjectName.xcworkspace, ábrelo (recomendado si usa dependencias).
Si solo hay ProjectName.xcodeproj, ábrelo.
Xcode suele abrir el archivo correcto automáticamente; si no, usa File → Open… y abre el .xcworkspace o .xcodeproj.
Cambiar a la rama pacman
Para trabajar con la versión de Pac-Man debes cambiar a la rama pacman. Hay dos formas fáciles dentro de Xcode:
Desde la barra de herramientas (branch menu):
En la parte superior (cerca del botón de ejecución) hay un selector de branch/scheme. Haz clic y selecciona pacman.
Desde el menú de Source Control:
Ve a Source Control → Branches..., busca pacman en la lista y selecciónala, o usa Source Control → Checkout y elige pacman.
Si Xcode no muestra la rama localmente, elige Source Control → Pull... o Source Control → Remote → Fetch para traer las ramas remotas, y luego haz checkout de origin/pacman.
Resolver dependencias (si aplica)
Si el proyecto usa Swift Package Manager u otro gestor, Xcode descargará las dependencias automáticamente al abrir el workspace/proyecto. Espera a que finalice la resolución.
Seleccionar scheme y destino (Simulator o dispositivo)
En la parte superior izquierda selecciona el scheme del juego (ej. PacmanApp) y el destino (p. ej. iPhone 15 Pro (Simulator) o un dispositivo conectado).
Compilar y ejecutar
Pulsa el botón Run (▶) o usa Cmd + R. Si aparece un aviso de firma de código (Signing & Capabilities), inicia sesión con tu Apple ID en Xcode → Settings → Accounts y selecciona un equipo de desarrollo en la configuración del proyecto.
