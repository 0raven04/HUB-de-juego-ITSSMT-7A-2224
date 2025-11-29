import tkinter as tk
from tkinter import messagebox
import random

class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor

    def __str__(self):
        return f"{self.valor}{self.palo}"

    def obtener_valor_numerico(self):
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11
        else:
            return int(self.valor)

    def obtener_conteo_hilo(self):
        val = self.obtener_valor_numerico()
        if 2 <= val <= 6:
            return 1
        elif val >= 10 or self.valor == 'A':
            return -1
        else:
            return 0

class Mazo:
    def __init__(self, num_mazos=6):
        self.palos = ['♥', '♦', '♣', '♠']
        self.valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cartas = [Carta(p, v) for p in self.palos for v in self.valores] * num_mazos
        self.conteo = 0
        random.shuffle(self.cartas)

    def sacar_carta(self):
        if not self.cartas:
            return None
        carta = self.cartas.pop()
        self.conteo += carta.obtener_conteo_hilo()
        return carta

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack - Echo/Valen Assistant")
        self.root.geometry("600x500")
        self.root.configure(bg="#2E8B57") 

        self.mazo = Mazo()
        self.mano_jugador = []
        self.mano_dealer = []
        self.jugando = False

        self.crear_interfaz()
        self.iniciar_juego()

    def crear_interfaz(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#2E8B57")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Dealer
        tk.Label(main_frame, text="Dealer", bg="#2E8B57", fg="white", font=("Arial", 12, "bold")).pack()
        self.lbl_dealer_cards = tk.Label(main_frame, text="", bg="#2E8B57", fg="white", font=("Arial", 16))
        self.lbl_dealer_cards.pack(pady=5)

        # Jugador
        tk.Label(main_frame, text="Tu Mano", bg="#2E8B57", fg="white", font=("Arial", 12, "bold")).pack(pady=(20, 0))
        self.lbl_player_cards = tk.Label(main_frame, text="", bg="#2E8B57", fg="white", font=("Arial", 16))
        self.lbl_player_cards.pack(pady=5)
        self.lbl_player_score = tk.Label(main_frame, text="Suma: 0", bg="#2E8B57", fg="#FFD700", font=("Arial", 12))
        self.lbl_player_score.pack()

        # Info del Sistema (Conteo y Sugerencia)
        info_frame = tk.Frame(main_frame, bg="#206040", bd=2, relief="groove")
        info_frame.pack(fill="x", pady=20, padx=50)
        
        self.lbl_count = tk.Label(info_frame, text="Conteo (Hi-Lo): 0", bg="#206040", fg="white", font=("Courier", 12))
        self.lbl_count.pack(pady=5)
        
        self.lbl_suggestion = tk.Label(info_frame, text="Sugerencia: ---", bg="#206040", fg="#00FF7F", font=("Arial", 12, "bold"))
        self.lbl_suggestion.pack(pady=5)

        # Botones
        btn_frame = tk.Frame(main_frame, bg="#2E8B57")
        btn_frame.pack(pady=10)

        self.btn_hit = tk.Button(btn_frame, text="Pedir Carta (Hit)", command=self.pedir_carta, bg="white", width=15)
        self.btn_hit.pack(side="left", padx=10)

        self.btn_stand = tk.Button(btn_frame, text="Plantarse (Stand)", command=self.plantarse, bg="white", width=15)
        self.btn_stand.pack(side="left", padx=10)
        
        self.btn_new = tk.Button(main_frame, text="Nueva Mano", command=self.iniciar_juego, bg="#FF6347", fg="white", width=20)
        self.btn_new.pack(pady=10)

    def calcular_mano(self, mano):
        suma = 0
        ases = 0
        for carta in mano:
            suma += carta.obtener_valor_numerico()
            if carta.valor == 'A':
                ases += 1
        
        while suma > 21 and ases > 0:
            suma -= 10
            ases -= 1
        return suma

    def actualizar_ui(self, revelar_dealer=False):
        self.lbl_player_cards.config(text="  ".join([str(c) for c in self.mano_jugador]))
        suma_jugador = self.calcular_mano(self.mano_jugador)
        self.lbl_player_score.config(text=f"Suma: {suma_jugador}")

        if revelar_dealer:
            self.lbl_dealer_cards.config(text="  ".join([str(c) for c in self.mano_dealer]))
        else:
            if self.mano_dealer:
                self.lbl_dealer_cards.config(text=f"??  {self.mano_dealer[1]}")
            else:
                self.lbl_dealer_cards.config(text="")

        self.lbl_count.config(text=f"Conteo del Mazo: {self.mazo.conteo}")
        
        if self.jugando:
            sugerencia = self.obtener_sugerencia(suma_jugador)
            self.lbl_suggestion.config(text=f"IA Dice: {sugerencia}")
        else:
            self.lbl_suggestion.config(text="IA Dice: ---")

    def obtener_sugerencia(self, suma_jugador):
        if not self.mano_dealer: return "---"
        dealer_visible = self.mano_dealer[1].obtener_valor_numerico()

        
        if suma_jugador >= 17:
            return "Plantarse"
        if suma_jugador <= 11:
            return "Pedir Carta"
        
        if 12 <= suma_jugador <= 16:
            if dealer_visible >= 7:
                if self.mazo.conteo > 5 and suma_jugador >= 15:
                    return "Plantarse (Conteo Alto)"
                return "Pedir Carta"
            else:
                return "Plantarse"
        
        return "Jugar con cuidado"

    def iniciar_juego(self):
        self.mano_jugador = [self.mazo.sacar_carta(), self.mazo.sacar_carta()]
        self.mano_dealer = [self.mazo.sacar_carta(), self.mazo.sacar_carta()]
        self.jugando = True
        self.btn_hit.config(state="normal")
        self.btn_stand.config(state="normal")
        self.actualizar_ui()

    def pedir_carta(self):
        if not self.jugando: return
        self.mano_jugador.append(self.mazo.sacar_carta())
        suma = self.calcular_mano(self.mano_jugador)
        
        self.actualizar_ui()
        
        if suma > 21:
            self.finalizar_juego("Te pasaste. Gana la casa :(")

    def plantarse(self):
        if not self.jugando: return
        self.jugando = False
        
        # Turno del dealer
        while self.calcular_mano(self.mano_dealer) < 17:
            self.mano_dealer.append(self.mazo.sacar_carta())
        
        self.actualizar_ui(revelar_dealer=True)
        self.determinar_ganador()

    def determinar_ganador(self):
        suma_jugador = self.calcular_mano(self.mano_jugador)
        suma_dealer = self.calcular_mano(self.mano_dealer)
        
        if suma_dealer > 21:
            self.finalizar_juego("¡Dealer se pasó! Ganaste")
        elif suma_dealer > suma_jugador:
            self.finalizar_juego("Dealer gana. Suerte pa' la próxima.")
        elif suma_dealer < suma_jugador:
            self.finalizar_juego("¡Ganaste! Bien jugado.")
        else:
            self.finalizar_juego("Empate (Push).")

    def finalizar_juego(self, mensaje):
        self.jugando = False
        self.actualizar_ui(revelar_dealer=True)
        self.btn_hit.config(state="disabled")
        self.btn_stand.config(state="disabled")
        messagebox.showinfo("Resultado", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()