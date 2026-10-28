"""
Ejecutor interactivo de las tareas: pide los datos por teclado y corre el algoritmo.

Uso (desde esta carpeta):
    python ejecutar.py          # muestra el menú de tareas
    python ejecutar.py 4        # va directo a la tarea 4

Cómo escribir los datos:
    Funciones : en términos de x, por ejemplo  x^3 + 4x^2 - 10   o   cos(x) - x
                (se aceptan ^, 4x, f(x)= al inicio y las funciones de math:
                 sin, cos, tan, exp, log, sqrt, pi, e, ...)
    Números   : 0.001   1e-6   2   pi/2   1/3        (decimales con PUNTO)
    Vectores  : una línea con los números separados por espacios o comas
    Matrices  : una fila por línea (números separados por espacios o comas) y una
                línea vacía para terminar. También se acepta [[2,1],[4,5]] o 2 1; 4 5.
                Escriba las fracciones sin espacios: 3/4
"""
import math
import numbers
import re
import sys
from fractions import Fraction

from tarea1_biseccion import biseccion
from tarea2_punto_fijo import cero_por_punto_fijo, punto_fijo
from tarea3_regla_falsa import regla_falsa
from tarea4_newton_raphson import newton_raphson
from tarea5_secante import secante
from tarea6_sustitucion_hacia_atras import sustitucion_hacia_atras
from tarea7_lu import factorizacion_lu
from tarea8_sustitucion_hacia_adelante import sustitucion_hacia_adelante
from tarea9_sistemas_lu import solucion_sistemas_lu
from tarea10_lup import lup
from tarea11_gauss_seidel import gauss_seidel
from tarea12_sumas_inferiores_superiores import sumas_inferior_superior
from tarea13_trapecio_compuesto import trapecio_compuesto
from tarea14_simpson_compuesto import simpson_compuesto

# Nombres permitidos al interpretar lo que se escribe (funciones y constantes de math)
NOMBRES = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
NOMBRES.update(ln=math.log, abs=abs, min=min, max=max, pow=pow, F=Fraction, Fraction=Fraction)

TAMANO_MAXIMO_CON_DETALLE = 12      # con matrices más grandes no se imprimen los pasos


class DatoInvalido(Exception):
    """El texto escrito no sirve como dato; se vuelve a preguntar."""


# ---------------------------------------------------------------------------
# Lectura y conversión de datos
# ---------------------------------------------------------------------------
def preparar_expresion(texto):
    """Pasa 'f(x) = x^3 + 4x^2' a código Python válido: 'x**3 + 4*x**2'."""
    t = re.sub(r"^\s*\w+\s*\(\s*x\s*\)\s*=", "", texto)     # quita el 'f(x) =' inicial
    t = t.strip().replace("^", "**").replace("−", "-")
    # multiplicación implícita: 4x -> 4*x, 2sin(x) -> 2*sin(x), (x+1)(x-1) -> (x+1)*(x-1)
    t = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?=(?![eE][+-]?\d)[A-Za-z(])", r"\1*", t)
    t = re.sub(r"\)\s*(?=[\w(])", ")*", t)
    return re.sub(r"(?<![\w.])x\s*(?=\()", "x*", t)


def crear_funcion(texto):
    """Convierte un texto en una función de x. Lanza DatoInvalido si está mal escrito."""
    expresion = preparar_expresion(texto)
    try:
        codigo = compile(expresion, "<funcion>", "eval")
    except SyntaxError:
        raise DatoInvalido(f"no se entiende la función «{texto}». Use * para multiplicar "
                           f"(4*x), ^ o ** para potencias y paréntesis en las funciones, p. ej. cos(x).")
    if any(hasattr(c, "co_code") for c in codigo.co_consts):      # lambda, comprensiones, ...
        raise DatoInvalido("escriba solo la expresión en x (por ejemplo x^2 - 2), sin lambda.")
    for nombre in codigo.co_names:
        if nombre != "x" and nombre not in NOMBRES:
            raise DatoInvalido(f"nombre desconocido «{nombre}»: use solo la variable x y las "
                               f"funciones de math (sin, cos, exp, log, sqrt, ...).")
    espacio = dict(NOMBRES)
    espacio["__builtins__"] = {}

    def f(x):
        espacio["x"] = x
        try:
            return eval(codigo, espacio)
        except (OverflowError, ZeroDivisionError, ValueError):
            raise
        except Exception as err:                    # TypeError, etc.: lo trata el algoritmo
            raise ValueError(str(err))

    return f


