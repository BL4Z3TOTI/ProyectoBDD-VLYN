from vistas.vista_estudiante import VistaEstudiante
from modelos.modelo_usuario import ModeloUsuario
from modelos.modelo_profesor import ModeloProfesor
from modelos.modelo_votacion import ModeloVotacion
from modelos.conexion_BD import obtener_conexion_db
from DetectarPulgar import detectar_pulgar_arriba 
import mysql.connector

class ControladorEstudiante:
    
    def __init__(self, user_id=None):
    def __init__(self):
        self.vista = VistaEstudiante()
        self.modelo_usuario = ModeloUsuario()
        self.modelo_profesor = ModeloProfesor()
        self.modelo_votacion = ModeloVotacion()
        self.user_id = user_id 
        self.rol = 'Estudiante'

    def iniciar_menu(self):
        if self.user_id is None:
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
            while True:
                opcion = self.vista.mostrar_menu_estudiante(logueado=True)
                
                if opcion == '1':
                    self._manejar_votacion()
                elif opcion == '2':
                    self._manejar_edicion_perfil() 
                elif opcion == '3':
                    self._manejar_recomendaciones()
                elif opcion == '4':
                    self.vista.mostrar_mensaje("Cerrando sesion de estudiante.")
                    break
                else:
                    self.vista.mostrar_mensaje("Opcion no valida. Intenta de nuevo.")

    def iniciar_menu(self):
        while True:
            opcion = self.vista.mostrar_menu_estudiante()
            
            if opcion == '1':
                self._manejar_registro()
            elif opcion == '2':
                self._manejar_votacion()
            elif opcion == '3':
                self.vista.mostrar_mensaje("Saliendo del menú de estudiante.")
                break
            else:
                self.vista.mostrar_mensaje("Opción no válida. Intenta de nuevo.")

    def _manejar_registro(self):
        datos = self.vista.obtener_datos_registro()
        nombre, apellido, matricula, email, username, password = datos
        
        if not all(datos):
            self.vista.mostrar_mensaje("Todos los campos son obligatorios.")
            self.vista.mostrar_mensaje("Todos los campos son obligatorios.")
            return

        self.vista.solicitar_confirmacion_gesto()
        
        gesto_detectado = detectar_pulgar_arriba()
        
        if not gesto_detectado:
            self.vista.mostrar_mensaje("Gesto de Pulgar Arriba no detectado. Registro cancelado.")
            self.vista.mostrar_mensaje("Gesto de Pulgar Arriba no detectado. Registro cancelado.")
            return
            
        success, mensaje = self.modelo_usuario.registrar_estudiante((username, nombre, apellido, matricula, email), password)
        
        if success:
            self.vista.mostrar_mensaje(f"{mensaje}")
        else:
            self.vista.mostrar_mensaje(f"{mensaje}")

    def _manejar_edicion_perfil(self):
        self.vista.mostrar_mensaje("\n--- EDICION DE PERFIL ---")
        
        datos_nuevos = self.vista.obtener_nuevos_datos_perfil() 
        
        if not datos_nuevos:
            self.vista.mostrar_mensaje("Edicion cancelada.")
            return

        success, mensaje = self.modelo_usuario.actualizar_datos(self.user_id, self.rol, datos_nuevos)
        
        self.vista.mostrar_mensaje(mensaje)

    def _manejar_recomendaciones(self):
        self.vista.mostrar_mensaje("\n--- PROFESORES RECOMENDADOS (POR POPULARIDAD) ---")
        recomendaciones = self.modelo_votacion.obtener_profesores_recomendados()
        
        if not recomendaciones:
            self.vista.mostrar_mensaje("Aun no hay suficientes datos para mostrar recomendaciones.")
            return
            
        self.vista.mostrar_recomendaciones(recomendaciones)

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


            self.vista.mostrar_mensaje(f" {mensaje}")
        else:
            self.vista.mostrar_mensaje(f"{mensaje}")

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
        

        try:
            consulta = "SELECT id FROM estudiantes WHERE matricula = %s"
            cursor.execute(consulta, (matricula,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def _manejar_votacion(self):
        profesores = self.modelo_profesor.listar_profesores_votacion()
        self.vista.mostrar_profesores(profesores)
        
        if not profesores:
            return

        id_profesor = self.vista.obtener_id_profesor_voto()

        if not id_profesor:
            self.vista.mostrar_mensaje("Debes ingresar el ID del profesor.")
            return

        id_estudiante_db = self._obtener_id_estudiante_por_user_id(self.user_id)
        
        if id_estudiante_db is None:
            self.vista.mostrar_mensaje("Error: No se pudo encontrar el ID de estudiante asociado a su cuenta.")
            return
            
        if self.modelo_votacion.verificar_voto_estudiante(id_estudiante_db):
            self.vista.mostrar_mensaje("Lo siento, ya has votado.")
        matricula_o_id, id_profesor = self.vista.obtener_datos_voto()

        if not matricula_o_id or not id_profesor:
            self.vista.mostrar_mensaje("Debes ingresar tu matrícula y el ID del profesor.")
            return

        id_estudiante_db = self._obtener_id_estudiante_por_matricula(matricula_o_id)
        
        if id_estudiante_db is None:
            self.vista.mostrar_mensaje(f"Error: La matrícula o ID '{matricula_o_id}' no está registrada como estudiante.")
            return
            
        if self.modelo_votacion.verificar_voto_estudiante(id_estudiante_db):
            self.vista.mostrar_mensaje(f"Lo siento, el estudiante con matrícula '{matricula_o_id}' ya ha votado.")
            return
            
        valid_ids = [p[0] for p in profesores]
        if id_profesor not in valid_ids:
            self.vista.mostrar_mensaje("ID de profesor no valido. Intenta de nuevo.")
            return

        success, mensaje = self.modelo_votacion.registrar_voto(id_estudiante_db, id_profesor)
        self.vista.mostrar_mensaje(f"\n{mensaje}")
            self.vista.mostrar_mensaje("ID de profesor no válido. Intenta de nuevo.")
            return

        success, mensaje = self.modelo_votacion.registrar_voto(id_estudiante_db, id_profesor)
        self.vista.mostrar_mensaje(f"\n{'' if success else ''} {mensaje}")

