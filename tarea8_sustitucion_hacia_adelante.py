"""
Tarea 8 - Algoritmo solución hacia adelante (sustitución progresiva)

Entrada:
    A : matriz n x n triangular inferior
    b : vector b, de tamaño n
Salida:
    Éxito  : "Se encontró el vector solución X = (x_i)"
    Fracaso: "No tiene solución o tiene infinitas soluciones"

Pasos:
    Paso 1: Iniciar X = (0)_{n x 1}
            x_1 = b_1 / a_11
    Paso 2: Para i = 2, ..., n
                x_i = ( b_i - sum_{j=1}^{i-1} a_ij x_j ) / a_ii
                Si a_ii != 0, en caso contrario Salida (Fracaso)
    Paso 3: Salida: el vector solución es X = (x_1, ..., x_n)

Nota: en Python los índices empiezan en 0, así que a_ii del cuaderno es A[i-1][i-1].
Los enteros se convierten a fracciones (fractions.Fraction) para obtener
resultados exactos. El parámetro `nombre` solo cambia la letra con que se
muestra el vector (la tarea 9 lo usa para mostrar y = (y_i)).
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


def fmt(v):
    """Muestra floats con 10 cifras significativas y negativos entre paréntesis."""
    t = f"{v:.10g}" if isinstance(v, float) else str(v)
    return f"({t})" if v < 0 else t


def validar_entrada(A, b):
    """Revisa que A y b sean coherentes. Devuelve un mensaje de error o None."""
    n = len(A)
    if n < 1:
        return "A debe tener al menos una fila."
    if any(len(fila) != n for fila in A):
        return f"A debe ser una matriz cuadrada de {n} x {n}."
    if len(b) != n:
        return f"b debe tener {n} componentes."
    for dato in [v for fila in A for v in fila] + list(b):
        if isinstance(dato, bool) or not isinstance(dato, numbers.Real) or not es_finito(dato):
            return f"A y b solo pueden tener números reales finitos (se encontró {dato!r})."
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                return (f"A no es triangular inferior: a_{i + 1}{j + 1} = {A[i][j]} "
                        f"(encima de la diagonal debe haber ceros).")
    return None


def sustitucion_hacia_adelante(A, b, mostrar=True, nombre="x"):
    error = validar_entrada(A, b)
    if error:
        print(error)
        return None

    n = len(A)
    A = [[a_exacto(v) for v in fila] for fila in A]
    b = [a_exacto(v) for v in b]

    # Si algún a_ii = 0 no hay solución única
    for i in range(n):
        if A[i][i] == 0:
            print(f"a_{i + 1}{i + 1} = 0. No tiene solución o tiene infinitas soluciones.")
            return None

    x = [0] * n

    # Paso 1: x_1 = b_1 / a_11
    x[0] = b[0] / A[0][0]
    if mostrar:
        print(f"{nombre}_1 = b_1 / a_11 = {fmt(b[0])} / {fmt(A[0][0])} = {fmt(x[0])}")

    # Paso 2: i = 2, ..., n
    for i in range(1, n):
        suma = 0
        for j in range(i):
            suma += A[i][j] * x[j]
        x[i] = (b[i] - suma) / A[i][i]
        if mostrar:
            print(f"{nombre}_{i + 1} = (b_{i + 1} - sum a_{i + 1}j {nombre}_j) / a_{i + 1}{i + 1} "
                  f"= ({fmt(b[i])} - {fmt(suma)}) / {fmt(A[i][i])} = {fmt(x[i])}")

    # Paso 3: salida
    if mostrar:
        print(f"\nSe encontró el vector solución {nombre} = ({', '.join(fmt(v) for v in x)})")
    return x


if __name__ == "__main__":
    # Ejemplo del cuaderno:
    #   (E1)  x1                    =  2
    #   (E2)  2x1 +  x2             = -2
    #   (E3) -3x1 + 3x2 +  x3       =  4
    #   (E4)  4x1 + 5x2 - 2x3 + x4  =  1
    print("Ejemplo del cuaderno (x1 = 2, x2 = -6, x3 = 28, x4 = 79):\n")
    A = [[1, 0, 0, 0],
         [2, 1, 0, 0],
         [-3, 3, 1, 0],
         [4, 5, -2, 1]]
    sustitucion_hacia_adelante(A, [2, -2, 4, 1])

    print("\n\nEjemplo con decimales:\n")
    sustitucion_hacia_adelante([[2.0, 0.0], [1.5, -4.0]], [3.0, 1.0])

    print("\n\nEjemplo con a_22 = 0 (fracaso):\n")
    sustitucion_hacia_adelante([[1, 0], [1, 0]], [1, 2])
