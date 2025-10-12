from ADMIN_VER_ESTUDIANTES_PROFESORES import *


if __name__ == "__main__":

    crear_tablas_uep()

    estudiantes, profesores = ver_todos_para_admin()

    print("=== Estudiantes ===")
    for e in estudiantes:
        print(e)

    print("\n=== Profesores ===")
    for p in profesores:
        print(p)
