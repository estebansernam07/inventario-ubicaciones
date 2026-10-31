# Sistema de Inventario con Ubicaciones

Programa de consola que guarda los productos de un local con un **código único** y una **ubicación específica**. Al buscar un producto, el sistema responde una de dos cosas:

- **No hay nada en el sistema** con ese código.
- **Sí hay**, y dice en qué ubicación está y cuántas unidades quedan.

Proyecto del taller *Plan de calidad, pruebas y despliegue*.

- **Autor:** Esteban Serna Muñoz
- **Versión actual:** 1.0.0

## Funciones

| Opción del menú | Función |
|---|---|
| 1 | Registrar un producto (código, nombre, ubicación, cantidad) |
| 2 | Buscar un producto por código |
| 3 | Registrar una entrada (suma unidades) |
| 4 | Registrar una salida (resta unidades, sin dejar negativos) |
| 5 | Cambiar la ubicación de un producto |
| 0 | Salir |

## Tecnologías

- Python 3.12 o superior
- SQLite 3 (incluida con Python)
- pytest y Coverage.py para pruebas y cobertura
- Git y GitHub para versiones

## Requisitos mínimos

- Windows 10 de 64 bits
- 4 GB de RAM
- 500 MB de espacio libre
- Python 3.12 o superior
- Git 2.40 o superior

## Instalación

```bash
git clone https://github.com/estebansernam07/inventario-ubicaciones.git
cd inventario-ubicaciones
pip install pytest coverage
```

## Uso

```bash
python main.py
```

Se abre el menú **INVENTARIO CON UBICACIONES**. Escribe el número de la opción y presiona Enter. La base de datos `inventario.db` se crea sola la primera vez.

## Pruebas

```bash
python -m pytest
```

Resultado esperado: **11 passed**.

Cobertura:

```bash
python -m coverage run -m pytest
python -m coverage report --include="inventario.py"
```

Resultado esperado: **100 %** (meta del proyecto: 80 % o más).

## Estructura del proyecto

```
inventario-ubicaciones/
├── inventario.py        # Lógica y acceso a la base de datos
├── main.py              # Menú de consola
├── test_inventario.py   # Pruebas automáticas (pytest)
├── CHANGELOG.md         # Historial de versiones
├── docs/
│   ├── manual_tecnico.md
│   └── manual_usuario.pdf
└── .gitignore
```

## Ramas

- `main`: versión estable.
- `develop`: trabajo en curso.
- `feature/*`: una rama por cada función nueva.

## Soporte

Los errores se reportan en la pestaña **Issues** del repositorio, con ID, fecha, quién reporta, qué pasó, pasos para repetirlo, resultado esperado y severidad.

## Documentación

- [Historial de cambios](CHANGELOG.md)
- [Manual técnico](docs/manual_tecnico.md)
- [Manual de usuario (PDF)](docs/manual_usuario.pdf)
