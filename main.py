import os
# Importamos todas las clases necesarias de sus respectivos archivos
from Clase1 import TipoUsuario
from Clase2 import Usuario
from Clase3 import TipoPedido
from Clase4 import Producto
from Clase5 import Pedido
from Clase6 import DetallePedido

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# =====================================================================
#        SISTEMA DE MENÚ INTERACTIVO (BUCLE WHILE)
# =====================================================================

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
        # Llamamos al método estático de Producto para listar desde la BD
        Producto.listar()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "2":
        limpiar_consola()
        print("=== REGISTRAR NUEVO USUARIO ===")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        correo = input("Correo electrónico: ")
        username = input("Nombre de usuario (username): ")
        password = input("Contraseña: ")
        edad = int(input("Edad: "))
        
        # Mostramos los roles disponibles para que elija un ID válido
        TipoUsuario.listar()
        id_tipo_usuario = int(input("\nSeleccione el ID del Tipo de Usuario para este registro: "))
        
        # Instanciamos el objeto con los datos capturados
        nuevo_usuario = Usuario(nombre, apellido, correo, username, password, edad, id_tipo_usuario)
        # Guardamos en la base de datos
        nuevo_usuario.guardar()
        
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "3":
        limpiar_consola()
        # Llamamos al método estático de Usuario para listar desde la BD
        Usuario.listar()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "4":
        limpiar_consola()
        print("=== CREANDO NUEVO PEDIDO ===")
        
        # Para crear un pedido requerimos asociarlo a un usuario y a un tipo de pedido
        Usuario.listar()
        id_cliente = input("\nIngresa el ID del usuario que realiza la compra: ")
        
        TipoPedido.listar()
        id_tipo_p = input("\nIngresa el ID del tipo de pedido: ")
        
        # Inicializamos el objeto Pedido
        pedido_actual = Pedido(id_usuario=id_cliente, id_tipo_pedido=id_tipo_p)
        
        limpiar_consola()
        while True:
            print("--- PRODUCTOS DISPONIBLES ---")
            Producto.listar()
            
            try:
                id_prod = int(input("\nIngresa el ID del producto (0 para terminar de añadir productos): "))
                if id_prod == 0:
                    break
                
                cant = int(input("¿Cuántas unidades?: "))
                if cant <= 0:
                    print("La cantidad debe ser mayor a 0.")
                    input("\nPresiona Enter para continuar...")
                    limpiar_consola()
                    continue
                
                precio = float(input("Confirme el precio unitario actual de este producto: $"))
                notas = input("Notas o descripción para este producto (opcional): ")
                
                # Agregamos el producto a la lista temporal del objeto pedido
                pedido_actual.agregar_producto(id_prod, cant, precio, notas if notas else "Sin notas")
                
            except ValueError:
                print("Por favor, introduce un dato válido.")
            
            input("\nPresiona Enter para continuar cargando productos...")
            limpiar_consola()

        # Al terminar el bucle, verificamos si se agregaron elementos a la lista temporal
        if len(pedido_actual.detalles_temporales) > 0:
            print(f"\nEl total acumulado del pedido es: ${pedido_actual.monto_pedido}")
            confirmar = input("¿Deseas guardar este pedido en la base de datos? (si/no): ").lower()
            
            if confirmar == 'si':
                # Al guardar el pedido completo, la clase genera el ID en la BD y vacía los detalles temporales
                # Nota: Modifiqué tu Clase 5 internamente para simular el comportamiento. Aquí se guarda.
                
                # Para poder pagar, necesitamos ejecutar primero el guardado que hace el commit de la cabecera y el detalle.
                # Tu método guardar_pedido_completo no retorna el ID directamente al main, pero imprime el éxito.
                # Como el método pagar_pedido requiere un ID, simularemos la confirmación final:
                
                # Guardamos en la base de datos (por defecto queda 'Pendiente')
                pedido_actual.guardar_pedido_completo()
                
                pagar = input("\n¿Deseas marcar este pedido como PAGADO inmediatamente? (si/no): ").lower()
                if pagar == 'si':
                    id_a_pagar = input("Por favor, repita el ID del Pedido recién generado que se muestra arriba: ")
                    Pedido.pagar_pedido(id_a_pagar)
            else:
                print("Pedido descartado. No se guardó nada en la base de datos.")
        else:
            print("\nNo se agregaron productos al pedido.")
            
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "5":
        limpiar_consola()
        # Llamamos al método estático para traer la sumatoria de la BD
        Pedido.mostrar_total_en_venta()
        input("\nPresiona Enter para volver al menú...")

    elif opcion == "6":
        limpiar_consola()
        print("Saliendo del sistema...")
        break
    
    else:
        print("Opción inválida. Intenta de nuevo.")
        input("\nPresiona Enter para continuar...")