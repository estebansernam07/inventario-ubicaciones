import sqlite3

from inventario import (
    buscar_producto,
    cambiar_ubicacion,
    conectar,
    registrar_entrada,
    registrar_producto,
    registrar_salida,
)

MENU = """
=== INVENTARIO CON UBICACIONES ===
1. Registrar producto
2. Buscar producto
3. Registrar entrada
4. Registrar salida
5. Cambiar ubicacion
0. Salir
"""


def pedir_texto(mensaje):
    """Pide un texto y lo devuelve en mayusculas, sin espacios sobrantes."""
    return input(mensaje).strip().upper()


def pedir_numero(mensaje):
    """Pide un numero entero (0 o mayor) hasta que lo escriban bien."""
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit():
            return int(texto)
        print("Escribe un numero entero, por favor.")


def opcion_registrar(conexion):
    codigo = pedir_texto("Codigo del producto: ")
    nombre = input("Nombre del producto: ").strip()
    ubicacion = pedir_texto("Ubicacion (por ejemplo A-3): ")
    cantidad = pedir_numero("Cantidad inicial: ")
    registrar_producto(conexion, codigo, nombre, ubicacion, cantidad)
    print("Producto registrado.")


def opcion_buscar(conexion):
    codigo = pedir_texto("Codigo a buscar: ")
    producto = buscar_producto(conexion, codigo)
    if producto is None:
        print("No hay nada en el sistema con el codigo " + codigo + ".")
    else:
        print(
            "El producto "
            + producto["codigo"]
            + " ("
            + producto["nombre"]
            + ") esta en la ubicacion "
            + producto["ubicacion"]
            + " y hay "
            + str(producto["cantidad"])
            + " unidades."
        )


def opcion_entrada(conexion):
    codigo = pedir_texto("Codigo del producto: ")
    unidades = pedir_numero("Unidades que entran: ")
    registrar_entrada(conexion, codigo, unidades)
    print("Entrada registrada.")


def opcion_salida(conexion):
    codigo = pedir_texto("Codigo del producto: ")
    unidades = pedir_numero("Unidades que salen: ")
    registrar_salida(conexion, codigo, unidades)
    print("Salida registrada.")


def opcion_ubicacion(conexion):
    codigo = pedir_texto("Codigo del producto: ")
    nueva = pedir_texto("Nueva ubicacion: ")
    cambiar_ubicacion(conexion, codigo, nueva)
    print("Ubicacion actualizada.")


OPCIONES = {
    "1": opcion_registrar,
    "2": opcion_buscar,
    "3": opcion_entrada,
    "4": opcion_salida,
    "5": opcion_ubicacion,
}


def main():
    conexion = conectar()
    while True:
        print(MENU)
        opcion = input("Elige una opcion: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        accion = OPCIONES.get(opcion)
        if accion is None:
            print("Opcion no valida.")
            continue
        try:
            accion(conexion)
        except sqlite3.IntegrityError:
            print("Ese codigo ya existe en el sistema.")
        except ValueError as error:
            print(error)
    conexion.close()


if __name__ == "__main__":
    main()
