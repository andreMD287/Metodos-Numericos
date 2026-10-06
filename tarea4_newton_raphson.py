"""
Tarea 4 - Algoritmo de Newton-Raphson

Entrada:
    f   : función
    df  : derivada de la función (f')
    x0  : valor inicial
    eps : precisión deseada
    M   : máximo de iteraciones
Salida:
    Éxito  : "Se obtuvo una aproximación de P"
    Fracaso: "Después de M iteraciones no se logró la precisión deseada"

Iteraciones:
    Para n = 1, 2, ..., M haga
        x_{n+1} = x_n - f(x_n) / f'(x_n)
        e_{n+1} = |x_{n+1} - x_n|
        Si e_{n+1} < eps, entonces Salida (Éxito). PARE
    Si n = M, entonces Salida (Fracaso). PARE
"""
import math


def evaluar(func, x, nombre):
    """Evalúa func(x) y verifica que el resultado sea un número real finito."""
    try:
        y = func(x)
    except (ValueError, OverflowError, ZeroDivisionError) as err:
        raise ValueError(f"no se pudo evaluar {nombre}({x}): {err}")
    if isinstance(y, complex) or not math.isfinite(y):
        raise ValueError(f"{nombre}({x}) = {y} no es un número real finito")
    return y


def revisar_derivada(f, df, x0):
    """Compara f'(x0) con una derivada numérica (diferencia central).
    Solo avisa: sirve para detectar si se escribió mal la derivada."""
    try:
        h = 1e-6 * max(1.0, abs(x0))
        numerica = (f(x0 + h) - f(x0 - h)) / (2 * h)
        dada = df(x0)
        if abs(dada - numerica) > 1e-4 * max(1.0, abs(numerica)):
            print(f"AVISO: f'({x0}) = {dada}, pero la derivada numérica da ≈ {numerica:.6f}. "
                  f"Revise que f' esté bien escrita.\n")
    except Exception:
        pass                         # si no se puede evaluar, lo detecta el algoritmo


def newton_raphson(f, df, x0, eps, M):
    # ---------- Validación de la entrada ----------
    if eps <= 0:
        print("La precisión deseada (eps) debe ser positiva.")
        return None
    if M < 1 or int(M) != M:
        print("M debe ser un entero mayor o igual a 1.")
        return None

    revisar_derivada(f, df, x0)

    dfx_enc = "f'(x_n)"
    print(f"{'n':>3} {'x_n':>18} {'f(x_n)':>15} {dfx_enc:>15} {'x_(n+1)':>18} {'|x_(n+1)-x_n|':>15}")

    x_n = x0
    for n in range(1, int(M) + 1):   # n = 1, 2, ..., M
        try:
            fx = evaluar(f, x_n, "f")
            dfx = evaluar(df, x_n, "f'")
        except ValueError as err:
            print(f"\nError en la iteración n = {n}: {err}.")
            print("Después de", n - 1, "iteración(es) no se logró la precisión deseada.")
            return None

        # Si x_n ya es raíz exacta, no hace falta seguir
        if fx == 0:
            print(f"{n:>3} {x_n:>18.10f} {fx:>15.6e} {dfx:>15.6e}")
            print(f"\nSe obtuvo una aproximación de P = {x_n} (f(x_n) = 0 exacto).")
            return x_n

        # Newton no se puede aplicar si f'(x_n) = 0 (recta tangente horizontal)
        if dfx == 0:
            print(f"{n:>3} {x_n:>18.10g} {fx:>15.6e} {dfx:>15.6e}")
            if abs(x_n) > 1e10:
                print(f"\nLa sucesión diverge (|x_n| = {abs(x_n):.3e}) y f'(x_n) se volvió 0 "
                      f"numéricamente. Pruebe con otro valor inicial x0.")
            else:
                print(f"\nf'(x_n) = 0 en x_n = {x_n}: la tangente es horizontal y el método "
                      f"no puede continuar. Pruebe con otro valor inicial x0.")
            return None

        x_n1 = x_n - fx / dfx
        if not math.isfinite(x_n1):
            print(f"\nEn la iteración n = {n} x_(n+1) no es finito: el método diverge.")
            return None

        e_n1 = abs(x_n1 - x_n)
        print(f"{n:>3} {x_n:>18.10f} {fx:>15.6e} {dfx:>15.6e} {x_n1:>18.10f} {e_n1:>15.6e}")

        if e_n1 < eps:
            print(f"\nSe obtuvo una aproximación de P ≈ {x_n1} en {n} iteración(es).")
            return x_n1

        x_n = x_n1

    print(f"\nDespués de M = {M} iteración(es) no se logró la precisión deseada.")
    return None


if __name__ == "__main__":
    # Ejemplo del cuaderno: f(x) = x^3 + 4x^2 - 10, f'(x) = 3x^2 + 8x, x0 = 1, hallar x4
    f = lambda x: x**3 + 4 * x**2 - 10
    df = lambda x: 3 * x**2 + 8 * x

    print("Ejemplo del cuaderno: x0 = 1, M = 4 (hasta x4)\n")
    newton_raphson(f, df, x0=1, eps=1e-12, M=4)

    print("\n\nMismo ejemplo con eps = 1e-8\n")
    newton_raphson(f, df, x0=1, eps=1e-8, M=50)
