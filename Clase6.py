from conexion import Conexion


class Pedido:

    def __init__(self, id_pedido, empleado, tipo_pedido, monto_pedido, estado_pedido):
        self.id_pedido = id_pedido
        self.empleado = empleado
        self.tipo_pedido = tipo_pedido
        self.monto_pedido = monto_pedido
        self.estado_pedido = estado_pedido

    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO pedidos
        (
            empleado,
            tipo_pedido,
            monto_pedido,
            estado_pedido
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        valores = (
            self.empleado,
            self.tipo_pedido,
            self.monto_pedido,
            self.estado_pedido
        )

        cursor.execute(sql, valores)
        conexion.commit()
        print("\nPedido registrado correctamente.")
        cursor.close()
        conexion.close()

    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_pedido,
            empleado,
            tipo_pedido,
            monto_pedido,
            estado_pedido
        FROM pedidos
        WHERE deleted = 0
        ORDER BY id_pedido DESC
        """

        cursor.execute(sql)
        pedidos = cursor.fetchall()
        print("\n===== PEDIDOS =====\n")
        for pedido in pedidos:
            print(
                f"ID Pedido: {pedido[0]} | "
                f"Empleado: {pedido[1]} | "
                f"Tipo: {pedido[2]} | "
                f"Monto: ${pedido[3]} | "
                f"Estado: {pedido[4]}"
            )

        cursor.close()
        conexion.close()

    @staticmethod
    def buscar():
        texto = input("Ingrese ID del pedido o empleado a buscar: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_pedido,
            empleado,
            tipo_pedido,
            monto_pedido,
            estado_pedido
        FROM pedidos
        WHERE (id_pedido LIKE %s OR empleado LIKE %s)
        AND deleted = 0
        ORDER BY id_pedido DESC
        """

        cursor.execute(sql, ('%' + texto + '%', '%' + texto + '%'))

        resultados = cursor.fetchall()
        print("\n===== RESULTADOS =====\n")
        if len(resultados) == 0:
            print("No se encontraron registros.")
        else:
            for pedido in resultados:
                print(
                    f"ID Pedido: {pedido[0]} | "
                    f"Empleado: {pedido[1]} | "
                    f"Tipo: {pedido[2]} | "
                    f"Monto: ${pedido[3]} | "
                    f"Estado: {pedido[4]}"
                )

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():
        id_pedido = input("Ingrese ID del pedido: ")
        nuevo_estado = input("Ingrese nuevo estado del pedido (Pagado/Cancelado): ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE pedidos
        SET estado_pedido = %s
        WHERE id_pedido = %s
        """

        valores = (nuevo_estado, id_pedido)
        cursor.execute(sql, valores)
        conexion.commit()
        print("\nEstado del pedido actualizado correctamente.")

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar():
        id_pedido = input("Ingrese ID del pedido: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE pedidos
        SET deleted = 1
        WHERE id_pedido = %s
        """

        cursor.execute(sql, (id_pedido,))
        conexion.commit()
        print("\nPedido eliminado correctamente.")
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
        total = resultado[0] if resultado[0] is not None else 0.0

        print("\n=========================================")
        print(f" TOTAL GENERAL EN VENTAS: ${total}")
        print("=========================================")

        cursor.close()
        conexion.close()