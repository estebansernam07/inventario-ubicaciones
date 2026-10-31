# Manual técnico - Sistema de Inventario con Ubicaciones

Versión 1.0.0. Dirigido a quien deba mantener o ampliar el código.

## 1. Arquitectura

El sistema tiene dos capas:

| Archivo | Responsabilidad |
|---|---|
| `inventario.py` | Lógica de negocio y acceso a SQLite. No pide datos ni imprime. |
| `main.py` | Menú de consola. Pide datos al usuario y llama a `inventario.py`. |
| `test_inventario.py` | Pruebas automáticas de la lógica. |

Separar la lógica del menú permite probar las funciones sin escribir en consola, lo que facilita la mantenibilidad.

## 2. Base de datos

Motor: SQLite 3. Archivo: `inventario.db` (se crea solo; no se sube a GitHub).

Tabla `productos`:

| Columna | Tipo | Restricción |
|---|---|---|
| `codigo` | TEXT | Clave primaria (no se repite) |
| `nombre` | TEXT | Obligatorio |
| `ubicacion` | TEXT | Obligatorio |
| `cantidad` | INTEGER | Obligatorio, `CHECK (cantidad >= 0)` |

La restricción `CHECK` impide guardar cantidades negativas aunque falle la validación del código.

## 3. Funciones de `inventario.py`

| Función | Qué hace | Errores |
|---|---|---|
| `conectar(nombre_bd)` | Abre la base y crea la tabla si no existe. Devuelve la conexión. | - |
| `registrar_producto(conexion, codigo, nombre, ubicacion, cantidad)` | Guarda un producto nuevo. | Falla si el código ya existe. |
| `buscar_producto(conexion, codigo)` | Devuelve un diccionario con los datos, o `None` si no existe. | - |
| `registrar_entrada(conexion, codigo, unidades)` | Suma unidades. | `ValueError`: producto no encontrado; unidades menores o iguales a 0. |
| `registrar_salida(conexion, codigo, unidades)` | Resta unidades. | `ValueError`: producto no encontrado; unidades menores o iguales a 0; no hay unidades suficientes. |
| `cambiar_ubicacion(conexion, codigo, nueva_ubicacion)` | Mueve el producto a otro estante. | `ValueError`: producto no encontrado. |

Todas las consultas usan parámetros (`?`) en lugar de concatenar texto, lo que evita inyección SQL.

## 4. Pruebas

Herramientas: pytest y Coverage.py.

```bash
python -m pytest
python -m coverage run -m pytest
python -m coverage report --include="inventario.py"
```

Resultados de la versión 1.0.0: 11 pruebas aprobadas y 100 % de cobertura (38 líneas, 0 sin cubrir).

| Métrica | Umbral | Resultado |
|---|---|---|
| M-01 Exactitud de la búsqueda | 100 % | 100 % |
| M-02 Consistencia de cantidades | 100 % | 100 % |
| M-03 Cobertura de pruebas | 80 % o más | 100 % |

## 5. Cómo agregar una función nueva

1. Crear la solicitud de cambio en GitHub Issues.
2. Crear la rama: `git checkout -b feature/nombre-de-la-funcion`.
3. Escribir primero la prueba en `test_inventario.py`, luego la función en `inventario.py`.
4. Si hace falta, agregar la opción al menú en `main.py`.
5. Correr `python -m pytest` hasta ver todo en verde.
6. Unir a `develop`, luego a `main`, y subir la etiqueta de versión (por ejemplo `v1.1.0`).
7. Anotar el cambio en `CHANGELOG.md`.

## 6. Flujo de ramas y versiones

- `main`: versión estable, con etiquetas (`v1.0.0`).
- `develop`: integración.
- `feature/*`: cada función nueva.

## 7. Reversión

```bash
copy inventario.db inventario_respaldo.db
git tag
git checkout v1.0.0
python -m pytest
```

Para volver a la última versión: `git checkout main`.
