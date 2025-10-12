#hola, buenos dias,tardes y noches

import mysql.connector
from mysql.connector import errorcode

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


def mostrar_profesores():
    cnx = get_db_connection()
    if not cnx:
        return

    cursor = cnx.cursor()
    try:
        query = "SELECT id, nombre, departamento FROM profesores ORDER BY nombre"
        cursor.execute(query)
        profesores = cursor.fetchall()

        if not profesores:
            print("\nNo hay profesores en la base de datos. Pídele al administrador que los agregue.")
            return

        print("\n--- PROFESORES DISPONIBLES ---")
        for (id, nombre, departamento) in profesores:
            print(f"[{id}] {nombre} ({departamento})")
        print("------------------------------")

    except mysql.connector.Error as err:
        print(f"Error al obtener profesores: {err}")

    finally:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    mostrar_profesores()
