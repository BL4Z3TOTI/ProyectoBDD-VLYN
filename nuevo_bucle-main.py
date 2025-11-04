while True:
        opcion = mostrar_menu_principal()

        if opcion == '1':
            username = input("Usuario: ").strip()
            password = input("Contrasena: ").strip()
            
            modelo_usuario = ModeloUsuario()
            user_id, rol, mensaje = modelo_usuario.iniciar_sesion(username, password)
            
            print(mensaje)
            
            if user_id and rol:
                if rol == 'Estudiante':
                    controlador_estudiante = ControladorEstudiante(user_id=user_id)
                    controlador_estudiante.iniciar_menu() 
                elif rol == 'Profesor':
                    controlador_profesor = ControladorProfesor(user_id=user_id)
                    controlador_profesor.iniciar_consulta() 
                elif rol == 'Administrador':
                    controlador_admin = ControladorAdministrador(user_id=user_id) 
                    controlador_admin.iniciar_menu()
                    
        elif opcion == '2':
            controlador_estudiante = ControladorEstudiante()
            controlador_estudiante._manejar_registro() 
            
        elif opcion == '3':
            print("Cerrando la aplicacion. Hasta pronto.")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")