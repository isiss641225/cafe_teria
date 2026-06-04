class Producto:
    # PRODUCTOS PREESTABLECIDOS (Se cargan automáticamente en el sistema)
    # Formato: id_producto: [Nombre, Precio, Stock, Descripción]
    inventario_preestablecido = {
        1: ["Café Mocca", 1500, 50, "Chocolate caliente"],
        2: ["Café Helado", 2000, 40, "Cafe con Helado"],
        3: ["Capuccino", 2200, 30, "Espresso, leche y espuma"],
        4: ["Medialuna", 1000, 15, "Medialuna"],
        5: ["Sandwich de Salame", 3500, 10, "Tostadito es mas rico"]
    }

    def __init__(self, id_producto):
        # Al crear un producto, busca sus datos en el inventario preestablecido usando el ID
        if id_producto in Producto.inventario_preestablecido:
            datos = Producto.inventario_preestablecido[id_producto]
            self.id_producto = id_producto
            self.nombre_producto = datos[0]
            self.precio_actual = datos[1]
            self.stock = datos[2]
            self.descripcion_producto = datos[3]
        else:
            print(f"Error: El ID de producto {id_producto} no existe.")

    @classmethod
    def mostrar_productos_y_valores(cls):
        print("\n=== INVENTARIO DE PRODUCTOS Y VALORES ===")
        for id_prod, datos in cls.inventario_preestablecido.items():
            print(f"ID: {id_prod} | Producto: {datos[0]:<25} | Valor: ${datos[1]:<8} | Stock: {datos[2]}")
        print("=========================================")

    def restar_stock(self, cantidad):
        # Actualiza el stock tanto en la instancia como en el almacén preestablecido
        self.stock -= cantidad
        Producto.inventario_preestablecido[self.id_producto][2] = self.stock

