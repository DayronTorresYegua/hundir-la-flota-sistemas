import random
import sys

# Constantes
TAMANIO_TABLERO = 10
BARCOS = {
    "Portaaviones": 4,
    "Buque": 3,
    "Crucero": 2,
    "Submarino": 2,
    "Lancha": 1
}

# FUNCIONES

# ENTRADA
def entrada_usuario():
    """Solicita al usuario que ingrese una coordenada (fila y columna) para disparar"""
    sys.stdout.write("Introduce la fila y columna (ejemplo: 3 5): ")
    sys.stdout.flush()
    entrada = sys.stdin.readline().strip() 

    try:
        fila, columna = map(int, entrada.split())
        if 0 <= fila < 10 and 0 <= columna < 10:
            return fila, columna
        print("Coordenadas fuera de rango. Intenta de nuevo.")
    except ValueError:
        print("Formato incorrecto. Introduce dos números separados por un espacio.")
    return entrada_usuario()  

# PROCESAMIENTO

def crear_tablero():
    """Crea un tablero vacío de 10x10"""
    return [['X' for _ in range(TAMANIO_TABLERO)] for _ in range(TAMANIO_TABLERO)]

def poder_colocar_barco(tablero, fila, columna, tamaño, orientacion):
    """Verifica si un barco cabe en la posición dada sin superponerse"""
    if orientacion == 'H':
        if columna + tamaño > TAMANIO_TABLERO:
            return False
        return all(tablero[fila][columna + i] == 'X' for i in range(tamaño))
    
    else:
        if fila + tamaño > TAMANIO_TABLERO:
            return False
        return all(tablero[fila + i][columna] == 'X' for i in range(tamaño))

def colocar_barcos(tablero):
    """Coloca los barcos en posiciones aleatorias en el tablero"""
    # Ya tenemos definido un barco de cada tipo en BARCOS
    for nombre, tamaño in BARCOS.items():
        colocado = False
        while not colocado:
            fila = random.randint(0, TAMANIO_TABLERO - 1)
            columna = random.randint(0, TAMANIO_TABLERO - 1)
            orientacion = random.choice(['H', 'V'])  # Horizontal o Vertical
            
            if poder_colocar_barco(tablero, fila, columna, tamaño, orientacion):
                for i in range(tamaño):
                    if orientacion == 'H':
                        tablero[fila][columna + i] = nombre[0]  # Representamos con la primera letra
                    else:
                        tablero[fila + i][columna] = nombre[0]
                colocado = True

def quedan_barcos(tablero):
    """Verifica si aún quedan barcos en el tablero"""
    for fila in tablero:
        for celda in fila:
            if celda not in ("X", "-", "T", "H"):  # Si hay una letra de barco, aún quedan barcos
                return True
    return False

def encontrar_todas_posiciones_barco(tablero, letra_barco, fila, columna):
    """Encuentra todas las posiciones de un barco específico"""
    posiciones = [(fila, columna)]
    
    # Primero determinar la orientación del barco
    # Verificar si hay partes del barco a la izquierda o derecha
    horizontal = (columna > 0 and (tablero[fila][columna-1] == letra_barco or tablero[fila][columna-1] == "T")) or \
                 (columna < TAMANIO_TABLERO-1 and (tablero[fila][columna+1] == letra_barco or tablero[fila][columna+1] == "T"))
    
    # Verificar si hay partes del barco arriba o abajo
    vertical = (fila > 0 and (tablero[fila-1][columna] == letra_barco or tablero[fila-1][columna] == "T")) or \
               (fila < TAMANIO_TABLERO-1 and (tablero[fila+1][columna] == letra_barco or tablero[fila+1][columna] == "T"))
    
    # Si es un barco de una sola casilla (como la lancha), no tiene orientación definida
    if not horizontal and not vertical:
        return posiciones
    
    # Si el barco es horizontal
    if horizontal:
        # Buscar hacia la izquierda
        c = columna - 1
        while c >= 0 and (tablero[fila][c] == letra_barco or tablero[fila][c] == "T"):
            posiciones.append((fila, c))
            c -= 1
        
        # Buscar hacia la derecha
        c = columna + 1
        while c < TAMANIO_TABLERO and (tablero[fila][c] == letra_barco or tablero[fila][c] == "T"):
            posiciones.append((fila, c))
            c += 1
    
    # Si el barco es vertical
    elif vertical:
        # Buscar hacia arriba
        f = fila - 1
        while f >= 0 and (tablero[f][columna] == letra_barco or tablero[f][columna] == "T"):
            posiciones.append((f, columna))
            f -= 1
        
        # Buscar hacia abajo
        f = fila + 1
        while f < TAMANIO_TABLERO and (tablero[f][columna] == letra_barco or tablero[f][columna] == "T"):
            posiciones.append((f, columna))
            f += 1
    
    return posiciones

