from vistas.vista_estudiante import VistaEstudiante
from modelos.modelo_usuario import ModeloUsuario
from modelos.modelo_profesor import ModeloProfesor
from modelos.modelo_votacion import ModeloVotacion
from modelos.conexion_BD import obtener_conexion_db
from DetectarPulgar import detectar_pulgar_arriba 
import mysql.connector

class ControladorEstudiante:
    
    # TAREA 1: Modificar constructor para aceptar user_id
    def __init__(self, user_id=None):
        self.vista = VistaEstudiante()
        self.modelo_usuario = ModeloUsuario()
        self.modelo_profesor = ModeloProfesor()
        self.modelo_votacion = ModeloVotacion()
        self.user_id = user_id 
        self.rol = 'Estudiante'

    # TAREA 1: Modificar iniciar_menu para el flujo logueado
    def iniciar_menu(self):
        if self.user_id is None:
            # Flujo de PRE-LOGIN (Solo Registro, la votación requiere login)
            while True:
                opcion = self.vista.mostrar_menu_estudiante(logueado=False)
                if opcion == '1':
                    self._manejar_registro()
                elif opcion == '2':
                    self.vista.mostrar_mensaje("Debes iniciar sesion para votar.")
                elif opcion == '3':
                    self.vista.mostrar_mensaje("Saliendo del menu de estudiante.")
                    break
                else:
                    self.vista.mostrar_mensaje("Opcion no valida. Intenta de nuevo.")
        else:
            # Flujo de POST-LOGIN (Votar y Perfil)
            while True:
                opcion = self.vista.mostrar_menu_estudiante(logueado=True)
                
                if opcion == '1':
                    self._manejar_votacion()
                elif opcion == '2':
                    self._manejar_edicion_perfil() # Nueva opción Tarea 1
                elif opcion == '3':
                    self.vista.mostrar_mensaje("Cerrando sesion de estudiante.")
                    break
                else:
                    self.vista.mostrar_mensaje("Opcion no valida. Intenta de nuevo.")

    def _manejar_registro(self):
        datos = self.vista.obtener_datos_registro()
        nombre, apellido, matricula, email, username, password = datos
        
        if not all(datos):
            self.vista.mostrar_mensaje("Todos los campos son obligatorios.")
            return

        self.vista.solicitar_confirmacion_gesto()
        
        gesto_detectado = detectar_pulgar_arriba()
        
        if not gesto_detectado:
            self.vista.mostrar_mensaje("Gesto de Pulgar Arriba no detectado. Registro cancelado.")
            return
            
        success, mensaje = self.modelo_usuario.registrar_estudiante((username, nombre, apellido, matricula, email), password)
        
        if success:
            self.vista.mostrar_mensaje(f"{mensaje}")
        else:
            self.vista.mostrar_mensaje(f"{mensaje}")

    # TAREA 1: Nuevo método para gestionar la edición de perfil
    def _manejar_edicion_perfil(self):
        self.vista.mostrar_mensaje("\n--- EDICION DE PERFIL ---")
        
        datos_nuevos = self.vista.obtener_nuevos_datos_perfil() 
        
        if not datos_nuevos:
            self.vista.mostrar_mensaje("Edicion cancelada.")
            return

        success, mensaje = self.modelo_usuario.actualizar_datos(self.user_id, self.rol, datos_nuevos)
        
        self.vista.mostrar_mensaje(mensaje)

    # Nuevo método auxiliar para obtener el ID de estudiante a partir del user_id logueado
    def _obtener_id_estudiante_por_user_id(self, user_id):
        conexion = obtener_conexion_db()
        if not conexion: 
            return None
        
        cursor = conexion.cursor()
        
        consulta = "SELECT id FROM estudiantes WHERE usuario_id = %s"
        cursor.execute(consulta, (user_id,))
        resultado = cursor.fetchone()
        
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
        
        return resultado[0] if resultado else None


    def _obtener_id_estudiante_por_matricula(self, matricula):
        conexion = obtener_conexion_db()
        if not conexion: 
            return None
        
        cursor = conexion.cursor()
        consulta = "SELECT id FROM estudiantes WHERE matricula = %s"
        cursor.execute(consulta, (matricula,))
        resultado = cursor.fetchone()
        
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
            
        return resultado[0] if resultado else None
        

    # TAREA 1: Modificar _manejar_votacion para usar el user_id logueado
    def _manejar_votacion(self):
        profesores = self.modelo_profesor.listar_profesores_votacion()
        self.vista.mostrar_profesores(profesores)
        
        if not profesores:
            return

        # Ahora solo pedimos el ID del profesor
        id_profesor = self.vista.obtener_id_profesor_voto()

        if not id_profesor:
            self.vista.mostrar_mensaje("Debes ingresar el ID del profesor.")
            return

        # Obtenemos el ID de estudiante usando el user_id
        id_estudiante_db = self._obtener_id_estudiante_por_user_id(self.user_id)
        
        if id_estudiante_db is None:
            self.vista.mostrar_mensaje("Error: No se pudo encontrar el ID de estudiante asociado a su cuenta.")
            return
            
        if self.modelo_votacion.verificar_voto_estudiante(id_estudiante_db):
            self.vista.mostrar_mensaje("Lo siento, ya has votado.")
            return
            
        valid_ids = [p[0] for p in profesores]
        if id_profesor not in valid_ids:
            self.vista.mostrar_mensaje("ID de profesor no valido. Intenta de nuevo.")
            return

        success, mensaje = self.modelo_votacion.registrar_voto(id_estudiante_db, id_profesor)
        self.vista.mostrar_mensaje(f"\n{mensaje}")