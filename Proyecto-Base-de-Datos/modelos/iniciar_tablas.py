
import mysql.connector
from mysql.connector import Error
from modelos.conexion_BD import obtener_conexion_db

class IniciarTablas:


    def inicializar_tablas(self):
 
        conexion = obtener_conexion_db()
        
        if not conexion:
            print("🔴 No se pudo inicializar las tablas debido a un error de conexión.")
            return

        cursor = None
        try:
            cursor = conexion.cursor()
            

            sql_usuarios = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                rol VARCHAR(20) NOT NULL
            );
            """
            cursor.execute(sql_usuarios)

            sql_profesores = """
            CREATE TABLE IF NOT EXISTS profesores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL UNIQUE,
                nombre VARCHAR(100) NOT NULL,      
                departamento VARCHAR(100),         
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
            """
            cursor.execute(sql_profesores)
            
            sql_administradores = """
            CREATE TABLE IF NOT EXISTS administradores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL UNIQUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
            """
            cursor.execute(sql_administradores)

            sql_estudiantes = """
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL UNIQUE,
                matricula VARCHAR(20) UNIQUE,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
            """
            cursor.execute(sql_estudiantes)


            sql_votos = """
            CREATE TABLE IF NOT EXISTS votos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT NOT NULL UNIQUE,
                profesor_id INT NOT NULL,
                voto INT NOT NULL DEFAULT 1, 
                fecha_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                FOREIGN KEY (profesor_id) REFERENCES profesores(id)
            );
            """
            cursor.execute(sql_votos)
            
            conexion.commit()
            print(" Tablas de la Base de Datos verificadas/creadas con éxito.")

        except Error as e:
            print(f" Error al crear/verificar tablas: {e}")
            if conexion:
                conexion.rollback()

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()