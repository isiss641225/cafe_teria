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
        INSERT INTO usuarios (nombre, apellido, correo, username, password_hash, edad, id_tipo_usuario, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        valores = (self.nombre, self.apellido, self.correo, self.username, 
                  self.password_hash, self.edad, self.id_tipo_usuario, self.created_by)
        
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
        SELECT u.id_usuario, u.nombre, u.apellido, u.correo, u.username, u.edad, t.nombre_tipo
        FROM usuarios u
        INNER JOIN tipo_usuarios t ON u.id_tipo_usuario = t.id_tipo_usuario
        WHERE u.deleted = 0
        ORDER BY u.nombre ASC
        """
        
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        
        print("\n===== USUARIOS =====\n")
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Nombre: {usuario[1]} {usuario[2]} | "
                  f"Correo: {usuario[3]} | Username: {usuario[4]} | "
                  f"Edad: {usuario[5]} | Rol: {usuario[6]}")
        
        cursor.close()
        conexion.close()