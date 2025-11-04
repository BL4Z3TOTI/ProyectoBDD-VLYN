def obtener_nuevos_datos_perfil(self):
        print("\n--- INGRESA LOS NUEVOS VALORES (deja vacio para no cambiar) ---")
        
        nuevos_datos = {}
        
        username = input("Nuevo nombre de Usuario: ").strip()
        if username:
            nuevos_datos['username'] = username
            
        password = input("Nueva Contrasena (se guardara sin hashear): ").strip()
        if password:
            nuevos_datos['password'] = password
            
        nombre = input("Nuevo Nombre: ").strip()
        if nombre:
            nuevos_datos['nombre'] = nombre
            
        apellido = input("Nuevo Apellido: ").strip()
        if apellido:
            nuevos_datos['apellido'] = apellido

        matricula = input("Nueva Matricula: ").strip()
        if matricula:
            nuevos_datos['matricula'] = matricula
            
        email = input("Nuevo Email: ").strip()
        if email:
            nuevos_datos['email'] = email
            
        return nuevos_datos