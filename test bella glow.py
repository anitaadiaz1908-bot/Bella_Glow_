import unittest

from bella_glow import Inventario, Producto


class PruebasBellaGlow(unittest.TestCase):
    def setUp(self):
        self.inventario = Inventario(":memory:")
        self.labial = self.inventario.registrar_producto(
            Producto("Labial mate", "Vogue", 25000, 10)
        )

    def test_registrar_producto(self):
        self.assertEqual(len(self.inventario.listar_productos()), 1)

    def test_no_registra_producto_sin_nombre(self):
        with self.assertRaises(ValueError):
            self.inventario.registrar_producto(Producto("", "Vogue", 25000, 5))

    def test_venta_descuenta_stock(self):
        self.inventario.registrar_venta(self.labial.id_producto, 3)
        producto = self.inventario.obtener_producto(self.labial.id_producto)
        self.assertEqual(producto.cantidad, 7)

    def test_no_vende_sin_stock_suficiente(self):
        with self.assertRaises(ValueError):
            self.inventario.registrar_venta(self.labial.id_producto, 20)


if __name__ == "__main__":
    unittest.main()
