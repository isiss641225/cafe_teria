class DetallePedido:
    def __init__(self, pedido, producto, cantidad, descripcion_pedido=""):
        self.pedido = pedido
        self.producto = producto
        self.cantidad = cantidad
        self.descripcion_pedido = descripcion_pedido
        self.precio_unitario = producto.precio_actual
        self.subtotal = self.cantidad * self.precio_unitario

    def calcular_subtotal_con_descuento(self, porcentaje_descuento):
        if 0 <= porcentaje_descuento <= 100:
            descuento = self.subtotal * (porcentaje_descuento / 100)
            return self.subtotal - descuento
        print("Error: El descuento debe estar entre 0 y 100.")
        return self.subtotal

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad > 0:
            self.cantidad = nueva_cantidad
            self.subtotal = self.cantidad * self.precio_unitario
            print(f"Cantidad actualizada a {nueva_cantidad}. Nuevo subtotal: ${self.subtotal:.2f}")
        else:
            print("Error: La cantidad debe ser mayor a 0.")

    def mostrar_linea_detalle(self):
        nombre_prod = getattr(self.producto, 'nombre', 'Producto')
        print(f"📦 {nombre_prod} x{self.cantidad} | P. Unitario: ${self.precio_unitario:.2f} | Subtotal: ${self.subtotal:.2f}")

    def __str__(self):
        return f"Detalle(Producto: {id(self.producto)}, Cantidad: {self.cantidad}, Subtotal: {self.subtotal})"