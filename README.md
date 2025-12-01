# 🎲 Blackjack con IA y GUI en Python

Este proyecto implementa un **juego completo de Blackjack** en Python, con interfaz gráfica usando **Tkinter** y un sistema de recomendaciones basado en una **red bayesiana simplificada**. El objetivo es ofrecer una experiencia interactiva y educativa, mostrando cómo la probabilidad puede apoyar la toma de decisiones en el juego.

---

## 🎮 Guía de Uso dentro del Juego

Una vez que el juego está abierto (ya sea desde `Juego.py` o `Juego.exe`), sigue estos pasos:

1. **Apuesta inicial 💰**
   - Ingresa la cantidad de puntos que deseas apostar en el campo de texto.
   - Presiona el botón **EMPEZAR 🎮** para iniciar la ronda.

2. **Reparto de cartas 🃏**
   - El jugador y el dealer reciben dos cartas iniciales.
   - Si alguno obtiene **Blackjack natural (A + 10/J/Q/K)**, la ronda puede terminar de inmediato.

3. **Turno del jugador 👤**
   - Dispones de varias acciones:
     - **PEDIR 📥**: Solicita una nueva carta.
     - **PLANTARSE ✋**: Mantén tu mano actual y cede el turno al dealer.
     - **DOBLAR ⬆️**: Duplica tu apuesta y recibe una carta adicional (solo disponible al inicio).
     - **RENDIRSE 🏳️**: Recupera la mitad de tu apuesta y termina la ronda.
   - La **IA 🤖** te mostrará una recomendación en pantalla, indicando la acción más conveniente y la probabilidad de pasarte.

4. **Turno del dealer 🎩**
   - El dealer revela su carta oculta.
   - Roba cartas hasta alcanzar al menos 17 puntos.
   - Si se pasa de 21, el jugador gana automáticamente.

5. **Resultado de la ronda 🏆**
   - El juego muestra un mensaje indicando si ganaste, perdiste o empataste.
   - Tus puntos se actualizan según el resultado:
     - **Victoria**: ganas el doble de tu apuesta.
     - **Blackjack**: recibes 1.5 veces tu apuesta.
     - **Derrota**: pierdes tu apuesta.
     - **Empate**: recuperas tu apuesta.

6. **Nueva ronda 🔄**
   - Al finalizar, puedes elegir jugar otra ronda o salir del juego.
   - Si tus puntos llegan a 0, el juego ofrece reiniciar con 50 puntos.

---

⚠️ **Nota sobre el archivo `.exe` en Windows:**  
Al ejecutar el juego desde `Juego.exe`, Windows puede mostrar una advertencia de seguridad indicando que el software podría ser inseguro. Esto ocurre porque es un archivo compilado por el propio usuario y **no significa que el programa sea dañino**. Puedes ejecutarlo con confianza, ya que el código fuente está disponible en este repositorio para revisión.


## 🚀 Características principales

- **Interfaz gráfica (Tkinter):**
  - Visualización de cartas con diseño personalizado.
  - Paneles para jugador y dealer con valores actualizados en tiempo real.
  - Botones interactivos para acciones: `PEDIR`, `PLANTARSE`, `DOBLAR`, `RENDIRSE`.

- **Red Bayesiana para decisiones:**
  - Cálculo de la probabilidad de pasarse según el valor actual y las cartas restantes.
  - Recomendaciones automáticas de acción (`PEDIR`, `PLANTARSE`, `DOBLAR`, `RENDIRSE`) basadas en estrategia básica mejorada.

- **Mecánicas del juego:**
  - Sistema de apuestas con puntos iniciales.
  - Detección de Blackjack natural.
  - Reglas completas del dealer (se planta en 17 o más).
  - Opciones de doblar apuesta y rendirse.
  - Mensajes dinámicos de victoria, derrota o empate.

---

## 📂 Estructura del código

- **`RedBayesianaBlackjack`**
  - Modela la probabilidad de pasarse.
  - Recomienda acciones según la mano del jugador y la carta visible del dealer.

- **`Carta`**
  - Clase encargada de dibujar las cartas en el canvas.
  - Incluye diseño de reverso y símbolos de palos.

- **`BlackjackGUI`**
  - Controlador principal del juego.
  - Maneja la lógica de apuestas, reparto de cartas y turnos.
  - Actualiza la interfaz gráfica y muestra recomendaciones de la IA.

- **Funciones clave:**
  - `crear_mazo()`: Genera y baraja el mazo.
  - `calcular_valor()`: Evalúa el valor de una mano considerando ases.
  - `es_blackjack()`: Detecta Blackjack natural.
  - `mostrar_recomendacion()`: Muestra la sugerencia de la IA.
  - `determinar_ganador()`: Decide el resultado de la ronda.

---

## 📖 Guía de Uso

### 🔹 Ejecución desde código fuente
1. Asegúrate de tener **Python 3.x** instalado.
2. Clona el repositorio:
   ```bash
   git clone https://github.com/0raven04/HUB-de-juego-ITSSMT-7A-2224.git
3. Accede al directorio:
   cd HUB-de-juego-ITSSMT-7A-2224
4.Ejecuta el juego directamente:
   python Juego.py
