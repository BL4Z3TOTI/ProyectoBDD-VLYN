class VistaEstudiante:
    
    # TAREA 1: Adaptar menu para login
    def mostrar_menu_estudiante(self, logueado=False):
        if not logueado:
            print("\n*** MENÚ DE ESTUDIANTE (PRE-LOGIN) ***")
            print("1. Registrar nuevo estudiante")
            print("2. Votar por un profesor (Requiere iniciar sesión)")
            print("3. Salir al Menú Principal")
            opcion = input("Selecciona una opcion: ").strip()
            return opcion
        else:
            print("\n*** MENÚ DE ESTUDIANTE LOGUEADO ***")
            print("1. Votar por un profesor")
            print("2. Ver/Editar mi Perfil") # Nueva opción Tarea 1
            print("3. Cerrar Sesion")
            opcion = input("Selecciona una opcion: ").strip()
            return opcion

    def obtener_datos_registro(self):
        print("\n--- REGISTRO DE ESTUDIANTE ---")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        matricula = input("Matricula: ").strip()
        email = input("Email: ").strip()
        username = input("Usuario: ").strip()
        password = input("Contrasena: ").strip()
        
        datos = (nombre, apellido, matricula, email, username, password)
        return datos

    def mostrar_profesores(self, profesores):
        print("\n--- PROFESORES DISPONIBLES PARA VOTACION ---")
        if not profesores:
            print("No hay profesores registrados para votar.")
            return

        print(f"{'ID':<5}{'NOMBRE':<30}{'DEPARTAMENTO':<20}")
        print("-" * 55)
        for id, nombre, departamento in profesores:
            print(f"[{id:<3}] {nombre:<30}{departamento:<20}")
        print("-" * 55)

    # TAREA 1: Nuevo metodo para obtener datos de edicion de perfil
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

    # Modificado para el flujo de login (Ya no pide matricula)
    def obtener_id_profesor_voto(self):
        print("\n--- EMITIR VOTO ---")
        try:
            id_profesor = int(input("Ingresa el ID del profesor a votar: ").strip())
        except ValueError:
            id_profesor = 0 
            
        return id_profesor
        
    # Removida funcion obtener_datos_voto del archivo original, ya que fue reemplazada.
        
    def mostrar_mensaje(self, mensaje):
        print(mensaje)
        
    def solicitar_confirmacion_gesto(self):
        confirmacion = input("Presiona ENTER para iniciar la deteccion del gesto con la camara...").strip()
        return confirmacion