import mysql.connector
from mysql.connector import errorcode
import getpass 

DB_HOST = "localhost"
DB_USER = "root" 
DB_PASSWORD = "12345678"
DB_NAME = "votos_profes"

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
        print("--------------------------")
        return None

def list_professors(cursor):
    query = "SELECT id, nombre, departamento FROM profesores ORDER BY nombre"
    cursor.execute(query)
    profesores = cursor.fetchall()

    if not profesores:
        print("\nNo hay profesores en la base de datos. Pídele al administrador que los agregue.")
        return None

    print("\n--- PROFESORES DISPONIBLES ---")
    for (id, nombre, departamento) in profesores:
        print(f"[{id}] {nombre} ({departamento})")
    print("------------------------------")
    return profesores

def cast_vote(cnx, cursor):
    print("\n--- EMITIR VOTO ---")
    student_id = input("Ingresa tu ID de estudiante (ej. 'A0012345'): ").strip()
    if not student_id:
        print("ID de estudiante no puede estar vacío.")
        return

    check_query = "SELECT profesor_id FROM votos WHERE estudiante_id = %s"
    cursor.execute(check_query, (student_id,))
    if cursor.fetchone():
        print(f"Lo siento, el estudiante con ID '{student_id}' ya ha votado.")
        return


    profesores = list_professors(cursor)
    if not profesores:
        return

    while True:
        try:
            profesor_id = int(input("Ingresa el NÚMERO del profesor por el que quieres votar: "))
            valid_ids = [p[0] for p in profesores]
            if profesor_id in valid_ids:
                break
            else:
                print("ID de profesor no válido. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")

    try:
        insert_vote_query = "INSERT INTO votos (profesor_id, estudiante_id) VALUES (%s, %s)"
        cursor.execute(insert_vote_query, (profesor_id, student_id))
        cnx.commit()
        print("\n¡Voto registrado con éxito! Gracias por tu participación.")
    except mysql.connector.Error as err:
        print(f"\nError al registrar el voto: {err}")
        cnx.rollback()

def show_results(cursor):
    print("\n--- RESULTADOS DE LA VOTACIÓN ---")
    
    query = (
        "SELECT p.nombre, p.departamento, COUNT(v.profesor_id) AS total_votos "
        "FROM profesores p LEFT JOIN votos v ON p.id = v.profesor_id "
        "GROUP BY p.id "
        "ORDER BY total_votos DESC, p.nombre"
    )
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("No hay resultados para mostrar.")
        return

    #formato de la tabla de resultados
    print(f"{'VOTOS':<8}{'PROFESOR':<30}{'DEPARTAMENTO':<20}")
    print("-" * 58)
    for nombre, departamento, votos in resultados:
        print(f"{votos:<8}{nombre:<30}{departamento:<20}")
    print("-" * 58)
    
    #total de votos
    total_votes_query = "SELECT COUNT(*) FROM votos"
    cursor.execute(total_votes_query)
    total_votes = cursor.fetchone()[0]
    print(f"Total de votos emitidos: {total_votes}")
    print("-----------------------------------")


def main_menu():
    cnx = get_db_connection()
    if not cnx:
        return

    cursor = cnx.cursor()

    while True:
        print("\n*** SISTEMA DE VOTACIÓN ESTUDIANTES-PROFESORES ***")
        print("1. Ver profesores y votar")
        print("2. Ver resultados (Administrador)")
        print("3. Salir")
        
        choice = input("Selecciona una opción: ").strip()

        if choice == '1':
            cast_vote(cnx, cursor)
        elif choice == '2':
            admin_pin = getpass.getpass("Ingresa el PIN de administrador para ver resultados: ")
            if admin_pin == "12345678":  
                show_results(cursor)
            else:
                print("PIN incorrecto.")
        elif choice == '3':
            print("Cerrando el sistema...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main_menu()