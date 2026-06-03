class TipoUsuario:
    total_tipos = 0
    
    def __init__(self, nombre_tipo, descripcion_tipo):
        self.id_tipo_usuario = TipoUsuario.total_tipos + 1
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
        self.total_tipos += 1  
        TipoUsuario.total_tipos += 1

    def mostrar_detalle(self):
        print(f"[{self.id_tipo_usuario}] Tipo: {self.nombre_tipo} | Descripción: {self.descripcion_tipo}")

    def actualizar_descripcion(self, nueva_descripcion):
        self.descripcion_tipo = nueva_descripcion
        print(f"Descripción de '{self.nombre_tipo}' actualizada con éxito.")

    def __str__(self):
        return f"TipoUsuario({self.id_tipo_usuario}: {self.nombre_tipo})"

    @classmethod
    def obtener_total_tipos(cls):
        return cls.total_tipos