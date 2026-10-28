# Métodos Numéricos - Tareas de Análisis Numérico

Implementaciones en Python de los algoritmos vistos en clase. Cada tarea es un archivo
independiente que se puede ejecutar directamente (trae ejemplos al final) o importar desde
otro script.

## Requisitos

- Python 3.8 o superior. No se necesita instalar ninguna librería (solo se usa la
  biblioteca estándar).
- Los comandos se ejecutan **desde esta carpeta** (abra una terminal en ella), porque algunas
  tareas importan a otras (ver la tabla de dependencias).
- En Windows, si `python` no se reconoce, use `py` en su lugar (`py tarea1_biseccion.py`).
  Si los acentos o símbolos (≈) salen mal en la consola, use `python -X utf8 tarea1_biseccion.py`.

## Correr una tarea con los datos que da el profesor

La forma más fácil es el ejecutor interactivo `ejecutar.py`: pregunta los datos por teclado y
corre la tarea, sin tocar el código.

```bash
python ejecutar.py        # muestra el menú: escriba el número de la tarea (q para salir)
python ejecutar.py 4      # va directo a la tarea 4
```

Responda lo que le pregunta. Ejemplo con la tarea 4 (Newton-Raphson); lo que usted escribe es
lo que va después del `=`:

```text
f(x) = x^3 + 4x^2 - 10
f'(x) = 3x^2 + 8x
x0 (valor inicial) = 1
eps (tolerancia) = 1e-8
M (máximo de iteraciones) = 50
```

Ejemplo con la tarea 9 (sistema `A x = b` con LU): la matriz se escribe una fila por línea y
se termina con una línea vacía; luego se escribe el vector `b`:

```text
Matriz A: una fila por línea (números separados por espacios o comas).
  A[1] = 2 1 0 3
  A[2] = 4 6 1 5
  A[3] = -6 9 6 -10
  A[4] = 8 24 -1 -46
  A[5] =                                   <- línea vacía para terminar
b (números separados por espacios o comas) = 16 39 -10 -131
```

**Cómo escribir los datos:**

| Dato | Cómo escribirlo | Ejemplos |
|---|---|---|
| Función | en términos de `x`; vale `^` o `**` para potencias, `4x` o `4*x`, y un `f(x)=` al inicio | `x^3 + 4x^2 - 10`, `cos(x) - x`, `e^x - 2`, `(x+1)(x-1)` |
| Funciones disponibles | las de `math`: `sin`, `cos`, `tan`, `exp`, `log` (o `ln`), `sqrt`, `atan`, `abs`, ... y las constantes `pi`, `e` | `sqrt(x) - 1`, `sin(2x)` |
| Número | decimales con **punto** (no coma); se aceptan `1e-6`, `pi/2`, `3/4` | `0.001`, `1e-6`, `pi/4` |
| Vector | una línea con los números separados por espacios o comas | `16 39 -10 -131` |
| Matriz | una fila por línea y una línea vacía al final; también se acepta `[[2,1],[4,5]]` o `2 1; 4 5` en una sola línea | `2 1 0 3` |
| Fracciones | sin espacios; en matrices y vectores se conservan exactas | `3/4`, `-1/2` |

Si un dato está mal escrito, el programa lo dice y vuelve a preguntarlo. Con matrices de más
de 12 x 12 muestra solo el resultado, sin los pasos. Para cancelar use `Ctrl+C`.

## Otras formas de correr una tarea

**Ejecutar los ejemplos que trae el archivo.** Cada archivo termina con un bloque
`if __name__ == "__main__":` con ejemplos (casi todos tomados del cuaderno):

```bash
python tarea1_biseccion.py
```

**Cambiar el ejemplo por sus datos.** Abra el archivo, edite los datos dentro del bloque
`if __name__ == "__main__":` del final y vuelva a ejecutarlo con el mismo comando.

**Llamar la función desde un script.** Cree un archivo (por ejemplo `prueba.py`) en esta misma
carpeta, importe la función y ejecútelo con `python prueba.py`:

```python
from tarea1_biseccion import biseccion

p = biseccion(lambda x: x**3 + 4 * x**2 - 10, 1, 2, eps=1e-6, M=50)
print(p)
```

