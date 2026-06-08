from conexion import Conexion

class TipoUsuario:
    def __init__(self, nombre_tipo=None, descripcion_tipo=None, created_by="admin"):
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
        self.created_by = created_by

    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
        INSERT INTO tipo_usuarios (nombre_tipo, descripcion_tipo, created_by)
        VALUES (%s, %s, %s)
        """
        
        valores = (self.nombre_tipo, self.descripcion_tipo, self.created_by)
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
        SELECT id_tipo_usuario, nombre_tipo, descripcion_tipo
        FROM tipo_usuarios
        WHERE deleted = 0
        """
        
        cursor.execute(sql)
        tipos = cursor.fetchall()
        
        print("\n===== TIPOS DE USUARIO =====\n")
        for tipo in tipos:
            print(f"ID: {tipo[0]} | Tipo: {tipo[1]} | Descripción: {tipo[2]}")
        
        cursor.close()
        conexion.close()