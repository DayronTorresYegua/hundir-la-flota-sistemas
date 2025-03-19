from tablero import crear_tablero, colocar_barcos, imprimir_tablero, quedan_barcos
from turnos import turno_jugador, turno_maquina, procesar_disparo_jugador
from estadisticas import anuncia_ganador
from constantes import NUMEROS_A_LETRAS

def inicializar_juego():
    """Inicializa los tableros y coloca los barcos"""
    # Crear tableros
    tablero_jugador = crear_tablero()
    tablero_maquina = crear_tablero()
    
    # Tablero de vista para la máquina (lo que ve el jugador)
    tablero_vista_maquina = crear_tablero()

    # Colocar barcos en los tableros
    colocar_barcos(tablero_jugador)
    colocar_barcos(tablero_maquina)
    
    return tablero_jugador, tablero_maquina, tablero_vista_maquina

def primer_turno_jugador(tablero_maquina, tablero_vista_maquina):
    """Gestiona el primer turno del jugador"""
    print("\nTU TURNO")
    print("\nTablero enemigo:")
    imprimir_tablero(tablero_vista_maquina)
    
    disparos_jugador = 0
    seguir_disparando = True
    jugador_gano = False
    
    while seguir_disparando:
        resultado, disparo_valido = procesar_disparo_jugador(tablero_maquina, tablero_vista_maquina)
        
        if disparo_valido:
            disparos_jugador += 1
            
            # Comprobar victoria
            if not quedan_barcos(tablero_maquina):
                jugador_gano = True
                break
                
            if resultado == "Agua":
                seguir_disparando = False  # Si es agua, termina el turno
    
    return jugador_gano, disparos_jugador

def ejecutar_partida():
    """Ejecuta el flujo principal de la partida"""
    # Inicialización
    tablero_jugador, tablero_maquina, tablero_vista_maquina = inicializar_juego()
    
    print("\n¡BIENVENIDO A HUNDIR LA FLOTA!")
    print("\nTu tablero inicial:")
    imprimir_tablero(tablero_jugador)
    
    # Contadores y estado del juego
    disparos_jugador = 0
    disparos_maquina = 0
    juego_terminado = False
    jugador_gano = False
    maquina_gano = False
    
    # Primer turno (especial)
    primer_turno = True
    
    while not juego_terminado:
        if primer_turno:
            # Gestionar el primer turno del jugador
            jugador_gano, disparos_primer_turno = primer_turno_jugador(tablero_maquina, tablero_vista_maquina)
            disparos_jugador += disparos_primer_turno
            primer_turno = False
        else:
            # Turno normal del jugador
            jugador_gano, disparos_jugador = turno_jugador(
                tablero_maquina, tablero_vista_maquina, tablero_jugador, disparos_jugador
            )

        # Verificar si el juego terminó después del turno del jugador
        if anuncia_ganador(jugador_gano, maquina_gano, disparos_jugador, disparos_maquina):
            juego_terminado = True
            continue
            
        # Turno de la máquina (solo si el jugador no ganó)
        if not jugador_gano:
            maquina_gano, disparos_maquina = turno_maquina(
                tablero_jugador, disparos_maquina
            )
            
            # Verificar si el juego terminó después del turno de la máquina
            if anuncia_ganador(jugador_gano, maquina_gano, disparos_jugador, disparos_maquina):
                juego_terminado = True