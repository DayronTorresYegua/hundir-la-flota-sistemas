def mostrar_movimientos_totales(disparos_jugador, disparos_maquina):
    """Muestra el número total de movimientos realizados por el jugador y la máquina"""
    print("\nNÚMERO TOTAL DE MOVIMIENTOS:")
    print(f"Tus movimientos: {disparos_jugador}")
    print(f"Movimientos de la máquina: {disparos_maquina}")
    print(f"Total de movimientos en la partida: {disparos_jugador + disparos_maquina}")

def anuncia_ganador(jugador_gano, maquina_gano, disparos_jugador, disparos_maquina):
    """Anuncia el ganador del juego y muestra el conteo de movimientos"""
    if jugador_gano:
        print("\n¡Felicidades! Has hundido toda la flota enemiga. ¡Ganaste!")
        mostrar_movimientos_totales(disparos_jugador, disparos_maquina)
        return True
    elif maquina_gano:
        print("\nLa máquina ha hundido toda tu flota. ¡Perdiste!")
        mostrar_movimientos_totales(disparos_jugador, disparos_maquina)
        return True
    return False