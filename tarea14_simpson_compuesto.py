"""
Tarea 14 - Algoritmo de la Regla de Simpson Compuesta

Entrada:
    f      : función
    [a, b] : extremos del intervalo
    M      : número entero, con n = 2M subintervalos (n siempre es par)
Salida:
    S(h) ≈ integral de a hasta b de f(x) dx

Inicialización:
    h  = (b - a) / n
    S0 = f(a) + f(b)
    S1 = 0
    S2 = 0
Suma:
    Para i = 1, 2, ..., 2M - 1 haga
        x = a + i h
        Si i es par,   entonces S2 = S2 + f(x)
        Si i es impar, entonces S1 = S1 + f(x)
Salida:
    S(h) = (h / 3) (S0 + 2 S2 + 4 S1)

Nota: en el ejemplo del cuaderno, f(x) = e^(-x^2) en [0, 2] con n = 8, se usa M = 4.
La regla es exacta para polinomios de grado menor o igual a 3.
"""
import math
import numbers


def evaluar(f, x):
    """Evalúa f(x) y verifica que el resultado sea un número real finito."""
    try:
        y = f(x)
    except (ValueError, OverflowError, ZeroDivisionError, TypeError) as err:
        raise ValueError(f"no se pudo evaluar f({x}): {err}")
    try:
        valido = isinstance(y, numbers.Real) and not isinstance(y, bool) and math.isfinite(y)
    except OverflowError:                    # entero demasiado grande para un float
        valido = False
    if not valido:
        raise ValueError(f"f({x}) = {y!r} no es un número real finito")
    return y


def simpson_compuesto(f, a, b, M, mostrar=True):
    # ---------- Validación de la entrada ----------
    extremos = []
    for nombre, v in (("a", a), ("b", b)):
        try:
            ok = isinstance(v, numbers.Real) and not isinstance(v, bool) and math.isfinite(float(v))
        except OverflowError:                # entero demasiado grande para un float
            ok = False
        if not ok:
            print(f"{nombre} debe ser un número real finito.")
            return None
        extremos.append(float(v))
    a, b = extremos
    if not a < b:
        print("Se requiere a < b.")
        return None
    if isinstance(M, bool) or not isinstance(M, numbers.Integral) or M < 1:
        print("M debe ser un entero mayor o igual a 1 (el número de subintervalos es n = 2M).")
        return None
    M = int(M)
    n = 2 * M

    # ---------- Inicialización ----------
    h = (b - a) / n
    try:
        fa = evaluar(f, a)
        fb = evaluar(f, b)
    except ValueError as err:
        print(f"Error en los extremos del intervalo: {err}.")
        return None
    S0 = fa + fb
    pares, impares = [], []            # valores f(x_i) con i par (S2) y con i impar (S1)

    if mostrar:
        print(f"n = 2M = {n}   h = (b - a) / n = ({b:.10g} - {a:.10g}) / {n} = {h:.10g}\n")
        print(f"{'i':>4} {'x_i':>14} {'f(x_i)':>16} {'peso':>6}")
        print(f"{0:>4} {a:>14.8g} {fa:>16.10g} {1:>6}")

    # ---------- Suma: i = 1, ..., 2M - 1 ----------
    for i in range(1, n):
        x = a + i * h
        try:
            fx = evaluar(f, x)
        except ValueError as err:
            print(f"\nError en i = {i}: {err}.")
            return None
        if i % 2 == 0:
            pares.append(fx)
        else:
            impares.append(fx)
        if mostrar:
            print(f"{i:>4} {x:>14.8g} {fx:>16.10g} {2 if i % 2 == 0 else 4:>6}")

    if mostrar:
        print(f"{n:>4} {b:>14.8g} {fb:>16.10g} {1:>6}")

    S1 = math.fsum(impares)
    S2 = math.fsum(pares)
    S = (h / 3) * (S0 + 2 * S2 + 4 * S1)

    print(f"\nS0 = f(a) + f(b) = {S0:.10g}")
    print(f"S1 = suma de f(x_i) con i impar = {S1:.10g}")
    print(f"S2 = suma de f(x_i) con i par   = {S2:.10g}")
    print(f"S(h) = (h/3)(S0 + 2 S2 + 4 S1) = ({h:.10g}/3)({S0:.10g} + 2({S2:.10g}) + 4({S1:.10g}))"
          f" = {S:.10g}")
    return S


if __name__ == "__main__":
    # Ejemplo del cuaderno: f(x) = e^(-x^2) en [0, 2], n = 8 (M = 4)  ->  ≈ 0.8820
    print("Ejemplo del cuaderno: f(x) = e^(-x^2) en [0, 2], n = 8 (M = 4)\n")
    simpson_compuesto(lambda x: math.exp(-x**2), 0, 2, 4)

    print("\n\nPolinomio de grado 3 (Simpson es exacto): x^3 en [0, 2], M = 1, integral = 4\n")
    simpson_compuesto(lambda x: x**3, 0, 2, 1)

    print("\n\nMás subintervalos: e^(-x^2) en [0, 2], n = 1000 (M = 500), valor exacto = 0.8820813908\n")
    simpson_compuesto(lambda x: math.exp(-x**2), 0, 2, 500, mostrar=False)
