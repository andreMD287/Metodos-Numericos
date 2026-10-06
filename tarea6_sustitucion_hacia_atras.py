"""
Tarea 6 - Algoritmo hacia atrás (sustitución regresiva)

Entrada:
    n : tamaño de la matriz
    A : matriz A (triangular superior), n x n
    b : vector b, de tamaño n
Salida:
    Vector solución x = (x1, x2, ..., xn)

Pasos:
    Paso 0*: Para i = 1, 2, ..., n
                 Si a_ii = 0  PARE  "El sistema no tiene solución"
                 En caso contrario continúe
    Paso 1:  x_n = b_n / a_nn
    Paso 2:  Para i = n-1, ..., 1
                 x_i = ( b_i - sum_{j=i+1}^{n} a_ij x_j ) / a_ii
    Paso 3:  Salida: vector x = (x1, x2, ..., xn)

Nota: en Python los índices empiezan en 0, así que a_ii del cuaderno es A[i-1][i-1].
Se puede usar con enteros, decimales o fracciones (fractions.Fraction) para
obtener resultados exactos.
"""
from fractions import Fraction


def fmt(v):
    """Muestra floats con 10 cifras significativas y negativos entre paréntesis."""
    t = f"{v:.10g}" if isinstance(v, float) else str(v)
    return f"({t})" if v < 0 else t


def validar_entrada(n, A, b):
    """Revisa que n, A y b sean coherentes. Devuelve un mensaje de error o None."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        return "n debe ser un entero mayor o igual a 1."
    if len(A) != n or any(len(fila) != n for fila in A):
        return f"A debe ser una matriz cuadrada de {n} x {n}."
    if len(b) != n:
        return f"b debe tener {n} componentes."
    for i in range(n):
        for j in range(i):
            if A[i][j] != 0:
                return (f"A no es triangular superior: a_{i + 1}{j + 1} = {A[i][j]} "
                        f"(debajo de la diagonal debe haber ceros).")
    return None


def sustitucion_hacia_atras(n, A, b, mostrar=True):
    error = validar_entrada(n, A, b)
    if error:
        print(error)
        return None

    # Paso 0*: revisar la diagonal
    for i in range(n):
        if A[i][i] == 0:
            print(f"a_{i + 1}{i + 1} = 0. El sistema no tiene solución.")
            return None

    x = [0] * n

    # Paso 1: x_n = b_n / a_nn
    x[n - 1] = b[n - 1] / A[n - 1][n - 1]
    if mostrar:
        print(f"x_{n} = b_{n} / a_{n}{n} = {fmt(b[n - 1])} / {fmt(A[n - 1][n - 1])} = {fmt(x[n - 1])}")

    # Paso 2: i = n-1, ..., 1
    for i in range(n - 2, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += A[i][j] * x[j]
        x[i] = (b[i] - suma) / A[i][i]
        if mostrar:
            print(f"x_{i + 1} = (b_{i + 1} - sum a_{i + 1}j x_j) / a_{i + 1}{i + 1} "
                  f"= ({fmt(b[i])} - {fmt(suma)}) / {fmt(A[i][i])} = {fmt(x[i])}")

    # Paso 3: salida
    if mostrar:
        print(f"\nVector solución x = ({', '.join(fmt(v) for v in x)})")
    return x


# ---------------------------------------------------------------------------
# Extra: el ejemplo del cuaderno es triangular INFERIOR (se despeja x1 primero),
# que corresponde a la sustitución hacia adelante. Se incluye para verificarlo.
# ---------------------------------------------------------------------------
def sustitucion_hacia_adelante(n, A, b, mostrar=True):
    if not isinstance(n, int) or n < 1 or len(A) != n or any(len(f) != n for f in A) or len(b) != n:
        print("Dimensiones inválidas.")
        return None
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                print(f"A no es triangular inferior: a_{i + 1}{j + 1} = {A[i][j]}.")
                return None
    for i in range(n):
        if A[i][i] == 0:
            print(f"a_{i + 1}{i + 1} = 0. El sistema no tiene solución.")
            return None

    x = [0] * n
    for i in range(n):
        suma = 0
        for j in range(i):
            suma += A[i][j] * x[j]
        x[i] = (b[i] - suma) / A[i][i]
        if mostrar:
            print(f"x_{i + 1} = ({fmt(b[i])} - {fmt(suma)}) / {fmt(A[i][i])} = {fmt(x[i])}")
    if mostrar:
        print(f"\nVector solución x = ({', '.join(fmt(v) for v in x)})")
    return x


if __name__ == "__main__":
    F = Fraction

    # Ejemplo de sustitución hacia atrás (matriz triangular superior)
    print("Sistema triangular superior:")
    print("  2x1 +  x2 -  x3 =  3")
    print("        3x2 + 2x3 = 12")
    print("              4x3 =  8\n")
    A = [[F(2), F(1), F(-1)],
         [F(0), F(3), F(2)],
         [F(0), F(0), F(4)]]
    b = [F(3), F(12), F(8)]
    sustitucion_hacia_atras(3, A, b)

    # Ejemplo del cuaderno (triangular inferior -> hacia adelante), con fracciones exactas
    print("\n\nEjemplo del cuaderno (triangular inferior, sustitución hacia adelante):\n")
    A_cuaderno = [[F(1), 0, 0, 0],
                  [F(3, 4), 1, 0, 0],
                  [F(-1, 2), -18, 1, 0],
                  [F(-5, 4), -15, F(4, 5), 1]]
    b_cuaderno = [8, 30, 15, 2]
    sustitucion_hacia_adelante(4, A_cuaderno, b_cuaderno)
