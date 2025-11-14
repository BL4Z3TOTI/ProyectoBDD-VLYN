
from vistas.vista_profesor import VistaProfesor
from modelos.modelo_profesor import ModeloProfesor

class ControladorProfesor:
    
    # TAREA 1: Modificar constructor para aceptar user_id
    def __init__(self, user_id=None):
        self.vista = VistaProfesor()
        self.modelo_profesor = ModeloProfesor()
        self.user_id = user_id

    def iniciar_login_profesor(self, parameter_list):

        # Este método es llamado por main.py, por eso devuelve el resultado del login
        self.user_id = None # Asegura que no arrastra un login previo
        
        opcion = self.vista.solicitar_tipo_login()
        pass

    

    def iniciar_consulta(self):
        id_profesor = self.vista.solicitar_id_profesor()
        
        if id_profesor is None:
            return

        votantes, mensaje_o_nombre = self.modelo_profesor.obtener_estudiantes_votantes(id_profesor)
        
        if votantes is None:
            self.vista.mostrar_mensaje(f" {mensaje_o_nombre}")
            return
            
        self.vista.mostrar_votantes(votantes, mensaje_o_nombre)