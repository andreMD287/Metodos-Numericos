"""
Tarea 10 - Método LUP

Entrada:
    A : matriz A = (a_ij) n x n
    b : vector b = (b_i) n x 1
Salida:
    Vector solución X = (x_i) n x 1
    Matrices P, L y U  (con P A = L U)

Pasos:
    Paso 1: Vector de permutación P: para i = 1, ..., n haga P_i = i
    Paso 2: Cómputo. Para j = 1, ..., n haga
        2.1 Pivoteo parcial: determine r en {j, ..., n} tal que |a_rj| = max_{i=j..n} |a_ij|
        2.2 Chequeo de singularidad: si a_rj = 0, A es singular (no tiene inversa).
            PARE (no hay solución única)
        2.3 Intercambio de filas si r != j:
                intercambie P_j y P_r
                intercambie b_j y b_r
                para k = 1, ..., n intercambie a_jk por a_rk
        2.4 Eliminación. Para i = j+1, ..., n haga
                a_ij = a_ij / a_jj ,   b_i = b_i - a_ij b_j
                para k = j+1, ..., n haga a_ik = a_ik - a_ij a_jk
    Paso 3: Chequeo de singularidad: si a_nn = 0, A es singular. PARE
            (ya lo cubre el paso 2.2 cuando j = n)
    Paso 4: Construcción de L, U y P. Sea S_ij = 1 si i = j y 0 si i != j
                L_ij = S_ij si i <= j ;  a_ij si i > j
                U_ij = a_ij si i <= j ;  0    si i > j
                P_ij = S(P_i, j)    (es decir, 1 si P_i = j y 0 en otro caso)
            Salida: L, U (y P)
    Paso 5: Solución del sistema: se usa el algoritmo de la tarea 9 con L U x = P b

Como los pasos 2.1-2.3 reordenan las filas de A, se cumple P A = L U, así que
A x = b equivale a L U x = P b, donde (P b)_i = b_{P_i}.

Nota: en Python los índices empiezan en 0 (P se guarda con valores 0, ..., n-1 y
se muestra con valores 1, ..., n). Los enteros se convierten a fracciones
(fractions.Fraction) para que los resultados sean exactos.
"""
from tarea7_lu import a_exacto, imprimir_matriz, texto, validar_matriz_cuadrada
from tarea9_sistemas_lu import MENSAJE_FRACASO, resolver_con_lu


def casi_igual(u, v):
    """Igualdad exacta para Fractions y con tolerancia relativa para floats."""
    return abs(u - v) <= 1e-9 * max(1, abs(u), abs(v))


def lup(A, b, mostrar=True):
    error = validar_matriz_cuadrada(A)
    if error:
        print(error)
        return None
    if len(b) != len(A):
        print(f"b debe tener {len(A)} componentes.")
        return None

    n = len(A)
    a = [[a_exacto(v) for v in fila] for fila in A]      # copia de trabajo de A
    b_trabajo = [a_exacto(v) for v in b]
    b_original = list(b_trabajo)

    # Paso 1: vector de permutación
    P = list(range(n))

    # Paso 2: cómputo
    for j in range(n):
        # 2.1 Pivoteo parcial (si hay empate se toma la fila más alta)
        r = max(range(j, n), key=lambda i: abs(a[i][j]))

        # 2.2 Chequeo de singularidad
        if a[r][j] == 0:
            print(f"No se encontró pivote distinto de 0 en la columna {j + 1}: "
                  f"A es singular (no tiene inversa).")
            print(MENSAJE_FRACASO)
            return None

        # 2.3 Intercambio de filas
        if r != j:
            P[j], P[r] = P[r], P[j]
            b_trabajo[j], b_trabajo[r] = b_trabajo[r], b_trabajo[j]
            a[j], a[r] = a[r], a[j]                      # intercambia las n columnas de la fila

        # 2.4 Eliminación (los multiplicadores quedan guardados en a_ij, i > j)
        for i in range(j + 1, n):
            a[i][j] = a[i][j] / a[j][j]
            b_trabajo[i] = b_trabajo[i] - a[i][j] * b_trabajo[j]
            for k in range(j + 1, n):
                a[i][k] = a[i][k] - a[i][j] * a[j][k]

    # Paso 4: construcción de L, U y P
    L = [[1 if i == j else (a[i][j] if i > j else 0) for j in range(n)] for i in range(n)]
    U = [[a[i][j] if i <= j else 0 for j in range(n)] for i in range(n)]
    Pm = [[1 if P[i] == j else 0 for j in range(n)] for i in range(n)]

    if mostrar:
        print("Vector de permutación P =", tuple(p + 1 for p in P), "\n")
        imprimir_matriz("P", Pm)
        print()
        imprimir_matriz("L", L)
        print()
        imprimir_matriz("U", U)

        # Verificación: P A = L U (fila i de P A es la fila P_i de A)
        ok = all(casi_igual(sum(L[i][k] * U[k][j] for k in range(n)), a_exacto(A[P[i]][j]))
                 for i in range(n) for j in range(n))
        print(f"\nVerificación P A = L U: {'correcta' if ok else 'INCORRECTA'}")

    # Paso 5: se resuelve L U x = P b con el algoritmo de la tarea 9
    Pb = [b_original[P[i]] for i in range(n)]
    x = resolver_con_lu(L, U, Pb, mostrar=mostrar)
    if x is None:
        return None

    print(f"\nSe encontró el vector solución: x = ({', '.join(texto(v) for v in x)})")
    return x, Pm, L, U


if __name__ == "__main__":
    print("Ejemplo 1: A x = b con solución x = (1, 1, 2)\n")
    lup([[2, 1, 1],
         [4, -6, 0],
         [-2, 7, 2]], [5, -2, 9])

    print("\n\nEjemplo 2: a_11 = 0 (la tarea 9 falla, LUP sí funciona), solución x = (1, 2, 3)\n")
    lup([[0, 2, 1],
         [1, 1, 1],
         [2, 1, 3]], [7, 6, 13])

    print("\n\nEjemplo 3: matriz singular, A = [[1, 2], [2, 4]]\n")
    lup([[1, 2], [2, 4]], [1, 2])
