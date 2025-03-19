import random
from constantes import TAMANIO_TABLERO, NUMEROS_A_LETRAS
from tablero import imprimir_tablero, quedan_barcos
from entrada import entrada_usuario
from disparos import disparar

def mostrar_estado_juego(tablero_jugador, tablero_vista_maquina, es_turno_jugador=True):
    """Muestra el estado actual del juego: primero el tablero del jugador, 
    luego si es turno del jugador, muestra el tablero enemigo"""
    print("\nTu tablero:")
    imprimir_tablero(tablero_jugador)
    
    if es_turno_jugador:
        print("\nTU TURNO")
        print("\nTablero enemigo (lo que has descubierto):")
        imprimir_tablero(tablero_vista_maquina)

def procesar_disparo_jugador(tablero_maquina, tablero_vista_maquina):
    """Procesa un disparo del jugador y devuelve el resultado"""
    fila, columna = entrada_usuario()
    resultado = disparar(tablero_maquina, tablero_vista_maquina, fila, columna)
    
    if resultado:
        letra_fila = NUMEROS_A_LETRAS[fila]
        print(f"Disparaste en {letra_fila}{columna} - Resultado: {resultado}")
        
        if resultado != "Agua":
            print("\nTablero enemigo actualizado:")
            imprimir_tablero(tablero_vista_maquina)
            
        return resultado, True
    
    return None, False

def turno_jugador(tablero_maquina, tablero_vista_maquina, tablero_jugador, disparos_jugador):
    """Permite al jugador realizar un disparo al tablero de la máquina"""
    mostrar_estado_juego(tablero_jugador, tablero_vista_maquina, True)
    
    seguir_disparando = True
    disparos_nuevos = 0
    
    while seguir_disparando:
        resultado, disparo_valido = procesar_disparo_jugador(tablero_maquina, tablero_vista_maquina)
        
        if disparo_valido:
            disparos_nuevos += 1
            
            if not quedan_barcos(tablero_maquina):
                return True, disparos_jugador + disparos_nuevos
                
            if resultado == "Agua":
                seguir_disparando = False
    
    return False, disparos_jugador + disparos_nuevos

def procesar_disparo_maquina(tablero_jugador):
    """Procesa un disparo de la máquina y devuelve el resultado"""
    fila = random.randint(0, TAMANIO_TABLERO - 1)
    columna = random.randint(0, TAMANIO_TABLERO - 1)
    
    resultado = disparar(tablero_jugador, tablero_jugador, fila, columna)
    
    if resultado:
        letra_fila = NUMEROS_A_LETRAS[fila]
        print(f"La máquina disparó en {letra_fila}{columna} - Resultado: {resultado}")
        
        if resultado != "Agua":
            print("\nTu tablero actualizado:")
            imprimir_tablero(tablero_jugador)
            
        return resultado, True
    
    return None, False

def turno_maquina(tablero_jugador, disparos_maquina):
    """Permite a la máquina realizar un disparo al tablero del jugador"""
    print("TURNO DE LA MÁQUINA")
    
    seguir_disparando = True
    disparos_nuevos = 0
    
    while seguir_disparando:
        resultado, disparo_valido = procesar_disparo_maquina(tablero_jugador)
        
        if disparo_valido:
            disparos_nuevos += 1
            
            if not quedan_barcos(tablero_jugador):
                return True, disparos_maquina + disparos_nuevos
                
            if resultado == "Agua":
                seguir_disparando = False
    
    return False, disparos_maquina + disparos_nuevos