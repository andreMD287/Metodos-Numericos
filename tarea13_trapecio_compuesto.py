"""
Tarea 13 - Algoritmo Regla Compuesta del Trapecio

Entrada:
    f(x)   : función
    a y b  : intervalo
    n      : número de iteraciones (número de subintervalos), entero mayor o igual a 1
Salida:
    T(h) ≈ integral de a hasta b de f(x) dx

Inicialización:
    h  = (b - a) / n
    S0 = f(a) + f(b)
    S1 = 0 y S = 0
Suma:
    Para i = 1, 2, ..., n - 1 haga
        x  = a + i h
        S1 = S1 + f(x)
Suma total:
    S = (h / 2) S0 + h S1
Salida:
    T(h) = S

Nota: en el ejemplo del cuaderno, f(x) = e^(-x^2) en [0, 2] con n = 5, se obtiene T(h) ≈ 0.8811.
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


def trapecio_compuesto(f, a, b, n, mostrar=True):
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
    if isinstance(n, bool) or not isinstance(n, numbers.Integral) or n < 1:
        print("n debe ser un entero mayor o igual a 1.")
        return None
    n = int(n)

    # ---------- Inicialización ----------
    h = (b - a) / n
    try:
        fa = evaluar(f, a)
        fb = evaluar(f, b)
    except ValueError as err:
        print(f"Error en los extremos del intervalo: {err}.")
        return None
    S0 = fa + fb
    interiores = []                    # valores f(x_i) para i = 1, ..., n - 1

    if mostrar:
        print(f"h = (b - a) / n = ({b:.10g} - {a:.10g}) / {n} = {h:.10g}\n")
        print(f"{'i':>4} {'x_i':>14} {'f(x_i)':>16} {'peso':>6}")
        print(f"{0:>4} {a:>14.8g} {fa:>16.10g} {1:>6}")

    # ---------- Suma: i = 1, ..., n - 1 ----------
    for i in range(1, n):
        x = a + i * h
        try:
            fx = evaluar(f, x)
        except ValueError as err:
            print(f"\nError en i = {i}: {err}.")
            return None
        interiores.append(fx)
        if mostrar:
            print(f"{i:>4} {x:>14.8g} {fx:>16.10g} {2:>6}")

    if mostrar:
        print(f"{n:>4} {b:>14.8g} {fb:>16.10g} {1:>6}")

    # ---------- Suma total ----------
    S1 = math.fsum(interiores)
    S = (h / 2) * S0 + h * S1

    print(f"\nS0 = f(a) + f(b) = {S0:.10g}")
    print(f"S1 = suma de f(x_i), i = 1, ..., n-1 = {S1:.10g}")
    print(f"T(h) = (h/2) S0 + h S1 = ({h:.10g}/2)({S0:.10g}) + {h:.10g}({S1:.10g}) = {S:.10g}")
    return S


if __name__ == "__main__":
    # Ejemplo del cuaderno: f(x) = e^(-x^2) en [0, 2], n = 5  ->  T(h) ≈ 0.8811
    print("Ejemplo del cuaderno: f(x) = e^(-x^2) en [0, 2], n = 5\n")
    trapecio_compuesto(lambda x: math.exp(-x**2), 0, 2, 5)

    print("\n\nFunción lineal (el trapecio es exacto): f(x) = 2x + 1 en [0, 3], n = 3, integral = 12\n")
    trapecio_compuesto(lambda x: 2 * x + 1, 0, 3, 3)

    print("\n\nMás subintervalos: e^(-x^2) en [0, 2], n = 1000, valor exacto = 0.8820813908\n")
    trapecio_compuesto(lambda x: math.exp(-x**2), 0, 2, 1000, mostrar=False)
