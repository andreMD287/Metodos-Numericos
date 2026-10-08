"""
Tarea 7 - Algoritmo LU

Entrada:
    A : matriz de tamaño n x n
Salida:
    Éxito  : Se puede factorizar A = LU, con
                 L = (l_ij) n x n triangular inferior
                 U = (u_ij) n x n triangular superior
    Fracaso: "No se pudo factorizar de la forma LU"

Pasos:
    Paso 1: Definir L = identidad(n), U = A
    Paso 2: Para i = 1, ..., n
                Para j = i+1, ..., n
                    Si u_ii != 0, en caso contrario Salida (Fracaso)
                    l_ji = u_ji / u_ii
                    Para k = i, ..., n
                        u_jk = u_jk - l_ji u_ik
    Paso 3: Salida: L = (l_ij) n x n  y  U = (u_ij) n x n

Teorema: si A = LU entonces |A| = |U| (|L| = 1 porque su diagonal es de unos),
es decir, el determinante de A es el producto de la diagonal de U.
Ejemplo del cuaderno: |A| = |U| = 2 * 4 * 3 * (-49) = -1176.

Nota: en Python los índices empiezan en 0. Los enteros se convierten a
fracciones (fractions.Fraction) para que los resultados sean exactos.
"""
import math
import numbers
from fractions import Fraction


def a_exacto(v):
    """Convierte enteros a Fraction (divisiones exactas); deja floats y Fractions igual."""
    if isinstance(v, numbers.Integral) and not isinstance(v, bool):
        return Fraction(v)
    return v


def es_finito(v):
    """True si el número real v no es inf ni nan (un entero enorme cuenta como finito)."""
    try:
        return math.isfinite(v)
    except OverflowError:
        return True


def texto(v):
    """Muestra floats con 10 cifras significativas y el resto con str()."""
    return f"{v:.10g}" if isinstance(v, float) else str(v)


def imprimir_matriz(nombre, M):
    """Imprime una matriz con las columnas alineadas a la derecha."""
    celdas = [[texto(v) for v in fila] for fila in M]
    ancho = max(len(c) for fila in celdas for c in fila)
    print(f"{nombre} =")
    for fila in celdas:
        print("    [ " + "  ".join(c.rjust(ancho) for c in fila) + " ]")


def validar_matriz_cuadrada(A):
    """Revisa que A sea una matriz cuadrada de números reales finitos.
    Devuelve un mensaje de error o None."""
    n = len(A)
    if n < 1:
        return "A debe tener al menos una fila."
    if any(len(fila) != n for fila in A):
        return f"A debe ser una matriz cuadrada de {n} x {n}."
    for fila in A:
        for v in fila:
            if isinstance(v, bool) or not isinstance(v, numbers.Real) or not es_finito(v):
                return f"A solo puede tener números reales finitos (se encontró {v!r})."
    return None


def factorizacion_lu(A, mostrar=True):
    error = validar_matriz_cuadrada(A)
    if error:
        print(error)
        return None

    n = len(A)

    # Paso 1: L = identidad(n), U = A
    L = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    U = [[a_exacto(v) for v in fila] for fila in A]

    # Paso 2: cuando i = n no hay filas por debajo, así que basta llegar a n-1
    for i in range(n - 1):
        if U[i][i] == 0:
            print(f"u_{i + 1}{i + 1} = 0 durante la eliminación.")
            print("No se pudo factorizar de la forma LU")
            return None
        for j in range(i + 1, n):
            L[j][i] = U[j][i] / U[i][i]
            for k in range(i, n):
                U[j][k] = U[j][k] - L[j][i] * U[i][k]
            U[j][i] = 0              # exactamente 0 (con floats quedaría un residuo ~1e-17)

    # Paso 3: salida
    if mostrar:
        print("Se puede factorizar A = LU\n")
        imprimir_matriz("L", L)
        print()
        imprimir_matriz("U", U)
        det = 1
        for i in range(n):
            det = det * U[i][i]
        diagonal = " * ".join(f"({texto(U[i][i])})" if U[i][i] < 0 else texto(U[i][i])
                              for i in range(n))
        print(f"\n|A| = |U| = {diagonal} = {texto(det)}")
    return L, U


if __name__ == "__main__":
    F = Fraction

    # A = L U con L = [[1,0,0,0],[2,1,0,0],[-3,3,1,0],[4,5,-2,1]]
    # y U = [[2,1,0,3],[0,4,1,-1],[0,0,3,2],[0,0,0,-49]]
    print("Ejemplo 1: |A| = 2 * 4 * 3 * (-49) = -1176\n")
    A = [[2, 1, 0, 3],
         [4, 6, 1, 5],
         [-6, 9, 6, -10],
         [8, 24, -1, -46]]
    factorizacion_lu(A)

    print("\n\nEjemplo 2: matriz con fracciones\n")
    factorizacion_lu([[F(1, 2), F(1, 3)], [F(1, 4), F(2, 5)]])

    print("\n\nEjemplo 3: u_11 = 0, no se puede factorizar\n")
    factorizacion_lu([[0, 1], [1, 0]])
