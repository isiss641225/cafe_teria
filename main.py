import os
from conexion import Conexion
from Clase1 import TipoUsuario
from Clase2 import Usuario
from Clase3 import Producto
from Clase4 import Pedido

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Datos iniciales - Crear tipo de usuario admin si no existe
def inicializar_datos():
    conexion = Conexion.conectar()
    cursor = conexion.cursor()
    
    # Verificar si existe tipo administrador
    cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = 'Administrador' AND deleted = 0")
    if not cursor.fetchone():
        tipo_admin = TipoUsuario("Administrador", "Acceso total al sistema")
        tipo_admin.guardar()
    
    # Verificar si hay datos de prueba
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    if count == 0:
        print("No hay productos. Por favor, ejecuta primero el script SQL con datos de prueba.")
    
    cursor.close()
    conexion.close()

while True:
    limpiar_consola()
    print("=========================================")
    print("      SISTEMA DE GESTIÓN DE CAFETERÍA     ")
    print("=========================================")
    print("1. Ver inventario de productos")
    print("2. Registrar nuevo usuario")
    print("3. Ver lista de usuarios")
    print("4. Crear un nuevo pedido (Venta)")
    print("5. Ver total histórico de ventas")
    print("6. Pagar pedidos pendientes")
    print("7. Salir")
    print("=========================================")
    
    opcion = input("Selecciona una opción (1-7): ")
    
    if opcion == "1":
        limpiar_consola()
        Producto.listar()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "2":
        limpiar_consola()
        print("=== REGISTRAR NUEVO USUARIO ===\n")
        
        # Mostrar tipos de usuario disponibles
        TipoUsuario.listar()
        
        nombre = input("\nNombre: ")
        apellido = input("Apellido: ")
        correo = input("Correo electrónico: ")
        username = input("Nombre de usuario: ")
        password = input("Contraseña: ")
        edad = int(input("Edad: "))
        id_tipo = int(input("ID del tipo de usuario: "))
        
        usuario = Usuario(nombre, apellido, correo, username, password, edad, id_tipo)
        usuario.guardar()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "3":
        limpiar_consola()
        Usuario.listar()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "4":
        limpiar_consola()
        print("=== CREAR NUEVO PEDIDO ===\n")
        
        # Mostrar usuarios para seleccionar
        Usuario.listar()
        try:
            id_usuario = int(input("\nID del usuario que realiza el pedido: "))
            id_tipo_pedido = int(input("ID del tipo de pedido (1: Local, 2: Delivery, 3: Para llevar): "))
            
            pedido_actual = Pedido(id_usuario, id_tipo_pedido)
            
            while True:
                limpiar_consola()
                print("=== AGREGAR PRODUCTOS AL PEDIDO ===\n")
                Producto.listar()
                
                try:
                    id_prod = int(input("\nIngresa ID del producto (0 para terminar): "))
                    if id_prod == 0:
                        break
                    
                    # Verificar si el producto existe
                    conexion = Conexion.conectar()
                    cursor = conexion.cursor()
                    cursor.execute("SELECT precio_actual, stock FROM productos WHERE id_producto = %s AND deleted = 0", (id_prod,))
                    producto = cursor.fetchone()
                    cursor.close()
                    conexion.close()
                    
                    if producto:
                        precio = float(producto[0])
                        stock = int(producto[1])
                        
                        cantidad = int(input(f"¿Cuántas unidades deseas? (Stock disponible: {stock}): "))
                        if cantidad <= 0:
                            print("La cantidad debe ser mayor a 0.")
                        elif cantidad > stock:
                            print(f"Stock insuficiente. Solo hay {stock} unidades.")
                        else:
                            pedido_actual.agregar_producto(id_prod, cantidad, precio)
                    else:
                        print("ID de producto no válido.")
                        
                except ValueError:
                    print("Por favor, introduce un número válido.")
                
                input("\nPresiona Enter para continuar...")
            
            if pedido_actual.detalles_temporales:
                print(f"\n📋 Resumen del pedido:")
                print(f"Total del pedido: ${pedido_actual.monto_pedido:,.2f}")
                confirmar = input("¿Confirmar pedido? (si/no): ").lower()
                if confirmar == 'si':
                    pedido_actual.guardar_pedido_completo()
                else:
                    print("Pedido cancelado.")
            else:
                print("\nNo se agregaron productos al pedido.")
            
        except ValueError:
            print("Error: Debes ingresar números válidos.")
        
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "5":
        limpiar_consola()
        Pedido.mostrar_total_en_venta()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "6":
        limpiar_consola()
        print("=== PAGAR PEDIDOS PENDIENTES ===\n")
        
        # Mostrar pedidos pendientes
        pedidos_pendientes = Pedido.listar_pedidos_pendientes()
        
        if pedidos_pendientes:
            try:
                id_pedido = int(input("\nIngrese el ID del pedido a pagar: "))
                Pedido.pagar_pedido(id_pedido)
            except ValueError:
                print("Error: Debes ingresar un número válido.")
        
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "7":
        limpiar_consola()
        print("👋 Saliendo del sistema...")
        print("¡Gracias por usar nuestro sistema!")
        break
    
    else:
        print("❌ Opción inválida. Intenta de nuevo.")
        input("\nPresiona Enter para continuar...")