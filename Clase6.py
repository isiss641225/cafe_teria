from conexion import Conexion

class DetallePedido:

    def __init__(self, id_pedido, id_producto, cantidad, precio_unitario, descripcion_pedido=""):

        self.id_pedido = id_pedido
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.descripcion_pedido = descripcion_pedido

    def guardar(self, created_by="admin"):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO detalles_pedidos
        (
            id_pedido,
            id_producto,
            cantidad,
            descripcion_pedido,
            precio_unitario,
            created_by
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            self.id_pedido,
            self.id_producto,
            self.cantidad,
            self.descripcion_pedido,
            self.precio_unitario,
            created_by
        )

        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar_cantidad(id_detalle_pedido, nueva_cantidad):
        if nueva_cantidad <= 0:
            print("Error: La cantidad debe ser mayor a 0.")
            return

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql_update = """
        UPDATE detalles_pedidos
        SET cantidad = %s
        WHERE id_detalle_pedido = %s AND deleted = 0
        """
        cursor.execute(sql_update, (nueva_cantidad, id_detalle_pedido))
        conexion.commit()

        sql_recalcular_pedido = """
        UPDATE pedidos p
        SET p.monto_pedido = (
            SELECT SUM(dp.subtotal) 
            FROM detalles_pedidos dp 
            WHERE dp.id_pedido = p.id_pedido AND dp.deleted = 0
        )
        WHERE p.id_pedido = (
            SELECT id_pedido FROM detalles_pedidos WHERE id_detalle_pedido = %s
        )
        """
        cursor.execute(sql_recalcular_pedido, (id_detalle_pedido,))
        conexion.commit()

        print(f"\nCantidad actualizada a {nueva_cantidad} en el detalle #{id_detalle_pedido}. Totales recalculados.")
        
        cursor.close()
        conexion.close()

    @staticmethod
    def consultar_detalles_de_pedido(id_pedido):

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT 
            p.nombre_producto, 
            dp.cantidad, 
            dp.precio_unitario, 
            dp.subtotal,
            dp.descripcion_pedido
        FROM detalles_pedidos dp
        INNER JOIN productos p ON dp.id_producto = p.id_producto
        WHERE dp.id_pedido = %s AND dp.deleted = 0
        """
        
        cursor.execute(sql, (id_pedido,))
        resultados = cursor.fetchall()

        print(f"\n===== DETALLES DEL PEDIDO #{id_pedido} =====")
        if not resultados:
            print("No hay productos registrados en este pedido.")
        else:
            for fila in resultados:
                print(
                    f"Producto: {fila[0]} | "
                    f"Cant: {fila[1]} | "
                    f"P. Unitario: ${fila[2]:.2f} | "
                    f"Subtotal: ${fila[3]:.2f} | "
                    f"Notas: {fila[4]}"
                )

        cursor.close()
        conexion.close()

    def calcular_subtotal_con_descuento(self, porcentaje_descuento):

        subtotal_local = self.cantidad * self.precio_unitario
        if 0 <= porcentaje_descuento <= 100:
            descuento = subtotal_local * (porcentaje_descuento / 100)
            return subtotal_local - descuento
            
        print("Error: El descuento debe estar entre 0 y 100.")
        return subtotal_local