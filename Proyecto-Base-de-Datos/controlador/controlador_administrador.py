
from vistas.vista_administrador import VistaAdministrador
from modelos.modelo_votacion import ModeloVotacion
from config_BD import PIN_ADMIN_PRINCIPAL, PIN_ADMIN_VOTOS
from modelos.conexion_BD import obtener_conexion_db 
import mysql.connector

class ControladorAdministrador:
    
    def __init__(self):
        self.vista = VistaAdministrador()
        self.modelo_votacion = ModeloVotacion()

    def iniciar_menu(self):
        pin = self.vista.solicitar_pin()
        
        if pin != PIN_ADMIN_PRINCIPAL:
            self.vista.mostrar_mensaje(" PIN de Administrador principal incorrecto.")
            return

        while True:
            opcion = self.vista.mostrar_menu_admin()
            if opcion == '1':
                self._manejar_ver_usuarios()
            elif opcion == '2':
                self._manejar_ver_resultados()
            elif opcion == '3':
                self.vista.mostrar_mensaje("Saliendo del menú de administrador.")
                break
            else:
                self.vista.mostrar_mensaje("Opción no válida. Intenta de nuevo.")

    def _obtener_estudiantes_y_profesores(self):
        conexion = obtener_conexion_db()
        if not conexion:
            return [], []

        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            
            sql_estudiantes = """
                SELECT e.id, e.nombre, e.apellido, e.matricula, e.email, u.username
                FROM estudiantes e
                JOIN usuarios u ON e.usuario_id = u.id;
            """
            cursor.execute(sql_estudiantes)
            estudiantes = cursor.fetchall()

            sql_profesores = """
                SELECT p.id, p.nombre, p.departamento, u.username
                FROM profesores p
                JOIN usuarios u ON p.usuario_id = u.id;
            """
            cursor.execute(sql_profesores)
            profesores = cursor.fetchall()

            return estudiantes, profesores

        except mysql.connector.Error as e:
            self.vista.mostrar_mensaje(f"Error al obtener datos de usuarios: {e}")
            return [], []

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def _manejar_ver_usuarios(self):
        estudiantes, profesores = self._obtener_estudiantes_y_profesores()
        self.vista.mostrar_todos_los_usuarios(estudiantes, profesores)

    def _manejar_ver_resultados(self):
        pin_votos = self.vista.solicitar_pin()
        
        if pin_votos != PIN_ADMIN_VOTOS:
            self.vista.mostrar_mensaje("❌ PIN de resultados de votación incorrecto.")
            return

        resultados, total_votos = self.modelo_votacion.obtener_resultados()
        self.vista.mostrar_resultados_votacion(resultados, total_votos)