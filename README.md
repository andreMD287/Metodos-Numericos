# Métodos Numéricos - Tareas de Análisis Numérico

Implementaciones en Python de los algoritmos vistos en clase. Cada tarea es un archivo
independiente que se puede ejecutar directamente (trae ejemplos al final) o importar desde
otro script.

## Requisitos

- Python 3.8 o superior. No se necesita instalar ninguna librería (solo se usa la
  biblioteca estándar).
- Los comandos se ejecutan **desde esta carpeta**, porque algunas tareas importan a otras
  (ver la tabla de dependencias).

## Ejecutar los ejemplos de cada tarea

```bash
python tarea1_biseccion.py
python tarea2_punto_fijo.py
python tarea3_regla_falsa.py
python tarea4_newton_raphson.py
python tarea5_secante.py
python tarea6_sustitucion_hacia_atras.py
python tarea7_lu.py
python tarea8_sustitucion_hacia_adelante.py
python tarea9_sistemas_lu.py
python tarea10_lup.py
```

Si en Windows los acentos o símbolos (≈, ´) salen mal en la consola, use:

```bash
python -X utf8 tarea1_biseccion.py
```

## Tareas

| Tarea | Archivo | Función principal | Depende de |
|---|---|---|---|
| 1 | `tarea1_biseccion.py` | `biseccion(f, a, b, eps, M)` | - |
| 2 | `tarea2_punto_fijo.py` | `punto_fijo(p0, g, eps, M)` | - |
| 3 | `tarea3_regla_falsa.py` | `regla_falsa(f, a0, b0, eps, M)` | - |
| 4 | `tarea4_newton_raphson.py` | `newton_raphson(f, df, x0, eps, M)` | - |
| 5 | `tarea5_secante.py` | `secante(f, x0, x1, eps, M)` | - |
| 6 | `tarea6_sustitucion_hacia_atras.py` | `sustitucion_hacia_atras(n, A, b)` | - |
| 7 | `tarea7_lu.py` | `factorizacion_lu(A)` | - |
| 8 | `tarea8_sustitucion_hacia_adelante.py` | `sustitucion_hacia_adelante(A, b)` | - |
| 9 | `tarea9_sistemas_lu.py` | `solucion_sistemas_lu(A, b)` | tareas 6, 7 y 8 |
| 10 | `tarea10_lup.py` | `lup(A, b)` | tareas 7 y 9 (y por tanto 6 y 8) |

Parámetros comunes: `f`, `g`, `df` son funciones de Python, `eps` es la tolerancia, `M` es el
número máximo de iteraciones. Todas las funciones imprimen el procedimiento paso a paso y
devuelven el resultado, o `None` si el método fracasa o la entrada no es válida.

## Uso con sus propios datos

Cree un archivo (por ejemplo `prueba.py`) en esta misma carpeta, o abra `python` en ella.

### Tareas 1 a 5: búsqueda de raíces

```python
import math
from tarea1_biseccion import biseccion
from tarea2_punto_fijo import punto_fijo, cero_por_punto_fijo
from tarea3_regla_falsa import regla_falsa
from tarea4_newton_raphson import newton_raphson
from tarea5_secante import secante

f = lambda x: x**3 + 4 * x**2 - 10
df = lambda x: 3 * x**2 + 8 * x

biseccion(f, 1, 2, eps=1e-6, M=50)                  # intervalo [a, b] con f(a) f(b) < 0
punto_fijo(1, math.cos, eps=1e-6, M=100)            # punto fijo de g(x) = cos(x), p0 = 1
cero_por_punto_fijo(1, lambda x: x - math.cos(x), 1e-6, 100)  # cero de f con g(x) = x - f(x)
regla_falsa(f, 1, 2, eps=1e-6, M=50)                # criterio de parada: error relativo
newton_raphson(f, df, x0=1, eps=1e-8, M=50)         # necesita la derivada f'
secante(f, 1, 2, eps=1e-8, M=50)                    # dos puntos iniciales x0 y x1
```

### Tareas 6 y 8: sistemas triangulares

```python
from tarea6_sustitucion_hacia_atras import sustitucion_hacia_atras
from tarea8_sustitucion_hacia_adelante import sustitucion_hacia_adelante

# Triangular superior (hacia atrás): se indica el tamaño n
sustitucion_hacia_atras(3, [[2, 1, -1], [0, 3, 2], [0, 0, 4]], [3, 12, 8])

# Triangular inferior (hacia adelante)
sustitucion_hacia_adelante([[1, 0, 0], [2, 1, 0], [-3, 3, 1]], [2, -2, 4])
```

La tarea 8 convierte los enteros a fracciones, así que el resultado sale exacto
(por ejemplo `7/6` en lugar de `1.1666...`). En la tarea 6 puede obtener el mismo efecto
escribiendo los datos como `Fraction(...)` (`from fractions import Fraction`).

### Tarea 7: factorización LU

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

Si algún `u_ii` es 0 durante la eliminación, imprime
`No se pudo factorizar de la forma LU` y devuelve `None` (en ese caso use la tarea 10).

### Tarea 9: sistemas con LU

```python
from tarea9_sistemas_lu import solucion_sistemas_lu

x = solucion_sistemas_lu(A, [16, 39, -10, -131])   # A de la tarea 7
```

Si no se puede factorizar o la matriz es singular, imprime
`No es posible hallar una solución única` y devuelve `None`.

### Tarea 10: método LUP (con pivoteo parcial)

```python
from tarea10_lup import lup

resultado = lup([[0, 2, 1], [1, 1, 1], [2, 1, 3]], [7, 6, 13])
if resultado is not None:
    x, P, L, U = resultado           # P A = L U
```

Funciona también cuando `a_11 = 0`, donde la tarea 9 falla. Imprime P, L, U, la
verificación `P A = L U` y la solución.

## Notas

- **Entradas válidas:** matrices como listas de listas (o tuplas) de números reales finitos:
  enteros, decimales o `Fraction`. Una entrada inválida (matriz no cuadrada, vector `b` de
  tamaño incorrecto, texto, `nan`, etc.) imprime un mensaje y devuelve `None`.
- **Salida reducida:** en las tareas 7, 9 y 10 use `mostrar=False` para no imprimir el
  procedimiento, útil con matrices grandes. Por ejemplo `lup(A, b, mostrar=False)`.
- **Enteros y fracciones:** en las tareas 7, 8, 9 y 10 los enteros se convierten a
  `Fraction`, por lo que los resultados son exactos. Si se usan decimales (`float`) los
  resultados son aproximados y el cero se compara de forma exacta, como en los algoritmos
  del cuaderno (sin tolerancia).
- **Tamaño:** probadas con matrices desde 1x1 hasta 300x300 (esta última tarda cerca de 1
  segundo con decimales).
