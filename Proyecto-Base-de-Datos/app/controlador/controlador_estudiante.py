from vistas.vista_estudiante import VistaEstudiante
from modelos.modelo_usuario import ModeloUsuario
from modelos.modelo_profesor import ModeloProfesor
from modelos.modelo_votacion import ModeloVotacion
from modelos.conexion_BD import obtener_conexion_db
from DetectarPulgar import detectar_pulgar_arriba
from controlador_biometrico import ControladorBiometrico
import mysql.connector
import time


class ControladorEstudiante:
    
    # TAREA 1: Modificar constructor para aceptar user_id (Limpio)
    def __init__(self, user_id=None):
        self.vista = VistaEstudiante()
        self.modelo_usuario = ModeloUsuario()
        self.modelo_profesor = ModeloProfesor()
        self.modelo_votacion = ModeloVotacion()
        self.controladorBiometrico = ControladorBiometrico()
        self.user_id = user_id 
        self.rol = 'Estudiante'


    def _manejar_registro(self):
        # Lógica de registro existente (mantiene la validación con gesto)
        datos = self.vista.obtener_datos_registro()
        nombre, apellido, email, username, password = datos
        
        if not all(datos):
            self.vista.mostrar_mensaje("❌ Todos los campos son obligatorios.")
            return

        gesto_detectado = detectar_pulgar_arriba()
        
        rol = ""
        datosProfesor = None
        datosEstudiante = None

        if gesto_detectado:
            rol="profes"
            datosProfesor = self.vista.obtener_datos_profesor()
            if not all(datosProfesor):
                self.vista.mostrar_mensaje("❌ Todos los campos son obligatorios")
                return
        else:
            rol = "estudiantes"
            datosEstudiante = self.vista.obtener_datos_estudiante()
            if not all(datosEstudiante):
                self.vista.mostrar_mensaje("❌ Todos los campos son obligatorios")
                return
        
        print("****************************")
        print("Se le tomarán los datos biometricos, siga las instrucciones")
        print("Saque las fotos de su rostro de manera enfocada y con buena iluminacion")
        print("Saque las fotos apretando la tecla espacio")
        print("Saque por lo menos 6 fotos")
        print("Para terminar presione escape")
        print("****************************")
        time.sleep(0.5)

        self.controladorBiometrico.registrarParametrosBiometricos(rol, username)

        datosGenerales = (username, nombre, apellido, matricula, email, gesto_detectado)
    
        success, mensaje = self.modelo_usuario
                                .registrar_usuario(datosGenerales, datosEstudiante, datosProfesor)
        
        self.vista.mostrar_mensaje(f"{mensaje}")


    def iniciar_menu(self):
        # Flujo de POST-LOGIN (Votar y Perfil - Limpio)❌
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

    # TAREA 4: Nuevo método para manejar el flujo de login del estudiante (Contraseña o Gesto)
    def iniciar_login_estudiante(self):
        # Este método es llamado por main.py, por eso devuelve el resultado del login
        self.user_id = None # Asegura que no arrastra un login previo
        
        opcion = self.vista.solicitar_tipo_login()
        
        if opcion == '1':
            # Acceso con Contraseña (Llamada al flujo estándar)
            username = input("Usuario: ").strip()
            password = input("Contrasena: ").strip()
            return self.modelo_usuario.iniciar_sesion(username, password)
            
        elif opcion == '2':
            # Acceso Biométrico por Gesto y Matrícula (TAREA 4)

            print("Se le abrirá la cámara para los datos biométricos")
            print("Saque la fotos de su rostro de manera enfocada y con buena iluminacion")
            print("Saque la foto apretando la tecla espacio")
            print("Para terminar presione escape")
            print("****************************")
            time.sleep(0.5)

            username = self.controladorBiometrico.reconocerRostro("estudiantes")
          
                           
            if username:
                return self.modelo_usuario.obtener_usuario(username)
            else:
                return None, None, "❌ Matrícula no corresponde a un Estudiante o no fue encontrada."
        
        else:
            return None, None, "Opción no válida. Volviendo al menú principal."
            
                


    # ... Resto de métodos de ControladorEstudiante (_manejar_edicion_perfil, _manejar_recomendaciones, etc.) ...
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
        

    def _manejar_votacion(self):
        profesores = self.modelo_profesor.listar_profesores_votacion()
        self.vista.mostrar_profesores(profesores)
        
        if not profesores:
            return

        # Obtenemos el ID de estudiante usando el user_id
        id_estudiante_db = self._obtener_id_estudiante_por_user_id(self.user_id)
        
        if id_estudiante_db is None:
            self.vista.mostrar_mensaje("Error: No se pudo encontrar el ID de estudiante asociado a su cuenta.")
            return
            
        if self.modelo_votacion.verificar_voto_estudiante(id_estudiante_db):
            self.vista.mostrar_mensaje("Lo siento, ya has votado.")
            return

        # Ahora solo pedimos el ID del profesor
        id_profesor = self.vista.obtener_id_profesor_voto()
        
        if not id_profesor:
            self.vista.mostrar_mensaje("Debes ingresar el ID del profesor.")
            return

        valid_ids = [p[0] for p in profesores]
        if id_profesor not in valid_ids:
            self.vista.mostrar_mensaje("❌ ID de profesor no válido. Intenta de nuevo.")
            return

        success, mensaje = self.modelo_votacion.registrar_voto(id_estudiante_db, id_profesor)
        self.vista.mostrar_mensaje(f"\n{'✅' if success else '❌'} {mensaje}")