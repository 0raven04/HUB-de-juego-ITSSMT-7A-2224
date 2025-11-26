
# Conecta 4 (2 jugadores o vs Tilin bebé)

import tkinter as tk
from tkinter import messagebox
import math, random

FILAS = 6
COLUMNAS = 7
VACIO = " "


def crear_tablero():
    return [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]

def movimiento_valido(tablero, col):
    return tablero[0][col] == VACIO

def obtener_fila_libre(tablero, col):
    for f in range(FILAS - 1, -1, -1):
        if tablero[f][col] == VACIO:
            return f

def colocar_ficha(tablero, fila, col, ficha):
    tablero[fila][col] = ficha

def tablero_lleno(tablero):
    return all(tablero[0][c] != VACIO for c in range(COLUMNAS))

def es_ganador(tablero, ficha):
    # Horizontal
    for f in range(FILAS):
        for c in range(COLUMNAS - 3):
            if all(tablero[f][c+i] == ficha for i in range(4)):
                return True
    # Vertical
    for f in range(FILAS - 3):
        for c in range(COLUMNAS):
            if all(tablero[f+i][c] == ficha for i in range(4)):
                return True
    # Diagonal positiva
    for f in range(FILAS - 3):
        for c in range(COLUMNAS - 3):
            if all(tablero[f+i][c+i] == ficha for i in range(4)):
                return True
    # Diagonal negativa
    for f in range(3, FILAS):
        for c in range(COLUMNAS - 3):
            if all(tablero[f-i][c+i] == ficha for i in range(4)):
                return True
    return False



def evaluar_ventana(ventana, ficha):
    oponente = "O" if ficha == "X" else "X"
    puntaje = 0
    if ventana.count(ficha) == 4:
        puntaje += 100
    elif ventana.count(ficha) == 3 and ventana.count(VACIO) == 1:
        puntaje += 10
    elif ventana.count(ficha) == 2 and ventana.count(VACIO) == 2:
        puntaje += 4
    if ventana.count(oponente) == 3 and ventana.count(VACIO) == 1:
        puntaje -= 6
    return puntaje

