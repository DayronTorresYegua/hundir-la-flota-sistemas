import sys
from constantes import LETRAS_A_NUMEROS

def entrada_usuario():
    """Solicita al usuario que ingrese una coordenada (letra y número) para disparar"""
    sys.stdout.write("Introduce la coordenada (ejemplo: A 5 o A5): ")
    sys.stdout.flush()
    entrada = sys.stdin.readline().strip().upper().replace(" ", "")

    try:
        if len(entrada) < 2:
            print("Formato incorrecto. Introduce una letra (A-J) seguida de un número (0-9).")
            return entrada_usuario()

        letra = entrada[0]
        columna_str = entrada[1:]
        
        if letra not in LETRAS_A_NUMEROS:
            print("Letra fuera de rango (A-J). Intenta de nuevo.")
            return entrada_usuario()
            
        fila = LETRAS_A_NUMEROS[letra]
        columna = int(columna_str)
        
        if 0 <= columna < 10:
            return fila, columna
        print("Columna fuera de rango (0-9). Intenta de nuevo.")
    except ValueError:
        print("Formato incorrecto. Introduce una letra (A-J) seguida de un número (0-9).")
    
    return entrada_usuario()