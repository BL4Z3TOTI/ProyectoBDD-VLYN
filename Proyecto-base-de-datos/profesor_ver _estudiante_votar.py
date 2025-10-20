import mysql.connector
from mysql.connector import errorcode


DB_HOST = "localhost"
DB_USER = "root" 
DB_PASSWORD = "contraseñaultrasecretabasededatos"
DB_NAME = "proyectobasededatosuep"


def get_db_connection():
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return cnx
    except mysql.connector.Error as err:
        print("\n--- ERROR DE CONEXIÓN ---")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"La base de datos '{DB_NAME}' no existe. Ejecuta 'Main.py' primero.")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Acceso denegado. Revisa tu usuario y contraseña de MySQL.")
        else:
            print(err)
        return None

def ver_estudiantes_que_votaron(profesor_id):

    cnx = get_db_connection()
    if not cnx:
        return

    cursor = cnx.cursor(dictionary=True)
    try:
        check_prof_query = "SELECT nombre FROM profesores WHERE id = %s"
        cursor.execute(check_prof_query, (profesor_id,))
        profesor = cursor.fetchone()

        if not profesor:
            print(f"\nError: No se encontró un profesor con ID {profesor_id}.")
            return
            
        print(f"\n--- ESTUDIANTES QUE VOTARON POR EL PROFESOR {profesor['nombre'].upper()} ---")

        query = """
            SELECT 
                e.nombre, 
                e.apellido, 
                e.matricula, 
                u.username 
            FROM votos v
            JOIN estudiantes e ON v.estudiante_id = e.id
            JOIN usuarios u ON e.usuario_id = u.id
            WHERE v.profesor_id = %s
            ORDER BY e.apellido, e.nombre;
        """
        cursor.execute(query, (profesor_id,))
        estudiantes_votantes = cursor.fetchall()

        if not estudiantes_votantes:
            print(f"El profesor {profesor['nombre']} aún no ha recibido votos.")
            return

        print(f"{'MATRÍCULA':<15}{'USUARIO':<15}{'NOMBRE COMPLETO':<40}")
        print("-" * 70)
        for estudiante in estudiantes_votantes:
            nombre_completo = f"{estudiante['nombre']} {estudiante['apellido']}"
            print(f"{estudiante['matricula']:<15}{estudiante['username']:<15}{nombre_completo:<40}")
        print("-" * 70)
        print(f"Total de votantes: {len(estudiantes_votantes)}")


    except mysql.connector.Error as err:
        print(f"Error al obtener votantes: {err}")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


if __name__ == '__main__':
    
    print("Simulación de visualización de votos para el Profesor con ID = 1")
    ver_estudiantes_que_votaron(profesor_id=1)