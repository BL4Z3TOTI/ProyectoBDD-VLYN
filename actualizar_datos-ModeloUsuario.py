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