import sqlite3

class creacion_db:
    
    def __init__(self,nombre_base_de_datos):
        self.nombre_base_de_datos=nombre_base_de_datos
        
    def conexion(self):
        self.cursor=sqlite3.connect(self.nombre_base_de_datos)
        return self.cursor
    
    def guardar(self):
        self.cursor.commit()
        
    def cerrar(self):
        self.cursor.close()

class tablas:
    
    def __init__(self,cursor):
        self.cursor=cursor
        
    def tabla_libros(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Libros (libro_id INTEGER PRIMARY KEY,
                Título TEXT VARCHAR(100),
                Autor TEXT VARCHAR(100))''')
        
    def tabla_usuarios(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (usuario_id INTEGER PRIMARY KEY,
                Nombre TEXT VARCHAR(100) not null,
                Email TEXT VARCHAR(100) unique)''')
        
    def tabla_prestamos(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Préstamos (id_prestamo INTEGER PRIMARY KEY autoincrement,
                libro_id INTEGER, usuario_id INTEGER,
                foreign key (usuario_id)
                references Usuarios (usuario_id)
                foreign key (libro_id)
                references Libros (libro_id))''')
        
class manipular_tablas:
    
    def __init__(self,cursor):
        self.cursor=cursor
        
    def ingreso_de_datos(self,lista_usuarios,lista_libros,lista_prestamos):
        self.cursor.executemany('''INSERT INTO Usuarios VALUES (NULL,?,?)''',lista_usuarios)
        
        self.cursor.executemany('''INSERT INTO Libros VALUES (NULL,?,?)''',lista_libros)
        
        self.cursor.executemany('''INSERT INTO Préstamos VALUES (NULL,?,?)''',lista_prestamos)

    def insert_libros(self,tupla_libros):
        self.cursor.execute('''INSERT INTO Libros VALUES (NULL,?,?)''',tupla_libros)
        
    def insert_usuario(self,tupla_usuario):
        self.cursor.execute('''INSERT INTO Usuarios VALUES(NULL,?,?)''',tupla_usuario)
        
    def insert_prestamo(self,tupla_prestamo):
        self.cursor.execute('''INSERT INTO Préstamos VALUES(NULL,?,?)''',tupla_prestamo)
        
    def actualizar_datos_libros(self,tupla_actualizar_libro):
        self.cursor.execute('''UPDATE Libros SET Título=?, Autor=? WHERE Título=?''',tupla_actualizar_libro)
        
    def actualizar_datos_usuarios(self,tupla_actualizar_usuario):
        self.cursor.execute('''UPDATE Usuarios SET Nombre=?, Email=? WHERE Email=?''',tupla_actualizar_usuario)
        
    def borrar_datos_usuario(self,Email):
        self.cursor.execute('''DELETE FROM Usuarios WHERE Email=?''',(Email,))
        
    def borrar_datos_libros(self,titulo):
        self.cursor.execute('''DELETE FROM Libros WHERE Título=?''',(titulo,))
    
    def borrar_datos_prestamos(self,titulo_borrar):
        self.cursor.execute('''DELETE FROM Préstamos WHERE libro_id=?''')
        
        self.borrar_datos_prestamos('''DELETE FROM Préstamos WHERE usuario_id=?''')    

#Aquí inicia la última parte de la práctica   
class consulta_de_informacion():
    
    def __init__(self,cursor):
        self.cursor=cursor
        
    def consulta_prestamos(self):
        resultado_consulta=self.cursor.execute('''SELECT Libros.Título, Préstamos.libro_id FROM Libros
                            INNER JOIN Préstamos ON Libros.libro_id=Préstamos.libro_id''')
        
        resultado_consulta_2=self.cursor.execute('''SELECT Usuarios.Nombre, Usuarios.Email, Préstamos.usuario_id 
                            FROM Usuarios INNER JOIN Préstamos ON Usuarios.usuario_id=Préstamos.usuario_id''')

        print('\nLibros préstados:',resultado_consulta.fetchall())
        print('\nUsuarios que tomaron prestados los libros:',resultado_consulta_2.fetchall())
        
    def consulta_no_prestamos(self):
        #este join da este error, no such column Prestamos.libro_id
        consulta_no_prestamos=self.cursor.execute('''SELECT Libros.Título, Libros.libro_id, Préstamos.libro_id FROM Libros
                            INNER JOIN Préstamos ON Libros.libro_id=Prestamos.libro_id 
                            WHERE Préstamos.libro_id IS NULL ''')
        
        print('\nResultado consulta no prestados:',consulta_no_prestamos.fetchall())
        

print('\nEste programa permite crear una base de datos básica y también permite insertar algunos datos en las tablas.')

#Este bloque de código es para ingresar automanticamente varios datos

instancia_creacion_db=creacion_db('Biblioteca')
instancia_creacion_db.conexion()
instancia_tablas=tablas(instancia_creacion_db.conexion())
instancia_tablas.tabla_libros()
instancia_tablas.tabla_prestamos()
instancia_tablas.tabla_usuarios()
instancia_insertar=manipular_tablas(instancia_creacion_db.conexion())

lista_usuarios=[('Juan Pérez','juan.perez@example.com'),
    ('María Rodríguez','maria.rodriguez@example.com'),
    ('Carlos González','carlos.gonzalez@example.com'),
    ('Ana Martínez','ana.martinez@example.com'),
    ('José López','jose.lopez@example.com'),
    ('Patricia García','patricia.garcia@example.com'),
    ('Luis Torres','luis.torres@example.com'),
    ('Carmen Morales','carmen.morales@example.com'),
    ('Francisco Herrera','francisco.herrera@example.com'),
    ('Teresa Guzmán','teresa.guzman@example.com')]

lista_libros=[('Don Quijote de la Mancha','Miguel de Cervantes'),
    ('Cien años de soledad','Gabriel García Márquez'),
    ('El señor de los anillos','J. R. R. Tolkien'),
    ('1984','George Orwell'),
    ('Un mundo feliz','Aldous Huxley'),
    ('Orgullo y prejuicio','Jane Austen'),
    ('El Código da Vinci','Dan Brown'),
    ('Harry Potter y la orden del fénix','J.K. Rowling'),
    ('El Alquimista','Paulo Coelho'),
    ('El último mohicano','James Fenimore Cooper')]

lista_prestamos=[(1, 10),
    (2, 1),
    (3, 9),
    (4, 2),
    (9, 6),
    (10, 5)]

instancia_insertar.ingreso_de_datos(lista_usuarios,lista_libros,lista_prestamos)
instancia_creacion_db.guardar()
instancia_creacion_db.cerrar()

#De aquí en adelante es para agregar funcionalidad a la base de datos y hacer lo solicitado
ciclo=True
while ciclo:
    
    inicio=str(input('\n¿Desea continuar? (si/no): '))
    if inicio.lower()=='no':
        input('Presione enter para finalizar.')
        ciclo=False
    
    elif inicio.lower()=='si':
        copia_lista_usuarios=lista_usuarios
        copia_lista_libros=lista_libros
    
        try:
            instancia_creacion_db=creacion_db('Biblioteca')
            instancia_creacion_db.conexion()
            instancia_tablas=tablas(instancia_creacion_db.conexion())
            instancia_tablas.tabla_libros()
            instancia_tablas.tabla_prestamos()
            instancia_tablas.tabla_usuarios()
            
            instancia_insertar=manipular_tablas(instancia_creacion_db.conexion())
            libro=str(input('\nIngrese el título de un libro: '))
            autor=str(input('Ingrese el autor: '))
            usuario=str(input('\nIngrese el nombre del usuario: '))
            correo_usuario=str(input('Ingrese el correo del usuario: '))
            
            instancia_insertar.insert_libros((libro,autor))
            instancia_insertar.insert_usuario((usuario,correo_usuario))
            instancia_creacion_db.guardar()
            instancia_creacion_db.cerrar()
            
            input('\nDatos ingresados con éxito, presione enter para continuar.')
            
            instancia_insertar=manipular_tablas(instancia_creacion_db.conexion())
            pregunta=str(input('\n¿Desea actualizar la información de algun libro? (si/no): '))
            if pregunta.lower()=='no':
                pass
            elif pregunta.lower()=='si':
                titulo=str(input('\nIngrese el título del libro a actualizar: '))
                nuevo_titulo=str(input('Ingrese el nuevo título: '))
                nuevo_autor=str(input('Ingrese el nuevo autor: '))
                tupla_actualizar_libro=(nuevo_titulo,nuevo_autor,titulo)
                instancia_insertar.actualizar_datos_libros(tupla_actualizar_libro)
                instancia_creacion_db.guardar()
                print('Libro actualizado con éxito.')
                
            pregunta2=str(input('\n¿Desea actualizar la información de algun usuario? (si/no): '))
            if pregunta2.lower()=='no':
                pass
            elif pregunta2.lower()=='si':
                correo=str(input('Ingrese el correo del usuario a actualizar: '))
                nuevo_nombre=str(input('Ingrese el nuevo nombre: '))
                nuevo_correo=str(input('Ingrese el nuevo correo: '))
                tupla_actualizar_usuario=(nuevo_nombre,nuevo_correo,correo)
                instancia_insertar.actualizar_datos_usuarios(tupla_actualizar_usuario)
                instancia_creacion_db.guardar()
                print('Usuario actualizado con éxito.')
                
            pregunta3=str(input('\n¿Desea eliminar algún libro? (si/no): '))
            if pregunta3.lower()=='no':
                pass
            elif pregunta3.lower()=='si':
                titulo_borrar=str(input('Ingrese el título del libro a eliminar: '))
                tupla_borrar_libro=(titulo_borrar)
                instancia_insertar.borrar_datos_libros(tupla_borrar_libro)
                instancia_creacion_db.guardar()
                print('Libro eliminado con éxito.')
                
            pregunta4=str(input('\n¿Desea eliminar a algún usuario? (si/no): '))
            if pregunta4.lower()=='no':
                pass
            elif pregunta4.lower()=='si':
                usuario_borrar=str(input('Ingrese el correo del usuario a eliminar: '))
                tupla_borrar_usuario=(usuario_borrar)
                instancia_insertar.borrar_datos_usuario(tupla_borrar_usuario)
                instancia_creacion_db.guardar()
                print('Usuario eliminado con éxito.')
            
            input('\nPresione enter para continuar.')
        
            print('\nInformación de los préstamos y los libros no prestados aún:')
            instancia_joins=consulta_de_informacion(instancia_creacion_db.conexion())
            instancia_joins.consulta_prestamos()
            print('   ')
            instancia_joins.consulta_no_prestamos()
            
            instancia_creacion_db.guardar()
            instancia_creacion_db.cerrar()
            
        except Exception as error:
            print('\nError en el tipo de dato:',error)
    
    elif inicio.lower()=='no':
        ciclo=False
        input('\nPresione enter para finalizar.')
    
    else:
        print('\nUna de las respuestas es inválida, intente de nuevo.')