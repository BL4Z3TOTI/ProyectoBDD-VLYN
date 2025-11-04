
import mysql.connector
from modelos.conexion_BD import obtener_conexion_db
from config_BD import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class ModeloVotacion:
    
    def _obtener_conexion(self):
        return obtener_conexion_db()

    def registrar_voto(self, id_estudiante, id_profesor):
        cnx = self._obtener_conexion()
        if not cnx: 
            return False, "Error de conexión a la base de datos."
        
        cursor = cnx.cursor()
        try:
            consulta_voto = "INSERT INTO votos (profesor_id, estudiante_id) VALUES (%s, %s)" 
            cursor.execute(consulta_voto, (id_profesor, id_estudiante))
            cnx.commit()
            return True, "Voto registrado con éxito."
        
        except mysql.connector.Error as e:
            cnx.rollback()
            mensaje_error = f"Error al registrar voto: {e}"
            if e.errno == 1062:
                mensaje_error = "❌ Ya existe un voto registrado para este estudiante."
            return False, mensaje_error
            
        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()

    def verificar_voto_estudiante(self, id_estudiante):
        cnx = self._obtener_conexion()
        if not cnx: 
            return True 
        
        cursor = cnx.cursor()
        try:
            consulta = "SELECT 1 FROM votos WHERE estudiante_id = %s"
            cursor.execute(consulta, (id_estudiante,))
            return cursor.fetchone() is not None
        
        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()

    def obtener_resultados(self):
        cnx = self._obtener_conexion()
        if not cnx: 
            return [], 0
        
        cursor = cnx.cursor()
        try:
            consulta_resultados = (
                "SELECT p.nombre, p.departamento, COUNT(v.profesor_id) AS total_votos "
                "FROM profesores p LEFT JOIN votos v ON p.id = v.profesor_id "
                "GROUP BY p.id "
                "ORDER BY total_votos DESC, p.nombre"
            )
            cursor.execute(consulta_resultados)
            resultados = cursor.fetchall()
            
            consulta_total = "SELECT COUNT(*) FROM votos"
            cursor.execute(consulta_total)
            total_votos = cursor.fetchone()[0]
            
            return resultados, total_votos

        except mysql.connector.Error as e:
            print(f"❌ Error al obtener resultados de votación: {e}")
            return [], 0
            
        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()