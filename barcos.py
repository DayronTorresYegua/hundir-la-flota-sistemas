from constantes import TAMANIO_TABLERO, BARCOS

def encontrar_todas_posiciones_barco(tablero, letra_barco, fila, columna):
    """Encuentra todas las posiciones de un barco específico"""
    posiciones = [(fila, columna)]
    
    # Verificar si hay partes del barco a la izquierda o derecha
    horizontal = (columna > 0 and (tablero[fila][columna-1] == letra_barco or tablero[fila][columna-1] == "T")) or \
                 (columna < TAMANIO_TABLERO-1 and (tablero[fila][columna+1] == letra_barco or tablero[fila][columna+1] == "T"))
    
    # Verificar si hay partes del barco arriba o abajo
    vertical = (fila > 0 and (tablero[fila-1][columna] == letra_barco or tablero[fila-1][columna] == "T")) or \
               (fila < TAMANIO_TABLERO-1 and (tablero[fila+1][columna] == letra_barco or tablero[fila+1][columna] == "T"))
    
    if not horizontal and not vertical:
        return posiciones
    
    if horizontal:
        c = columna - 1
        while c >= 0 and (tablero[fila][c] == letra_barco or tablero[fila][c] == "T"):
            posiciones.append((fila, c))
            c -= 1
        
        c = columna + 1
        while c < TAMANIO_TABLERO and (tablero[fila][c] == letra_barco or tablero[fila][c] == "T"):
            posiciones.append((fila, c))
            c += 1
    
    elif vertical:
        f = fila - 1
        while f >= 0 and (tablero[f][columna] == letra_barco or tablero[f][columna] == "T"):
            posiciones.append((f, columna))
            f -= 1
        
        f = fila + 1
        while f < TAMANIO_TABLERO and (tablero[f][columna] == letra_barco or tablero[f][columna] == "T"):
            posiciones.append((f, columna))
            f += 1
    
    return posiciones

def comprobar_hundido(tablero, letra_barco, fila, columna):
    """Comprueba si todas las partes de un barco específico han sido tocadas"""
    posiciones_barco = encontrar_todas_posiciones_barco(tablero, letra_barco, fila, columna)
    
    for f, c in posiciones_barco:
        if tablero[f][c] != "T":
            return False, posiciones_barco
    
    return True, posiciones_barco

def obtener_nombre_barco(letra_barco):
    """Devuelve el nombre completo del barco a partir de su letra inicial"""
    for nombre, _ in BARCOS.items():
        if nombre[0] == letra_barco:
            return nombre
    return None