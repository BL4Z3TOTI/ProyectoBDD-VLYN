

class VistaEstudiante:
    
    def mostrar_menu_estudiante(self):
        print("\n*** MENÚ DE ESTUDIANTE ***")
        print("1. Registrar nuevo estudiante")
        print("2. Votar por un profesor")
        print("3. Salir al Menú Principal")
        opcion = input("Selecciona una opción: ").strip()
        return opcion

    def obtener_datos_registro(self):
        print("\n--- REGISTRO DE ESTUDIANTE ---")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        matricula = input("Matrícula: ").strip()
        email = input("Email: ").strip()
        username = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()
        
        datos = (nombre, apellido, matricula, email, username, password)
        return datos

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

    def obtener_datos_voto(self):
        print("\n--- EMITIR VOTO ---")
        id_estudiante_o_matricula = input("Ingresa tu Matrícula (o ID): ").strip()
        try:
            id_profesor = int(input("Ingresa el ID del profesor a votar: ").strip())
        except ValueError:
            id_profesor = 0 
            
        return id_estudiante_o_matricula, id_profesor
        
    def mostrar_mensaje(self, mensaje):
        print(mensaje)
        
    def solicitar_confirmacion_gesto(self):
        confirmacion = input("Presiona ENTER para iniciar la detección del gesto con la cámara...").strip()
        return confirmacion