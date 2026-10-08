"""
Tarea 11 - Algoritmo de Gauss-Seidel

Entrada:
    A  : matriz cuadrada A = (a_ij) n x n
    b  : vector de constantes b = (b_i) n x 1
    x0 : valor inicial X^0 = (x_1^0, x_2^0, ..., x_n^0)
    eps: tolerancia
    M  : máximo de iteraciones
Salida:
    Éxito  : "Se encuentra una solución aproximada al sistema Ax = b"
    Fracaso: "Después de M iteraciones no fue posible hallar una solución al sistema Ax = b"

Pasos:
    k = 1
    Mientras k <= M
        1ro. Sea X = (x_1, x_2, ..., x_n)
             Para i = 1, ..., n
                 x_i = ( b_i - sum_{j != i} a_ij x_j ) / a_ii
             siempre y cuando a_ii != 0; si a_ii = 0, Salida (Fracaso)
        2do. Si ||X - X^0|| <= eps, Salida (Éxito): una solución es X
             En caso contrario X^0 = X
             Si k = M, Salida (Fracaso)
        k = k + 1

Gauss-Seidel: al calcular x_i se usan los valores ya actualizados de esta misma
iteración (x_1, ..., x_{i-1}) y los de la iteración anterior (x_{i+1}, ..., x_n).
Con usar_valores_anteriores=True se usan los de la iteración anterior para todos los
x_j, tal como se lee la fórmula del cuaderno (con X_j^0); eso es el método de Jacobi.

Nota: la norma ||.|| del cuaderno no está especificada; se usa la norma del máximo,
||v|| = max |v_i|. Los datos se pasan a decimales (float) porque con fracciones el
tamaño de los números crece sin control a lo largo de las iteraciones.
La convergencia está garantizada, por ejemplo, si A es diagonalmente dominante.
"""
import math
import numbers

from tarea7_lu import es_finito, validar_matriz_cuadrada


def a_decimal(v):
    """Convierte un número real a float. Devuelve None si no cabe en un float."""
    try:
        return float(v)
    except OverflowError:
        return None


def validar_entrada(A, b, x0, eps, M):
    """Revisa que los datos sean coherentes. Devuelve un mensaje de error o None."""
    error = validar_matriz_cuadrada(A)
    if error:
        return error
    n = len(A)
    if len(b) != n:
        return f"b debe tener {n} componentes."
    if len(x0) != n:
        return f"El valor inicial x0 debe tener {n} componentes."
    for dato in list(b) + list(x0):
        if isinstance(dato, bool) or not isinstance(dato, numbers.Real) or not es_finito(dato):
            return f"b y x0 solo pueden tener números reales finitos (se encontró {dato!r})."
    if isinstance(eps, bool) or not isinstance(eps, numbers.Real) or not es_finito(eps) or eps <= 0:
        return "La tolerancia (eps) debe ser un número positivo."
    if isinstance(M, bool) or not isinstance(M, numbers.Integral) or M < 1:
        return "M debe ser un entero mayor o igual a 1."
    return None


def gauss_seidel(A, b, x0, eps, M, mostrar=True, usar_valores_anteriores=False):
    error = validar_entrada(A, b, x0, eps, M)
    if error:
        print(error)
        return None

    n = len(A)
    datos = [a_decimal(v) for fila in A for v in fila] + [a_decimal(v) for v in list(b) + list(x0)]
    if any(v is None for v in datos):
        print("Algún dato es demasiado grande para representarse como decimal.")
        return None
    a = [datos[i * n:(i + 1) * n] for i in range(n)]
    bb = datos[n * n:n * n + n]
    x_ant = datos[n * n + n:]                     # X^0

    # Si algún a_ii = 0 no se puede despejar x_i
    for i in range(n):
        if a[i][i] == 0:
            print(f"a_{i + 1}{i + 1} = 0: no se puede despejar x_{i + 1}, el método no se puede aplicar.")
            print(f"No fue posible hallar una solución al sistema Ax = b (a_{i + 1}{i + 1} = 0).")
            return None

    if mostrar:
        columnas = " ".join(f"{'x_' + str(i + 1):>16}" for i in range(n))
        print(f"{'k':>4} {columnas} {'||X - X^0||':>14}")
        print(f"{0:>4} " + " ".join(f"{v:>16.10g}" for v in x_ant) + f" {'':>14}")

    for k in range(1, int(M) + 1):
        x = list(x_ant)
        fuente = x_ant if usar_valores_anteriores else x    # x se va actualizando en el ciclo
        for i in range(n):
            suma = 0.0
            for j in range(n):
                if j != i:
                    suma += a[i][j] * fuente[j]
            x[i] = (bb[i] - suma) / a[i][i]

        if not all(math.isfinite(v) for v in x):
            print(f"\nEn la iteración k = {k} aparecieron valores infinitos o no numéricos: "
                  f"el método diverge.")
            print("No fue posible hallar una solución al sistema Ax = b.")
            return None

        err = max(abs(x[i] - x_ant[i]) for i in range(n))
        if mostrar:
            print(f"{k:>4} " + " ".join(f"{v:>16.10g}" for v in x) + f" {err:>14.6e}")

        if err <= eps:
            print(f"\nSe encuentra una solución aproximada al sistema Ax = b "
                  f"(k = {k}, ||X - X^0|| = {err:.3e}).")
            print(f"Una solución es X = ({', '.join(f'{v:.10g}' for v in x)})")
            return x

        x_ant = x

    print(f"\nDespués de M = {M} iteraciones no fue posible hallar una solución al sistema Ax = b.")
    return None


if __name__ == "__main__":
    # Sistema diagonalmente dominante, solución exacta x = (1, 2, -1, 1)
    A = [[10, -1, 2, 0],
         [-1, 11, -1, 3],
         [2, -1, 10, -1],
         [0, 3, -1, 8]]
    b = [6, 25, -11, 15]

    print("Ejemplo 1: Gauss-Seidel, solución exacta x = (1, 2, -1, 1)\n")
    gauss_seidel(A, b, [0, 0, 0, 0], eps=1e-8, M=100)

    print("\n\nEjemplo 2: mismo sistema con la fórmula literal del cuaderno (Jacobi)\n")
    gauss_seidel(A, b, [0, 0, 0, 0], eps=1e-8, M=100, usar_valores_anteriores=True)

    print("\n\nEjemplo 3: no converge, A = [[1, 2], [3, 1]]\n")
    gauss_seidel([[1, 2], [3, 1]], [3, 4], [0, 0], eps=1e-8, M=10)

    print("\n\nEjemplo 4: a_11 = 0\n")
    gauss_seidel([[0, 1], [1, 1]], [1, 2], [0, 0], eps=1e-8, M=10)
