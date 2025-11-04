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
            if e.errno == 1062:
                if 'username' in str(e):
                    mensaje_error = f"El nombre de usuario '{username}' ya está en uso."
                elif 'matricula' in str(e):
                    mensaje_error = f"La matrícula '{matricula}' ya está registrada."
                elif 'email' in str(e):
                    mensaje_error = f"El email '{email}' ya está registrado."
                else:
                    mensaje_error = "Error de registro. Datos duplicados."
            
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
    
    # TAREA 1: NUEVOS MÉTODOS
    def iniciar_sesion(self, username, password_plana):
        cnx = self._obtener_conexion()
        if not cnx:
            return None, None, "Error de conexion a la base de datos."

        cursor = cnx.cursor(dictionary=True)
        
        sql = "SELECT id, password_hash, rol FROM usuarios WHERE username = %s"
        cursor.execute(sql, (username,))
        usuario = cursor.fetchone()

        if usuario and usuario['password_hash'] == password_plana:
            cursor.close()
            cnx.close()
            return usuario['id'], usuario['rol'], "Inicio de sesion exitoso."
        elif usuario:
            cursor.close()
            cnx.close()
            return None, None, "Contrasena incorrecta."
        else:
            cursor.close()
            cnx.close()
            return None, None, f"Usuario '{username}' no encontrado."
            
    def actualizar_datos(self, usuario_id, rol, datos_perfil):
        cnx = self._obtener_conexion()
        if not cnx:
            return False, "Error de conexion a la base de datos."

        cursor = cnx.cursor()
        
        updates = []
        data = []
        
        if 'username' in datos_perfil:
            updates.append("username = %s")
            data.append(datos_perfil['username'])
        if 'password' in datos_perfil:
            updates.append("password_hash = %s")
            data.append(datos_perfil['password'])

        if updates:
            sql_user = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s"
            data.append(usuario_id)
            cursor.execute(sql_user, tuple(data))
        
        if rol == 'Estudiante':
            cursor.execute("SELECT id FROM estudiantes WHERE usuario_id = %s", (usuario_id,))
            e_id_result = cursor.fetchone()
            
            if e_id_result:
                e_id = e_id_result[0]
                sql_est = "UPDATE estudiantes SET nombre=%s, apellido=%s, matricula=%s, email=%s WHERE id=%s"
                
                datos_update = (
                    datos_perfil.get('nombre', None),
                    datos_perfil.get('apellido', None),
                    datos_perfil.get('matricula', None),
                    datos_perfil.get('email', None),
                    e_id
                )
                cursor.execute(sql_est, datos_update)
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return True, "Datos actualizados con exito."