def ver_todos_para_admin():
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT e.id, e.nombre, e.apellido, e.matricula, e.email, u.username
                FROM estudiantes e
                JOIN usuarios u ON e.usuario_id = u.id;
            """)
            estudiantes = cursor.fetchall()

            cursor.execute("""
                SELECT p.id, u.username
                FROM profesores p
                JOIN usuarios u ON p.usuario_id = u.id;
            """)
            profesores = cursor.fetchall()

            return estudiantes, profesores

    except Error as e:
        print("Error al obtener datos:", e)
        return [], []

    finally:
        if 'conexion' in locals() and conexion and conexion.is_connected():
            if 'cursor' in locals() and cursor:
                cursor.close()
            conexion.close()