def convertir_numero(token):
    """'5' -> 5, '3/4' -> Fraction(3, 4), '1e-6' -> 1e-06, 'pi/2' -> 1.5707..."""
    t = token.strip().replace("^", "**").replace("−", "-")
    if re.fullmatch(r"[+-]?\d+", t):
        return int(t)
    if re.fullmatch(r"[+-]?\d+/\d+", t):
        numerador, denominador = t.split("/")
        if int(denominador) == 0:
            raise DatoInvalido(f"«{token}» tiene denominador 0.")
        return Fraction(int(numerador), int(denominador))
    try:
        valor = eval(t, {"__builtins__": {}}, dict(NOMBRES))
    except Exception:
        raise DatoInvalido(f"«{token}» no es un número (los decimales llevan punto, p. ej. 0.5).")
    if isinstance(valor, tuple):
        raise DatoInvalido(f"«{token}» no es un solo número (los decimales llevan punto, p. ej. 0.5).")
    if isinstance(valor, bool) or not isinstance(valor, numbers.Real) or not math.isfinite(valor):
        raise DatoInvalido(f"«{token}» no es un número real finito.")
    return valor


def convertir_fila(linea):
    """'2 1, 3/4' -> [2, 1, Fraction(3, 4)]"""
    fichas = [t for t in re.split(r"[,;\s]+", linea.strip().strip("[]")) if t]
    if not fichas:
        raise DatoInvalido("no escribió ningún número.")
    return [convertir_numero(t) for t in fichas]


def preguntar(texto, convertir):
    """Repite la pregunta hasta que el dato sea válido."""
    while True:
        respuesta = input(texto).strip()
        if not respuesta:
            continue
        try:
            return convertir(respuesta)
        except DatoInvalido as err:
            print(f"  Dato inválido: {err}")


def leer_funcion(nombre):
    return preguntar(f"{nombre}(x) = ", crear_funcion)


def leer_numero(nombre):
    return preguntar(f"{nombre} = ", convertir_numero)


def leer_entero(nombre):
    def convertir(texto):
        valor = convertir_numero(texto)
        if isinstance(valor, Fraction):
            valor = valor.numerator if valor.denominator == 1 else valor
        if isinstance(valor, float) and valor.is_integer():
            valor = int(valor)
        if not isinstance(valor, int) or valor < 1:
            raise DatoInvalido("debe ser un entero mayor o igual a 1.")
        return valor

    return preguntar(f"{nombre} = ", convertir)


def leer_vector(nombre):
    return preguntar(f"{nombre} (números separados por espacios o comas) = ", convertir_fila)


def matriz_desde_texto(texto):
    """Acepta '[[2,1],[4,5]]' o '2 1; 4 5' en una sola línea."""
    t = texto.strip()
    if t.startswith("[["):
        filas = [f for f in re.findall(r"\[([^\[\]]*)\]", t)]
    else:
        filas = [f for f in t.split(";") if f.strip()]
    return [convertir_fila(f) for f in filas]


def leer_matriz(nombre):
    print(f"Matriz {nombre}: una fila por línea (números separados por espacios o comas).")
    print("Línea vacía para terminar.")
    while True:
        filas = []
        try:
            while True:
                linea = input(f"  {nombre}[{len(filas) + 1}] = ").strip()
                if not linea:
                    if filas:
                        break
                    continue
                if "[[" in linea or ";" in linea:           # toda la matriz en una línea
                    filas = matriz_desde_texto(linea)
                    break
                filas.append(convertir_fila(linea))
            return filas
        except DatoInvalido as err:
            print(f"  Dato inválido: {err} Escriba la matriz otra vez.")


def mostrar_detalle(*matrices):
    """Con matrices grandes no se imprimen todos los pasos."""
    n = len(matrices[0])
    if n > TAMANO_MAXIMO_CON_DETALLE:
        print(f"(Matriz de {n} x {n}: se muestra solo el resultado, sin los pasos.)")
        return False
    return True


# ---------------------------------------------------------------------------
# Una función por tarea: pide los datos y llama al algoritmo
# ---------------------------------------------------------------------------
def tarea1():
    f = leer_funcion("f")
    a, b = leer_numero("a"), leer_numero("b")
    eps, M = leer_numero("eps (tolerancia)"), leer_entero("M (máximo de iteraciones)")
    print()
    return biseccion(f, a, b, eps, M)


def tarea2():
    print("  1) Punto fijo de una función g(x)")
    print("  2) Cero de una función f(x), usando g(x) = x - f(x)")
    def convertir_opcion(texto):
        if texto not in ("1", "2"):
            raise DatoInvalido("escriba 1 o 2.")
        return texto

    opcion = preguntar("Opción (1 o 2) = ", convertir_opcion)
    f = leer_funcion("g" if opcion == "1" else "f")
    p0 = leer_numero("p0 (punto inicial)")
    eps, M = leer_numero("eps (tolerancia)"), leer_entero("M (máximo de iteraciones)")
    print()
    return punto_fijo(p0, f, eps, M) if opcion == "1" else cero_por_punto_fijo(p0, f, eps, M)


def tarea3():
    f = leer_funcion("f")
    a0, b0 = leer_numero("a0"), leer_numero("b0")
    eps, M = leer_numero("eps (tolerancia)"), leer_entero("M (máximo de iteraciones)")
    print()
    return regla_falsa(f, a0, b0, eps, M)


