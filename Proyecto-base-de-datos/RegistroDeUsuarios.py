import mysql.connector
from mysql.connector import Error
import getpass
import hashlib
from Dectectarpulgar import detectar_pulgar_arriba 

DB_HOST = 'localhost'
DB_NAME = 'proyectobasededatosuep'
DB_USER = 'root'
DB_PASSWORD = 'contraseñaultrasecretabasededatos' 


def registrar_estudiante():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    matricula = input("Matrícula: ")
    email = input("Email: ")
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ") 
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    gesto_detectado = detectar_pulgar_arriba()
    
    if not gesto_detectado:
        return

    conexion = None
    usuario_id = None
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexion.cursor()
        
        sql_usuario = "INSERT INTO usuarios (username, password_hash, rol) VALUES (%s, %s, %s)"
        cursor.execute(sql_usuario, (username, password_hash, 'Estudiante'))
        
        usuario_id = cursor.lastrowid
        
        sql_estudiante = """
        INSERT INTO estudiantes (usuario_id, matricula, nombre, apellido, email) 
        VALUES (%s, %s, %s, %s, %s)
        """
        datos_estudiante = (usuario_id, matricula, nombre, apellido, email)
        cursor.execute(sql_estudiante, datos_estudiante)
        
        conexion.commit()

    except Error:
        if usuario_id:
             try:
                 cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                 conexion.commit()
             except:
                 pass
        pass

    finally:
        if 'conexion' in locals() and conexion and conexion.is_connected():
            if 'cursor' in locals() and cursor:
                cursor.close()
            conexion.close()

if __name__ == "__main__":
    registrar_estudiante()