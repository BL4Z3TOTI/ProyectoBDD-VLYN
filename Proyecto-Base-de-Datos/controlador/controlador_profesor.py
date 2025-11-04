
from vistas.vista_profesor import VistaProfesor
from modelos.modelo_profesor import ModeloProfesor

class ControladorProfesor:
    
    def __init__(self):
        self.vista = VistaProfesor()
        self.modelo_profesor = ModeloProfesor()

    def iniciar_consulta(self):
        id_profesor = self.vista.solicitar_id_profesor()
        
        if id_profesor is None:
            return

        votantes, mensaje_o_nombre = self.modelo_profesor.obtener_estudiantes_votantes(id_profesor)
        
        if votantes is None:
            self.vista.mostrar_mensaje(f" {mensaje_o_nombre}")
            return
            
        self.vista.mostrar_votantes(votantes, mensaje_o_nombre)