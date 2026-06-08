from conexion import Conexion


class TipoPedido:

    def __init__(self, id_tipo_pedido, descripcion_tipo):
        self.id_tipo_pedido = id_tipo_pedido
        self.descripcion_tipo = descripcion_tipo

    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO tipos_pedido
        (
            descripcion_tipo
        )
        VALUES
        (
            %s
        )
        """

        valores = (self.descripcion_tipo,)

        cursor.execute(sql, valores)
        conexion.commit()
        print("\nTipo de pedido agregado correctamente.")
        cursor.close()
        conexion.close()

    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_tipo_pedido,
            descripcion_tipo
        FROM tipos_pedido
        WHERE deleted = 0
        ORDER BY id_tipo_pedido ASC
        """

        cursor.execute(sql)
        tipos = cursor.fetchall()
        print("\n===== TIPOS DE PEDIDO =====\n")
        for tipo in tipos:
            print(
                f"ID: {tipo[0]} | "
                f"Descripción: {tipo[1]}"
            )

        cursor.close()
        conexion.close()

    @staticmethod
    def buscar():
        texto = input("Ingrese tipo de pedido o parte de él: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_tipo_pedido,
            descripcion_tipo
        FROM tipos_pedido
        WHERE descripcion_tipo LIKE %s
        AND deleted = 0
        ORDER BY id_tipo_pedido ASC
        """

        cursor.execute(sql, ('%' + texto + '%',))

        resultados = cursor.fetchall()
        print("\n===== RESULTADOS =====\n")
        if len(resultados) == 0:
            print("No se encontraron registros.")
        else:
            for tipo in resultados:
                print(
                    f"ID: {tipo[0]} | "
                    f"Descripción: {tipo[1]}"
                )

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():
        id_tipo_pedido = input("Ingrese ID del tipo de pedido: ")
        nueva_descripcion = input("Ingrese nueva descripción: ")

        if nueva_descripcion.strip():
            conexion = Conexion.conectar()
            cursor = conexion.cursor()

            sql = """
            UPDATE tipos_pedido
            SET descripcion_tipo = %s
            WHERE id_tipo_pedido = %s
            """

            valores = (nueva_descripcion, id_tipo_pedido)
            cursor.execute(sql, valores)
            conexion.commit()
            print("\nTipo de pedido actualizado correctamente.")
            cursor.close()
            conexion.close()