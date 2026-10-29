import sqlite3

NOMBRE_BD = "inventario.db"


def conectar(nombre_bd=NOMBRE_BD):
    """Abre la base de datos y crea la tabla si no existe."""
    conexion = sqlite3.connect(nombre_bd)
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            cantidad INTEGER NOT NULL CHECK (cantidad >= 0)
        )
        """
    )
    conexion.commit()
    return conexion


def registrar_producto(conexion, codigo, nombre, ubicacion, cantidad):
    """Guarda un producto nuevo. Falla si el codigo ya existe."""
    conexion.execute(
        "INSERT INTO productos (codigo, nombre, ubicacion, cantidad) "
        "VALUES (?, ?, ?, ?)",
        (codigo, nombre, ubicacion, cantidad),
    )
    conexion.commit()


def buscar_producto(conexion, codigo):
    """Devuelve los datos del producto, o None si no existe."""
    fila = conexion.execute(
        "SELECT codigo, nombre, ubicacion, cantidad "
        "FROM productos WHERE codigo = ?",
        (codigo,),
    ).fetchone()
    if fila is None:
        return None
    return {
        "codigo": fila[0],
        "nombre": fila[1],
        "ubicacion": fila[2],
        "cantidad": fila[3],
    }


def registrar_entrada(conexion, codigo, unidades):
    """Suma unidades a un producto que ya existe."""
    producto = buscar_producto(conexion, codigo)
    if producto is None:
        raise ValueError("Producto no encontrado")
    if unidades <= 0:
        raise ValueError("Las unidades deben ser mayores que 0")
    conexion.execute(
        "UPDATE productos SET cantidad = ? WHERE codigo = ?",
        (producto["cantidad"] + unidades, codigo),
    )
    conexion.commit()


def registrar_salida(conexion, codigo, unidades):
    """Resta unidades a un producto sin dejarlo en negativo."""
    producto = buscar_producto(conexion, codigo)
    if producto is None:
        raise ValueError("Producto no encontrado")
    if unidades <= 0:
        raise ValueError("Las unidades deben ser mayores que 0")
    if unidades > producto["cantidad"]:
        raise ValueError("No hay unidades suficientes")
    conexion.execute(
        "UPDATE productos SET cantidad = ? WHERE codigo = ?",
        (producto["cantidad"] - unidades, codigo),
    )
    conexion.commit()


def cambiar_ubicacion(conexion, codigo, nueva_ubicacion):
    """Mueve un producto a otro estante."""
    if buscar_producto(conexion, codigo) is None:
        raise ValueError("Producto no encontrado")
    conexion.execute(
        "UPDATE productos SET ubicacion = ? WHERE codigo = ?",
        (nueva_ubicacion, codigo),
    )
    conexion.commit()
