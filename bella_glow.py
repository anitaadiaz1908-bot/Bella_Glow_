"""
Bella Glow - Sistema de inventario y ventas
Primer incremento: registrar productos de maquillaje y registrar ventas
descontando el stock automaticamente.

Autora: Ana Maria Diaz
"""

import sqlite3

BASE_DATOS = "bella_glow.db"


class Producto:
    def __init__(self, nombre, marca, precio, cantidad, id_producto=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.marca = marca
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return (f"{self.id_producto}. {self.nombre} ({self.marca}) - "
                f"${self.precio:,.0f} - disponibles: {self.cantidad}")


class Inventario:
    def __init__(self, ruta_bd=BASE_DATOS):
        self.conexion = sqlite3.connect(ruta_bd)
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                marca TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                total REAL NOT NULL,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )
        """)
        self.conexion.commit()

    # HU-01: registrar productos de maquillaje
    def registrar_producto(self, producto):
        if not producto.nombre.strip() or not producto.marca.strip():
            raise ValueError("El nombre y la marca son obligatorios.")
        if producto.precio <= 0 or producto.cantidad < 0:
            raise ValueError("El precio debe ser mayor a 0 y la cantidad no puede ser negativa.")
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, marca, precio, cantidad) VALUES (?, ?, ?, ?)",
            (producto.nombre.strip(), producto.marca.strip(), producto.precio, producto.cantidad),
        )
        self.conexion.commit()
        producto.id_producto = cursor.lastrowid
        return producto

    def buscar_producto(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT nombre, marca, precio, cantidad, id FROM productos WHERE nombre LIKE ?",
            (f"%{nombre}%",),
        )
        return [Producto(*fila) for fila in cursor.fetchall()]

    def obtener_producto(self, id_producto):
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT nombre, marca, precio, cantidad, id FROM productos WHERE id = ?",
            (id_producto,),
        )
        fila = cursor.fetchone()
        return Producto(*fila) if fila else None

    def listar_productos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT nombre, marca, precio, cantidad, id FROM productos ORDER BY id")
        return [Producto(*fila) for fila in cursor.fetchall()]

    # HU-02: registrar una venta y descontar el stock
    def registrar_venta(self, id_producto, cantidad):
        producto = self.obtener_producto(id_producto)
        if producto is None:
            raise ValueError("El producto no existe.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if cantidad > producto.cantidad:
            raise ValueError(f"No hay stock suficiente. Disponibles: {producto.cantidad}.")
        total = producto.precio * cantidad
        cursor = self.conexion.cursor()
        cursor.execute(
            "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
            (cantidad, id_producto),
        )
        cursor.execute(
            "INSERT INTO ventas (id_producto, cantidad, total) VALUES (?, ?, ?)",
            (id_producto, cantidad, total),
        )
        self.conexion.commit()
        return total

    def cerrar(self):
        self.conexion.close()


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingrese un numero valido.")


def menu():
    inventario = Inventario()
    while True:
        print("\n===== BELLA GLOW =====")
        print("1. Registrar producto")
        print("2. Buscar producto")
        print("3. Ver inventario")
        print("4. Registrar venta")
        print("5. Salir")
        opcion = input("Seleccione una opcion: ")

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                marca = input("Marca: ")
                precio = float(input("Precio: "))
                cantidad = leer_entero("Cantidad disponible: ")
                producto = inventario.registrar_producto(Producto(nombre, marca, precio, cantidad))
                print(f"Producto registrado con el numero {producto.id_producto}.")
            elif opcion == "2":
                resultados = inventario.buscar_producto(input("Nombre a buscar: "))
                if resultados:
                    for p in resultados:
                        print(p)
                else:
                    print("No se encontraron productos.")
            elif opcion == "3":
                for p in inventario.listar_productos():
                    print(p)
            elif opcion == "4":
                id_producto = leer_entero("Numero del producto: ")
                cantidad = leer_entero("Cantidad vendida: ")
                total = inventario.registrar_venta(id_producto, cantidad)
                print(f"Venta registrada. Total: ${total:,.0f}")
            elif opcion == "5":
                inventario.cerrar()
                print("Hasta pronto.")
                break
            else:
                print("Opcion no valida.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    menu()
