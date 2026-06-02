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
        print("\n=== LISTA DE USUARIOS ===")
        for u in cls.lista_usuarios:
            print(f"ID: {u.id_usuario} | Nombre: {u.nombre_completo} | Username: {u.username} | Rol: {u.tipo_usuario.nombre_tipo}")
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
        1: ["Café Mocca", 1500, 50, "Chocolate caliente"],
        2: ["Café Helado", 2000, 40, "Cafe con Helado"],
        3: ["Capuccino", 2200, 30, "Espresso, leche y espuma"],
        4: ["Medialuna", 1000, 15, "Medialuna"],
        5: ["Sandwich de Salame", 3500, 10, "Tostadito es mas rico"]
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
            print(f"Error: El ID de producto {id_producto} no existe.")

    @classmethod
    def mostrar_productos_y_valores(cls):
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


        # =====================================================================
#        SISTEMA DE MENÚ INTERACTIVO (BUCLE WHILE)
# =====================================================================

# Datos base iniciales obligatorios para que el sistema funcione
rol_admin = TipoUsuario("Administrador", "Acceso total")
usuario_base = Usuario("Sebastian Anabalon", "seba@cafe.com", "seba_admin", "7777", 30, rol_admin)
empleado_base = Empleado("Carlos A.", usuario_base)
tipo_entrega = TipoPedido("Local")

while True:
    limpiar_consola()
    print("=========================================")
    print("      SISTEMA DE GESTIÓN DE CAFETERÍA     ")
    print("=========================================")
    print("1. Ver inventario de productos y precios")
    print("2. Registrar nuevo usuario")
    print("3. Ver lista de usuarios")
    print("4. Crear un nuevo pedido (Venta)")
    print("5. Ver total histórico de ventas")
    print("6. Salir")
    print("=========================================")
    
    opcion = input("Selecciona una opción (1-6): ")

    if opcion == "1":
        limpiar_consola()
        Producto.mostrar_productos_y_valores()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "2":
        limpiar_consola()
        print("=== REGISTRAR NUEVO USUARIO ===")
        nombre = input("Nombre completo: ")
        correo = input("Correo electrónico: ")
        username = input("Nombre de usuario (username): ")
        password = input("Contraseña: ")
        edad = int(input("Edad: "))
        
        # Le asignamos el rol básico de administrador creado arriba para simplificar
        Usuario(nombre, correo, username, password, edad, rol_admin)
        print("\nUsuario registrado con éxito!")
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "3":
        limpiar_consola()
        Usuario.mostrar_usuarios()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "4":
        limpiar_consola()
        print("=== CREANDO NUEVO PEDIDO ===")
        # Inicializamos un pedido vacío
        pedido_actual = Pedido(empleado_base, tipo_entrega)
        
        while True:
            Producto.mostrar_productos_y_valores()
            try:
                id_prod = int(input("\nIngresa el ID del producto que deseas llevar (0 para terminar el pedido): "))
                if id_prod == 0:
                    break
                
                if id_prod in Producto.inventario_preestablecido:
                    cant = int(input(f"¿Cuántas unidades deseas?: "))
                    if cant <= 0:
                        print("La cantidad debe ser mayor a 0.")
                        continue
                    
                    # Instanciamos el producto con su id
                    producto_elegido = Producto(id_prod)
                    pedido_actual.agregar_producto(producto_elegido, cant)
                else:
                    print("ID de producto no válido.")
            except ValueError:
                print("Por favor, introduce un número válido.")
            
            input("\nPresiona Enter para continuar cargando productos...")
            limpiar_consola()

        # Al terminar de agregar productos, procedemos al pago si compró algo
        if pedido_actual.monto_pedido > 0:
            print(f"\nEl total del pedido es: ${pedido_actual.monto_pedido}")
            pagar = input("¿Deseas confirmar el pago de este pedido? (si/no): ").lower()
            if pagar == 'si':
                pedido_actual.pagar_pedido()
                print("Pedido pagado con éxito y registrado en el historial!")
            else:
                print("Pedido cancelado (se devolvió el stock de este menú simulado)")
        else:
            print("\nNo se agregaron productos al pedido.")
            
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "5":
        limpiar_consola()
        Pedido.mostrar_total_en_venta()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "6":
        limpiar_consola()
        print("Saliendo del sistema...")
        break
    
    else:
        print("Opción inválida. Intenta de nuevo.")
        input("\nPresiona Enter para continuar...")