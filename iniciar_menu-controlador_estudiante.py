def iniciar_menu(self):
        if not self.user_id:
            self.vista.mostrar_mensaje("Error: Debes iniciar sesion para usar el menu de estudiante.")
            return

        while True:
            opcion = self.vista.mostrar_menu_estudiante(logueado=True) 
            
            if opcion == '1':
                self._manejar_votacion()
            elif opcion == '2':
                self._manejar_edicion_perfil()
            elif opcion == '3':
                self.vista.mostrar_mensaje("Cerrando sesion de estudiante.")
                break
            else:
                self.vista.mostrar_mensaje("Opcion no valida. Intenta de nuevo.")