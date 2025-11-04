from modelos.iniciar_tablas import IniciarTablas
from controlador.controlador_administrador import ControladorAdministrador
from controlador.controlador_estudiante import ControladorEstudiante
from controlador.controlador_profesor import ControladorProfesor
from modelos.modelo_usuario import ModeloUsuario # TAREA 1: Nueva Importación
import traceback 

def mostrar_menu_principal():
    # TAREA 1: Menú de Login
    print("\n==================================")
    print("=== PROYECTO BASE DE DATOS ===")
    print("==================================")
    print("1. Iniciar Sesion (Estudiante/Profesor/Admin)")
    print("2. Registrar nuevo estudiante")
    print("3. Salir")
    opcion = input("Selecciona una opcion: ").strip()
    return opcion

if __name__ == "__main__":
    
    # 1. Inicializa las tablas de la DB antes de que empiece el menú
    iniciador = IniciarTablas()
    iniciador.inicializar_tablas()

    print("Inicializacion de DB completada. Iniciando menu interactivo...")

    # 2. Bucle principal para manejar el LOGIN/REGISTRO
    while True:
        opcion = mostrar_menu_principal()

        if opcion == '1':
            username = input("Usuario: ").strip()
            password = input("Contrasena: ").strip()
            
            modelo_usuario = ModeloUsuario()
            user_id, rol, mensaje = modelo_usuario.iniciar_sesion(username, password)
            
            print(mensaje)
            
            if user_id and rol:
                # Redirige a los menús específicos, pasando el ID de usuario
                if rol == 'Estudiante':
                    controlador_estudiante = ControladorEstudiante(user_id=user_id)
                    controlador_estudiante.iniciar_menu() 
                elif rol == 'Profesor':
                    controlador_profesor = ControladorProfesor(user_id=user_id)
                    controlador_profesor.iniciar_consulta() 
                elif rol == 'Administrador':
                    controlador_admin = ControladorAdministrador(user_id=user_id) 
                    controlador_admin.iniciar_menu()
                    
        elif opcion == '2':
            # La opcion 2 ahora es el registro
            controlador_estudiante = ControladorEstudiante()
            controlador_estudiante._manejar_registro() 
            
        elif opcion == '3':
            print("Cerrando la aplicacion. Hasta pronto.")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")