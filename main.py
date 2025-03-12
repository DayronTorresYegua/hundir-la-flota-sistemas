import random
import sys

# Constantes

TAMANIO_TABLERO = 10
BARCOS = {
    "Portaaviones": 5,
    "Acorazado": 4,
    "Crucero": 3,
    "Submarino": 3,
    "Destructor": 2
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
    """Crea un tablero vacío de 10x10 """
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
                        tablero[fila][columna + i] = nombre[0]  # Representamos con la primera letra
                    else:
                        tablero[fila + i][columna] = nombre[0]
                colocado = True

# SALIDA

def imprimir_tablero(tablero):
    """Muestra el tablero en la terminal"""
    print("  " + " ".join(str(i) for i in range(TAMANIO_TABLERO)))
    for i, fila in enumerate(tablero):
        print(str(i) + " " + " ".join(fila))



def main():

    tablero_jugador = crear_tablero()
    colocar_barcos(tablero_jugador)
    imprimir_tablero(tablero_jugador)


if __name__ == "__main__":
    main()