def puntuar_tablero(tablero, ficha):
    puntaje = 0
    columna_central = [tablero[f][COLUMNAS // 2] for f in range(FILAS)]
    puntaje += columna_central.count(ficha) * 5

    for f in range(FILAS):
        fila = [tablero[f][c] for c in range(COLUMNAS)]
        for c in range(COLUMNAS - 3):
            puntaje += evaluar_ventana(fila[c:c+4], ficha)
    for c in range(COLUMNAS):
        col = [tablero[f][c] for f in range(FILAS)]
        for f in range(FILAS - 3):
            puntaje += evaluar_ventana(col[f:f+4], ficha)
    for f in range(FILAS - 3):
        for c in range(COLUMNAS - 3):
            diag1 = [tablero[f+i][c+i] for i in range(4)]
            diag2 = [tablero[f+3-i][c+i] for i in range(4)]
            puntaje += evaluar_ventana(diag1, ficha)
            puntaje += evaluar_ventana(diag2, ficha)
    return puntaje

def minimax(tablero, profundidad, alfa, beta, maximizador):
    if es_ganador(tablero, "X"):
        return (None, 100000)
    elif es_ganador(tablero, "O"):
        return (None, -100000)
    elif tablero_lleno(tablero) or profundidad == 0:
        return (None, puntuar_tablero(tablero, "X"))

    if maximizador:
        mejor_valor = -math.inf
        mejor_col = random.choice([c for c in range(COLUMNAS) if movimiento_valido(tablero, c)])
        for col in range(COLUMNAS):
            if movimiento_valido(tablero, col):
                fila = obtener_fila_libre(tablero, col)
                copia = [r[:] for r in tablero]
                colocar_ficha(copia, fila, col, "X")
                _, valor = minimax(copia, profundidad - 1, alfa, beta, False)
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_col = col
                alfa = max(alfa, valor)
                if alfa >= beta:
                    break
        return mejor_col, mejor_valor
    else:
        peor_valor = math.inf
        peor_col = random.choice([c for c in range(COLUMNAS) if movimiento_valido(tablero, c)])
        for col in range(COLUMNAS):
            if movimiento_valido(tablero, col):
                fila = obtener_fila_libre(tablero, col)
                copia = [r[:] for r in tablero]
                colocar_ficha(copia, fila, col, "O")
                _, valor = minimax(copia, profundidad - 1, alfa, beta, True)
                if valor < peor_valor:
                    peor_valor = valor
                    peor_col = col
                beta = min(beta, valor)
                if alfa >= beta:
                    break
        return peor_col, peor_valor

# -----------------------------------------------------------
# Interfaz gráfica
# -----------------------------------------------------------

class Conecta4GUI:
    def __init__(self, modo="vs_tilin"):
        self.modo = modo
        self.tablero = crear_tablero()
        self.turno = "O"
        self.juego_terminado = False

        self.root = tk.Tk()
        self.root.title("Conecta 4 - Tilin bebé edition")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.botones = []
        for c in range(COLUMNAS):
            b = tk.Button(self.frame, text=str(c), width=6, height=2, 
                          command=lambda c=c: self.jugar_turno(c))
            b.grid(row=0, column=c)
            self.botones.append(b)

        self.celdas = []
        for f in range(FILAS):
            fila = []
            for c in range(COLUMNAS):
                lbl = tk.Label(self.frame, text=" ", width=6, height=3, 
                               borderwidth=1, relief="solid", bg="white", font=("Arial", 14))
                lbl.grid(row=f+1, column=c)
                fila.append(lbl)
            self.celdas.append(fila)

        self.info = tk.Label(self.root, text="Turno de O (amarillo)", font=("Arial", 14))
        self.info.pack(pady=10)

        self.root.mainloop()

    def actualizar_tablero(self):
        for f in range(FILAS):
            for c in range(COLUMNAS):
                color = "white"
                if self.tablero[f][c] == "O":
                    color = "yellow"
                elif self.tablero[f][c] == "X":
                    color = "red"
                self.celdas[f][c].config(bg=color)

    def jugar_turno(self, col):
        if self.juego_terminado or not movimiento_valido(self.tablero, col):
            return

        ficha_actual = self.turno
        fila = obtener_fila_libre(self.tablero, col)
        colocar_ficha(self.tablero, fila, col, ficha_actual)
        self.actualizar_tablero()

        if es_ganador(self.tablero, ficha_actual):
            self.info.config(text=f"¡Jugador {ficha_actual} gana! 🎉")
            self.juego_terminado = True
            messagebox.showinfo("Fin del juego", f"¡Jugador {ficha_actual} gana! 🎉")
            return

        if tablero_lleno(self.tablero):
            self.info.config(text="Empate")
            messagebox.showinfo("Fin del juego", "Empate")
            return

        # Si se juega contra Tilin bebé
        if self.modo == "vs_tilin":
            if ficha_actual == "O":
                self.info.config(text="Turno de Tilin bebé")
                self.root.after(500, self.turno_tilin)
        else:
            # Cambio de jugador (juegan 2)
            self.turno = "X" if self.turno == "O" else "O"
            self.info.config(text=f"Turno de {self.turno}")

    def turno_tilin(self):
        col, _ = minimax(self.tablero, 3, -math.inf, math.inf, True)  
        fila = obtener_fila_libre(self.tablero, col)
        colocar_ficha(self.tablero, fila, col, "X")
        self.actualizar_tablero()

        if es_ganador(self.tablero, "X"):
            self.info.config(text="Tilin bebé gana")
            self.juego_terminado = True
            messagebox.showinfo("Fin del juego", "Tilin bebé gana")
            return

        if tablero_lleno(self.tablero):
            self.info.config(text="Empate")
            messagebox.showinfo("Fin del juego", "Empate")
            return

        self.info.config(text="Tu turno (O)")

#menu 

def menu_inicial():
    root = tk.Tk()
    root.title("Conecta 4 - Menú principal")

    label = tk.Label(root, text="Elige un modo de juego:", font=("Arial", 14))
    label.pack(pady=20)

    def jugar_vs_tilin():
        root.destroy()
        Conecta4GUI(modo="vs_tilin")

    def jugar_dos_jugadores():
        root.destroy()
        Conecta4GUI(modo="2p")

    btn1 = tk.Button(root, text="Jugar contra Tilin bebé", font=("Arial", 12), width=25, command=jugar_vs_tilin)
    btn1.pack(pady=10)

    btn2 = tk.Button(root, text="Dos jugadores (mismo teclado)", font=("Arial", 12), width=25, command=jugar_dos_jugadores)
    btn2.pack(pady=10)

    root.mainloop()

#metodo main para inicar

if __name__ == "__main__":
    menu_inicial()
