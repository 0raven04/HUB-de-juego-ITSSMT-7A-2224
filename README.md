# 🎲 Blackjack con IA y GUI en Python

Este proyecto implementa un **juego completo de Blackjack** en Python, con interfaz gráfica usando **Tkinter** y un sistema de recomendaciones basado en una **red bayesiana simplificada**. El objetivo es ofrecer una experiencia interactiva y educativa, mostrando cómo la probabilidad puede apoyar la toma de decisiones en el juego.

---

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

## 🖥️ Requisitos

- Python 3.x
- Librerías estándar:
  - `tkinter`
  - `random`
  - `collections`

---

## ▶️ Ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/0raven04/HUB-de-juego-ITSSMT-7A-2224.git
