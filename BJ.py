import random  # Módulo para operaciones aleatorias (barajar, etc.)
from collections import defaultdict  # Diccionario con valores por defecto

class RedBayesiana:
    #Implementa una red bayesiana simplificada para Blackjack
    
    def __init__(self, mazo):  
        # Constructor: inicializa la red bayesiana con referencia al mazo actual
        self.mazo = mazo  # referencia al mazo actual para analizar probabilidades
        
    def contar_cartas_restantes(self):
        #Cuenta las cartas que quedan en el mazo por valor numérico
        conteo = defaultdict(int)  # diccionario que inicializa valores en 0 automáticamente
        # Recorrer todas las cartas del mazo
        for carta in self.mazo:
            # Figuras (J, Q, K) valen 10
            if carta in ['J', 'Q', 'K']:
                conteo[10] += 1
            # As vale 11 inicialmente
            elif carta == 'A':
                conteo[11] += 1
            # Cartas numéricas valen su número
            else:
                conteo[int(carta)] += 1
        return conteo  # retorna diccionario {valor: cantidad}
    
    def probabilidad_pasarse(self, valor_actual):
        #Calcula P(Pasarse | Valor actual, Mazo)
        #Probabilidad de exceder 21 si se pide una carta
        # Si ya está en 21 o más, no puede mejorar sin pasarse
        if valor_actual >= 21:
            return 1.0 if valor_actual > 21 else 0.0
        
        # Contar cartas restantes en el mazo
        conteo = self.contar_cartas_restantes()
        total = sum(conteo.values())  # total de cartas en el mazo
        
        # Si no hay cartas, retornar probabilidad neutral
        if total == 0:
            return 0.5
        
        # Contar cuántas cartas harían que el jugador se pase de 21
        cartas_peligrosas = 0
        for valor_carta, cantidad in conteo.items():
            # Para ases, considerar valor mínimo de 1
            nuevo_valor = valor_actual + (1 if valor_carta == 11 else valor_carta)
            # Si el nuevo valor excede 21, es una carta peligrosa
            if nuevo_valor > 21:
                cartas_peligrosas += cantidad
        
        # Probabilidad = cartas peligrosas / total de cartas
        return cartas_peligrosas / total
    
    def recomendar_accion(self, valor_jugador, carta_visible_dealer, puede_doblar=True, puede_rendirse=True):
        #Recomienda acción óptima basada en análisis bayesiano y estrategia básica
        
        # Calcular probabilidad de pasarse con el mazo actual
        prob_pasarse = self.probabilidad_pasarse(valor_jugador)
        
        # Convertir carta visible del dealer a valor numérico
        if carta_visible_dealer in ['J', 'Q', 'K']:
            valor_dealer = 10
        elif carta_visible_dealer == 'A':
            valor_dealer = 11
        else:
            valor_dealer = int(carta_visible_dealer)
        
        # Mostrar análisis probabilístico
        print("\n--- ANÁLISIS BAYESIANO ---")
        print(f"Probabilidad de pasarse: {prob_pasarse:.1%}")
        
        # Estrategia básica mejorada basada en valor del jugador
        # Valores bajos (8 o menos): siempre pedir
        if valor_jugador <= 8:
            recomendacion = "PEDIR"
        # Valor 9: doblar contra cartas débiles del dealer si es posible
        elif valor_jugador == 9:
            if valor_dealer in [3, 4, 5, 6] and puede_doblar:
                recomendacion = "DOBLAR"
            else:
                recomendacion = "PEDIR"
        # Valor 10: doblar contra la mayoría de cartas si es posible
        elif valor_jugador == 10:
            if valor_dealer <= 9 and puede_doblar:
                recomendacion = "DOBLAR"
            else:
                recomendacion = "PEDIR"
        # Valor 11: siempre doblar si es posible (mejor mano para doblar)
        elif valor_jugador == 11:
            if puede_doblar:
                recomendacion = "DOBLAR"
            else:
                recomendacion = "PEDIR"
        # Valor 12: plantarse contra cartas débiles del dealer
        elif valor_jugador == 12:
            if valor_dealer in [4, 5, 6]:
                recomendacion = "PLANTARSE"
            else:
                recomendacion = "PEDIR"
        # Valores 13-16: zona crítica, depende de la carta del dealer
        elif 13 <= valor_jugador <= 16:
            if valor_dealer <= 6:
                # Dealer tiene carta débil, plantarse
                recomendacion = "PLANTARSE"
            else:
                # Dealer tiene carta fuerte
                # Considerar rendirse con 15-16 contra 9, 10 o As
                if puede_rendirse and valor_jugador in [15, 16] and valor_dealer >= 9:
                    recomendacion = "RENDIRSE"
                else:
                    recomendacion = "PEDIR"
        # Valor 17 o más: generalmente plantarse
        elif valor_jugador >= 17:
            if valor_jugador >= 19:
                # 19 o más: siempre plantarse
                recomendacion = "PLANTARSE"
            elif puede_rendirse and valor_jugador == 16 and valor_dealer >= 9:
                # 16 contra carta fuerte: considerar rendirse
                recomendacion = "RENDIRSE"
            else:
                recomendacion = "PLANTARSE"
        
        # Mostrar recomendación
        print(f"RECOMENDACIÓN: {recomendacion}")
        print("-------------------------")
        
        return recomendacion


