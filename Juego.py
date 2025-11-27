import random
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict


class RedBayesianaBlackjack:
    """Implementa una red bayesiana simplificada para Blackjack"""
    
    def __init__(self, mazo):
        self.mazo = mazo
        
    def contar_cartas_restantes(self):
        """Cuenta las cartas que quedan en el mazo por valor"""
        conteo = defaultdict(int)
        for carta in self.mazo:
            if carta in ['J', 'Q', 'K']:
                conteo[10] += 1
            elif carta == 'A':
                conteo[11] += 1
            else:
                conteo[int(carta)] += 1
        return conteo
    
    def probabilidad_pasarse(self, valor_actual):
        """P(Pasarse | Valor actual, Mazo)"""
        if valor_actual >= 21:
            return 1.0 if valor_actual > 21 else 0.0
        
        conteo = self.contar_cartas_restantes()
        total = sum(conteo.values())
        if total == 0:
            return 0.5
        
        cartas_peligrosas = 0
        for valor_carta, cantidad in conteo.items():
            valor_ajustado = 1 if (valor_carta == 11 and valor_actual + 11 > 21) else valor_carta
            if valor_actual + valor_ajustado > 21:
                cartas_peligrosas += cantidad
        
        return cartas_peligrosas / total
    
    def recomendar_accion(self, valor_jugador, carta_visible_dealer, puede_doblar=True, puede_rendirse=True):
        """Recomienda acción basada en la red bayesiana"""
        prob_pasarse = self.probabilidad_pasarse(valor_jugador)
        
        if carta_visible_dealer in ['J', 'Q', 'K']:
            valor_dealer = 10
        elif carta_visible_dealer == 'A':
            valor_dealer = 11
        else:
            valor_dealer = int(carta_visible_dealer)
        
        # Estrategia básica mejorada
        if valor_jugador <= 8:
            recomendacion = "PEDIR"
        elif valor_jugador == 9:
            if valor_dealer in [3, 4, 5, 6] and puede_doblar:
                recomendacion = "DOBLAR"
            else:
                recomendacion = "PEDIR"
        elif valor_jugador == 10:
            if valor_dealer <= 9 and puede_doblar:
                recomendacion = "DOBLAR"
            else:
                recomendacion = "PEDIR"
        elif valor_jugador == 11:
            if puede_doblar:
                recomendacion = "DOBLAR"
            else:
                recomendacion = "PEDIR"
        elif valor_jugador == 12:
            if valor_dealer in [4, 5, 6]:
                recomendacion = "PLANTARSE"
            else:
                recomendacion = "PEDIR"
        elif 13 <= valor_jugador <= 16:
            if valor_dealer <= 6:
                recomendacion = "PLANTARSE"
            else:
                if puede_rendirse and valor_jugador in [15, 16] and valor_dealer >= 9:
                    recomendacion = "RENDIRSE"
                else:
                    recomendacion = "PEDIR"
        elif valor_jugador >= 17:
            if valor_jugador >= 19:
                recomendacion = "PLANTARSE"
            elif puede_rendirse and valor_jugador == 16 and valor_dealer >= 9:
                recomendacion = "RENDIRSE"
            else:
                recomendacion = "PLANTARSE"
        
        return recomendacion, prob_pasarse