def tarea4():
    f = leer_funcion("f")
    df = leer_funcion("f'")
    x0 = leer_numero("x0 (valor inicial)")
    eps, M = leer_numero("eps (tolerancia)"), leer_entero("M (máximo de iteraciones)")
    print()
    return newton_raphson(f, df, x0, eps, M)


def tarea5():
    f = leer_funcion("f")
    x0, x1 = leer_numero("x0"), leer_numero("x1")
    eps, M = leer_numero("eps (tolerancia)"), leer_entero("M (máximo de iteraciones)")
    print()
    return secante(f, x0, x1, eps, M)


def tarea6():
    A = leer_matriz("A (triangular superior)")
    b = leer_vector("b")
    print()
    return sustitucion_hacia_atras(len(A), A, b, mostrar=mostrar_detalle(A))


def tarea7():
    A = leer_matriz("A")
    print()
    return factorizacion_lu(A, mostrar=mostrar_detalle(A))


def tarea8():
    A = leer_matriz("A (triangular inferior)")
    b = leer_vector("b")
    print()
    return sustitucion_hacia_adelante(A, b, mostrar=mostrar_detalle(A))


def tarea9():
    A = leer_matriz("A")
    b = leer_vector("b")
    print()
    return solucion_sistemas_lu(A, b, mostrar=mostrar_detalle(A))


def tarea10():
    A = leer_matriz("A")
    b = leer_vector("b")
    print()
    return lup(A, b, mostrar=mostrar_detalle(A))


def tarea11():
    A = leer_matriz("A")
    b = leer_vector("b")
    x0 = leer_vector("x0 (valor inicial)")
    eps, M = leer_numero("eps (tolerancia)"), leer_entero("M (máximo de iteraciones)")
    print()
    return gauss_seidel(A, b, x0, eps, M, mostrar=mostrar_detalle(A))


def tarea12():
    f = leer_funcion("f")
    a, b = leer_numero("a"), leer_numero("b")
    n = leer_entero("n (número de particiones)")
    print()
    return sumas_inferior_superior(f, a, b, n, mostrar=n <= 50)


def tarea13():
    f = leer_funcion("f")
    a, b = leer_numero("a"), leer_numero("b")
    n = leer_entero("n (número de subintervalos)")
    print()
    return trapecio_compuesto(f, a, b, n, mostrar=n <= 50)


def tarea14():
    f = leer_funcion("f")
    a, b = leer_numero("a"), leer_numero("b")
    M = leer_entero("M (el número de subintervalos es n = 2M)")
    print()
    return simpson_compuesto(f, a, b, M, mostrar=M <= 25)


TAREAS = {
    1: ("Bisección", tarea1),
    2: ("Punto fijo", tarea2),
    3: ("Regla falsa", tarea3),
    4: ("Newton-Raphson", tarea4),
    5: ("Secante", tarea5),
    6: ("Sustitución hacia atrás", tarea6),
    7: ("Factorización LU", tarea7),
    8: ("Sustitución hacia adelante", tarea8),
    9: ("Sistemas con LU", tarea9),
    10: ("Método LUP", tarea10),
    11: ("Gauss-Seidel", tarea11),
    12: ("Sumas inferiores y superiores", tarea12),
    13: ("Regla compuesta del trapecio", tarea13),
    14: ("Regla de Simpson compuesta", tarea14),
}


def ejecutar_tarea(numero):
    nombre, funcion = TAREAS[numero]
    print(f"\n=== Tarea {numero}: {nombre} ===\n")
    try:
        funcion()
    except (KeyboardInterrupt, EOFError):
        raise
    except Exception as err:                        # un fallo no debe cerrar el programa
        print(f"\nOcurrió un error inesperado al ejecutar la tarea: {type(err).__name__}: {err}")


def lista_de_tareas():
    return ", ".join(str(n) for n in TAREAS)


def menu():
    print("\nTareas disponibles:")
    for numero, (nombre, _) in TAREAS.items():
        print(f"  {numero:>2}) {nombre}")


def principal(argumentos):
    try:
        if argumentos:
            try:
                numero = int(argumentos[0])
            except ValueError:
                numero = None
            if numero not in TAREAS:
                print(f"Use: python ejecutar.py [número de tarea: {lista_de_tareas()}]")
                return 1
            ejecutar_tarea(numero)
            return 0
        while True:
            menu()
            eleccion = input("\nNúmero de tarea (q para salir) = ").strip().lower()
            if eleccion in ("q", "salir"):
                return 0
            if eleccion.isdigit() and int(eleccion) in TAREAS:
                ejecutar_tarea(int(eleccion))
            elif eleccion:
                print(f"Escriba un número de la lista ({lista_de_tareas()}), o q para salir.")
    except (KeyboardInterrupt, EOFError):
        print("\nSe canceló la ejecución.")
        return 0


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