class Blackjack:
    #Clase principal que maneja la lógica completa del juego de Blackjack
    
    def __init__(self):  
        # Constructor: inicializa el juego con valores por defecto
        # Lista de valores posibles en las cartas
        self.valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.mazo = []  # lista que contendrá las cartas del mazo
        self.puntos_jugador = 50  # Puntos iniciales del jugador (sistema de fichas)
        self.apuesta_actual = 0  # apuesta de la ronda actual
        self.crear_mazo()  # crear y barajar el mazo inicial
        self.red_bayesiana = RedBayesiana(self.mazo)  # inicializar red bayesiana
    
    def crear_mazo(self):
        #Crea un mazo estándar de 52 cartas (4 de cada valor) y lo baraja
        # Comprensión de lista: 4 copias de cada valor (simula 4 palos)
        self.mazo = [valor for _ in range(4) for valor in self.valores]
        random.shuffle(self.mazo)  # mezclar aleatoriamente el mazo
    
    def repartir_carta(self):
        #Reparte (extrae) una carta del mazo
        # Si quedan pocas cartas, crea un nuevo mazo
        if len(self.mazo) < 10:
            self.crear_mazo()
        return self.mazo.pop()  # extraer y devolver la última carta
    
    def calcular_valor(self, mano):
        #Calcula el valor total de una mano considerando ases flexibles
        
        valor = 0  # acumulador del valor total
        ases = 0  # contador de ases (para ajustar su valor)
        
        # Sumar valores de todas las cartas
        for carta in mano:
            # Figuras valen 10
            if carta in ['J', 'Q', 'K']:
                valor += 10
            # As vale 11 inicialmente
            elif carta == 'A':
                ases += 1
                valor += 11
            # Cartas numéricas valen su número
            else:
                valor += int(carta)
        
        # Ajustar ases de 11 a 1 si el total excede 21
        while valor > 21 and ases > 0:
            valor -= 10  # cambiar un as de 11 a 1 (restar 10)
            ases -= 1  # decrementar contador de ases
        
        return valor  # retornar valor final óptimo
    
    def es_blackjack(self, mano):
        #Verifica si una mano es Blackjack natural (A + carta de valor 10)

        # Blackjack solo puede ocurrir con exactamente 2 cartas
        if len(mano) != 2:
            return False
        # Obtener valores numéricos de ambas cartas
        valores = [self.calcular_valor_de_carta(carta) for carta in mano]
        # Es blackjack si tiene un As (11) y una carta de 10
        return (11 in valores and 10 in valores)
    
    def calcular_valor_de_carta(self, carta):
        #Calcula el valor numérico de una carta individual
        
        if carta in ['J', 'Q', 'K']:
            return 10
        elif carta == 'A':
            return 11  # As por defecto vale 11
        else:
            return int(carta)
    
    def mostrar_mano(self, mano, nombre, ocultar_primera=False):
        #Muestra las cartas de una mano por consola
        
        cartas = []  # lista para representación visual
        # Construir representación de cada carta
        for i, carta in enumerate(mano):
            if i == 0 and ocultar_primera:
                # Primera carta oculta (dealer)
                cartas.append('[??]')
            else:
                # Carta visible
                cartas.append(f'[{carta}]')
        
        # Imprimir nombre y cartas
        print(f"{nombre}: {' '.join(cartas)}", end='')
        # Si no se oculta ninguna carta, mostrar el valor total
        if not ocultar_primera:
            print(f" = {self.calcular_valor(mano)}")
        else:
            print()  # nueva línea si hay carta oculta
    
    def puede_dividir(self, mano):
        #Verifica si la mano puede dividirse (split)
        #Condición: exactamente 2 cartas del mismo valor
        
        # Solo se puede dividir con exactamente 2 cartas
        if len(mano) != 2:
            return False
        # Las dos cartas deben tener el mismo valor numérico
        return self.calcular_valor_de_carta(mano[0]) == self.calcular_valor_de_carta(mano[1])
    
    def hacer_apuesta(self):
        #Maneja el proceso de apuesta del jugador
        # Solicita al jugador cuánto quiere apostar y valida la entrada
        print(f"\nTus puntos actuales: {self.puntos_jugador}")
        # Bucle hasta obtener una apuesta válida
        while True:
            try:
                # Solicitar cantidad a apostar
                apuesta = int(input("¿Cuánto quieres apostar? "))
                # Validar que sea mayor a 0
                if apuesta <= 0:
                    print("La apuesta debe ser mayor a 0.")
                # Validar que el jugador tenga suficientes puntos
                elif apuesta > self.puntos_jugador:
                    print(f"No tienes suficientes puntos. Máximo: {self.puntos_jugador}")
                else:
                    # Apuesta válida
                    self.apuesta_actual = apuesta
                    self.puntos_jugador -= apuesta  # descontar de puntos
                    print(f"Apuesta realizada: {apuesta} puntos")
                    break
            except ValueError:
                # Error si no se ingresa un número
                print("Por favor ingresa un número válido.")
    
    def jugar_mano(self, mano, es_mano_principal=True, apuesta_mano=None):
        #Juega una mano individual con todas las opciones disponibles
        
        # Si no se especifica apuesta, usar la apuesta actual
        if apuesta_mano is None:
            apuesta_mano = self.apuesta_actual
        
        mano_doblada = False  # flag para saber si se dobló
        rendido = False  # flag para saber si se rindió
        
        # Bucle principal de decisiones del jugador
        while True:
            valor_actual = self.calcular_valor(mano)
            print(f"\nValor actual de la mano: {valor_actual}")
            
            # Verificar si se pasó de 21
            if valor_actual > 21:
                print("¡Te pasaste de 21!")
                return "perdio", apuesta_mano
            
            # Obtener recomendación de la red bayesiana
            carta_visible = self.mano_dealer[1]  # segunda carta del dealer (visible)
            # Puede doblar solo en mano principal con 2 cartas y puntos suficientes
            puede_doblar = es_mano_principal and len(mano) == 2 and self.puntos_jugador >= apuesta_mano
            # Puede rendirse solo en mano principal con 2 cartas
            puede_rendirse = es_mano_principal and len(mano) == 2
            
            # Obtener recomendación basada en análisis bayesiano
            recomendacion = self.red_bayesiana.recomendar_accion(
                valor_actual, carta_visible, puede_doblar, puede_rendirse
            )
            
            # Mostrar opciones disponibles al jugador
            print("\n¿Qué deseas hacer?")
            print("1. Pedir carta")
            print("2. Plantarse")
            
            # Lista de opciones extra disponibles
            opciones_extra = []
            # Opción 3: Doblar (si cumple condiciones)
            if puede_doblar:
                print("3. Doblar apuesta")
                opciones_extra.append(3)
            # Opción 4: Rendirse (si cumple condiciones)
            if puede_rendirse:
                print("4. Rendirse")
                opciones_extra.append(4)
            # Opción 5: Dividir (si tiene 2 cartas iguales y puntos suficientes)
            if self.puede_dividir(mano) and es_mano_principal and self.puntos_jugador >= apuesta_mano:
                print("5. Dividir mano")
                opciones_extra.append(5)
            
            # Obtener elección del jugador
            opcion = input("Elige una opción: ").strip()
            
            # Procesar la opción elegida
            if opcion == '1':
                # OPCIÓN 1: Pedir carta (Hit)
                print("\nPides una carta...")
                mano.append(self.repartir_carta())  # agregar carta a la mano
                self.mostrar_mano(mano, "Tu mano")  # mostrar mano actualizada
                
            elif opcion == '2':
                # OPCIÓN 2: Plantarse (Stand)
                print("\nTe plantas.")
                return "jugando", apuesta_mano  # terminar turno
                
            elif opcion == '3' and 3 in opciones_extra:
                # OPCIÓN 3: Doblar apuesta (Double Down)
                print(f"\nDoblas tu apuesta a {apuesta_mano * 2}")
                self.puntos_jugador -= apuesta_mano  # descontar apuesta adicional
                apuesta_mano *= 2  # duplicar apuesta
                mano.append(self.repartir_carta())  # recibir UNA carta
                self.mostrar_mano(mano, "Tu mano")
                mano_doblada = True
                return "jugando", apuesta_mano  # terminar turno automáticamente
                
            elif opcion == '4' and 4 in opciones_extra:
                # OPCIÓN 4: Rendirse (Surrender)
                print("\nTe rindes. Recuperas la mitad de tu apuesta.")
                rendido = True
                return "rendido", apuesta_mano  # terminar turno
                
            elif opcion == '5' and 5 in opciones_extra:
                # OPCIÓN 5: Dividir mano (Split)
                print("\nDivides tu mano.")
                return "dividir", apuesta_mano  # señalar que se quiere dividir
                
            else:
                # Opción inválida
                print("Opción inválida. Por favor elige una opción válida.")
    
    def jugar_ronda(self):
        #Juega una ronda completa de Blackjack con todas las reglas
        # Maneja: apuestas, repartición, blackjack natural, divisiones, etc.
        # Separador visual
        print()        
        # Paso 1: Hacer apuesta
        self.hacer_apuesta()
        
        # Paso 2: Repartir cartas iniciales (2 para jugador, 2 para dealer)
        self.mano_jugador = [self.repartir_carta(), self.repartir_carta()]
        self.mano_dealer = [self.repartir_carta(), self.repartir_carta()]
        
        # Actualizar red bayesiana con el mazo actual
        self.red_bayesiana = RedBayesiana(self.mazo)
        
        # Paso 3: Mostrar manos iniciales (primera carta del dealer oculta)
        print("\nCartas iniciales:")
        self.mostrar_mano(self.mano_jugador, "Jugador")
        self.mostrar_mano(self.mano_dealer, "Dealer", ocultar_primera=True)
        
        # Paso 4: Verificar Blackjack natural (21 con 2 cartas iniciales)
        jugador_blackjack = self.es_blackjack(self.mano_jugador)
        dealer_blackjack = self.es_blackjack(self.mano_dealer)
        
        if jugador_blackjack:
            print("\n¡BLACKJACK NATURAL!")
            if dealer_blackjack:
                # Ambos tienen blackjack: empate (push)
                print("El dealer también tiene Blackjack. ¡EMPATE!")
                self.puntos_jugador += self.apuesta_actual  # devolver apuesta
                return
            else:
                # Solo jugador tiene blackjack: paga 3:2 (1.5x)
                ganancia = self.apuesta_actual * 1.5
                self.puntos_jugador += self.apuesta_actual + int(ganancia)
                print(f"¡GANASTE! Pago 3:2 -> +{int(ganancia)} puntos")
                return
        
        if dealer_blackjack:
            # Solo dealer tiene blackjack: jugador pierde
            print("\nEl dealer tiene Blackjack natural.")
            self.mostrar_mano(self.mano_dealer, "Dealer")
            print("Pierdes tu apuesta.")
            return
        
        # Paso 5: Jugar mano principal del jugador
        resultado, apuesta_final = self.jugar_mano(self.mano_jugador.copy())
        
        # Caso especial: División de mano (Split)
        if resultado == "dividir":
            print("\n--- DIVIDIENDO MANO ---")
            # Crear dos nuevas manos con una carta de la mano original cada una
            mano1 = [self.mano_jugador[0], self.repartir_carta()]
            mano2 = [self.mano_jugador[1], self.repartir_carta()]
            
            # Jugar primera mano dividida
            print("\nMano 1:")
            self.mostrar_mano(mano1, "Mano 1")
            resultado1, apuesta1 = self.jugar_mano(mano1, False, self.apuesta_actual)
            
            # Jugar segunda mano dividida
            print("\nMano 2:")
            self.mostrar_mano(mano2, "Mano 2")
            resultado2, apuesta2 = self.jugar_mano(mano2, False, self.apuesta_actual)
            
            # Jugar turno del dealer
            self.turno_dealer()
            # Determinar ganador para ambas manos
            self.determinar_ganador_manos([(mano1, resultado1, apuesta1), 
                                         (mano2, resultado2, apuesta2)])
            return
        
        # Caso: Jugador se rindió (Surrender)
        if resultado == "rendido":
            # Devolver mitad de la apuesta
            self.puntos_jugador += self.apuesta_actual // 2
            return
        
        # Caso: Jugador se pasó de 21
        if resultado == "perdio":
            # Ya perdió, no hay nada más que hacer
            return
        
        # Paso 6: Turno del dealer (si el jugador no se pasó ni se rindió)
        self.turno_dealer()
        
        # Paso 7: Determinar ganador comparando manos finales
        self.determinar_ganador(self.mano_jugador, apuesta_final)
    
    def turno_dealer(self):
        """Ejecuta el turno del dealer según las reglas estándar
        Regla: dealer pide hasta tener 17 o más"""
        # Separador visual
        print()
        print("---TURNO DEL DEALER---")
        print()
        
        # Revelar mano completa del dealer
        print("\nDealer revela su mano:")
        self.mostrar_mano(self.mano_dealer, "Dealer")
        
        # Dealer pide cartas hasta tener 17 o más
        while self.calcular_valor(self.mano_dealer) < 17:
            print("\nDealer pide carta...")
            self.mano_dealer.append(self.repartir_carta())
            self.mostrar_mano(self.mano_dealer, "Dealer")
            
            # Verificar si el dealer se pasó
            if self.calcular_valor(self.mano_dealer) > 21:
                print("\n¡DEALER SE PASÓ DE 21!")
                break
        else:
            # Si el bucle terminó normalmente (no por break)
            if self.calcular_valor(self.mano_dealer) <= 21:
                print("\nDealer se planta.")
    
    def determinar_ganador(self, mano_jugador, apuesta):
        #Determina el ganador de la ronda comparando manos finales
        
        # Calcular valores finales
        valor_jugador = self.calcular_valor(mano_jugador)
        valor_dealer = self.calcular_valor(self.mano_dealer)
        
        # Separador visual
        print()
        print("---RESULTADO FINAL---")
        print()
        
        # Mostrar manos finales
        self.mostrar_mano(mano_jugador, "Jugador")
        self.mostrar_mano(self.mano_dealer, "Dealer")
        
        print()
        # Determinar resultado y ajustar puntos
        if valor_jugador > 21:
            # Jugador se pasó: dealer gana
            print("--- DEALER GANA --- (Jugador se pasó)")
        elif valor_dealer > 21:
            # Dealer se pasó: jugador gana (paga 1:1)
            print("--- JUGADOR GANA --- (Dealer se pasó)")
            self.puntos_jugador += apuesta * 2  # devuelve apuesta + ganancia
            print(f"+{apuesta * 2} puntos")
        elif valor_jugador > valor_dealer:
            # Jugador tiene mayor valor: gana (paga 1:1)
            print("--- JUGADOR GANA ---")
            self.puntos_jugador += apuesta * 2
            print(f"+{apuesta * 2} puntos")
        elif valor_dealer > valor_jugador:
            # Dealer tiene mayor valor: gana
            print("--- DEALER GANA ---")
        else:
            # Mismo valor: empate (push)
            print("--- EMPATE ---")
            self.puntos_jugador += apuesta  # devolver apuesta
            print(f"Se devuelve la apuesta: +{apuesta} puntos")
        
        # Mostrar puntos totales actualizados
        print(f"\nPuntos totales: {self.puntos_jugador}")
    
    def determinar_ganador_manos(self, manos):
        #Determina ganador para múltiples manos (en caso de split)

        # Valor final del dealer
        valor_dealer = self.calcular_valor(self.mano_dealer)
        
        # Separador visual
        print(f"\n{'='*40}")
        print("RESULTADOS FINALES - MANOS DIVIDIDAS")
        print(f"{'='*40}")
        
        # Evaluar cada mano dividida por separado
        for i, (mano, resultado, apuesta) in enumerate(manos, 1):
            valor_jugador = self.calcular_valor(mano)
            
            # Mostrar número de mano
            print(f"\nMano {i}:")
            self.mostrar_mano(mano, "Jugador")
            self.mostrar_mano(self.mano_dealer, "Dealer")
            
            # Determinar resultado de esta mano específica
            if resultado == "perdio" or valor_jugador > 21:
                print("Resultado: Pierdes")
            elif valor_dealer > 21:
                print("Resultado: Ganas")
                self.puntos_jugador += apuesta * 2
            elif valor_jugador > valor_dealer:
                print("Resultado: Ganas")
                self.puntos_jugador += apuesta * 2
            elif valor_dealer > valor_jugador:
                print("Resultado: Pierdes")
            else:
                print("Resultado: Empate")
                self.puntos_jugador += apuesta
        
        # Mostrar puntos totales después de evaluar todas las manos
        print(f"\nPuntos totales: {self.puntos_jugador}")


def main():
    # Función principal: punto de entrada del programa
    # Título del juego
    print("-------------")
    print("| BLACKJACK |")
    print("-------------")
    
    # Crear instancia del juego
    juego = Blackjack()
    
    # Ejecutar una única ronda
    print()
    juego.jugar_ronda()
    
    # Mensaje final con puntos obtenidos
    print(f"\n Puntos finales: {juego.puntos_jugador}")


# Punto de entrada: ejecutar main() si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()