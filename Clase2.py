class Usuario:
    lista_usuarios = []

    def __init__(self, nombre, correo, username, password_hash, edad, tipo_usuario):
        self.id_usuario = len(Usuario.lista_usuarios) + 1
        self.nombre = nombre
        self.correo = correo
        self.username = username
        self.password_hash = password_hash
        self.edad = edad
        self.tipo_usuario = tipo_usuario
        Usuario.lista_usuarios.append(self)

    @classmethod
    def mostrar_usuarios(cls):
        print("\n=== LISTA DE USUARIOS ===")
        for u in cls.lista_usuarios:
            print(f"ID: {u.id_usuario} | Nombre: {u.nombre} | Username: {u.username} | Rol: {u.tipo_usuario.nombre_tipo}")
        print("=========================")

