# Historial de cambios

Todos los cambios importantes del proyecto se registran aquí. El versionado sigue SemVer (MAYOR.MENOR.PARCHE).

## [1.0.0] - 2026-10-31

Primera versión estable.

### Agregado
- Base de datos SQLite con la tabla `productos` (código, nombre, ubicación, cantidad).
- Registro de productos con código único.
- Búsqueda por código: responde "No hay nada en el sistema" o muestra ubicación y cantidad.
- Entradas y salidas de unidades, sin permitir cantidades negativas.
- Cambio de ubicación de un producto.
- Menú de consola (`main.py`).
- 11 pruebas automáticas con pytest y cobertura del 100 %.
- Archivo `.gitignore`.
- Documentación: README, CHANGELOG, manual técnico y manual de usuario.

## Plan de versiones

- **PARCHE** (1.0.x): corrección de un error pequeño.
- **MENOR** (1.x.0): una función nueva.
- **MAYOR** (x.0.0): cambios que rompen lo anterior.
