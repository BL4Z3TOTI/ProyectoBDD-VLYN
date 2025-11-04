

class VistaAdministrador:
    
    def mostrar_menu_admin(self):
        print("\n*** MENÚ DE ADMINISTRACIÓN ***")
        print("1. Ver todos los Usuarios (Estudiantes y Profesores)")
        print("2. Ver Resultados de Votación")
        print("3. Salir al Menú Principal")
        opcion = input("Selecciona una opción: ").strip()
        return opcion
    
    def mostrar_todos_los_usuarios(self, estudiantes, profesores):
        
        print("=== ADMINISTRACIÓN: LISTA DE ESTUDIANTES ===")

        
        if estudiantes:
            print(f"{'ID':<5}{'MATRÍCULA':<15}{'USUARIO':<15}{'NOMBRE COMPLETO':<35}{'EMAIL':<30}")
            print("-" * 105)
            for e in estudiantes:
                nombre_completo = f"{e['nombre']} {e['apellido']}"
                print(f"{e['id']:<5}{e['matricula']:<15}{e['username']:<15}{nombre_completo:<35}{e['email']:<30}")
        else:
            print("No hay estudiantes registrados.")

        print("=== ADMINISTRACIÓN: LISTA DE PROFESORES ===")
        
        if profesores:
            print(f"{'ID':<5}{'NOMBRE COMPLETO':<35}{'DEPARTAMENTO':<20}{'USUARIO':<15}")
            print("-" * 75)
            for p in profesores:
                print(f"{p['id']:<5}{p['nombre']:<35}{p['departamento']:<20}{p.get('username', 'N/A'):<15}")
        else:
            print("No hay profesores registrados.")
            
    def mostrar_resultados_votacion(self, resultados, total_votos):
        
        print("\n--- RESULTADOS DE LA VOTACIÓN ---")
        if not resultados and total_votos == 0:
            print("No hay resultados ni votos para mostrar.")
            return
        
        print(f"{'VOTOS':<8}{'PROFESOR':<30}{'DEPARTAMENTO':<20}")
        print("-" * 58)
        
        for nombre, departamento, votos in resultados:
            print(f"{votos:<8}{nombre:<30}{departamento:<20}")
            
        print("-" * 58)
        print(f"Total de votos emitidos: {total_votos}")
        
    def solicitar_pin(self):
        return input(" Ingresa el PIN de administrador: ").strip()

    def mostrar_mensaje(self, mensaje):
        print(mensaje)