import os # --> ejecuta comandos en consola
def limpiar_consola(): # limpian consola del terminal
    os.system('cls')

class TipoUsuario:
    total_tipos = 0
    
    def __init__(self, nombre_tipo, descripcion_tipo):
        self.id_tipo_usuario = TipoUsuario.total_tipos + 1
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
        TipoUsuario.total_tipos += 1


class Usuario:
    lista_usuarios = []

    def __init__(self, nombre_completo, correo, username, password_hash, edad, tipo_usuario):
        self.id_usuario = len(Usuario.lista_usuarios) + 1
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.username = username
        self.password_hash = password_hash
        self.edad = edad
        self.tipo_usuario = tipo_usuario
        Usuario.lista_usuarios.append(self)

    @classmethod
    def mostrar_usuarios(cls):
        """Consulta: Mostrar usuarios"""
        print("\n=== LISTA DE USUARIOS ===")
        for u in cls.lista_usuarios:
            print(f"ID: {u.id_usuario} | Nombre: {u.nombre_completo} | Username: @{u.username} | Rol: {u.tipo_usuario.nombre_tipo}")
        print("=========================")


class Empleado:
    def __init__(self, nombre_empleado, usuario):
        self.nombre_empleado = nombre_empleado
        self.usuario = usuario


class TipoPedido:
    def __init__(self, descripcion_tipo):
        self.descripcion_tipo = descripcion_tipo


class Producto:
    # PRODUCTOS PREESTABLECIDOS (Se cargan automáticamente en el sistema)
    # Formato: id_producto: [Nombre, Precio, Stock, Descripción]
    inventario_preestablecido = {
        1: ["Café Espresso", 1500.00, 50, "Café concentrado puro"],
        2: ["Café Latte", 2000.00, 40, "Espresso con leche al vapor"],
        3: ["Capuccino", 2200.00, 30, "Espresso, leche y espuma"],
        4: ["Muffin de Chocolate", 950.00, 15, "Muffin con chips de chocolate"],
        5: ["Sandwich de Jamón y Queso", 3500.00, 10, "Tostado en pan de masa madre"]
    }

    def __init__(self, id_producto):
        # Al crear un producto, busca sus datos en el inventario preestablecido usando el ID
        if id_producto in Producto.inventario_preestablecido:
            datos = Producto.inventario_preestablecido[id_producto]
            self.id_producto = id_producto
            self.nombre_producto = datos[0]
            self.precio_actual = datos[1]
            self.stock = datos[2]
            self.descripcion_producto = datos[3]
        else:
            print(f"Error: El ID de producto {id_producto} no existe en los preestablecidos.")

    @classmethod
    def mostrar_productos_y_valores(cls):
        """Consulta: Mostrar producto y valor del producto"""
        print("\n=== INVENTARIO DE PRODUCTOS Y VALORES ===")
        for id_prod, datos in cls.inventario_preestablecido.items():
            print(f"ID: {id_prod} | Producto: {datos[0]:<25} | Valor: ${datos[1]:<8} | Stock: {datos[2]}")
        print("=========================================")

    def restar_stock(self, cantidad):
        # Actualiza el stock tanto en la instancia como en el almacén preestablecido
        self.stock -= cantidad
        Producto.inventario_preestablecido[self.id_producto][2] = self.stock


class Pedido:
    total_ventas_historico = 0.0

    def __init__(self, empleado, tipo_pedido):
        self.id_pedido = 1
        self.empleado = empleado
        self.tipo_pedido = tipo_pedido
        self.monto_pedido = 0.0
        self.estado_pedido = "Pendiente"
        self.detalles = [] 

    def agregar_producto(self, producto, cantidad, descripcion="Sin notas"):
        if producto.stock >= cantidad:
            nuevo_detalle = DetallePedido(self, producto, cantidad, descripcion)
            self.detalles.append(nuevo_detalle)
            self.monto_pedido += nuevo_detalle.subtotal
            producto.restar_stock(cantidad) # Descuenta del inventario general
        else:
            print(f"Stock insuficiente de {producto.nombre_producto}. Disponible: {producto.stock}")

    def pagar_pedido(self):
        self.estado_pedido = "Pagado"
        Pedido.total_ventas_historico += self.monto_pedido

    @classmethod
    def mostrar_total_en_venta(cls):
        """Consulta: Mostrar total en venta"""
        print("\n=========================================")
        print(f" TOTAL GENERAL EN VENTAS: ${cls.total_ventas_historico}")
        print("=========================================")


class DetallePedido:
    def __init__(self, pedido, producto, cantidad, descripcion_pedido=""):
        self.pedido = pedido
        self.producto = producto
        self.cantidad = cantidad
        self.descripcion_pedido = descripcion_pedido
        self.precio_unitario = producto.precio_actual
        self.subtotal = self.cantidad * self.precio_unitario