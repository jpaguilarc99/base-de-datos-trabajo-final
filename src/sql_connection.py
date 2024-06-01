import pyodbc
import os
import cmd

from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver= os.getenv('DB_DRIVER')

try:
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()    
    print("Conexión exitosa a la base de datos\n")    
except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    print(sqlstate)

def insert_into_table(table_name, column_names, values):
    cursor.execute(f"SELECT MAX({column_names[0]}) FROM {table_name}")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1
    placeholders = ', '.join('?' * (len(column_names)))
    cursor.execute(f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})", new_id, *values)
    connection.commit()

class DatabaseShell(cmd.Cmd):
    intro = """
    #################################################################################################################
    Bienvenido a la base de datos de registro y consulta para la Biblioteca. Escribe help o ? para listar comandos.
    #################################################################################################################\n"""
    prompt = '(Biblioteca -> Acción a realizar:) '

    def do_add_autor(self, line):
        """Agrega un nuevo autor a la base de datos"""
        nombre_autor = input("Nombre del autor: ")
        iniciales_autor = input("Iniciales del autor: ")
        pais_autor = input("País del autor: ")
        insert_into_table("Autor", ["id_autor", "nombre_autor", "iniciales_autor", "pais_autor"], [nombre_autor, iniciales_autor, pais_autor])        
        print("Autor agregado exitosamente")

    def do_query_autor(self, line):
        """Consulta los autores en la base de datos"""
        cursor.execute("SELECT * FROM Autor")
        for row in cursor:
            print(row)

    def do_add_editorial(self, line):
        """Agrega una nueva editorial a la base de datos"""
        nombre_editorial = input("Nombre de la editorial: ")
        pais_editorial = input("País de la editorial: ")
        tipo_editorial = input("Tipo de la editorial: ")        
        insert_into_table("Editorial", ["id_editorial", "nombre_editorial", "pais_editorial", "tipo_editorial"], [nombre_editorial, pais_editorial, tipo_editorial])
        print("Editorial agregada exitosamente")

    def do_query_editorial(self, line):
        """Consulta las editoriales en la base de datos"""
        cursor.execute("SELECT * FROM Editorial")
        for row in cursor:
            print(row)

    def do_add_programa(self, line):
        """Agrega un nuevo programa a la base de datos"""
        nombre_programa = input("Nombre del programa: ")
        insert_into_table("Programa", ["id_programa", "nombre_programa"], [nombre_programa])
        print("Programa agregado exitosamente")

    def do_query_programa(self, line):
        """Consulta los programas en la base de datos"""
        cursor.execute("SELECT * FROM Programa")
        for row in cursor:
            print(row)

    def do_add_material(self, line):
        """Agrega un nuevo material a la base de datos"""
        id_autor = input("ID del autor: ")
        id_editorial = input("ID de la editorial: ")
        año_publicacion = input("Año de publicación: ")
        tipo = input("Tipo de material: ")
        dias_prestamo = input("Días de préstamo: ")
        ISBN = input("ISBN: ")
        insert_into_table("Material", ["id_material", "id_autor", "id_editorial", "año_publicacion", "tipo", "dias_prestamo", "ISBN"], [id_autor, id_editorial, año_publicacion, tipo, dias_prestamo, ISBN])
        print("Material agregado exitosamente")

    def do_query_material(self, line):
        """Consulta los materiales en la base de datos"""
        cursor.execute("SELECT * FROM Material")
        for row in cursor:
            print(row)

    def do_add_estudiante(self, line):
        """Agrega un nuevo estudiante a la base de datos"""
        id_programa = input("ID del programa: ")
        nombre_estudiante = input("Nombre del estudiante: ")
        apellido_estudiante = input("Apellido del estudiante: ")
        email = input("Email del estudiante: ")
        telefono = input("Teléfono del estudiante: ")
        insert_into_table("Estudiante", ["id_estudiante", "id_programa", "nombre_estudiante", "apellido_estudiante", "email", "telefono"], [id_programa, nombre_estudiante, apellido_estudiante, email, telefono])
        print("Estudiante agregado exitosamente")

    def do_query_estudiante(self, line):
        """Consulta los estudiantes en la base de datos"""
        cursor.execute("SELECT * FROM Estudiante")
        for row in cursor:
            print(row)    

    def do_add_prestamo(self, line):
        """Agrega un nuevo préstamo a la base de datos"""
        id_material = input("ID del material: ")
        id_estudiante = input("ID del estudiante: ")
        fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), '%Y-%m-%d')
        fecha_final = datetime.strptime(input("Fecha final (YYYY-MM-DD): "), '%Y-%m-%d')
        dias_prestamo = int(input("Días de préstamo: "))
        perdido = input("Perdido (0 para no, 1 para sí): ")

        dias_transcurridos = (fecha_final - fecha_inicio).days
        valor_mora = 0
        if dias_transcurridos > dias_prestamo:
            valor_mora = (dias_transcurridos - dias_prestamo) * 500  # Se asume que la mora es de 500 por día

        if perdido == '1':
            valor_mora += 20000  # Se añade una multa de 20000 si el libro se perdió

        insert_into_table("Prestamo", ["id_prestamo", "id_material", "id_estudiante", "fecha_inicio", "fecha_final", "dias_prestamo", "valor_mora", "perdido"], [id_material, id_estudiante, fecha_inicio.strftime('%Y-%m-%d'), fecha_final.strftime('%Y-%m-%d'), dias_prestamo, valor_mora, perdido])
        print("Préstamo agregado exitosamente")

    def do_query_prestamo(self, line):
        """Consulta los préstamos en la base de datos"""
        cursor.execute("SELECT * FROM Prestamo")
        for row in cursor:
            print(row)    

    def do_query_materialxautor(self, line):
        """Consulta las relaciones Material-Autor en la base de datos"""
        cursor.execute("SELECT * FROM MaterialXAutor")
        for row in cursor:
            print(row)    

    def do_query_editorialxmaterial(self, line):
        """Consulta las relaciones Editorial-Material en la base de datos"""
        cursor.execute("SELECT * FROM EditorialXMaterial")
        for row in cursor:
            print(row)

    def do_add_area(self, line):
        """Agrega una nueva área a la base de datos"""
        nombre_area = input("Nombre del área: ")
        descripcion_area = input("Descripción del área: ")
        id_material = input("ID del material: ")
        insert_into_table("Area", ["id_area", "nombre_area", "descripcion_area", "id_material"], [nombre_area, descripcion_area, id_material])
        print("Área agregada exitosamente")

    def do_query_area(self, line):
        """Consulta las áreas en la base de datos"""
        cursor.execute("SELECT * FROM Area")
        for row in cursor:
            print(row)

    def do_exit(self, line):
        """Salir del programa"""
        return True
    
if __name__ == '__main__':
    DatabaseShell().cmdloop()