def mostrar_menu_estudiante(self, logueado=False):
        if not logueado:
            print("\n*** MENÚ DE ESTUDIANTE (REGISTRO) ***")
            print("1. Registrar nuevo estudiante")
            print("2. Votar por un profesor")
            print("3. Salir al Menú Principal")
            opcion = input("Selecciona una opcion: ").strip()
            return opcion
        else:
            print("\n*** MENÚ DE ESTUDIANTE LOGUEADO ***")
            print("1. Votar por un profesor")
            print("2. Ver/Editar mi Perfil")
            print("3. Cerrar Sesion")
            opcion = input("Selecciona una opcion: ").strip()
            return opcion