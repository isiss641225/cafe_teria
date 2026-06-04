class TipoPedido:
    def __init__(self, descripcion_tipo):
        self.descripcion_tipo = descripcion_tipo

    def mostrar_informacion(self):
        print(f"Tipo de Pedido: {self.descripcion_tipo}")

    def cambiar_descripcion(self, nueva_descripcion):
        if nueva_descripcion.strip():  # Validación simple para que no quede vacío
            self.descripcion_tipo = nueva_descripcion
        else:
            print("Error: La descripción no puede estar vacía.")

    def __str__(self):
        return f"TipoPedido(descripcion='{self.descripcion_tipo}')"