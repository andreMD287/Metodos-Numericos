"""
Tarea 9 - Algoritmo solución de sistemas LU

Entrada:
    A : matriz cuadrada n x n
    b : vector n x 1
Salida:
    Éxito  : "Se encuentra la solución"  x = (x_1, ..., x_n)
    Fracaso: "No es posible hallar una solución única"

Pasos:
    Paso 1: Factorizar A = LU                      (llama a la tarea 7)
    Paso 2: Sea Y = (0)_{n x 1}
            Solucionamos L y = b                   (llama a la tarea 8)
    Paso 3: Solucionamos U x = y                   (sustitución hacia atrás, tarea 6)
            Salida: x = (x_1, ..., x_n)

Como A x = b y A = LU, entonces L (U x) = b: primero se halla y = U x con L y = b
y después se halla x con U x = y.
"""
from tarea6_sustitucion_hacia_atras import sustitucion_hacia_atras
from tarea7_lu import factorizacion_lu, validar_matriz_cuadrada, texto
from tarea8_sustitucion_hacia_adelante import sustitucion_hacia_adelante

MENSAJE_FRACASO = "No es posible hallar una solución única"


def resolver_con_lu(L, U, b, mostrar=True):
    """Pasos 2 y 3: resuelve L U x = b cuando ya se tienen L y U.
    Devuelve x, o None si no hay solución única."""
    n = len(L)

    # Paso 2: L y = b
    if mostrar:
        print("\nPaso 2: se resuelve L y = b (sustitución hacia adelante)\n")
    y = sustitucion_hacia_adelante(L, b, mostrar=mostrar, nombre="y")
    if y is None:
        print(MENSAJE_FRACASO)
        return None

    # Paso 3: U x = y
    if mostrar:
        print("\nPaso 3: se resuelve U x = y (sustitución hacia atrás)\n")
    x = sustitucion_hacia_atras(n, U, y, mostrar=mostrar)
    if x is None:
        print(MENSAJE_FRACASO)
        return None
    return x


def solucion_sistemas_lu(A, b, mostrar=True):
    error = validar_matriz_cuadrada(A)
    if error:
        print(error)
        return None
    if len(b) != len(A):
        print(f"b debe tener {len(A)} componentes.")
        return None

    # Paso 1: A = LU
    if mostrar:
        print("Paso 1: factorización A = LU\n")
    factores = factorizacion_lu(A, mostrar=mostrar)
    if factores is None:
        print(MENSAJE_FRACASO)
        return None
    L, U = factores

    x = resolver_con_lu(L, U, b, mostrar=mostrar)
    if x is None:
        return None

    print(f"\nSe encuentra la solución: x = ({', '.join(texto(v) for v in x)})")
    return x


if __name__ == "__main__":
    # A = L U con L = [[1,0,0,0],[2,1,0,0],[-3,3,1,0],[4,5,-2,1]] y diagonal de U = 2, 4, 3, -49
    A = [[2, 1, 0, 3],
         [4, 6, 1, 5],
         [-6, 9, 6, -10],
         [8, 24, -1, -46]]
    b = [16, 39, -10, -131]          # b = A (1, 2, 3, 4)

    print("Ejemplo 1: A x = b con solución x = (1, 2, 3, 4)\n")
    solucion_sistemas_lu(A, b)

    print("\n\nEjemplo 2: matriz singular, A = [[1, 2], [2, 4]]\n")
    solucion_sistemas_lu([[1, 2], [2, 4]], [1, 2])

    print("\n\nEjemplo 3: u_11 = 0, no se puede factorizar (hace falta la tarea 10)\n")
    solucion_sistemas_lu([[0, 1], [1, 0]], [1, 2])
