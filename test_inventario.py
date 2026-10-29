import pytest

from inventario import (
    buscar_producto,
    cambiar_ubicacion,
    conectar,
    registrar_entrada,
    registrar_producto,
    registrar_salida,
)


@pytest.fixture
def bodega():
    """Una base de datos en memoria, nueva y vacia para cada prueba."""
    conexion = conectar(":memory:")
    yield conexion
    conexion.close()


@pytest.fixture
def bodega_con_p001(bodega):
    """La bodega con el producto P-001 ya registrado."""
    registrar_producto(bodega, "P-001", "Tornillo", "A-3", 25)
    return bodega


# ---------- Casos de prueba del plan (CP-01 a CP-04) ----------

def test_cp01_buscar_producto_existente(bodega_con_p001):
    producto = buscar_producto(bodega_con_p001, "P-001")
    assert producto["ubicacion"] == "A-3"
    assert producto["cantidad"] == 25


def test_cp02_buscar_producto_inexistente(bodega_con_p001):
    assert buscar_producto(bodega_con_p001, "P-999") is None


def test_cp03_registrar_salida(bodega_con_p001):
    registrar_salida(bodega_con_p001, "P-001", 5)
    assert buscar_producto(bodega_con_p001, "P-001")["cantidad"] == 20


def test_cp04_guardar_en_sqlite(tmp_path):
    archivo = str(tmp_path / "prueba.db")

    conexion = conectar(archivo)
    registrar_producto(conexion, "P-002", "Tuerca", "A-4", 10)
    conexion.close()

    # Se abre de nuevo, como si se reiniciara el programa
    conexion = conectar(archivo)
    producto = buscar_producto(conexion, "P-002")
    conexion.close()

    assert producto["ubicacion"] == "A-4"
    assert producto["cantidad"] == 10


# ---------- Pruebas adicionales (metricas M-02 y M-03) ----------

def test_registrar_entrada(bodega_con_p001):
    registrar_entrada(bodega_con_p001, "P-001", 10)
    assert buscar_producto(bodega_con_p001, "P-001")["cantidad"] == 35


def test_salida_mayor_que_existencias_no_cambia_la_cantidad(bodega_con_p001):
    with pytest.raises(ValueError):
        registrar_salida(bodega_con_p001, "P-001", 100)
    assert buscar_producto(bodega_con_p001, "P-001")["cantidad"] == 25


def test_salida_de_producto_inexistente(bodega):
    with pytest.raises(ValueError):
        registrar_salida(bodega, "P-999", 1)


def test_entrada_de_producto_inexistente(bodega):
    with pytest.raises(ValueError):
        registrar_entrada(bodega, "P-999", 1)


def test_unidades_deben_ser_mayores_que_cero(bodega_con_p001):
    with pytest.raises(ValueError):
        registrar_entrada(bodega_con_p001, "P-001", 0)
    with pytest.raises(ValueError):
        registrar_salida(bodega_con_p001, "P-001", 0)


def test_cambiar_ubicacion(bodega_con_p001):
    cambiar_ubicacion(bodega_con_p001, "P-001", "B-2")
    assert buscar_producto(bodega_con_p001, "P-001")["ubicacion"] == "B-2"


def test_cambiar_ubicacion_de_producto_inexistente(bodega):
    with pytest.raises(ValueError):
        cambiar_ubicacion(bodega, "P-999", "B-2")
