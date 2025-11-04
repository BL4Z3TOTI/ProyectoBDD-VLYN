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
                self._manejar_baja_profesores()
            elif opcion == '4':
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

    def _manejar_baja_profesores(self):
        
        profesores = self.modelo_votacion.obtener_profesores_sin_votos()
        
        if profesores is None:
            self.vista.mostrar_mensaje("❌ Error en la base de datos al obtener candidatos a baja.")
            return
            
        if not profesores:
            self.vista.mostrar_mensaje("✅ No hay profesores inactivos (sin votos) que cumplan el criterio de baja.")
            return

        self.vista.mostrar_candidatos_baja(profesores)
        
        confirmacion = self.vista.solicitar_confirmacion_baja(len(profesores))
        
        if confirmacion.upper() != 'S':
            self.vista.mostrar_mensaje("Operación de baja cancelada por el administrador.")
            return
            
        bajas_exitosas = 0
        bajas_fallidas = 0
        
        for p in profesores:
            profesor_id = p['profesor_id']
            usuario_id = p['usuario_id']
            
            success, mensaje = self.modelo_votacion.ejecutar_baja_profesor(profesor_id, usuario_id)
            
            if success:
                bajas_exitosas += 1
                print(f"✅ Baja Exitosa: Profesor {p['nombre']} (ID: {profesor_id})")
            else:
                bajas_fallidas += 1
                print(f"❌ Baja Fallida: Profesor {p['nombre']}. Razón: {mensaje}")
                
        self.vista.mostrar_mensaje(f"\n--- Resumen de Bajas ---\n"
                                  f"Bajas Exitosas: {bajas_exitosas}\n"
                                  f"Bajas Fallidas: {bajas_fallidas}\n"
                                  f"------------------------")