import mysql.connector
from modelos.conexion_BD import obtener_conexion_db

class ModeloVotacion:
    
    def _obtener_conexion(self):
        return obtener_conexion_db()
    
    # ... (métodos existentes como obtener_resultados, verificar_voto_estudiante, registrar_voto, etc.)

    def obtener_profesores_sin_votos(self):
        cnx = self._obtener_conexion()
        if not cnx:
            return None
        
        cursor = cnx.cursor(dictionary=True)
        try:
            consulta = """
                SELECT 
                    p.id AS profesor_id, 
                    p.nombre, 
                    p.departamento,
                    p.usuario_id
                FROM profesores p
                LEFT JOIN votos v ON p.id = v.profesor_id
                WHERE v.profesor_id IS NULL;
            """
            cursor.execute(consulta)
            profesores_inactivos = cursor.fetchall()
            return profesores_inactivos
            
        except mysql.connector.Error:
            return None

        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()
                
    def ejecutar_baja_profesor(self, profesor_id, usuario_id):
        cnx = self._obtener_conexion()
        if not cnx:
            return False, "Error de conexión a la base de datos."
        
        cursor = cnx.cursor()
        try:
            sql_profesor = "DELETE FROM profesores WHERE id = %s"
            cursor.execute(sql_profesor, (profesor_id,))
            
            sql_usuario = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(sql_usuario, (usuario_id,))
            
            cnx.commit()
            return True, "Profesor eliminado exitosamente."
        
        except mysql.connector.Error as e:
            cnx.rollback()
            return False, f"Error de MySQL al ejecutar la baja: {e}"

        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()