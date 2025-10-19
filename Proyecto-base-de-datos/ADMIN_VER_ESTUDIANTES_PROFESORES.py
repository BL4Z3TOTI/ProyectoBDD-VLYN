import mysql.connector
from mysql.connector import Error
from Main import crear_tablas_uep # Importamos la función de Main.py

DB_HOST = 'localhost'
DB_NAME = 'proyectobasededatosuep'
DB_USER = 'root'
DB_PASSWORD = 'contraseñaultrasecretabasededatos' 

def ver_todos_para_admin():
    
    conexion = None
    cursor = None # Inicializar cursor fuera del try para el finally
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT e.id, e.nombre, e.apellido, e.matricula, e.email, u.username
                FROM estudiantes e
                JOIN usuarios u ON e.usuario_id = u.id;
            """)
            estudiantes = cursor.fetchall()

            cursor.execute("""
                SELECT p.id, p.nombre, p.departamento, u.username
                FROM profesores p
                JOIN usuarios u ON p.usuario_id = u.id;
            """)
            profesores = cursor.fetchall()

            return estudiantes, profesores

    except Error as e:
        print("Error al obtener datos:", e)
        return [], []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexion' in locals() and conexion and conexion.is_connected():
            conexion.close()


if __name__ == "__main__":

    crear_tablas_uep() 

    estudiantes, profesores = ver_todos_para_admin()

    print("=== Estudiantes ===")
    if estudiantes:
        for e in estudiantes:
            print(f"ID: {e['id']}, Nombre: {e['nombre']} {e['apellido']}, Matrícula: {e['matricula']}, Email: {e['email']}, Usuario: {e['username']}")
    else:
        print("No hay estudiantes registrados.")

    print("\n=== Profesores ===")
    if profesores:
        for p in profesores:
            print(f"ID: {p['id']}, Nombre: {p['nombre']}, Departamento: {p['departamento']}, Usuario: {p['username']}")
    else:
        print("No hay profesores registrados.")
