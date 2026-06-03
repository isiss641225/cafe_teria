import os # --> ejecuta comandos en consola
def limpiar_consola(): # limpian consola del terminal
    os.system('cls')

        # =====================================================================
#        SISTEMA DE MENÚ INTERACTIVO (BUCLE WHILE)
# =====================================================================

# Datos base iniciales obligatorios para que el sistema funcione
# rol_admin = TipoUsuario("Administrador", "Acceso total")
# usuario_base = Usuario("Sebastian Anabalon", "seba@cafe.com", "seba_admin", "7777", 30, rol_admin)
# empleado_base = Empleado("Carlos A.", usuario_base)
# tipo_entrega = TipoPedido("Local")

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
        #Producto.mostrar_productos_y_valores()
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
        #Usuario(nombre, correo, username, password, edad, rol_admin)
        print("\nUsuario registrado con éxito!")
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "3":
        limpiar_consola()
        #Usuario.mostrar_usuarios()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "4":
        limpiar_consola()
        print("=== CREANDO NUEVO PEDIDO ===")
        # Inicializamos un pedido vacío
        #pedido_actual = Pedido(empleado_base, tipo_entrega)
        
        while True:
            #Producto.mostrar_productos_y_valores()
            try:
                id_prod = int(input("\nIngresa el ID del producto que deseas llevar (0 para terminar el pedido): "))
                if id_prod == 0:
                    break
                
                #if id_prod in Producto.inventario_preestablecido:
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
        #if pedido_actual.monto_pedido > 0:
            #print(f"\nEl total del pedido es: ${pedido_actual.monto_pedido}")
            pagar = input("¿Deseas confirmar el pago de este pedido? (si/no): ").lower()
            if pagar == 'si':
                #pedido_actual.pagar_pedido()
                print("Pedido pagado con éxito y registrado en el historial!")
            else:
                print("Pedido cancelado (se devolvió el stock de este menú simulado)")
        else:
            print("\nNo se agregaron productos al pedido.")
            
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "5":
        limpiar_consola()
       #Pedido.mostrar_total_en_venta()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "6":
        limpiar_consola()
        print("Saliendo del sistema...")
        break
    
    else:
        print("Opción inválida. Intenta de nuevo.")
        input("\nPresiona Enter para continuar...")