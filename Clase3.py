class Empleado:
    def __init__(self, nombre_empleado, usuario):
        self.nombre_empleado = nombre_empleado
        self.usuario = usuario 
        self.conectado = False 

    def presentarse(self):
        return f"Hola, soy {self.nombre_empleado} y mi usuario es '{self.usuario}'."

    def iniciar_sesion(self):
        if not self.conectado:
            self.conectado = True
            print(f"[{self.usuario}] Ha iniciado sesión con éxito.")
        else:
            print(f"[{self.usuario}] Ya está en línea.")

    def cerrar_sesion(self):
        if self.conectado:
            self.conectado = False
            print(f"[{self.usuario}] Ha cerrado sesión.")
        else:
            print(f"[{self.usuario}] Ya estaba desconectado.")

    def cambiar_usuario(self, nuevo_usuario):
        if len(nuevo_usuario) >= 4:
            anterior = self.usuario
            self.usuario = nuevo_usuario
            print(f"Usuario actualizado: {anterior} -> {self.usuario}")
        else:
            print("Error: El nombre de usuario debe tener al menos 4 caracteres.")