import random
from constantes import TAMANIO_TABLERO, BARCOS, NUMEROS_A_LETRAS

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
    for nombre, tamaño in BARCOS.items():
        colocado = False
        while not colocado:
            fila = random.randint(0, TAMANIO_TABLERO - 1)
            columna = random.randint(0, TAMANIO_TABLERO - 1)
            orientacion = random.choice(['H', 'V'])  # Horizontal o Vertical
            
            if poder_colocar_barco(tablero, fila, columna, tamaño, orientacion):
                for i in range(tamaño):
                    if orientacion == 'H':
                        tablero[fila][columna + i] = nombre[0]  
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

def imprimir_tablero(tablero):
    """Muestra el tablero en la terminal con letras para las filas"""
    print("  " + " ".join(str(i) for i in range(TAMANIO_TABLERO)))
    for i, fila in enumerate(tablero):
        letra_fila = NUMEROS_A_LETRAS[i]
        print(letra_fila + " " + " ".join(fila))