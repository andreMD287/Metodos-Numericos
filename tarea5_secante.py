"""
Tarea 5 - Algoritmo de la Secante

Entrada:
    f      : función
    x0, x1 : puntos iniciales
    eps    : precisión deseada
    M      : máximo de iteraciones
Salida:
    Éxito  : "Se halla una aproximación de la raíz de f"
    Fracaso: "Después de M iteraciones no se encontró una aproximación con la precisión deseada"

Iteraciones:
    Para n = 1, 2, ..., M (mientras n <= M)
        x_{n+1} = (x_{n-1} f(x_n) - x_n f(x_{n-1})) / (f(x_n) - f(x_{n-1}))
        e_{n+1} = |(x_{n+1} - x_n) / x_{n+1}|
        Si e_{n+1} < eps, entonces Salida (Éxito). PARE
    Si n = M + 1, entonces Salida (Fracaso). PARE

Nota: el uso de e_{n+1} como criterio de detención no obedece a algún motivo en particular.
"""
import math


def evaluar(f, x):
    """Evalúa f(x) y verifica que el resultado sea un número real finito."""
    try:
        y = f(x)
    except (ValueError, OverflowError, ZeroDivisionError) as err:
        raise ValueError(f"no se pudo evaluar f({x}): {err}")
    if isinstance(y, complex) or not math.isfinite(y):
        raise ValueError(f"f({x}) = {y} no es un número real finito")
    return y


def secante(f, x0, x1, eps, M):
    # ---------- Validación de la entrada ----------
    if eps <= 0:
        print("La precisión deseada (eps) debe ser positiva.")
        return None
    if M < 1 or int(M) != M:
        print("M debe ser un entero mayor o igual a 1.")
        return None
    if x0 == x1:
        print("x0 y x1 deben ser distintos (se necesitan dos puntos para trazar la secante).")
        return None

    try:
        f0 = evaluar(f, x0)
        f1 = evaluar(f, x1)
    except ValueError as err:
        print(f"Error en los puntos iniciales: {err}.")
        return None

    # Si un punto inicial ya es raíz, se devuelve directamente
    if f0 == 0:
        print(f"Se halla una aproximación de la raíz de f: x = {x0} (f(x0) = 0).")
        return x0
    if f1 == 0:
        print(f"Se halla una aproximación de la raíz de f: x = {x1} (f(x1) = 0).")
        return x1

    print(f"{'n':>3} {'x_(n-1)':>18} {'x_n':>18} {'f(x_n)':>14} {'x_(n+1)':>18} "
          f"{'|(x_(n+1)-x_n)/x_(n+1)|':>24}")

    x_ant, x_n = x0, x1              # x_{n-1}, x_n
    f_ant, f_n = f0, f1              # f(x_{n-1}), f(x_n)

    n = 1
    while n <= M:
        # Si f(x_n) = f(x_{n-1}) la secante es horizontal: no corta al eje x
        if f_n == f_ant:
            if abs(x_n) > 1e10:
                print(f"\nEn n = {n}: la sucesión diverge (|x_n| = {abs(x_n):.3e}) y "
                      f"f(x_n) = f(x_(n-1)) numéricamente. Pruebe con otros puntos iniciales.")
            else:
                print(f"\nEn n = {n}: f(x_n) = f(x_(n-1)) = {f_n}. La secante es horizontal "
                      f"y el método no puede continuar. Pruebe con otros puntos iniciales.")
            return None

        x_sig = (x_ant * f_n - x_n * f_ant) / (f_n - f_ant)
        x_sig = x_sig + 0.0            # convierte -0.0 en 0.0

        try:
            f_sig = evaluar(f, x_sig)
        except ValueError as err:
            print(f"\nError en la iteración n = {n}: {err}.")
            print("La sucesión se salió del dominio de f o diverge.")
            return None

        if x_sig != 0:
            e_sig = abs((x_sig - x_n) / x_sig)
            texto_error = f"{e_sig:.6e}"
        else:
            e_sig = None             # no se puede dividir por x_{n+1} = 0
            texto_error = "---- (x_(n+1)=0)"

        print(f"{n:>3} {x_ant:>18.10f} {x_n:>18.10f} {f_n:>14.6e} {x_sig:>18.10f} "
              f"{texto_error:>24}")

        # Criterio de parada
        if e_sig is not None and e_sig < eps:
            print(f"\nSe halla una aproximación de la raíz de f: x ≈ {x_sig} "
                  f"(n = {n}, f(x) = {f_sig:.3e}).")
            return x_sig

        # Si x_{n+1} es raíz exacta no hace falta seguir
        if f_sig == 0:
            print(f"\nSe halla una aproximación de la raíz de f: x = {x_sig} "
                  f"(f(x) = 0 exacto, n = {n}).")
            return x_sig

        # Se corren los puntos: (x_{n-1}, x_n) <- (x_n, x_{n+1})
        x_ant, f_ant = x_n, f_n
        x_n, f_n = x_sig, f_sig
        n += 1

    # n = M + 1
    print(f"\nDespués de M = {M} iteración(es) no se encontró una aproximación "
          f"con la precisión deseada.")
    return None


if __name__ == "__main__":
    # Ejemplo del libro (Burden, sección 2.3): f(x) = cos x - x, x0 = 0.5, x1 = pi/4
    print("Ejemplo: f(x) = cos(x) - x, x0 = 0.5, x1 = pi/4\n")
    secante(lambda x: math.cos(x) - x, 0.5, math.pi / 4, eps=1e-10, M=50)

    # Mismo polinomio de las tareas anteriores
    print("\n\nEjemplo: f(x) = x^3 + 4x^2 - 10, x0 = 1, x1 = 2\n")
    secante(lambda x: x**3 + 4 * x**2 - 10, 1, 2, eps=1e-10, M=50)
