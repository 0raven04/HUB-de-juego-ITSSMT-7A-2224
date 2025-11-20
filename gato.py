import random

class Gato:
    """Clase para representar el juego del Gato (Tic-Tac-Toe)."""
    def __init__(self):
        # Inicializa el tablero con 9 espacios vacíos
        self.tablero = [' ' for _ in range(9)]
        # El jugador humano es 'X', la máquina es 'O'
        self.jugador_humano = 'X'
        self.jugador_maquina = 'O'

    def imprimir_tablero(self):
        """Muestra el tablero actual en la consola."""
        # Crea una representación visual del tablero
        print('-------------')
        print(f'| {self.tablero[0]} | {self.tablero[1]} | {self.tablero[2]} |')
        print('-------------')
        print(f'| {self.tablero[3]} | {self.tablero[4]} | {self.tablero[5]} |')
        print('-------------')
        print(f'| {self.tablero[6]} | {self.tablero[7]} | {self.tablero[8]} |')
        print('-------------')

    def verificar_ganador(self, tablero, ficha):
        """Verifica si el jugador con la 'ficha' ha ganado."""
        # Se verifica si hay 3 en raya en filas, columnas o diagonales
        return ((tablero[0] == ficha and tablero[1] == ficha and tablero[2] == ficha) or # Fila 1
                (tablero[3] == ficha and tablero[4] == ficha and tablero[5] == ficha) or # Fila 2
                (tablero[6] == ficha and tablero[7] == ficha and tablero[8] == ficha) or # Fila 3
                (tablero[0] == ficha and tablero[3] == ficha and tablero[6] == ficha) or # Columna 1
                (tablero[1] == ficha and tablero[4] == ficha and tablero[7] == ficha) or # Columna 2
                (tablero[2] == ficha and tablero[5] == ficha and tablero[8] == ficha) or # Columna 3
                (tablero[0] == ficha and tablero[4] == ficha and tablero[8] == ficha) or # Diagonal 1
                (tablero[2] == ficha and tablero[4] == ficha and tablero[6] == ficha))   # Diagonal 2

    def obtener_movimientos_disponibles(self):
        """Devuelve una lista de los índices de las casillas vacías."""
        return [i for i, casilla in enumerate(self.tablero) if casilla == ' ']

    def hacer_movimiento(self, indice, ficha):
        """Realiza un movimiento en el tablero."""
        if self.tablero[indice] == ' ':
            self.tablero[indice] = ficha
            return True
        return False

    def movimiento_maquina(self):
        """Lógica de la máquina (IA básica)."""
        disponibles = self.obtener_movimientos_disponibles()

        # 1. Intentar ganar en el siguiente movimiento
        for i in disponibles:
            tablero_copia = self.tablero[:]
            tablero_copia[i] = self.jugador_maquina
            if self.verificar_ganador(tablero_copia, self.jugador_maquina):
                return i

        # 2. Bloquear al jugador humano de ganar
        for i in disponibles:
            tablero_copia = self.tablero[:]
            tablero_copia[i] = self.jugador_humano
            if self.verificar_ganador(tablero_copia, self.jugador_humano):
                return i

        # 3. Tomar el centro si está disponible (índice 4)
        if 4 in disponibles:
            return 4

        # 4. Tomar una esquina aleatoria (índices 0, 2, 6, 8)
        esquinas = [i for i in [0, 2, 6, 8] if i in disponibles]
        if esquinas:
            return random.choice(esquinas)

        # 5. Tomar un lado aleatorio (índices 1, 3, 5, 7)
        lados = [i for i in [1, 3, 5, 7] if i in disponibles]
        if lados:
            return random.choice(lados)

        # Si no queda otra opción, elige un movimiento aleatorio
        return random.choice(disponibles)

def jugar():
    """Función principal para iniciar el juego."""
    juego = Gato()
    print("¡Bienvenido al juego del Gato!")
    print("Eres 'X' y la máquina es 'O'.")
    print("Introduce un número de 1 a 9 para hacer tu movimiento, siguiendo este esquema:")
    
    # Muestra el esquema de la numeración
    print('-------------')
    print('| 1 | 2 | 3 |')
    print('-------------')
    print('| 4 | 5 | 6 |')
    print('-------------')
    print('| 7 | 8 | 9 |')
    print('-------------')
    
    turno = 'humano' # Comienza el humano

    while True:
        juego.imprimir_tablero()

        if turno == 'humano':
            # Turno del jugador humano
            try:
                movimiento = int(input("Tu turno (1-9): ")) - 1 # Se resta 1 para el índice de la lista
                if 0 <= movimiento <= 8 and juego.hacer_movimiento(movimiento, juego.jugador_humano):
                    if juego.verificar_ganador(juego.tablero, juego.jugador_humano):
                        juego.imprimir_tablero()
                        print("\n ¡Felicidades! ¡Has ganado! ")
                        break
                    if not juego.obtener_movimientos_disponibles():
                        juego.imprimir_tablero()
                        print("\n ¡Es un empate! ")
                        break
                    turno = 'maquina'
                else:
                    print("Movimiento inválido o casilla ocupada. Intenta de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número.")

        else:
            # Turno de la máquina
            print("Turno de la máquina...")
            movimiento_ia = juego.movimiento_maquina()
            juego.hacer_movimiento(movimiento_ia, juego.jugador_maquina)
            
            if juego.verificar_ganador(juego.tablero, juego.jugador_maquina):
                juego.imprimir_tablero()
                print("\n La máquina ha ganado. Mejor suerte la próxima vez. ")
                break
            if not juego.obtener_movimientos_disponibles():
                juego.imprimir_tablero()
                print("\n¡Es un empate! ")
                break
            turno = 'humano'

# Inicia el juego
if __name__ == "__main__":
    jugar()