
from modelos.iniciar_tablas import IniciarTablas
from controlador.controlador_administrador import ControladorAdministrador
from controlador.controlador_estudiante import ControladorEstudiante
from controlador.controlador_profesor import ControladorProfesor

def mostrar_menu_principal():
    print("=== PROYECTO BASE DE DATOS ===")
    print("1. Menú Estudiante (Registro y Votación)")
    print("2. Menú Profesor (Consultar Votantes)")
    print("3. Menú Administrador")
    print("4. Salir")
    opcion = input("Selecciona una opción: ").strip()
    return opcion

if __name__ == "__main__":
    
    iniciador = IniciarTablas()
    iniciador.inicializar_tablas()

    while True:
        opcion = mostrar_menu_principal()

        if opcion == '1':
            controlador_estudiante = ControladorEstudiante()
            controlador_estudiante.iniciar_menu()
        elif opcion == '2':
            controlador_profesor = ControladorProfesor()
            controlador_profesor.iniciar_consulta()
        elif opcion == '3':
            controlador_admin = ControladorAdministrador()
            controlador_admin.iniciar_menu()
        elif opcion == '4':
            print("Cerrando la aplicación. ¡Hasta pronto! 👋")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")