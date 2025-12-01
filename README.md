♠️ Blackjack Trainer - Simulador con Asistente de Conteo Hi-Lo

¡Bienvenido al Blackjack Trainer! Este es un proyecto desarrollado en Python con tkinter que simula una mesa de Blackjack de casino.

Lo que hace realmente especial a esta aplicación es que integra un Asistente de Estrategia que utiliza el popular sistema de Conteo de Cartas Hi-Lo para darte sugerencias en tiempo real sobre si "Pedir Carta" o "Plantarse". ¡Es la herramienta perfecta para entrenar tus habilidades de juego y estrategia!

✨ Características Principales

Simulación de Juego Completa: Lógica de reparto, cálculo de manos (incluyendo Ases flexibles), turno del Dealer (se planta en 17).

Interfaz Gráfica (GUI): Interfaz simple y visual construida con tkinter para una experiencia de juego intuitiva.

Contador Hi-Lo en Vivo: Muestra el Conteo Acumulado (Running Count) de la zapatera (shoe) en cada ronda.

Asistente de Sugerencias (IA Dice): Proporciona la jugada óptima (Hit o Stand) basada en una estrategia básica simplificada, con ajustes estratégicos basados en el Conteo Hi-Lo actual.

Mazo de Múltiples Barajas: Utiliza 6 mazos combinados para simular condiciones reales de casino.

🛠️ Tecnologías Utilizadas

Lenguaje: Python 3.x

GUI: tkinter (incluido en la biblioteca estándar de Python)

Lógica de Juego: Clases Carta y Mazo personalizadas.

🚀 Cómo Ejecutar el Proyecto

1. Busca el archivo .exe en la lista de archivos y haz clic en él para abrirlo.
2. En la parte superior del archivo, haz clic en el botón "Raw" o el icono de descarga
3. Ejecuta el juego
Si se muestra una ventana de windows es un falso positivo, al ser de dependecia indie lo concidera como malware
4. Dar click en el texto donde dice "Mas informacion" incluso esta subrayado
5. Una vez que se dio click aparece el boton de ejecutar de todas formas
6. Darle click al boton de ejecutar de todas formas
7. Disfruta el juego


🧠 Lógica de Conteo (Hi-Lo)

El sistema de Conteo Hi-Lo se implementa en el método obtener_conteo_hilo() de la clase Carta y se actualiza en el Mazo.

Carta

Valor de Conteo

Razón

2, 3, 4, 5, 6

+1

Salen del mazo; quedan más cartas altas.

7, 8, 9

0

Neutras; no afectan significativamente el equilibrio.

10, J, Q, K, A

-1

Salen del mazo; quedan más cartas bajas.

Un Conteo Alto (número positivo grande) indica que el mazo es rico en cartas de valor 10 y Ases, lo que da ventaja al jugador.
