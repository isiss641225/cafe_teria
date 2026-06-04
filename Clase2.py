from conexion import Conexion

class Usuario:

    def __init__(self, nombre, apellido, correo, username, password_hash, edad, id_tipo_usuario, created_by="admin"):

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.username = username
        self.password_hash = password_hash
        self.edad = edad
        self.id_tipo_usuario = id_tipo_usuario
        self.created_by = created_by

    def guardar(self):

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO usuarios
        (
            nombre,
            apellido,
            correo,
            username,
            password_hash,
            edad,
            id_tipo_usuario,
            created_by
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        valores = (
            self.nombre,
            self.apellido,
            self.correo,
            self.username,
            self.password_hash,
            self.edad,
            self.id_tipo_usuario,
            self.created_by
        )

        cursor.execute(sql, valores)
        conexion.commit()

        print("\nUsuario agregado correctamente.")

        cursor.close()
        conexion.close()

    @staticmethod
    def listar():

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            u.id_usuario,
            u.nombre,
            u.apellido,
            u.correo,
            u.username,
            u.edad,
            t.nombre_tipo
        FROM usuarios u
        INNER JOIN tipo_usuarios t
            ON u.id_tipo_usuario = t.id_tipo_usuario
        WHERE u.deleted = 0
        ORDER BY u.nombre ASC
        """

        cursor.execute(sql)

        usuarios = cursor.fetchall()

        print("\n===== USUARIOS =====\n")

        for usuario in usuarios:

            print(
                f"ID: {usuario[0]} | "
                f"Nombre: {usuario[1]} {usuario[2]} | "
                f"Correo: {usuario[3]} | "
                f"Username: {usuario[4]} | "
                f"Edad: {usuario[5]} | "
                f"Rol: {usuario[6]}"
            )

        cursor.close()
        conexion.close()

    @staticmethod
    def buscar():

        texto = input(
            "Ingrese nombre o parte del nombre: "
        )

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            u.id_usuario,
            u.nombre,
            u.apellido,
            u.username,
            t.nombre_tipo
        FROM usuarios u
        INNER JOIN tipo_usuarios t
            ON u.id_tipo_usuario = t.id_tipo_usuario
        WHERE u.nombre LIKE %s
        AND u.deleted = 0
        ORDER BY u.nombre ASC
        """

        cursor.execute(
            sql,
            ('%' + texto + '%',)
        )

        resultados = cursor.fetchall()

        print("\n===== RESULTADOS =====\n")

        if len(resultados) == 0:
            print("No se encontraron usuarios.")

        else:

            for usuario in resultados:

                print(
                    f"ID: {usuario[0]} | "
                    f"Nombre: {usuario[1]} {usuario[2]} | "
                    f"Username: {usuario[3]} | "
                    f"Rol: {usuario[4]}"
                )

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():

        id_usuario = input(
            "Ingrese ID del usuario: "
        )

        nuevo_nombre = input(
            "Ingrese nuevo nombre: "
        )

        nueva_edad = input(
            "Ingrese nueva edad: "
        )

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE usuarios
        SET
            nombre = %s,
            edad = %s
        WHERE id_usuario = %s
        """

        valores = (
            nuevo_nombre,
            nueva_edad,
            id_usuario
        )

        cursor.execute(sql, valores)

        conexion.commit()

        print(
            "\nUsuario actualizado correctamente."
        )

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar():

        id_usuario = input(
            "Ingrese ID del usuario: "
        )

        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE usuarios
        SET deleted = 1
        WHERE id_usuario = %s
        """

        cursor.execute(sql, (id_usuario,))

        conexion.commit()

        print(
            "\nUsuario eliminado correctamente."
        )

        cursor.close()
        conexion.close()