Todas las funciones imprimen el procedimiento paso a paso y devuelven el resultado, o `None` si
el método fracasa o la entrada no es válida.

## Resumen

| Tarea | Tema | Archivo | Función principal | Depende de |
|---|---|---|---|---|
| 1 | Bisección | `tarea1_biseccion.py` | `biseccion(f, a, b, eps, M)` | - |
| 2 | Punto fijo | `tarea2_punto_fijo.py` | `punto_fijo(p0, g, eps, M)` | - |
| 3 | Regla falsa | `tarea3_regla_falsa.py` | `regla_falsa(f, a0, b0, eps, M)` | - |
| 4 | Newton-Raphson | `tarea4_newton_raphson.py` | `newton_raphson(f, df, x0, eps, M)` | - |
| 5 | Secante | `tarea5_secante.py` | `secante(f, x0, x1, eps, M)` | - |
| 6 | Sustitución hacia atrás | `tarea6_sustitucion_hacia_atras.py` | `sustitucion_hacia_atras(n, A, b)` | - |
| 7 | Factorización LU | `tarea7_lu.py` | `factorizacion_lu(A)` | - |
| 8 | Sustitución hacia adelante | `tarea8_sustitucion_hacia_adelante.py` | `sustitucion_hacia_adelante(A, b)` | - |
| 9 | Sistemas con LU | `tarea9_sistemas_lu.py` | `solucion_sistemas_lu(A, b)` | tareas 6, 7 y 8 |
| 10 | Método LUP | `tarea10_lup.py` | `lup(A, b)` | tareas 7 y 9 (y por tanto 6 y 8) |
| 11 | Gauss-Seidel | `tarea11_gauss_seidel.py` | `gauss_seidel(A, b, x0, eps, M)` | tarea 7 |
| 12 | Sumas inferiores y superiores | `tarea12_sumas_inferiores_superiores.py` | `sumas_inferior_superior(f, a, b, n)` | - |
| 14 | Regla de Simpson compuesta | `tarea14_simpson_compuesto.py` | `simpson_compuesto(f, a, b, M)` | - |

Parámetros comunes: `f`, `g`, `df` son funciones de Python (por ejemplo `lambda x: x**2 - 2`),
`eps` es la tolerancia y `M` es el número máximo de iteraciones. Las matrices son listas de
listas y los vectores son listas.

---

## Tarea 1 - Bisección

**Con los datos del profesor:** `python ejecutar.py 1` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo** (problema del abrevadero):

```bash
python tarea1_biseccion.py
```

**Con sus datos:**

```python
from tarea1_biseccion import biseccion

f = lambda x: x**3 + 4 * x**2 - 10
p = biseccion(f, a=1, b=2, eps=1e-6, M=50)
```

Requiere `f(a)` y `f(b)` con signos opuestos. Devuelve la aproximación `p` de la raíz, o
`None` (con el mensaje de fracaso) si no se logra la tolerancia en `M` iteraciones.

## Tarea 2 - Punto fijo

**Con los datos del profesor:** `python ejecutar.py 2` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo** (`g(x) = x^3 - x` y `g(x) = cos(x)`):

```bash
python tarea2_punto_fijo.py
```

**Con sus datos:**

```python
import math
from tarea2_punto_fijo import punto_fijo, cero_por_punto_fijo

punto_fijo(1, math.cos, eps=1e-6, M=100)         # punto fijo de g(x) = cos(x), p0 = 1

# Cero de una función f usando g(x) = x - f(x)
cero_por_punto_fijo(1, lambda x: x - math.cos(x), 1e-6, 100)
```

Si la sucesión diverge o se sale del dominio de `g`, lo avisa y devuelve `None`.

## Tarea 3 - Regla falsa (posición falsa)

**Con los datos del profesor:** `python ejecutar.py 3` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo** (`f(x) = x^3 + 4x^2 - 10` en `[1, 2]`):

```bash
python tarea3_regla_falsa.py
```

**Con sus datos:**

```python
from tarea3_regla_falsa import regla_falsa

f = lambda x: x**3 + 4 * x**2 - 10
regla_falsa(f, a0=1, b0=2, eps=1e-6, M=50)
```

Requiere `f(a0) f(b0) < 0`. El criterio de parada es el error relativo.

## Tarea 4 - Newton-Raphson

