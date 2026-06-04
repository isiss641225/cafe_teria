class Pedido:
    total_ventas_historico = 0.0

    def __init__(self, empleado, tipo_pedido):
        self.id_pedido = 1
        self.empleado = empleado
        self.tipo_pedido = tipo_pedido
        self.monto_pedido = 0.0
        self.estado_pedido = "Pendiente"
        self.detalles = [] 

    def agregar_producto(self, producto, cantidad, descripcion="Sin notas"):
        if producto.stock >= cantidad:
            #nuevo_detalle = DetallePedido(self, producto, cantidad, descripcion)
            #self.detalles.append(nuevo_detalle)
            #self.monto_pedido += nuevo_detalle.subtotal
            producto.restar_stock(cantidad) # Descuenta del inventario general
        else:
            print(f"Stock insuficiente de {producto.nombre_producto}. Disponible: {producto.stock}")

    def pagar_pedido(self):
        self.estado_pedido = "Pagado"
        Pedido.total_ventas_historico += self.monto_pedido

    @classmethod
    def mostrar_total_en_venta(cls):

        print("\n=========================================")
        print(f" TOTAL GENERAL EN VENTAS: ${cls.total_ventas_historico}")
        print("=========================================")
