import GestionProfesores
import GestionAlumnos
import GestionCursos


def menuPrincipal():
    salida = False
    while not salida:
        print("-" * 5, "Menu principal", "-" * 5, "\n1. Gestion Alumnos", "\n2. Gestion Profesores", "\n3. Gestion Cursos", "\n0. Salir")
        respuesta = input()
        if respuesta is not None:
            if respuesta == "0":
                salida = True
            elif respuesta == "1":
                menuAlumnos()
            elif respuesta == "2":
                menuProfesores()
            elif respuesta == "3":
                menuCursos()
        else:
            print("\nIntroduzca una opcion valida\n")


def menuAlumnos():
    salida = False
    while not salida:
        print("\t", "-" * 5, "Menu Alumnos",  "-" * 5, "\n\t1. Alta", "\n\t2. Baja", "\n\t3. Modificar", "\n\t4. Buscar", "\n\t5. Mostrar todos", "\n\t0. volver")
        respuesta = input()
        if respuesta is not None:
            if respuesta == "0":
                salida = True
            elif respuesta == "1":
                GestionAlumnos.alta()
            elif respuesta == "2":
                GestionAlumnos.baja()
            elif respuesta == "3":
                GestionAlumnos.modificar()
            elif respuesta == "4":
                GestionAlumnos.mostrarUno()
            elif respuesta == "5":
                GestionAlumnos.mostrarTodos()
            else:
                print("Opcion no valida")
        else:
            print("\nIntroduzca una opcion valida\n")


def menuProfesores():
    salida = False
    while not salida:
        print("\t", "-" * 5, "Menu Profesores", "-" * 5, "\n\t1. Alta", "\n\t2. Baja", "\n\t3. Modificar", "\n\t4. Buscar", "\n\t5. Mostrar todos", "\n\t0. volver")
        respuesta = input()
        if respuesta is not None:
            if respuesta == "0":
                salida = True
            elif respuesta == "1":
                GestionProfesores.alta()
            elif respuesta == "2":
                GestionProfesores.baja()
            elif respuesta == "3":
                GestionProfesores.modificar()
            elif respuesta == "4":
                GestionProfesores.buscar()
            elif respuesta == "5":
                GestionProfesores.mostrarTodos()
            else:
                print("Opcion no valida")
        else:
            print("\nIntroduzca una opcion valida\n")


def menuCursos():
    salida = False
    while not salida:
        print("\t", "-" * 5, "Menu Cursos", "-" * 5, "\n\t1. Alta", "\n\t2. Baja", "\n\t3. Modificar", "\n\t4. Buscar","\n\t5. Mostrar todos", "\n\t6. relacionar", "\n\t0. volver")
        respuesta = input()
        if respuesta is not None:
            if respuesta == "0":
                salida = True
            elif respuesta == "1":
                GestionCursos.alta()
            elif respuesta == "2":
                GestionCursos.baja()
            elif respuesta == "3":
                GestionCursos.modificar()
            elif respuesta == "4":
                GestionCursos.buscar()
            elif respuesta == "5":
                GestionCursos.mostrarTodos()
            elif respuesta == "6":
                GestionCursos.relacionar()
            else:
                print("Opcion no valida")
        else:
            print("\nIntroduzca una opcion valida\n")