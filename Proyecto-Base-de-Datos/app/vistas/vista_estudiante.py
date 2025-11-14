class VistaEstudiante:
    
    # TAREA 1: Adaptar menu para login (Limpio)
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
            print("2. Ver/Editar mi Perfil")
            print("3. Ver Recomendaciones de Profesores")
            print("4. Cerrar Sesion")
            opcion = input("Selecciona una opcion: ").strip()
            return opcion
            
    # TAREA 4: Nuevo método para solicitar el tipo de login
    def solicitar_tipo_login(self):
        print("\n"*80)
        print("\n--- INICIO DE SESIÓN ESTUDIANTE ---")
        print("1. Acceder con Nombre de Usuario y Contraseña")
        print("2. Acceder con Gesto de Pulgar (Biométrico)")
        opcion = input("Selecciona una opcion: ").strip()
        return opcion

    def obtener_datos_registro(self):
        print("\n--- REGISTRO DE ESTUDIANTE ---")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        email = input("Email: ").strip()
        username = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()
        
        datos = (nombre, apellido, matricula, email, username, password)
        return datos


    def obtener_datos_estudiante(self):
        print("\n--- REGISTRO DE ESTUDIANTE ---")
        matricula = input("Matricula: ").strip()
        
        datos = ( matricula)
        return datos

    def obtener_datos_estudiante(self):
        print("\n--- REGISTRO DE PROFESOR ---")
        departamento = input("Departamento: ").strip()
        
        datos = ( departamento)
        return datos
        
    # TAREA 4: Nuevo método para solicitar la matrícula
    def solicitar_matricula(self):
        return input("Ingresa tu Matrícula para el acceso biométrico: ").strip()



    def mostrar_profesores(self, profesores):
        print("\n--- PROFESORES DISPONIBLES PARA VOTACIÓN ---")
        if not profesores:
            print("No hay profesores registrados para votar.")
            return

        print(f"{'ID':<5}{'NOMBRE':<30}{'DEPARTAMENTO':<20}")
        print("-" * 55)
        for id, nombre, departamento in profesores:
            print(f"[{id:<3}] {nombre:<30}{departamento:<20}")
        print("-" * 55)

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

    def obtener_id_profesor_voto(self):
        print("\n--- EMITIR VOTO ---")
        try:
            id_profesor = int(input("Ingresa el ID del profesor a votar: ").strip())
        except ValueError:
            id_profesor = 0 
            
        return id_profesor
        
    def mostrar_mensaje(self, mensaje):
        print(mensaje)
        
    def solicitar_confirmacion_gesto(self):
        input("Presiona ENTER para iniciar la detección del gesto con la cámara...")
        
    def mostrar_recomendaciones(self, recomendaciones):
        print(f"{'VOTOS':<8}{'PROFESOR':<30}{'DEPARTAMENTO':<20}")
        print("-" * 58)
        
        for r in recomendaciones:
            votos = r.get('total_votos', 0)
            print(f"{votos:<8}{r['nombre']:<30}{r['departamento']:<20}")
            
        print("-" * 58)
        if not recomendaciones:
            print("No hay profesores para recomendar en este momento.")