**Con los datos del profesor:** `python ejecutar.py 4` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo:**

```bash
python tarea4_newton_raphson.py
```

**Con sus datos** (hay que dar también la derivada `df`):

```python
from tarea4_newton_raphson import newton_raphson

f = lambda x: x**3 + 4 * x**2 - 10
df = lambda x: 3 * x**2 + 8 * x
newton_raphson(f, df, x0=1, eps=1e-8, M=50)
```

Avisa si la derivada escrita no coincide con una derivada numérica, y falla con un mensaje
claro si `f'(x_n) = 0`.

## Tarea 5 - Secante

**Con los datos del profesor:** `python ejecutar.py 5` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo:**

```bash
python tarea5_secante.py
```

**Con sus datos** (dos puntos iniciales distintos):

```python
from tarea5_secante import secante

f = lambda x: x**3 + 4 * x**2 - 10
secante(f, x0=1, x1=2, eps=1e-8, M=50)
```

## Tarea 6 - Sustitución hacia atrás

**Con los datos del profesor:** `python ejecutar.py 6` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo:**

```bash
python tarea6_sustitucion_hacia_atras.py
```

**Con sus datos** (`A` triangular superior, se indica el tamaño `n`):

```python
from tarea6_sustitucion_hacia_atras import sustitucion_hacia_atras

A = [[2, 1, -1],
     [0, 3, 2],
     [0, 0, 4]]
x = sustitucion_hacia_atras(3, A, [3, 12, 8])
```

Si algún `a_ii = 0` dice que el sistema no tiene solución. Para resultados exactos escriba los
datos como `Fraction(...)` (`from fractions import Fraction`).

## Tarea 7 - Factorización LU

**Con los datos del profesor:** `python ejecutar.py 7` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo** (la matriz del ejemplo tiene |A| = -1176):

```bash
python tarea7_lu.py
```

**Con sus datos:**

```python
from tarea7_lu import factorizacion_lu

A = [[2, 1, 0, 3],
     [4, 6, 1, 5],
     [-6, 9, 6, -10],
     [8, 24, -1, -46]]

resultado = factorizacion_lu(A)      # imprime L, U y |A|
if resultado is not None:
    L, U = resultado
```

Si algún `u_ii` es 0 durante la eliminación, imprime `No se pudo factorizar de la forma LU` y
devuelve `None` (en ese caso use la tarea 10).

## Tarea 8 - Sustitución hacia adelante

**Con los datos del profesor:** `python ejecutar.py 8` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo del cuaderno** (resultado `x = (2, -6, 28, 79)`):

```bash
python tarea8_sustitucion_hacia_adelante.py
```

**Con sus datos** (`A` triangular inferior):

```python
from tarea8_sustitucion_hacia_adelante import sustitucion_hacia_adelante

A = [[1, 0, 0],
     [2, 1, 0],
     [-3, 3, 1]]
x = sustitucion_hacia_adelante(A, [2, -2, 4])
```

Los enteros se convierten a fracciones, así que el resultado sale exacto (por ejemplo `7/6` en
lugar de `1.1666...`).

## Tarea 9 - Sistemas con LU

**Con los datos del profesor:** `python ejecutar.py 9` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo:**

```bash
python tarea9_sistemas_lu.py
```

**Con sus datos** (resuelve `A x = b`):

```python
from tarea9_sistemas_lu import solucion_sistemas_lu

A = [[2, 1, 0, 3],
     [4, 6, 1, 5],
     [-6, 9, 6, -10],
     [8, 24, -1, -46]]
x = solucion_sistemas_lu(A, [16, 39, -10, -131])
```

Si no se puede factorizar o la matriz es singular, imprime
`No es posible hallar una solución única` y devuelve `None`.

## Tarea 10 - Método LUP (con pivoteo parcial)

**Con los datos del profesor:** `python ejecutar.py 10` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo:**

```bash
python tarea10_lup.py
```

**Con sus datos:**

```python
from tarea10_lup import lup

resultado = lup([[0, 2, 1],
                 [1, 1, 1],
                 [2, 1, 3]], [7, 6, 13])
if resultado is not None:
    x, P, L, U = resultado           # P A = L U
```

Funciona también cuando `a_11 = 0`, donde la tarea 9 falla. Imprime P, L, U, la verificación
`P A = L U` y la solución.

