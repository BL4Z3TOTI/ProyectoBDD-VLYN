
import mysql.connector
from modelos.conexion_BD import obtener_conexion_db
from config_BD import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class ModeloUsuario:

    def _obtener_conexion(self):
        return obtener_conexion_db()

    def registrar_estudiante(self, datos_estudiante, contrasena):
        cnx = self._obtener_conexion()
        if not cnx: 
            return False, "Error de conexión a la base de datos."
        
        username, nombre, apellido, matricula, email = datos_estudiante
        
        contrasena_plana = contrasena 
        
        usuario_id = None
        cursor = cnx.cursor()

        try:
            sql_usuario = "INSERT INTO usuarios (username, password_hash, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql_usuario, (username, contrasena_plana, 'Estudiante'))
            usuario_id = cursor.lastrowid
            

            sql_estudiante = """
            INSERT INTO estudiantes (usuario_id, matricula, nombre, apellido, email) 
            VALUES (%s, %s, %s, %s, %s)
            """
            datos_insert_estudiante = (usuario_id, matricula, nombre, apellido, email)
            cursor.execute(sql_estudiante, datos_insert_estudiante)
            
            cnx.commit()
            return True, f"Estudiante '{nombre} {apellido}' registrado con éxito."

        except mysql.connector.Error as e:
            mensaje_error = "Error desconocido de MySQL. Revisa los logs."
            if e.errno == 1062: # Error de duplicidad (UNIQUE constraint))
                if 'username' in str(e):
                    mensaje_error = f"❌ El nombre de usuario '{username}' ya está en uso."
                elif 'matricula' in str(e):
                    mensaje_error = f"❌ La matrícula '{matricula}' ya está registrada."
                elif 'email' in str(e):
                    mensaje_error = f"❌ El email '{email}' ya está registrado."
                else:
                    mensaje_error = "❌ Error de registro. Datos duplicados."
            
            if usuario_id:
                try:
                    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                    cnx.commit()
                except:
                    pass
            cnx.rollback()
            return False, mensaje_error

        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()