def comprobar_hundido(tablero, letra_barco, fila, columna):
    """Comprueba si todas las partes de un barco específico han sido tocadas"""
    # Encontrar todas las posiciones del barco
    posiciones_barco = encontrar_todas_posiciones_barco(tablero, letra_barco, fila, columna)
    
    # Verificar si todas están marcadas como tocadas
    for f, c in posiciones_barco:
        if tablero[f][c] != "T":  # Si alguna parte no está tocada
            return False, posiciones_barco
    
    return True, posiciones_barco

def disparar(tablero, tablero_vista, fila, columna):
    """Evalúa el disparo y devuelve el resultado: Agua, Tocado o Hundido"""
    if tablero_vista[fila][columna] in ("T", "H", "-"):
        print("Ya has disparado en esta posición. Intenta otra vez.")
        return None  # Disparo no válido
    
    if tablero[fila][columna] == "X":
        tablero[fila][columna] = "-"  # Marcar agua en tablero real
        tablero_vista[fila][columna] = "-"  # Marcar agua en tablero de vista
        return "Agua"
    
    # Si hay un barco
    letra_barco = tablero[fila][columna]  # Guardar la letra antes de cambiarla
    tablero[fila][columna] = "T"  # Marcar como tocado en tablero real
    tablero_vista[fila][columna] = "T"  # Marcar como tocado en tablero de vista
    
    # Comprobar si el barco está hundido
    hundido, posiciones = comprobar_hundido(tablero, letra_barco, fila, columna)
    
    if hundido:
        # Marcar todas las posiciones del barco como hundidas
        for f, c in posiciones:
            tablero[f][c] = "H"
            tablero_vista[f][c] = "H"
        
        # Identificar qué barco se ha hundido
        for nombre, _ in BARCOS.items():
            if nombre[0] == letra_barco:
                return f"Hundido ({nombre})"
        
        return "Hundido"
    
    return "Tocado"

def mostrar_estado_juego(tablero_jugador, tablero_vista_maquina, es_turno_jugador=True):
    """Muestra el estado actual del juego: primero el tablero del jugador, 
    luego si es turno del jugador, muestra el tablero enemigo"""
    print("\n" + "="*50)
    print("Tu tablero:")
    imprimir_tablero(tablero_jugador)
    
    if es_turno_jugador:
        print("\nTU TURNO")
        print("\nTablero enemigo (lo que has descubierto):")
        imprimir_tablero(tablero_vista_maquina)

def turno_jugador(tablero_maquina, tablero_vista_maquina, tablero_jugador):
    """Permite al jugador realizar un disparo al tablero de la máquina"""
    # Primero mostramos los tableros en el orden deseado
    mostrar_estado_juego(tablero_jugador, tablero_vista_maquina)
    
    seguir_disparando = True
    while seguir_disparando:
        fila, columna = entrada_usuario()
        resultado = disparar(tablero_maquina, tablero_vista_maquina, fila, columna)

        if resultado:
            print(f"Resultado: {resultado}")
            if resultado != "Agua":
                print("\nTablero enemigo actualizado:")
                imprimir_tablero(tablero_vista_maquina)

            # Comprobar si el jugador ganó después de este disparo
            if not quedan_barcos(tablero_maquina):
                return True  # El jugador ha ganado
                
            if resultado == "Agua":
                seguir_disparando = False  # Si es agua, termina el turno
    
    return False  # No ha ganado todavía

