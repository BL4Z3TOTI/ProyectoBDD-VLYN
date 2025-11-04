

from vistas.vista_estudiante import VistaEstudiante
from modelos.modelo_usuario import ModeloUsuario
from modelos.modelo_profesor import ModeloProfesor
from modelos.modelo_votacion import ModeloVotacion
from modelos.conexion_BD import obtener_conexion_db
from DetectarPulgar import detectar_pulgar_arriba 
import mysql.connector

class ControladorEstudiante:
    
    def __init__(self):
        self.vista = VistaEstudiante()
        self.modelo_usuario = ModeloUsuario()
        self.modelo_profesor = ModeloProfesor()
        self.modelo_votacion = ModeloVotacion()

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
            self.vista.mostrar_mensaje("❌ Todos los campos son obligatorios.")
            return

        self.vista.solicitar_confirmacion_gesto()
        
        gesto_detectado = detectar_pulgar_arriba()
        
        if not gesto_detectado:
            self.vista.mostrar_mensaje("❌ Gesto de Pulgar Arriba no detectado. Registro cancelado.")
            return
            
        success, mensaje = self.modelo_usuario.registrar_estudiante((username, nombre, apellido, matricula, email), password)
        
        if success:
            self.vista.mostrar_mensaje(f"✅ {mensaje}")
        else:
            self.vista.mostrar_mensaje(f"{mensaje}")

    def _obtener_id_estudiante_por_matricula(self, matricula):
        conexion = obtener_conexion_db()
        if not conexion: 
            return None
        
        cursor = conexion.cursor()
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

        matricula_o_id, id_profesor = self.vista.obtener_datos_voto()

        if not matricula_o_id or not id_profesor:
            self.vista.mostrar_mensaje("❌ Debes ingresar tu matrícula y el ID del profesor.")
            return

        id_estudiante_db = self._obtener_id_estudiante_por_matricula(matricula_o_id)
        
        if id_estudiante_db is None:
            self.vista.mostrar_mensaje(f"❌ Error: La matrícula o ID '{matricula_o_id}' no está registrada como estudiante.")
            return
            
        if self.modelo_votacion.verificar_voto_estudiante(id_estudiante_db):
            self.vista.mostrar_mensaje(f"❌ Lo siento, el estudiante con matrícula '{matricula_o_id}' ya ha votado.")
            return
            
        valid_ids = [p[0] for p in profesores]
        if id_profesor not in valid_ids:
            self.vista.mostrar_mensaje("❌ ID de profesor no válido. Intenta de nuevo.")
            return

        success, mensaje = self.modelo_votacion.registrar_voto(id_estudiante_db, id_profesor)
        self.vista.mostrar_mensaje(f"\n{'✅' if success else '❌'} {mensaje}")