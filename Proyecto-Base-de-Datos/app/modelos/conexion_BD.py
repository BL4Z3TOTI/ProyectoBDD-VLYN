
import mysql.connector
from mysql.connector import errorcode
from config_BD import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def obtener_conexion_db(host=DB_HOST, usuario=DB_USER, contrasena=DB_PASSWORD, nombre_db=DB_NAME):
    """
    Establece y retorna una conexión a la base de datos única (proyectobasededatosuep).
    
    Retorna:
      objeto_conexion: El objeto de conexión si es exitoso, o None en caso de error.
    """
    try:
        conexion_db = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contrasena,
            database=nombre_db
        )
        return conexion_db
    except mysql.connector.Error as error:
        print("\nERROR DE CONEXIÓN A LA BASE DE DATOS ")
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"La base de datos '{nombre_db}' no existe. Asegúrate de crearla.")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Acceso denegado. Revisa el usuario y contraseña de MySQL en 'config_uep.py'.")
        else:
            print(f"Error desconocido de MySQL: {error}")
        return None