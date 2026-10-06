"""
Tarea 1 - Algoritmo de Bisección

Entrada:
    f   : función
    a, b: extremos del intervalo
    eps : precisión deseada (tolerancia)
    M   : máximo de iteraciones
Salida:
    Éxito  : "Se encontró una aproximación a la raíz de la función con tolerancia deseada (p_i)"
    Fracaso: "No se encontró una raíz a la función con la tolerancia deseada y número de iteraciones"
"""
import math


def signo(x):
    """Devuelve 1, -1 o 0. Se usa en lugar de f(a)*f(p) para evitar
    que el producto se vuelva 0 por underflow con valores muy pequeños."""
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def biseccion(f, a, b, eps, M):
    # Validación de la entrada
    if eps <= 0 or M < 1:
        print("La tolerancia debe ser positiva y M debe ser al menos 1.")
        return None
    if a > b:
        a, b = b, a                  # se ordena el intervalo

    fa = f(a)
    fb = f(b)

    # Si un extremo ya es raíz, se devuelve directamente
    if fa == 0:
        print(f"Se encontró una aproximación a la raíz de la función con tolerancia deseada: p = {a}")
        return a
    if fb == 0:
        print(f"Se encontró una aproximación a la raíz de la función con tolerancia deseada: p = {b}")
        return b

    # Condición necesaria: f(a) y f(b) con signos opuestos
    if signo(fa) == signo(fb):
        print("f(a) y f(b) tienen el mismo signo: el método no se puede aplicar en [a, b].")
        return None

    print(f"{'i':>3} {'a':>12} {'b':>12} {'p_i':>12} {'f(p_i)':>14} {'(b-a)/2':>12}")

    i = 1
    while i <= M:
        p = a + (b - a) / 2          # punto medio
        fp = f(p)
        error = (b - a) / 2

        print(f"{i:>3} {a:>12.6f} {b:>12.6f} {p:>12.6f} {fp:>14.6e} {error:>12.6f}")

        # Criterio de parada
        if fp == 0 or error < eps:
            print(f"\nSe encontró una aproximación a la raíz de la función "
                  f"con tolerancia deseada: p_{i} = {p}")
            return p

        # Escoger el subintervalo donde está la raíz
        if signo(fa) == signo(fp):
            a = p
            fa = fp
        else:
            b = p

        i += 1

    print(f"\nNo se encontró una raíz a la función con la tolerancia deseada "
          f"y número de iteraciones (M = {M}).")
    return None


if __name__ == "__main__":
    # Ejemplo: abrevadero (Cap. 2, Ej. 15) con L = 10, r = 1, V = 12.4
    def f(h):
        return 12.4 - 5 * math.pi + 10 * math.asin(h) + 10 * h * math.sqrt(1 - h**2)

    h = biseccion(f, a=0, b=1, eps=0.01, M=20)
    if h is not None:
        print(f"Profundidad del agua = r - h = {1 - h:.4f} pies")
