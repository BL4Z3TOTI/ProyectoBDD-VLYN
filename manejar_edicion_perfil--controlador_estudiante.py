def _manejar_edicion_perfil(self):
        self.vista.mostrar_mensaje("\n--- EDICION DE PERFIL ---")
        
        datos_nuevos = self.vista.obtener_nuevos_datos_perfil() 
        
        if not datos_nuevos:
            self.vista.mostrar_mensaje("Edicion cancelada.")
            return

        success, mensaje = self.modelo_usuario.actualizar_datos(self.user_id, self.rol, datos_nuevos)
        
        self.vista.mostrar_mensaje(mensaje)