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
        print(f"Producto ID {id_producto} agregado. Subtotal: ${subtotal_item}")

    def guardar_pedido_completo(self):
        if not self.detalles_temporales:
            print("No se puede guardar un pedido sin productos.")
            return False
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        try:
            # Insertar pedido
            sql_pedido = """
            INSERT INTO pedidos (id_usuario, id_tipo_pedido, monto_pedido, estado_pedido, created_by)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores_pedido = (self.id_usuario, self.id_tipo_pedido, self.monto_pedido, 
                            self.estado_pedido, self.created_by)
            cursor.execute(sql_pedido, valores_pedido)
            id_pedido_generado = cursor.lastrowid
            
            # Insertar detalles
            sql_detalle = """
            INSERT INTO detalles_pedidos (id_pedido, id_producto, cantidad, descripcion_pedido, precio_unitario, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            for item in self.detalles_temporales:
                valores_detalle = (id_pedido_generado, item["id_producto"], item["cantidad"],
                                  item["descripcion_pedido"], item["precio_unitario"], self.created_by)
                cursor.execute(sql_detalle, valores_detalle)
            
            conexion.commit()
            print(f"\nPedido #{id_pedido_generado} guardado con éxito. Total: ${self.monto_pedido}")
            
            # Preguntar si desea pagar ahora
            pagar_ahora = input("\n¿Desea pagar este pedido ahora? (si/no): ").lower()
            if pagar_ahora == 'si':
                self.pagar_pedido(id_pedido_generado)
            
            self.detalles_temporales = []
            return True
            
        except Exception as e:
            conexion.rollback()
            print(f"Error al registrar el pedido: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def pagar_pedido(id_pedido):
        """Método para marcar un pedido como pagado"""
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        try:
            sql = """
            UPDATE pedidos 
            SET estado_pedido = 'Pagado' 
            WHERE id_pedido = %s AND deleted = 0
            """
            
            cursor.execute(sql, (id_pedido,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"\n Pedido #{id_pedido} marcado como PAGADO exitosamente.")
            else:
                print(f"\n No se encontró el pedido #{id_pedido} o ya está pagado.")
                
        except Exception as e:
            conexion.rollback()
            print(f"Error al pagar el pedido: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar_pedidos_pendientes():
        """Lista todos los pedidos pendientes de pago"""
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
        SELECT p.id_pedido, u.nombre, u.apellido, p.monto_pedido, p.created_at
        FROM pedidos p
        INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE p.estado_pedido = 'Pendiente' AND p.deleted = 0
        ORDER BY p.created_at DESC
        """
        
        cursor.execute(sql)
        pedidos = cursor.fetchall()
        
        print("\n===== PEDIDOS PENDIENTES DE PAGO =====\n")
        if len(pedidos) == 0:
            print("No hay pedidos pendientes de pago.")
        else:
            for pedido in pedidos:
                print(f"ID: {pedido[0]} | Cliente: {pedido[1]} {pedido[2]} | "
                      f"Monto: ${pedido[3]} | Fecha: {pedido[4]}")
        
        cursor.close()
        conexion.close()
        return pedidos

    @staticmethod
    def mostrar_total_en_venta():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Mostrar total de ventas pagadas
        sql_pagado = "SELECT SUM(monto_pedido) FROM pedidos WHERE estado_pedido = 'Pagado' AND deleted = 0"
        cursor.execute(sql_pagado)
        resultado_pagado = cursor.fetchone()
        total_pagado = resultado_pagado[0] if resultado_pagado[0] is not None else 0.0
        
        # Mostrar total pendiente
        sql_pendiente = "SELECT SUM(monto_pedido) FROM pedidos WHERE estado_pedido = 'Pendiente' AND deleted = 0"
        cursor.execute(sql_pendiente)
        resultado_pendiente = cursor.fetchone()
        total_pendiente = resultado_pendiente[0] if resultado_pendiente[0] is not None else 0.0
        
        # Mostrar total general
        sql_general = "SELECT SUM(monto_pedido) FROM pedidos WHERE deleted = 0"
        cursor.execute(sql_general)
        resultado_general = cursor.fetchone()
        total_general = resultado_general[0] if resultado_general[0] is not None else 0.0
        
        print("\n" + "="*45)
        print("     RESUMEN DE VENTAS")
        print("="*45)
        print(f"Total pagado:        ${total_pagado:,.2f}")
        print(f"Total pendiente:     ${total_pendiente:,.2f}")
        print(f"{'-'*45}")
        print(f"Total general:       ${total_general:,.2f}")
        print("="*45)
        
        cursor.close()
        conexion.close()