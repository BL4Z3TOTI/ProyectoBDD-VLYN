import mysql.connector
from mysql.connector import errorcode

# --- Configuración de la Conexión ---
DB_HOST = "localhost"
DB_USER = "root"  
DB_PASSWORD = "12345678"
DB_NAME = "votos_profes"

# --- Definición del Esquema de la Base de Datos ---
TABLES = {}
TABLES['profesores'] = (
    "CREATE TABLE profesores ("
    "  id INT PRIMARY KEY AUTO_INCREMENT,"
    "  nombre VARCHAR(50) NOT NULL,"
    "  departamento VARCHAR(50)"
    ") ENGINE=InnoDB"
)


TABLES['votos'] = (
    "CREATE TABLE votos ("
    "  id INT PRIMARY KEY AUTO_INCREMENT,"
    "  profesor_id INT NOT NULL,"
    "  estudiante_id VARCHAR(20) NOT NULL UNIQUE," 
    "  voto_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (profesor_id) REFERENCES profesores(id)"
    ") ENGINE=InnoDB"
)

# --- Profesores Iniciales ---
INITIAL_PROFESSORS = [
    ("Carlos Carden", "Base de datos"),
]

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"Base de datos '{DB_NAME}' creada o ya existente.")
        cursor.execute(f"USE {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")
        exit(1)


def create_tables(cursor):
    for name, ddl in TABLES.items():
        try:
            print(f"Creando tabla {name}: ", end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("ya existe.")
            else:
                print(err.msg)
        else:
            print("OK.")

def populate_professors(cnx, cursor):
    insert_prof_query = "INSERT IGNORE INTO profesores (nombre, departamento) VALUES (%s, %s)"
    

    cursor.execute("SELECT COUNT(*) FROM profesores")
    if cursor.fetchone()[0] == 0:
        print("Insertando profesores iniciales...")

        try:
            for prof in INITIAL_PROFESSORS:
                cursor.execute(insert_prof_query, prof)
            cnx.commit()
            print(f"{len(INITIAL_PROFESSORS)} profesores insertados.")

        except mysql.connector.Error as err:
            print(f"Error al insertar datos: {err}")
            cnx.rollback()
    else:
        print("La tabla de profesores ya contiene datos.")

def setup_db():
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: El nombre de usuario o contraseña de MySQL es incorrecto.")
        elif err.errno == errorcode.CR_CONN_ERROR:
            print("Error: No se pudo conectar al servidor MySQL. Asegúrate de que esté corriendo.")
        else:
            print(err)
        return

    cursor = cnx.cursor()

    create_database(cursor)
    create_tables(cursor)
    populate_professors(cnx, cursor)

    cursor.close()
    cnx.close()
    print("\nConfiguración de la base de datos completada.")

if __name__ == '__main__':
    setup_db()