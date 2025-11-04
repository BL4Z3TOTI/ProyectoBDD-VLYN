def mostrar_menu_principal():
    print("\n==================================")
    print("=== PROYECTO BASE DE DATOS ===")
    print("==================================")
    print("1. Iniciar Sesion (Estudiante/Profesor/Admin)")
    print("2. Registrar nuevo estudiante")
    print("3. Salir")
    opcion = input("Selecciona una opcion: ").strip()
    return opcion