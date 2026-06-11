from conexion import Conexion

class Producto:
    def __init__(self, nombre_producto, precio_actual, stock, descripcion_producto, id_producto=None):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.precio_actual = precio_actual
        self.stock = stock
        self.descripcion_producto = descripcion_producto

    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
        INSERT INTO productos (nombre_producto, precio_actual, stock, descripcion_producto)
        VALUES (%s, %s, %s, %s)
        """
        
        valores = (self.nombre_producto, self.precio_actual, self.stock, self.descripcion_producto)
        cursor.execute(sql, valores)
        conexion.commit()
        print("\nProducto agregado correctamente.")
        cursor.close()
        conexion.close()

    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
        SELECT id_producto, nombre_producto, precio_actual, stock
        FROM productos
        WHERE deleted = 0
        ORDER BY nombre_producto ASC
        """
        
        cursor.execute(sql)
        productos = cursor.fetchall()
        
        print("\n===== PRODUCTOS =====\n")
        for producto in productos:
            print(f"ID: {producto[0]} | Nombre: {producto[1]} | "
                  f"Precio: ${producto[2]} | Stock: {producto[3]}")
        
        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():
        id_producto = input("Ingrese ID del producto: ")
        nuevo_precio = input("Ingrese nuevo precio: ")
        nuevo_stock = input("Ingrese nuevo stock: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
        UPDATE productos
        SET precio_actual = %s,
            stock = %s
        WHERE id_producto = %s AND deleted = 0
        """
        
        valores = (nuevo_precio, nuevo_stock, id_producto)
        cursor.execute(sql, valores)
        conexion.commit()
        
        if cursor.rowcount > 0:
            print("\nProducto actualizado correctamente.")
        else:
            print("\nNo se encontró el producto.")
        
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar():
        id_producto = input("Ingrese ID del producto: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
        UPDATE productos
        SET deleted = 1
        WHERE id_producto = %s AND deleted = 0
        """
        
        cursor.execute(sql, (id_producto,))
        conexion.commit()
        
        if cursor.rowcount > 0:
            print("\nProducto eliminado correctamente.")
        else:
            print("\nNo se encontró el producto.")
        
        cursor.close()
        conexion.close()