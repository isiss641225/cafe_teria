from conexion import Conexion

class TipoUsuario:

    def __init__(
        self,
        nombre_tipo=None,
        descripcion_tipo=None,
        created_by="admin"
    ):
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
        self.created_by = created_by

    def guardar(self):

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO tipo_usuarios
        (
            nombre_tipo,
            descripcion_tipo,
            created_by
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """

        valores = (
            self.nombre_tipo,
            self.descripcion_tipo,
            self.created_by
        )

        cursor.execute(sql, valores)
        conexion.commit()

        print("Tipo de usuario agregado correctamente.")

        cursor.close()
        conexion.close()

    @staticmethod
    def listar():

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_tipo_usuario,
            nombre_tipo,
            descripcion_tipo
        FROM tipo_usuarios
        WHERE deleted = 0
        """

        cursor.execute(sql)

        tipos = cursor.fetchall()

        print("\n===== TIPOS DE USUARIO =====\n")

        for tipo in tipos:
            print(
                f"ID: {tipo[0]} | "
                f"Tipo: {tipo[1]} | "
                f"Descripción: {tipo[2]}"
            )

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():

        id_tipo = input("Ingrese ID del tipo: ")
        nueva_descripcion = input("Nueva descripción: ")

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE tipo_usuarios
        SET descripcion_tipo = %s
        WHERE id_tipo_usuario = %s
        """

        cursor.execute(
            sql,
            (
                nueva_descripcion,
                id_tipo
            )
        )

        conexion.commit()

        print("Descripción actualizada.")

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar():

        id_tipo = input("Ingrese ID del tipo: ")

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE tipo_usuarios
        SET deleted = 1
        WHERE id_tipo_usuario = %s
        """

        cursor.execute(sql, (id_tipo,))
        conexion.commit()

        print("Tipo de usuario eliminado.")

        cursor.close()
        conexion.close()