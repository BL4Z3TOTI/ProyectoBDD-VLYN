class VistaAdministrador:

    def solicitar_pin(self):
        return input("🔑 Ingresa el PIN: ").strip()

    def mostrar_menu_admin(self):
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Ver Listado de Usuarios (Estudiantes y Profesores)")
        print("2. Ver Resultados de Votación")
        print("3. Ejecutar Módulo de Baja Automática (Inactivos)")
        print("4. Salir")
        return input("Selecciona una opción: ").strip()
        
    def mostrar_mensaje(self, mensaje):
        print(f"\n[INFO] {mensaje}")

    def mostrar_candidatos_baja(self, profesores):
        print("\n--- CANDIDATOS A BAJA (PROFESORES SIN VOTOS) ---")
        for p in profesores:
            print(f"ID: {p['profesor_id']} | Nombre: {p['nombre']} | Depto: {p['departamento']} | Usuario ID: {p['usuario_id']}")
        print("-------------------------------------------------")
        
    def solicitar_confirmacion_baja(self, cantidad):
        return input(f"🚨 CONFIRMACIÓN: ¿Deseas eliminar permanentemente a los {cantidad} profesores de la lista? (S/N): ").strip()

    def mostrar_todos_los_usuarios(self, estudiantes, profesores):
        print("\n--- LISTADO COMPLETO DE USUARIOS ---")
        print("ESTUDIANTES:")
        for e in estudiantes:
            print(f"ID: {e['id']} | Matrícula: {e['matricula']} | Nombre: {e['nombre']} {e['apellido']} | Usuario: {e['username']}")
        print("\nPROFESORES:")
        for p in profesores:
            print(f"ID: {p['id']} | Nombre: {p['nombre']} | Depto: {p['departamento']} | Usuario: {p['username']}")
        print("------------------------------------")
        
    def mostrar_resultados_votacion(self, resultados, total_votos):
        print("\n--- RESULTADOS DE VOTACIÓN ---")
        print(f"Total de votos emitidos: {total_votos}")
        for r in resultados:
            print(f"Profesor: {r['nombre']} ({r['departamento']}) - Votos: {r['total_votos']}")
        print("------------------------------")

