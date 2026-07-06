from conexion import Conexion


class Empleado:

    def __init__(self, nombre_empleado=None, usuario=None):
        self.nombre_empleado = nombre_empleado
        self.usuario = usuario
        self.conectado = False

    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO empleados
        (
            nombre_empleado,
            usuario,
            conectado
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """

        valores = (
            self.nombre_empleado,
            self.usuario,
            self.conectado
        )

        cursor.execute(sql, valores)
        conexion.commit()
        print("\nEmpleado agregado correctamente.")
        cursor.close()
        conexion.close()

    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_empleado,
            nombre_empleado,
            usuario
        FROM empleados
        WHERE deleted = 0
        ORDER BY nombre_empleado ASC
        """

        cursor.execute(sql)
        empleados = cursor.fetchall()
        print("\n===== EMPLEADOS =====\n")
        for empleado in empleados:
            print(
                f"ID: {empleado[0]} | "
                f"Nombre: {empleado[1]} | "
                f"Usuario: {empleado[2]}"
            )

        cursor.close()
        conexion.close()

    @staticmethod
    def buscar():
        texto = input("Ingrese nombre o parte del nombre: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_empleado,
            nombre_empleado,
            usuario
        FROM empleados
        WHERE nombre_empleado LIKE %s
        AND deleted = 0
        ORDER BY nombre_empleado ASC
        """

        cursor.execute(sql, ('%' + texto + '%',))

        resultados = cursor.fetchall()
        print("\n===== RESULTADOS =====\n")
        if len(resultados) == 0:
            print("No se encontraron registros.")
        else:
            for empleado in resultados:
                print(
                    f"ID: {empleado[0]} | "
                    f"Nombre: {empleado[1]} | "
                    f"Usuario: {empleado[2]}"
                )

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():
        id_empleado = input("Ingrese ID del empleado: ")
        nuevo_usuario = input("Ingrese nuevo nombre de usuario: ")

        if len(nuevo_usuario) >= 4:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()

            sql = """
            UPDATE empleados
            SET usuario = %s
            WHERE id_empleado = %s
            """

            valores = (nuevo_usuario, id_empleado)
            cursor.execute(sql, valores)
            conexion.commit()
            print("\nUsuario actualizado correctamente.")

            cursor.close()
            conexion.close()
        else:
            print("\nError: El nombre de usuario debe tener al menos 4 caracteres.")

    @staticmethod
    def eliminar():
        id_empleado = input("Ingrese ID del empleado: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE empleados
        SET deleted = 1
        WHERE id_empleado = %s
        """

        cursor.execute(sql, (id_empleado,))
        conexion.commit()
        print("\nEmpleado eliminado correctamente.")
        cursor.close()
        conexion.close()