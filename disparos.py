from barcos import comprobar_hundido, obtener_nombre_barco

def disparar(tablero, tablero_vista, fila, columna):
    """Evalúa el disparo y devuelve el resultado: Agua, Tocado o Hundido"""
    if tablero_vista[fila][columna] in ("T", "H", "-"):
        print("Ya has disparado en esta posición. Intenta otra vez.")
        return None  
    
    if tablero[fila][columna] == "X":
        tablero[fila][columna] = "-"
        tablero_vista[fila][columna] = "-"
        return "Agua"

    letra_barco = tablero[fila][columna] 
    tablero[fila][columna] = "T" 
    tablero_vista[fila][columna] = "T" 
    
    hundido, posiciones = comprobar_hundido(tablero, letra_barco, fila, columna)
    
    if hundido:
        for f, c in posiciones:
            tablero[f][c] = "H"
            tablero_vista[f][c] = "H"
        
        nombre_barco = obtener_nombre_barco(letra_barco)
        if nombre_barco:
            return f"Hundido ({nombre_barco})"
        
        return "Hundido"
    
    return "Tocado"