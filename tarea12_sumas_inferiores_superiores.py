"""
Tarea 12 - Algoritmo integración: sumas superiores e inferiores

Entrada:
    f : función
    a, b : intervalo [a, b]
    n : número de particiones
Salida:
    L : suma inferior
    U : suma superior

Pasos:
    Paso 1: h = (b - a) / n ,   x_i = a + i h
    Paso 2: Para i en {0, ..., n-1}
                f_i = min{ f(x_i), f(x_{i+1}) }
                F_i = max{ f(x_i), f(x_{i+1}) }
    Paso 3: L = h sum_{i=0}^{n-1} f_i
            U = h sum_{i=0}^{n-1} F_i
    Salida: L y U

Nota: el mínimo y el máximo se toman entre los dos extremos de cada subintervalo, así
que L <= integral <= U se garantiza cuando f es monótona (creciente o decreciente) en
cada subintervalo. Si f sube y baja dentro de un subintervalo, aumentar n lo corrige.
"""
import math
import numbers


def evaluar(f, x):
    """Evalúa f(x) y verifica que el resultado sea un número real finito."""
    try:
        y = f(x)
    except (ValueError, OverflowError, ZeroDivisionError) as err:
        raise ValueError(f"no se pudo evaluar f({x}): {err}")
    try:
        valido = isinstance(y, numbers.Real) and not isinstance(y, bool) and math.isfinite(y)
    except OverflowError:                    # entero demasiado grande para un float
        valido = False
    if not valido:
        raise ValueError(f"f({x}) = {y!r} no es un número real finito")
    return y


def sumas_inferior_superior(f, a, b, n, mostrar=True):
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

    # Paso 1: h y los puntos x_i = a + i h (el último se fija en b para evitar error de redondeo)
    h = (b - a) / n
    x = [a + i * h for i in range(n)] + [b]
    try:
        fx = [evaluar(f, xi) for xi in x]
    except ValueError as err:
        print(f"Error: {err}.")
        return None

    if mostrar:
        print(f"h = (b - a) / n = ({b} - {a}) / {n} = {h:.10g}\n")
        print(f"{'i':>4} {'x_i':>14} {'f(x_i)':>16} {'f_i = min':>16} {'F_i = max':>16}")

    # Pasos 2 y 3
    minimos, maximos = [], []
    for i in range(n):
        minimos.append(min(fx[i], fx[i + 1]))
        maximos.append(max(fx[i], fx[i + 1]))
        if mostrar:
            print(f"{i:>4} {x[i]:>14.8g} {fx[i]:>16.10g} {minimos[i]:>16.10g} {maximos[i]:>16.10g}")
    if mostrar:
        print(f"{n:>4} {x[n]:>14.8g} {fx[n]:>16.10g}")

    L = h * math.fsum(minimos)
    U = h * math.fsum(maximos)

    print(f"\nSuma inferior L = h * sum f_i = {h:.10g} * {math.fsum(minimos):.10g} = {L:.10g}")
    print(f"Suma superior U = h * sum F_i = {h:.10g} * {math.fsum(maximos):.10g} = {U:.10g}")
    return L, U


if __name__ == "__main__":
    # Ejemplo del cuaderno: f(x) = x^2 en [1, 5], n = 8  ->  L = 35.5, U = 47.5
    # (la integral exacta es 124/3 = 41.33...)
    print("Ejemplo del cuaderno: f(x) = x^2 en [1, 5], n = 8\n")
    sumas_inferior_superior(lambda x: x**2, 1, 5, 8)

    print("\n\nEjemplo con f decreciente: f(x) = 1/x en [1, 2], n = 4 (integral = ln 2 = 0.6931)\n")
    sumas_inferior_superior(lambda x: 1 / x, 1, 2, 4)

    print("\n\nMás particiones: f(x) = x^2 en [1, 5], n = 1000 (integral = 41.3333)\n")
    sumas_inferior_superior(lambda x: x**2, 1, 5, 1000, mostrar=False)
