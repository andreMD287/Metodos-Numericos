"""
Tarea 2 - Algoritmo de Punto Fijo

Entrada:
    p0  : punto inicial
    g   : función
    eps : precisión deseada
    M   : número máximo de iteraciones
Salida:
    Éxito  : "Se obtuvo la aproximación al punto fijo P"
    Fracaso: "Después de M iteraciones no se logró la precisión deseada"

Iteraciones:
    Para n = 0, 1, 2, ...
        x_{n+1} = g(x_n)
        e_{n+1} = |x_{n+1} - x_n|
        Si e_{n+1} < eps  -> Salida (Éxito), x_{n+1} ≈ P. PARE
        Si se llega a M iteraciones -> Salida (Fracaso). PARE

OJO: sirve para
    1) Punto fijo de una función g
    2) Cero de una función f, usando g(x) = x - f(x)
"""
import math


def punto_fijo(p0, g, eps, M):
    # Validación de la entrada
    if eps <= 0:
        print("La precisión deseada (eps) debe ser positiva.")
        return None
    if M < 1 or int(M) != M:
        print("M debe ser un entero mayor o igual a 1.")
        return None

    print(f"{'n':>3} {'x_n':>20} {'g(x_n) = x_(n+1)':>20} {'|x_(n+1) - x_n|':>18}")

    x_n = p0
    for n in range(int(M)):          # n = 0, 1, ..., M-1  ->  M iteraciones
        # x_{n+1} = g(x_n), protegido contra errores de dominio y desbordamiento
        try:
            x_n1 = g(x_n)
        except (ValueError, OverflowError, ZeroDivisionError) as err:
            print(f"\nEn la iteración {n + 1} no se pudo evaluar g({x_n}): {err}.")
            print(f"Después de {n} iteración(es) no se logró la precisión deseada "
                  "(la sucesión se salió del dominio de g o diverge).")
            return None

        if isinstance(x_n1, complex) or not math.isfinite(x_n1):
            print(f"{n:>3} {x_n:>20.10g} {str(x_n1):>20}")
            print(f"\nEn la iteración {n + 1} g(x_n) dio un valor no real o infinito.")
            print(f"Después de {n + 1} iteración(es) no se logró la precisión deseada "
                  "(la sucesión diverge o sale de los números reales).")
            return None

        e_n1 = abs(x_n1 - x_n)
        print(f"{n:>3} {x_n:>20.10g} {x_n1:>20.10g} {e_n1:>18.6e}")

        if e_n1 < eps:
            print(f"\nSe obtuvo la aproximación al punto fijo P ≈ {x_n1} "
                  f"en {n + 1} iteración(es).")
            return x_n1

        x_n = x_n1

    print(f"\nDespués de M = {M} iteraciones no se logró la precisión deseada.")
    return None


def cero_por_punto_fijo(p0, f, eps, M):
    """Caso 2 del OJO: cero de f usando g(x) = x - f(x)."""
    return punto_fijo(p0, lambda x: x - f(x), eps, M)


if __name__ == "__main__":
    # Ejemplo del cuaderno: g(x) = x^3 - x con x0 = 2, 4 iteraciones
    print("Ejemplo del cuaderno: g(x) = x^3 - x, x0 = 2, M = 4\n")
    punto_fijo(2, lambda x: x**3 - x, eps=1e-5, M=4)

    # Ejemplo que sí converge: g(x) = cos(x), x0 = 1
    print("\n\nEjemplo convergente: g(x) = cos(x), x0 = 1\n")
    punto_fijo(1, math.cos, eps=1e-5, M=100)
