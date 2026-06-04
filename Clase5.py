from conexion import Conexion

class Pedido:

    def __init__(self, id_usuario, id_tipo_pedido, created_by="admin"):
        self.id_usuario = id_usuario
        self.id_tipo_pedido = id_tipo_pedido
        self.monto_pedido = 0.0
        self.estado_pedido = "Pendiente"
        self.created_by = created_by
        self.detalles_temporales = []

    def agregar_producto(self, id_producto, cantidad, precio_unitario, descripcion="Sin notas"):
        subtotal_item = cantidad * precio_unitario
        detalle = {
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "descripcion_pedido": descripcion
        }
        
        self.detalles_temporales.append(detalle)
        self.monto_pedido += subtotal_item
        print(f"Producto ID {id_producto} agregado temporalmente al pedido. Subtotal: ${subtotal_item}")

    def guardar_pedido_completo(self):
        if not self.detalles_temporales:
            print("No se puede guardar un pedido sin productos.")
            return

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        try:
            sql_pedido = """
            INSERT INTO pedidos 
            (id_usuario, id_tipo_pedido, monto_pedido, estado_pedido, created_by) 
            VALUES (%s, %s, %s, %s, %s)
            """
            valores_pedido = (
                self.id_usuario,
                self.id_tipo_pedido,
                self.monto_pedido,
                self.estado_pedido,
                self.created_by
            )
            cursor.execute(sql_pedido, valores_pedido)
            
            id_pedido_generado = cursor.lastrowid

            sql_detalle = """
            INSERT INTO detalles_pedidos 
            (id_pedido, id_producto, cantidad, descripcion_pedido, precio_unitario, created_by) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            for item in self.detalles_temporales:
                valores_detalle = (
                    id_pedido_generado,
                    item["id_producto"],
                    item["cantidad"],
                    item["descripcion_pedido"],
                    item["precio_unitario"],
                    self.created_by
                )
                cursor.execute(sql_detalle, valores_detalle)

            conexion.commit()
            print(f"\nPedido #{id_pedido_generado} y sus detalles guardados con éxito por ${self.monto_pedido}.")

            self.detalles_temporales = []

        except Exception as e:
            conexion.rollback()
            print(f"Error al registrar el pedido: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def pagar_pedido(id_pedido):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE pedidos 
        SET estado_pedido = 'Pagado' 
        WHERE id_pedido = %s AND deleted = 0
        """
        
        cursor.execute(sql, (id_pedido,))
        conexion.commit()
        
        print(f"\nPedido #{id_pedido} marcado como PAGADO en la base de datos.")
        
        cursor.close()
        conexion.close()

    @staticmethod
    def mostrar_total_en_venta():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT SUM(monto_pedido) 
        FROM pedidos 
        WHERE estado_pedido = 'Pagado' AND deleted = 0
        """
        
        cursor.execute(sql)
        resultado = cursor.fetchone()
        
        # Validamos si no hay ventas aún para evitar que devuelva None
        total = resultado[0] if resultado[0] is not None else 0.0

        print("\n=========================================")
        print(f" TOTAL GENERAL HISTÓRICO EN VENTAS: ${total}")
        print("=========================================")

        cursor.close()
        conexion.close()