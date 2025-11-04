def __init__(self, user_id=None):
        self.vista = VistaEstudiante()
        self.modelo_usuario = ModeloUsuario()
        self.modelo_profesor = ModeloProfesor()
        self.modelo_votacion = ModeloVotacion()
        self.user_id = user_id 
        self.rol = 'Estudiante'