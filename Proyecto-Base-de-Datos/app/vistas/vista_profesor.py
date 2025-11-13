
class VistaProfesor:
    
    def solicitar_id_profesor(self):
        print("\n--- CONSULTAR VOTANTES ---")
        try:
            id_profesor = int(input("Ingresa tu ID de Profesor para ver tus votantes: ").strip())
            return id_profesor
        except ValueError:
            self.mostrar_mensaje("Entrada no válida. El ID debe ser un número.")
            return None

    def mostrar_votantes(self, votantes, nombre_profesor):
        
        print(f"\n--- ESTUDIANTES QUE VOTARON POR EL PROFESOR {nombre_profesor.upper()} ---")
        
        if not votantes:
            print(f"El profesor {nombre_profesor} aún no ha recibido votos.")
            return

        print(f"{'MATRÍCULA':<15}{'USUARIO':<15}{'NOMBRE COMPLETO':<40}")
        print("-" * 70)
        
        for estudiante in votantes:
            nombre_completo = f"{estudiante['nombre']} {estudiante['apellido']}"
            print(f"{estudiante['matricula']:<15}{estudiante['username']:<15}{nombre_completo:<40}")
            
        print("-" * 70)
        print(f"Total de votantes: {len(votantes)}")

    def mostrar_mensaje(self, mensaje):
        print(mensaje)