## Tarea 11 - Gauss-Seidel

**Con los datos del profesor:** `python ejecutar.py 11` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo** (solución exacta `x = (1, 2, -1, 1)`):

```bash
python tarea11_gauss_seidel.py
```

**Con sus datos:**

```python
from tarea11_gauss_seidel import gauss_seidel

A = [[10, -1, 2, 0],
     [-1, 11, -1, 3],
     [2, -1, 10, -1],
     [0, 3, -1, 8]]
b = [6, 25, -11, 15]

x = gauss_seidel(A, b, x0=[0, 0, 0, 0], eps=1e-8, M=100)
```

Se detiene cuando `||X - X0|| <= eps` (norma del máximo). Si no converge en `M` iteraciones, si
hay un `a_ii = 0` o si los valores divergen, imprime el mensaje de fracaso y devuelve `None`.
La convergencia está garantizada, por ejemplo, si `A` es diagonalmente dominante.

Gauss-Seidel usa los valores ya actualizados de la misma iteración. La fórmula del cuaderno se
lee con `X_j^0` para todos los `j`, lo que corresponde al método de Jacobi; para obtener esa
versión use `gauss_seidel(..., usar_valores_anteriores=True)`.

## Tarea 12 - Sumas inferiores y superiores

**Con los datos del profesor:** `python ejecutar.py 12` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo del cuaderno** (`x^2` en `[1, 5]`, `n = 8`, da `L = 35.5` y `U = 47.5`):

```bash
python tarea12_sumas_inferiores_superiores.py
```

**Con sus datos:**

```python
from tarea12_sumas_inferiores_superiores import sumas_inferior_superior

L, U = sumas_inferior_superior(lambda x: x**2, 1, 5, 8)
```

Calcula `L` y `U` con `n` particiones del intervalo `[a, b]` (se requiere `a < b`). El mínimo y
el máximo de cada subintervalo se toman entre sus dos extremos, así que `L <= integral <= U` se
cumple cuando `f` es monótona en cada subintervalo; si no, aumente `n`.

## Tarea 14 - Regla de Simpson compuesta

**Con los datos del profesor:** `python ejecutar.py 14` y escriba los datos cuando se los pida.

**Ejecutar el ejemplo del cuaderno** (`e^(-x^2)` en `[0, 2]` con `n = 8`, es decir `M = 4`):

```bash
python tarea14_simpson_compuesto.py
```

**Con sus datos:**

```python
import math
from tarea14_simpson_compuesto import simpson_compuesto

S = simpson_compuesto(lambda x: math.exp(-x**2), 0, 2, M=4)    # n = 2M = 8 subintervalos
```

La entrada es `M` y el número de subintervalos es `n = 2M` (siempre par): si le piden `n = 8`
use `M = 4`. Calcula `S(h) = (h/3)(S0 + 2 S2 + 4 S1)`, donde `S0 = f(a) + f(b)`, `S2` es la suma
de `f(x_i)` con `i` par y `S1` la suma con `i` impar. La regla es exacta para polinomios de grado
menor o igual a 3. Con el ejemplo del cuaderno da `0.88207` (el cuaderno anota `0.8819` porque la
cuenta a mano usa solo 4 decimales); el valor exacto de la integral es `0.88208`.

---

## Notas

- **Entradas válidas:** matrices como listas de listas (o tuplas) de números reales finitos:
  enteros, decimales o `Fraction`. Una entrada inválida (matriz no cuadrada, vector `b` de
  tamaño incorrecto, texto, `nan`, etc.) imprime un mensaje y devuelve `None`.
- **Salida reducida:** en las tareas 7, 9, 10, 11, 12 y 14 use `mostrar=False` para no imprimir el
  procedimiento, útil con matrices grandes. Por ejemplo `lup(A, b, mostrar=False)`.
- **Enteros y fracciones:** en las tareas 7, 8, 9 y 10 los enteros se convierten a `Fraction`,
  por lo que los resultados son exactos. Si se usan decimales (`float`) los resultados son
  aproximados y el cero se compara de forma exacta, como en los algoritmos del cuaderno (sin
  tolerancia).
- **Tamaño:** probadas con matrices desde 1x1 hasta 300x300 (esta última tarda cerca de 1
  segundo con decimales).
