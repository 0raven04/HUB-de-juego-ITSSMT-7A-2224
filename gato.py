import tkinter as tk
from tkinter import messagebox
import random

class GatoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Gato (Tic-Tac-Toe)")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        # Variables del juego
        self.turno = 'humano'
        self.jugador_humano = 'X'
        self.jugador_maquina = 'O'
        self.tablero = [' ' for _ in range(9)]
        self.botones = []

        # Crear la pantalla del menú principal
        self.crear_menu_principal()

    def crear_menu_principal(self):
        """Crea la interfaz de bienvenida."""
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(expand=True, fill='both')

        titulo = tk.Label(self.frame_menu, text="El Gato", font=("Arial", 30, "bold"))
        titulo.pack(pady=50)

        instrucciones = tk.Label(self.frame_menu, text="Tú eres 'X' - La Máquina es 'O'", font=("Arial", 12))
        instrucciones.pack(pady=10)

        # Botón para iniciar
        btn_iniciar = tk.Button(self.frame_menu, text="Iniciar Juego", font=("Arial", 16), 
                                command=self.iniciar_juego, bg="#4CAF50", fg="white", padx=20, pady=10)
        btn_iniciar.pack(pady=20)

    def iniciar_juego(self):
        """Destruye el menú y carga el tablero."""
        self.frame_menu.destroy() # Elimina el menú visualmente
        self.crear_tablero()

    def crear_tablero(self):
        """Crea la cuadrícula de botones 3x3."""
        self.frame_juego = tk.Frame(self.root)
        self.frame_juego.pack(expand=True, pady=20)

        for i in range(9):
            btn = tk.Button(self.frame_juego, text="", font=("Arial", 24, "bold"), width=5, height=2,
                            command=lambda idx=i: self.clic_humano(idx))
            
            # Ubicar botones en grilla (filas 0-2, columnas 0-2)
            fila = i // 3
            columna = i % 3
            btn.grid(row=fila, column=columna, padx=5, pady=5)
            self.botones.append(btn)

        # Botón de reiniciar (aparece abajo)
        btn_reiniciar = tk.Button(self.root, text="Reiniciar Partida", command=self.reiniciar_juego)
        btn_reiniciar.pack(pady=10)

    def clic_humano(self, indice):
        """Maneja el clic del usuario en una casilla."""
        if self.tablero[indice] == ' ' and self.turno == 'humano':
            # Actualizar lógica y visuales
            self.realizar_movimiento(indice, self.jugador_humano)
            
            # Verificar si ganó el humano
            if self.verificar_estado_juego():
                return
            
            # Cambiar turno y activar IA
            self.turno = 'maquina'
            # Pequeña pausa para que parezca que la máquina "piensa"
            self.root.after(500, self.turno_maquina)

    def turno_maquina(self):
        """Ejecuta la lógica de la IA."""
        if self.turno == 'maquina':
            indice = self.movimiento_maquina_logica()
            self.realizar_movimiento(indice, self.jugador_maquina)
            
            if self.verificar_estado_juego():
                return
            
            self.turno = 'humano'

    def realizar_movimiento(self, indice, ficha):
        """Actualiza la lista interna y el botón visual."""
        self.tablero[indice] = ficha
        color = "blue" if ficha == 'X' else "red"
        self.botones[indice].config(text=ficha, state="disabled", disabledforeground=color)

    def verificar_estado_juego(self):
        """Revisa si hay ganador o empate y muestra mensaje."""
        ganador = None
        
        # Revisamos si X o O ganaron
        if self.verificar_ganador(self.tablero, self.jugador_humano):
            ganador = "¡Felicidades! ¡Has ganado!"
        elif self.verificar_ganador(self.tablero, self.jugador_maquina):
            ganador = "La máquina ha ganado."
        elif ' ' not in self.tablero:
            ganador = "¡Es un empate!"

        if ganador:
            messagebox.showinfo("Fin del juego", ganador)
            self.reiniciar_juego()
            return True # El juego terminó
        return False # El juego sigue

    def reiniciar_juego(self):
        """Resetea el tablero para jugar de nuevo."""
        self.tablero = [' ' for _ in range(9)]
        self.turno = 'humano'
        for btn in self.botones:
            btn.config(text="", state="normal", bg="SystemButtonFace")

    # --- LÓGICA ORIGINAL DEL USUARIO (Adaptada a la clase) ---

    def verificar_ganador(self, tablero, ficha):
        """(Lógica original) Verifica si el jugador con la 'ficha' ha ganado."""
        return ((tablero[0] == ficha and tablero[1] == ficha and tablero[2] == ficha) or
                (tablero[3] == ficha and tablero[4] == ficha and tablero[5] == ficha) or
                (tablero[6] == ficha and tablero[7] == ficha and tablero[8] == ficha) or
                (tablero[0] == ficha and tablero[3] == ficha and tablero[6] == ficha) or
                (tablero[1] == ficha and tablero[4] == ficha and tablero[7] == ficha) or
                (tablero[2] == ficha and tablero[5] == ficha and tablero[8] == ficha) or
                (tablero[0] == ficha and tablero[4] == ficha and tablero[8] == ficha) or
                (tablero[2] == ficha and tablero[4] == ficha and tablero[6] == ficha))

    def obtener_movimientos_disponibles(self):
        return [i for i, casilla in enumerate(self.tablero) if casilla == ' ']

    def movimiento_maquina_logica(self):
        """(Lógica original) IA básica."""
        disponibles = self.obtener_movimientos_disponibles()

        # 1. Intentar ganar
        for i in disponibles:
            tablero_copia = self.tablero[:]
            tablero_copia[i] = self.jugador_maquina
            if self.verificar_ganador(tablero_copia, self.jugador_maquina):
                return i

        # 2. Bloquear al jugador
        for i in disponibles:
            tablero_copia = self.tablero[:]
            tablero_copia[i] = self.jugador_humano
            if self.verificar_ganador(tablero_copia, self.jugador_humano):
                return i

        # 3. Centro
        if 4 in disponibles:
            return 4

        # 4. Esquinas
        esquinas = [i for i in [0, 2, 6, 8] if i in disponibles]
        if esquinas:
            return random.choice(esquinas)

        # 5. Lados
        lados = [i for i in [1, 3, 5, 7] if i in disponibles]
        if lados:
            return random.choice(lados)

        return random.choice(disponibles)

# Bloque principal de ejecución
if __name__ == "__main__":
    root = tk.Tk()
    app = GatoGUI(root)
    root.mainloop()