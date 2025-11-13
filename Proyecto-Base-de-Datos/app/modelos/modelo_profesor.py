
import mysql.connector
from modelos.conexion_BD import obtener_conexion_db
from config_BD import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class ModeloProfesor:
    
    def _obtener_conexion(self):
        return obtener_conexion_db()

    def listar_profesores_votacion(self):
        cnx = self._obtener_conexion()
        if not cnx: 
            return []
        
        cursor = cnx.cursor()
        try:
            consulta = "SELECT id, nombre, departamento FROM profesores ORDER BY nombre"
            cursor.execute(consulta)
            return cursor.fetchall()
        
        except mysql.connector.Error as e:
            print(f" Error al listar profesores para votación: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()

    def obtener_estudiantes_votantes(self, id_profesor):
        cnx = self._obtener_conexion()
        if not cnx: 
            return None, "Error de conexión a la Base de Datos Única."
        
        cursor = cnx.cursor(dictionary=True) 
        try:
            consulta_profesor = "SELECT nombre FROM profesores WHERE id = %s"
            cursor.execute(consulta_profesor, (id_profesor,))
            profesor = cursor.fetchone()
            
            if not profesor:
                return None, f"No se encontró el profesor con ID {id_profesor}."
            
            nombre_profesor = profesor['nombre']

            consulta_votantes = """
                SELECT 
                    e.nombre, e.apellido, e.matricula, u.username 
                FROM votos v
                JOIN estudiantes e ON v.estudiante_id = e.id
                JOIN usuarios u ON e.usuario_id = u.id
                WHERE v.profesor_id = %s
                ORDER BY e.apellido, e.nombre;
            """
            cursor.execute(consulta_votantes, (id_profesor,))
            votantes = cursor.fetchall()
            
            return votantes, nombre_profesor

        except mysql.connector.Error as e:
            return None, f"Error de MySQL al obtener votantes: {e}"

        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()