class Carta:
    """Clase para dibujar una carta visual"""
    
    def __init__(self, canvas, x, y, valor, oculta=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.valor = valor
        self.oculta = oculta
        self.ancho = 80
        self.alto = 110
        
        self.dibujar()
    
    def obtener_palo_y_color(self):
        """Determina el palo y color de la carta"""
        # Para este ejemplo simplificado, alternamos entre rojo y negro
        rojos = ['A', '3', '5', '7', '9', 'J', 'K']
        if self.valor in rojos:
            return '♥', 'red'
        else:
            return '♠', 'black'
    
    def dibujar(self):
        """Dibuja la carta en el canvas"""
        # Fondo de la carta
        if self.oculta:
            # Carta oculta - diseño de reverso
            self.canvas.create_rectangle(
                self.x, self.y, 
                self.x + self.ancho, self.y + self.alto,
                fill='#1a4d8f', outline='white', width=2
            )
            # Patrón de reverso
            for i in range(5):
                for j in range(7):
                    self.canvas.create_oval(
                        self.x + 10 + i * 15, self.y + 10 + j * 15,
                        self.x + 15 + i * 15, self.y + 15 + j * 15,
                        fill='#2e6db5', outline='#2e6db5'
                    )
        else:
            # Carta visible
            self.canvas.create_rectangle(
                self.x, self.y, 
                self.x + self.ancho, self.y + self.alto,
                fill='white', outline='black', width=2
            )
            
            palo, color = self.obtener_palo_y_color()
            
            # Valor en la esquina superior izquierda
            self.canvas.create_text(
                self.x + 15, self.y + 20,
                text=self.valor,
                font=('Arial', 16, 'bold'),
                fill=color
            )
            
            # Palo debajo del valor
            self.canvas.create_text(
                self.x + 15, self.y + 40,
                text=palo,
                font=('Arial', 20),
                fill=color
            )
            
            # Valor grande en el centro
            self.canvas.create_text(
                self.x + self.ancho/2, self.y + self.alto/2,
                text=self.valor,
                font=('Arial', 24, 'bold'),
                fill=color
            )
            
            # Palo grande en el centro
            self.canvas.create_text(
                self.x + self.ancho/2, self.y + self.alto/2 + 25,
                text=palo,
                font=('Arial', 28),
                fill=color
            )
            
            # Valor en la esquina inferior derecha (invertido)
            self.canvas.create_text(
                self.x + self.ancho - 15, self.y + self.alto - 20,
                text=self.valor,
                font=('Arial', 16, 'bold'),
                fill=color,
                angle=180
            )
            
            # Palo en la esquina inferior derecha (invertido)
            self.canvas.create_text(
                self.x + self.ancho - 15, self.y + self.alto - 40,
                text=palo,
                font=('Arial', 20),
                fill=color,
                angle=180
            )


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack - Juego Completo")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1a5f3e")
        
        # Inicializar variables del juego
        self.valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.mazo = []
        self.puntos_jugador = 50
        self.apuesta_actual = 0
        self.mano_jugador = []
        self.mano_dealer = []
        self.en_juego = False
        self.crear_mazo()
        
        self.crear_interfaz()
        
    def crear_mazo(self):
        """Crea y baraja el mazo"""
        self.mazo = [valor for _ in range(4) for valor in self.valores]
        random.shuffle(self.mazo)
        
    def repartir_carta(self):
        """Reparte una carta del mazo"""
        if len(self.mazo) < 10:
            self.crear_mazo()
        return self.mazo.pop()
    
    def calcular_valor(self, mano):
        """Calcula el valor de una mano"""
        valor = 0
        ases = 0
        
        for carta in mano:
            if carta in ['J', 'Q', 'K']:
                valor += 10
            elif carta == 'A':
                ases += 1
                valor += 11
            else:
                valor += int(carta)
        
        while valor > 21 and ases > 0:
            valor -= 10
            ases -= 1
        
        return valor
    
    def es_blackjack(self, mano):
        """Verifica si es Blackjack natural"""
        if len(mano) != 2:
            return False
        valores = [self.calcular_valor_carta(c) for c in mano]
        return (11 in valores and 10 in valores)
    
    def calcular_valor_carta(self, carta):
        """Calcula el valor de una carta individual"""
        if carta in ['J', 'Q', 'K']:
            return 10
        elif carta == 'A':
            return 11
        else:
            return int(carta)
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Frame superior - Info y controles
        frame_superior = tk.Frame(self.root, bg="#1a5f3e")
        frame_superior.pack(pady=15)
        
        # Puntos del jugador
        self.label_puntos = tk.Label(
            frame_superior,
            text=f"💰 Puntos: {self.puntos_jugador}",
            font=("Arial", 18, "bold"),
            bg="#1a5f3e",
            fg="white"
        )
        self.label_puntos.pack(side=tk.LEFT, padx=20)
        
        # Apuesta actual
        self.label_apuesta = tk.Label(
            frame_superior,
            text="🎲 Apuesta: 0",
            font=("Arial", 18, "bold"),
            bg="#1a5f3e",
            fg="yellow"
        )
        self.label_apuesta.pack(side=tk.LEFT, padx=20)
        
        # Frame de apuesta
        self.frame_apuesta = tk.Frame(self.root, bg="#1a5f3e")
        self.frame_apuesta.pack(pady=10)
        
        tk.Label(
            self.frame_apuesta,
            text="Apuesta:",
            font=("Arial", 14),
            bg="#1a5f3e",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.entry_apuesta = tk.Entry(
            self.frame_apuesta,
            font=("Arial", 14),
            width=10
        )
        self.entry_apuesta.pack(side=tk.LEFT, padx=5)
        
        # Botón Empezar
        self.btn_empezar = tk.Button(
            self.frame_apuesta,
            text="🎮 EMPEZAR",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.empezar_juego,
            width=12,
            height=1
        )
        self.btn_empezar.pack(side=tk.LEFT, padx=10)
        
        # Canvas para las cartas del dealer
        frame_dealer = tk.Frame(self.root, bg="#1a5f3e")
        frame_dealer.pack(pady=10)
        
        tk.Label(
            frame_dealer,
            text="🎩 DEALER",
            font=("Arial", 16, "bold"),
            bg="#1a5f3e",
            fg="white"
        ).pack()
        
        self.canvas_dealer = tk.Canvas(
            frame_dealer,
            width=600,
            height=140,
            bg="#0d4028",
            highlightthickness=0
        )
        self.canvas_dealer.pack()
        
        self.label_dealer_valor = tk.Label(
            frame_dealer,
            text="",
            font=("Arial", 14, "bold"),
            bg="#1a5f3e",
            fg="yellow"
        )
        self.label_dealer_valor.pack()
        
        # Frame de recomendación
        self.frame_recomendacion = tk.Frame(self.root, bg="#2d4a3e", relief=tk.RIDGE, bd=2)
        self.frame_recomendacion.pack(pady=10)
        
        self.label_recomendacion = tk.Label(
            self.frame_recomendacion,
            text="",
            font=("Arial", 12, "italic"),
            bg="#2d4a3e",
            fg="#90EE90",
            wraplength=700
        )
        self.label_recomendacion.pack(padx=10, pady=5)
        
        # Canvas para las cartas del jugador
        frame_jugador = tk.Frame(self.root, bg="#1a5f3e")
        frame_jugador.pack(pady=10)
        
        tk.Label(
            frame_jugador,
            text="👤 JUGADOR",
            font=("Arial", 16, "bold"),
            bg="#1a5f3e",
            fg="white"
        ).pack()
        
        self.canvas_jugador = tk.Canvas(
            frame_jugador,
            width=600,
            height=140,
            bg="#0d4028",
            highlightthickness=0
        )
        self.canvas_jugador.pack()
        
        self.label_jugador_valor = tk.Label(
            frame_jugador,
            text="",
            font=("Arial", 14, "bold"),
            bg="#1a5f3e",
            fg="yellow"
        )
        self.label_jugador_valor.pack()
        
        # Frame de botones de acción
        self.frame_acciones = tk.Frame(self.root, bg="#1a5f3e")
        self.frame_acciones.pack(pady=15)
        
        self.btn_pedir = tk.Button(
            self.frame_acciones,
            text="📥 PEDIR",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.pedir_carta,
            width=12,
            state=tk.DISABLED
        )
        self.btn_pedir.pack(side=tk.LEFT, padx=5)
        
        self.btn_plantarse = tk.Button(
            self.frame_acciones,
            text="✋ PLANTARSE",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.plantarse,
            width=12,
            state=tk.DISABLED
        )
        self.btn_plantarse.pack(side=tk.LEFT, padx=5)
        
        self.btn_doblar = tk.Button(
            self.frame_acciones,
            text="⬆️ DOBLAR",
            font=("Arial", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            command=self.doblar,
            width=12,
            state=tk.DISABLED
        )
        self.btn_doblar.pack(side=tk.LEFT, padx=5)
        
        self.btn_rendirse = tk.Button(
            self.frame_acciones,
            text="🏳️ RENDIRSE",
            font=("Arial", 12, "bold"),
            bg="#F44336",
            fg="white",
            command=self.rendirse,
            width=12,
            state=tk.DISABLED
        )
        self.btn_rendirse.pack(side=tk.LEFT, padx=5)
        
        # Mensajes
        self.label_mensaje = tk.Label(
            self.root,
            text="Ingresa tu apuesta y presiona EMPEZAR 🎰",
            font=("Arial", 14, "bold"),
            bg="#1a5f3e",
            fg="white"
        )
        self.label_mensaje.pack(pady=10)
    
    def dibujar_cartas(self, canvas, mano, ocultar_primera=False):
        """Dibuja las cartas en el canvas"""
        canvas.delete("all")
        
        # Calcular posición inicial para centrar las cartas
        num_cartas = len(mano)
        espacio_entre_cartas = 95
        ancho_total = (num_cartas - 1) * espacio_entre_cartas + 80
        x_inicial = (600 - ancho_total) / 2
        y = 15
        
        for i, carta in enumerate(mano):
            x = x_inicial + (i * espacio_entre_cartas)
            oculta = (i == 0 and ocultar_primera)
            Carta(canvas, x, y, carta, oculta)
    
    def actualizar_display(self, ocultar_dealer=False):
        """Actualiza la visualización de las cartas"""
        # Dibujar cartas del jugador
        self.dibujar_cartas(self.canvas_jugador, self.mano_jugador)
        self.label_jugador_valor.config(text=f"Valor: {self.calcular_valor(self.mano_jugador)}")
        
        # Dibujar cartas del dealer
        self.dibujar_cartas(self.canvas_dealer, self.mano_dealer, ocultar_dealer)
        
        if ocultar_dealer:
            self.label_dealer_valor.config(text="")
        else:
            self.label_dealer_valor.config(text=f"Valor: {self.calcular_valor(self.mano_dealer)}")
    
    def mostrar_recomendacion(self):
        """Muestra la recomendación de la red bayesiana"""
        if not self.en_juego or len(self.mano_jugador) == 0:
            return
        
        valor_jugador = self.calcular_valor(self.mano_jugador)
        carta_visible = self.mano_dealer[1] if len(self.mano_dealer) > 1 else '10'
        
        puede_doblar = len(self.mano_jugador) == 2 and self.puntos_jugador >= self.apuesta_actual
        puede_rendirse = len(self.mano_jugador) == 2
        
        self.red_bayesiana = RedBayesianaBlackjack(self.mazo)
        recomendacion, prob_pasarse = self.red_bayesiana.recomendar_accion(
            valor_jugador, carta_visible, puede_doblar, puede_rendirse
        )
        
        texto = f"🤖 IA recomienda: {recomendacion} | Probabilidad de pasarse: {prob_pasarse:.1%}"
        self.label_recomendacion.config(text=texto)
    
    def empezar_juego(self):
        """Inicia una nueva ronda"""
        try:
            apuesta = int(self.entry_apuesta.get())
            if apuesta <= 0:
                messagebox.showerror("Error", "La apuesta debe ser mayor a 0")
                return
            if apuesta > self.puntos_jugador:
                messagebox.showerror("Error", f"No tienes suficientes puntos. Máximo: {self.puntos_jugador}")
                return
            
            self.apuesta_actual = apuesta
            self.puntos_jugador -= apuesta
            self.actualizar_puntos()
            
            # Repartir cartas
            self.mano_jugador = [self.repartir_carta(), self.repartir_carta()]
            self.mano_dealer = [self.repartir_carta(), self.repartir_carta()]
            
            self.en_juego = True
            self.actualizar_display(ocultar_dealer=True)
            
            # Verificar Blackjack
            if self.es_blackjack(self.mano_jugador):
                if self.es_blackjack(self.mano_dealer):
                    self.finalizar_juego("¡EMPATE! Ambos tienen Blackjack 🤝", empate=True)
                else:
                    ganancia = int(self.apuesta_actual * 1.5)
                    self.puntos_jugador += self.apuesta_actual + ganancia
                    self.finalizar_juego(f"🎉 ¡BLACKJACK! Ganas {ganancia} puntos extra", gano=True)
                return
            
            if self.es_blackjack(self.mano_dealer):
                self.actualizar_display(ocultar_dealer=False)
                self.finalizar_juego("El dealer tiene Blackjack. ¡Pierdes! 😢", gano=False)
                return
            
            # Activar botones
            self.btn_pedir.config(state=tk.NORMAL)
            self.btn_plantarse.config(state=tk.NORMAL)
            
            if len(self.mano_jugador) == 2:
                if self.puntos_jugador >= self.apuesta_actual:
                    self.btn_doblar.config(state=tk.NORMAL)
                self.btn_rendirse.config(state=tk.NORMAL)
            
            # Deshabilitar apuesta
            self.btn_empezar.config(state=tk.DISABLED)
            self.entry_apuesta.config(state=tk.DISABLED)
            
            self.label_mensaje.config(text="Tu turno - Elige una acción ⚡")
            self.mostrar_recomendacion()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
    
    def pedir_carta(self):
        """El jugador pide una carta"""
        nueva_carta = self.repartir_carta()
        self.mano_jugador.append(nueva_carta)
        self.actualizar_display(ocultar_dealer=True)
        
        valor = self.calcular_valor(self.mano_jugador)
        if valor > 21:
            self.actualizar_display(ocultar_dealer=False)
            self.finalizar_juego("¡Te pasaste de 21! Pierdes 💥", gano=False)
        else:
            # Deshabilitar doblar y rendirse después de pedir
            self.btn_doblar.config(state=tk.DISABLED)
            self.btn_rendirse.config(state=tk.DISABLED)
            self.mostrar_recomendacion()
    
    def plantarse(self):
        """El jugador se planta"""
        self.turno_dealer()
    
    def doblar(self):
        """El jugador dobla su apuesta"""
        if self.puntos_jugador < self.apuesta_actual:
            messagebox.showerror("Error", "No tienes suficientes puntos para doblar")
            return
        
        self.puntos_jugador -= self.apuesta_actual
        self.apuesta_actual *= 2
        self.actualizar_puntos()
        
        nueva_carta = self.repartir_carta()
        self.mano_jugador.append(nueva_carta)
        self.actualizar_display(ocultar_dealer=True)
        
        valor = self.calcular_valor(self.mano_jugador)
        if valor > 21:
            self.actualizar_display(ocultar_dealer=False)
            self.finalizar_juego("¡Te pasaste de 21! Pierdes 💥", gano=False)
        else:
            self.turno_dealer()
    
    def rendirse(self):
        """El jugador se rinde"""
        self.puntos_jugador += self.apuesta_actual // 2
        self.finalizar_juego("Te rendiste. Recuperas la mitad de tu apuesta 🏳️", gano=False)
    
    def turno_dealer(self):
        """Ejecuta el turno del dealer"""
        self.actualizar_display(ocultar_dealer=False)
        self.label_mensaje.config(text="Turno del dealer... 🎲")
        self.root.update()
        self.root.after(1000)
        
        while self.calcular_valor(self.mano_dealer) < 17:
            self.mano_dealer.append(self.repartir_carta())
            self.actualizar_display(ocultar_dealer=False)
            self.root.update()
            self.root.after(800)
        
        self.determinar_ganador()
    
    def determinar_ganador(self):
        """Determina el ganador de la ronda"""
        valor_jugador = self.calcular_valor(self.mano_jugador)
        valor_dealer = self.calcular_valor(self.mano_dealer)
        
        if valor_dealer > 21:
            self.puntos_jugador += self.apuesta_actual * 2
            self.finalizar_juego(f"¡Dealer se pasó! Ganas {self.apuesta_actual * 2} puntos 🎉", gano=True)
        elif valor_jugador > valor_dealer:
            self.puntos_jugador += self.apuesta_actual * 2
            self.finalizar_juego(f"¡Ganaste! +{self.apuesta_actual * 2} puntos 🏆", gano=True)
        elif valor_dealer > valor_jugador:
            self.finalizar_juego("Dealer gana. Pierdes 😔", gano=False)
        else:
            self.puntos_jugador += self.apuesta_actual
            self.finalizar_juego("¡Empate! Se devuelve tu apuesta 🤝", empate=True)
    
    def finalizar_juego(self, mensaje, gano=False, empate=False):
        """Finaliza la ronda actual"""
        self.en_juego = False
        self.label_mensaje.config(text=mensaje)
        self.label_recomendacion.config(text="")
        
        # Deshabilitar todos los botones de acción
        self.btn_pedir.config(state=tk.DISABLED)
        self.btn_plantarse.config(state=tk.DISABLED)
        self.btn_doblar.config(state=tk.DISABLED)
        self.btn_rendirse.config(state=tk.DISABLED)
        
        # Habilitar nueva ronda
        self.btn_empezar.config(state=tk.NORMAL)
        self.entry_apuesta.config(state=tk.NORMAL)
        self.entry_apuesta.delete(0, tk.END)
        
        self.actualizar_puntos()
        
        if self.puntos_jugador <= 0:
            respuesta = messagebox.askyesno("Juego Terminado", "¡Te has quedado sin puntos! 🎰\n¿Quieres reiniciar el juego con 50 puntos?")
            if respuesta:
                self.puntos_jugador = 50
                self.actualizar_puntos()
                self.label_mensaje.config(text="¡Juego reiniciado! Ingresa tu apuesta 🎰")
            else:
                self.root.quit()
        else:
            respuesta = messagebox.askyesno("Fin de ronda", f"{mensaje}\n\n¿Quieres jugar otra ronda?")
            if not respuesta:
                self.root.quit()
    
    def actualizar_puntos(self):
        """Actualiza la visualización de puntos"""
        self.label_puntos.config(text=f"💰 Puntos: {self.puntos_jugador}")
        self.label_apuesta.config(text=f"🎲 Apuesta: {self.apuesta_actual}")


def main():
    root = tk.Tk()
    juego = BlackjackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()