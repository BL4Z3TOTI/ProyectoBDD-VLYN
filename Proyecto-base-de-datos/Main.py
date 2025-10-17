import mysql.connector
from mysql.connector import Error

DB_HOST = 'localhost'
DB_NAME = 'proyectobasededatosuep'
DB_USER = 'root'
DB_PASSWORD = 'contraseñaultrasecretabasededatos' 

def crear_tablas_uep():
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        if conexion.is_connected():
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
                estudiante_id INT NOT NULL,
                profesor_id INT NOT NULL,
                voto INT NOT NULL CHECK (voto >= 1 AND voto <= 5),
                fecha_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                FOREIGN KEY (profesor_id) REFERENCES profesores(id),
                UNIQUE KEY unique_voto (estudiante_id, profesor_id)
            );
            """
            cursor.execute(sql_votos)
            
            conexion.commit()

    except Error:
        pass

    finally:
        if 'conexion' in locals() and conexion and conexion.is_connected():
            if 'cursor' in locals() and cursor:
                cursor.close()
            conexion.close()

if __name__ == "__main__":
    crear_tablas_uep()
