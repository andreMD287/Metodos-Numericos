"""
Tarea 3 - Algoritmo de la Regla Falsa (Posición Falsa)

Entrada:
    f      : función
    a0, b0 : valores iniciales, con a0 < b0 y f(a0) f(b0) < 0
    eps    : tolerancia (precisión deseada)
    M      : máximo de iteraciones
Salida:
    Éxito  : "Se obtuvo una aproximación de P"
    Fracaso: "Después de M iteraciones no se logró la precisión deseada"

Iteraciones:
    Mientras n < M (n = 0, 1, ...) haga
        x_n = (a_n f(b_n) - b_n f(a_n)) / (f(b_n) - f(a_n))
        Si n > 0 y x_n != 0 y |(x_n - x_{n-1}) / x_n| < eps  (error relativo)
            Salida (Éxito). PARE
        En caso contrario
            Si f(x_n) f(a_n) < 0:  b_{n+1} = x_n,  a_{n+1} = a_n
            En caso contrario:     a_{n+1} = x_n,  b_{n+1} = b_n
    Si n = M, Salida (Fracaso). PARE
"""
import math


def signo(v):
    """1, -1 o 0. Se usa en lugar del producto f(x)f(a) para evitar
    que el producto se vuelva 0 (underflow) o infinito (overflow)."""
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


def evaluar(f, x):
    """Evalúa f(x) y verifica que el resultado sea un número real finito."""
    try:
        y = f(x)
    except (ValueError, OverflowError, ZeroDivisionError) as err:
        raise ValueError(f"no se pudo evaluar f({x}): {err}")
    if isinstance(y, complex) or not math.isfinite(y):
        raise ValueError(f"f({x}) = {y} no es un número real finito")
    return y


def regla_falsa(f, a0, b0, eps, M):
    # ---------- Validación de la entrada ----------
    if eps <= 0:
        print("La tolerancia (eps) debe ser positiva.")
        return None
    if M < 1 or int(M) != M:
        print("M debe ser un entero mayor o igual a 1.")
        return None
    if a0 == b0:
        print("a0 y b0 deben ser distintos (se requiere a0 < b0).")
        return None
    if a0 > b0:
        a0, b0 = b0, a0              # se ordena para cumplir a0 < b0

    try:
        fa = evaluar(f, a0)
        fb = evaluar(f, b0)
    except ValueError as err:
        print(f"Error en los valores iniciales: {err}.")
        return None

    # Si un extremo ya es raíz, se devuelve directamente
    if fa == 0:
        print(f"Se obtuvo una aproximación de P = {a0} (f(a0) = 0).")
        return a0
    if fb == 0:
        print(f"Se obtuvo una aproximación de P = {b0} (f(b0) = 0).")
        return b0

    # Condición f(a0) f(b0) < 0
    if signo(fa) == signo(fb):
        print("No se cumple f(a0) f(b0) < 0: el método no se puede aplicar en [a0, b0].")
        return None

    # ---------- Iteraciones ----------
    a, b = a0, b0
    x_ant = None                     # x_{n-1}

    print(f"{'n':>3} {'a_n':>13} {'b_n':>13} {'f(a_n)':>13} {'f(b_n)':>13} "
          f"{'x_n':>13} {'f(x_n)':>13} {'|(x_n-x_(n-1))/x_n|':>20}")

    n = 0
    while n < M:
        x = (a * fb - b * fa) / (fb - fa)
        try:
            fx = evaluar(f, x)
        except ValueError as err:
            print(f"\nError en la iteración n = {n}: {err}.")
            return None

        if n > 0 and x != 0:
            error = abs((x - x_ant) / x)
            texto_error = f"{error:.6e}"
        else:
            error = None
            texto_error = "----"

        print(f"{n:>3} {a:>13.8f} {b:>13.8f} {fa:>13.6e} {fb:>13.6e} "
              f"{x:>13.8f} {fx:>13.6e} {texto_error:>20}")

        # Criterio de parada (error relativo)
        if error is not None and error < eps:
            print(f"\nSe obtuvo una aproximación de P ≈ {x} (n = {n}).")
            return x

        # Si x_n es raíz exacta no hace falta seguir
        if fx == 0:
            print(f"\nSe obtuvo una aproximación de P = {x} (f(x_n) = 0 exacto, n = {n}).")
            return x

        # Actualización del intervalo
        if signo(fx) != signo(fa):   # f(x_n) f(a_n) < 0
            b, fb = x, fx
        else:
            a, fa = x, fx

        x_ant = x
        n += 1

    print(f"\nDespués de M = {M} iteración(es) no se logró la precisión deseada.")
    return None


if __name__ == "__main__":
    # Ejemplo del cuaderno: f(x) = x^3 + 4x^2 - 10 en [1, 2]
    f = lambda x: x**3 + 4 * x**2 - 10

    print("Ejemplo del cuaderno: f(x) = x^3 + 4x^2 - 10 en [1, 2], M = 5\n")
    regla_falsa(f, 1, 2, eps=1e-4, M=5)

    print("\n\nMismo ejemplo con tolerancia 1e-8\n")
    regla_falsa(f, 1, 2, eps=1e-8, M=100)
