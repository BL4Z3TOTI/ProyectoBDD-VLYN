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
            
