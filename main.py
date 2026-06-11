import os
from conexion import Conexion
from Clase1 import TipoUsuario
from Clase2 import Usuario
from Clase3 import Producto
from Clase4 import Pedido

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    limpiar_consola()
    print("=========================================")
    print("      SISTEMA DE GESTIÓN DE CAFETERÍA     ")
    print("=========================================")
    print("1. Ver inventario de productos")
    print("2. Agregar nuevo producto")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Registrar nuevo usuario")
    print("6. Ver lista de usuarios")
    print("7. Crear un nuevo pedido")
    print("8. Ver pedidos pendientes")
    print("9. Pagar pedido")
    print("10. Ver total de ventas")
    print("11. Salir")
    print("=========================================")
    
    opcion = input("Selecciona una opción (1-11): ")
    
    # ========== CRUD PRODUCTO ==========
    
    if opcion == "1":  # READ
        limpiar_consola()
        Producto.listar()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "2":  # CREATE
        limpiar_consola()
        print("=== AGREGAR NUEVO PRODUCTO ===\n")
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio: $"))
        stock = int(input("Stock: "))
        descripcion = input("Descripción: ")
        
        producto = Producto(nombre, precio, stock, descripcion)
        producto.guardar()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "3":  # UPDATE
        limpiar_consola()
        Producto.listar()
        print("\n=== ACTUALIZAR PRODUCTO ===\n")
        Producto.actualizar()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "4":  # DELETE
        limpiar_consola()
        Producto.listar()
        print("\n=== ELIMINAR PRODUCTO ===\n")
        Producto.eliminar()
        input("\nPresiona Enter para volver al menú...")
    
    # ========== USUARIOS ==========
    
    elif opcion == "5":
        limpiar_consola()
        print("=== REGISTRAR NUEVO USUARIO ===\n")
        
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
    
    elif opcion == "6":
        limpiar_consola()
        Usuario.listar()
        input("\nPresiona Enter para volver al menú...")
    
    # ========== PEDIDOS ==========
    
    elif opcion == "7":
        limpiar_consola()
        print("=== CREAR NUEVO PEDIDO ===\n")
        
        Usuario.listar()
        id_usuario = int(input("\nID del usuario: "))
        id_tipo_pedido = int(input("ID del tipo de pedido (1: Local, 2: Delivery): "))
        
        pedido_actual = Pedido(id_usuario, id_tipo_pedido)
        
        while True:
            limpiar_consola()
            print("=== AGREGAR PRODUCTOS ===\n")
            Producto.listar()
            
            try:
                id_prod = int(input("\nID del producto (0 para terminar): "))
                if id_prod == 0:
                    break
                
                conexion = Conexion.conectar()
                cursor = conexion.cursor()
                cursor.execute("SELECT precio_actual, stock FROM productos WHERE id_producto = %s AND deleted = 0", (id_prod,))
                producto = cursor.fetchone()
                cursor.close()
                conexion.close()
                
                if producto:
                    precio = float(producto[0])
                    stock = int(producto[1])
                    
                    cantidad = int(input(f"Cantidad (stock: {stock}): "))
                    if cantidad <= 0:
                        print("Cantidad debe ser mayor a 0.")
                    elif cantidad > stock:
                        print(f"Stock insuficiente. Solo hay {stock}.")
                    else:
                        pedido_actual.agregar_producto(id_prod, cantidad, precio)
                else:
                    print("Producto no válido.")
                    
            except ValueError:
                print("Ingrese un número válido.")
            
            input("\nPresiona Enter para continuar...")
        
        if pedido_actual.detalles_temporales:
            print(f"\nTotal: ${pedido_actual.monto_pedido}")
            confirmar = input("¿Confirmar pedido? (si/no): ").lower()
            if confirmar == 'si':
                pedido_actual.guardar_pedido_completo()
            else:
                print("Pedido cancelado.")
        else:
            print("No se agregaron productos.")
        
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "8":
        limpiar_consola()
        Pedido.listar_pedidos_pendientes()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "9":
        limpiar_consola()
        Pedido.listar_pedidos_pendientes()
        try:
            id_pedido = int(input("\nID del pedido a pagar: "))
            Pedido.pagar_pedido(id_pedido)
        except ValueError:
            print("Ingrese un número válido.")
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "10":
        limpiar_consola()
        Pedido.mostrar_total_en_venta()
        input("\nPresiona Enter para volver al menú...")
    
    elif opcion == "11":
        limpiar_consola()
        print("Saliendo del sistema...")
        break
    
    else:
        print("Opción inválida.")
        input("\nPresiona Enter para continuar...")