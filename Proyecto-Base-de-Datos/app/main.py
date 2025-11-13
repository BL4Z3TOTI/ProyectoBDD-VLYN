from modelos.iniciar_tablas import IniciarTablas
from controlador.controlador_administrador import ControladorAdministrador
from controlador.controlador_estudiante import ControladorEstudiante
from controlador.controlador_profesor import ControladorProfesor
from modelos.modelo_usuario import ModeloUsuario 
import traceback 

def mostrar_menu_principal():
    print("\n==================================")
    print("=== PROYECTO BASE DE DATOS ===")
    print("==================================")
    print("1. Iniciar Sesion (Estudiante/Profesor/Admin)")
    print("2. Registrar nuevo estudiante")
    print("3. Salir")
    opcion = input("Selecciona una opcion: ").strip()
    return opcion

if __name__ == "__main__":
    
    iniciador = IniciarTablas()
    iniciador.inicializar_tablas()

    print("Inicializacion de DB completada. Iniciando menu interactivo...")

    while True:
        opcion = mostrar_menu_principal()

        if opcion == '1':
            
            print("\n--- SELECCIÓN DE ROL ---")
            print("1. Estudiante")
            print("2. Profesor")
            print("3. Administrador")
            opcion_rol = input("Ingresa tu rol (1-3): ").strip()
            
            user_id, rol, mensaje = None, None, "Login cancelado o rol no válido."
            
            if opcion_rol == '1':
                controlador_estudiante = ControladorEstudiante() 
                user_id, rol, mensaje = controlador_estudiante.iniciar_login_estudiante() # Nuevo método
                
            elif opcion_rol in ('2', '3'):
                rol_str = 'Profesor' if opcion_rol == '2' else 'Administrador'
                username = input(f"Usuario ({rol_str}): ").strip()
                password = input("Contrasena: ").strip()
                
                modelo_usuario = ModeloUsuario()
                user_id, rol, mensaje = modelo_usuario.iniciar_sesion(username, password)
                
                if user_id and rol != rol_str:
                    user_id, rol, mensaje = None, None, f"Login fallido: El usuario '{username}' es de rol '{rol}', no '{rol_str}'."
            
            print(mensaje)
            
            if user_id and rol:
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
            controlador_estudiante = ControladorEstudiante()
            controlador_estudiante._manejar_registro() 
            
        elif opcion == '3':
            print("Cerrando la aplicacion. Hasta pronto.")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")