def turno_maquina(tablero_jugador):
    """Permite a la máquina realizar un disparo al tablero del jugador"""
    print("\n" + "="*50)
    print("TURNO DE LA MÁQUINA")
    
    seguir_disparando = True
    while seguir_disparando:
        fila = random.randint(0, TAMANIO_TABLERO - 1)
        columna = random.randint(0, TAMANIO_TABLERO - 1)
        
        # La máquina no necesita un tablero de vista, ya que dispara aleatoriamente
        resultado = disparar(tablero_jugador, tablero_jugador, fila, columna)

        if resultado:
            print(f"La máquina disparó en ({fila}, {columna}) - Resultado: {resultado}")
            
            if resultado != "Agua" or not seguir_disparando:
                print("\nTu tablero actualizado:")
                imprimir_tablero(tablero_jugador)

            # Comprobar si la máquina ganó después de este disparo
            if not quedan_barcos(tablero_jugador):
                return True  # La máquina ha ganado
                
            if resultado == "Agua":
                seguir_disparando = False  # Si es agua, termina el turno
    
    return False  # No ha ganado todavía

def anuncia_ganador(jugador_gano, maquina_gano):
    """Anuncia el ganador del juego"""
    if jugador_gano:
        print("\n¡Felicidades! Has hundido toda la flota enemiga. ¡Ganaste! 🎉")
        return True
    elif maquina_gano:
        print("\nLa máquina ha hundido toda tu flota. ¡Perdiste! 😢")
        return True
    return False

# SALIDA

def imprimir_tablero(tablero):
    """Muestra el tablero en la terminal"""
    print("  " + " ".join(str(i) for i in range(TAMANIO_TABLERO)))
    for i, fila in enumerate(tablero):
        print(str(i) + " " + " ".join(fila))

def mostrar_leyenda():
    """Muestra la leyenda de símbolos del tablero"""
    print("\nLeyenda:")
    print("X - Casilla sin descubrir")
    print("- - Agua")
    print("T - Barco tocado")
    print("H - Barco hundido")
    print("P, B, C, S, L - Tus barcos (Portaaviones, Buque, Crucero, Submarino, Lancha)")

def main():
    """Función principal que controla el flujo del juego"""
    # Crear tableros
    tablero_jugador = crear_tablero()
    tablero_maquina = crear_tablero()
    
    # Tablero de vista para la máquina (lo que ve el jugador)
    tablero_vista_maquina = crear_tablero()

    # Colocar barcos en los tableros
    colocar_barcos(tablero_jugador)
    colocar_barcos(tablero_maquina)

    print("\n¡BIENVENIDO A HUNDIR LA FLOTA!\n")
    mostrar_leyenda()
    
    print("\nTu tablero inicial:")
    imprimir_tablero(tablero_jugador)

    # Turnos alternos
    juego_terminado = False
    primer_turno = True
    jugador_gano = False
    maquina_gano = False

    while not juego_terminado:
        if primer_turno:
            # En el primer turno no mostramos el tablero del jugador de nuevo
            print("\n" + "="*50)
            print("\nTU TURNO")
            print("\nTablero enemigo:")
            imprimir_tablero(tablero_vista_maquina)
            
            seguir_disparando = True
            while seguir_disparando:
                fila, columna = entrada_usuario()
                resultado = disparar(tablero_maquina, tablero_vista_maquina, fila, columna)

                if resultado:
                    print(f"Resultado: {resultado}")
                    if resultado != "Agua":
                        print("\nTablero enemigo actualizado:")
                        imprimir_tablero(tablero_vista_maquina)
                        
                    # Comprobar victoria
                    if not quedan_barcos(tablero_maquina):
                        jugador_gano = True
                        break
                        
                    if resultado == "Agua":
                        seguir_disparando = False  # Si es agua, termina el turno
            
            primer_turno = False
        else:
            # Turno del jugador
            jugador_gano = turno_jugador(tablero_maquina, tablero_vista_maquina, tablero_jugador)

        # Verificar si el juego terminó después del turno del jugador
        if anuncia_ganador(jugador_gano, maquina_gano):
            juego_terminado = True
            continue
            
        # Turno de la máquina (solo si el jugador no ganó)
        if not jugador_gano:
            maquina_gano = turno_maquina(tablero_jugador)
            
            # Verificar si el juego terminó después del turno de la máquina
            if anuncia_ganador(jugador_gano, maquina_gano):
                juego_terminado = True

if __name__ == "__main__":
    main()