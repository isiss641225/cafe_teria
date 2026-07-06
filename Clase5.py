from conexion import Conexion


class Producto:

    def __init__(self, id_producto, nombre_producto, precio_actual, stock, descripcion_producto):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.precio_actual = precio_actual
        self.stock = stock
        self.descripcion_producto = descripcion_producto

    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO productos
        (
            id_producto,
            nombre_producto,
            precio_actual,
            stock,
            descripcion_producto
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        valores = (
            self.id_producto,
            self.nombre_producto,
            self.precio_actual,
            self.stock,
            self.descripcion_producto
        )

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
        SELECT
            id_producto,
            nombre_producto,
            precio_actual,
            stock
        FROM productos
        WHERE deleted = 0
        ORDER BY nombre_producto ASC
        """

        cursor.execute(sql)
        productos = cursor.fetchall()
        print("\n===== PRODUCTOS =====\n")
        for producto in productos:
            print(
                f"ID: {producto[0]} | "
                f"Nombre: {producto[1]} | "
                f"Precio: {producto[2]} | "
                f"Stock: {producto[3]}"
            )

        cursor.close()
        conexion.close()

    @staticmethod
    def buscar():
        texto = input("Ingrese nombre o parte del nombre: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        SELECT
            id_producto,
            nombre_producto,
            precio_actual,
            stock
        FROM productos
        WHERE nombre_producto LIKE %s
        AND deleted = 0
        ORDER BY nombre_producto ASC
        """

        cursor.execute(sql, ('%' + texto + '%',))

        resultados = cursor.fetchall()
        print("\n===== RESULTADOS =====\n")
        if len(resultados) == 0:
            print("No se encontraron registros.")
        else:
            for producto in resultados:
                print(
                    f"ID: {producto[0]} | "
                    f"Nombre: {producto[1]} | "
                    f"Precio: {producto[2]} | "
                    f"Stock: {producto[3]}"
                )

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar():
        id_producto = input("Ingrese ID del producto: ")
        nuevo_precio = input("Ingrese nuevo precio: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE productos
        SET precio_actual = %s
        WHERE id_producto = %s
        """

        valores = (nuevo_precio, id_producto)
        cursor.execute(sql, valores)
        conexion.commit()
        print("\nPrecio actualizado correctamente.")

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
        WHERE id_producto = %s
        """

        cursor.execute(sql, (id_producto,))
        conexion.commit()
        print("\nProducto eliminado correctamente.")
        cursor.close()
        conexion.close()