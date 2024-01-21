import GestorBaseDeDatos
import BaseDeDatosM
import Utiles


def alta():
    print("Alta curso:")
    done = False
    while not done:
        descripcion = None
        nombre = Utiles.check_campo("nombre", 25)
        if nombre is not None and GestorBaseDeDatos.select1("Cursos", nombre) is None:
            descripcion = Utiles.check_campo("Descripcion", 50)
        else:
            if GestorBaseDeDatos.select1("Cursos", nombre) is not None:
                print("El nombre pertenece a otro curso")
        if descripcion is not None:
            datos = {'nombre': nombre, 'descripcion': descripcion}
            if GestorBaseDeDatos.insert('Cursos', datos):
                print('Alta realizada con exito' + '\n')
            else:
                print('Fallo al realizar el alta.' + '\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro curso?"):  # Preguntamos si quiere dar otro curso de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print("\n")


def baja():
    if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
        print("Baja curso:")
        done = False
        while not done:
            nombre = Utiles.check_campo("nombre", 25)
            if nombre is not None:
                curso = GestorBaseDeDatos.select1("Cursos", nombre)
                if curso is not None:
                    if Utiles.confirmacion("Seguro que desea eliminar " + curso.nombre + " del centro?"):
                        if GestorBaseDeDatos.delete("Cursos", nombre):
                            print('Alta realizada con exito' + '\n')
                        else:
                            print('Fallo al realizar el alta.' + '\n')
                    else:
                        print("Baja cancelada." + '\n')
                else:
                    print("El nombre no se corresponde con el de ningun curso existente." + '\n')
            if len(GestorBaseDeDatos.selectAll2("Cursos")) == 0:
                print("Ya no quedan cursos que borrar.")
                done = True
                print("-" * 20 + "\n")
            else:
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro curso?"):
                    done = True
                    print("-" * 20 + "\n")
                else:
                   print("\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def modificacion(curso):
    elec = ""
    cont = 0
    while(elec != "0"):
        elec = input("1. Nombre\n2. Descripcion\n0. Volver\n")
        if elec == "1":
            nueNomb = Utiles.check_campo("nombre", 25)
            if nueNomb is not None and GestorBaseDeDatos.select1("Cursos", nueNomb) is None:
                if Utiles.confirmacion("Seguro que desea modificar el nombre " + curso.nombre + " por " + nueNomb + "?"):
                    if BaseDeDatosM.update("Cursos", "nombre", curso.nombre, nueNomb):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')
            else:
                if GestorBaseDeDatos.select1("Cursos", nueNomb) is not None:
                    print("El nombre pertenece a otro curso")

        elif elec == "2":
            nueDesc = Utiles.check_campo("descripcion", 25)
            if nueDesc is not None:
                if Utiles.confirmacion("Seguro que desea modificar la descripcion " + curso.descipcion + " por " + nueDesc + "?"):
                    if BaseDeDatosM.update("Cunsos", "descripcion", curso.nombre, nueDesc):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')

        elif elec == "0":
            print("Saliendo de menu de modificacion." + "\n")
        else:
            print("Opticon no valida")
            cont += 1
            print("Fallos ", cont, "/5")
            if cont == 5:
                print("Cometiste demasiados fallos")
                elec = "0"


def modificar():
    if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
        print("Modificar curso")
        done = False
        while not done:
            nombre = Utiles.check_campo("nombre", 25)
            if nombre is not None:
                curso = GestorBaseDeDatos.select1("Cursos", nombre)
                if curso is not None:
                    modificacion(curso)

            if not Utiles.confirmacion("Quieres tratar de dar de modificar otro curso?"):
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def buscar():
    if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
        print("Buscar curso")
        done = False
        while not done:
            nombre = Utiles.check_campo("nombre", 25)
            if nombre is not None:
                curso = GestorBaseDeDatos.select1("Cursos", nombre)
                if curso is not None:
                    print("Nombre: " + curso.nombre)
                    print("Descripcion: " + curso.descripcion)
                    print()

                else:
                    print("El nombre no se corresponde con el de ningun curso existente." + '\n')

            if not Utiles.confirmacion("Quieres tratar de dar de buscar otro curso?"):
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def mostrarTodos():
    if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
        print("Mostrar todos los cursos:")
        cursos = GestorBaseDeDatos.selectAll2("Cursos")
        for curso in cursos:
            print()
            print("Nombre: " + curso['nombre'])
            print("Descripcion: " + curso['descripcion'])

        print("-" * 20 + "\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def relacionCursProf(curso):
    print("Introduzca el dni del profesor que desea modificar.")
    dni = Utiles.check_dni()
    if dni is not None:
        profesor = GestorBaseDeDatos.select1("Profesores", dni)
        if profesor is not None:
            aux = BaseDeDatosM.selectJoin("Cursos", curso.nombre)
            print(aux, type(aux))
            for row in aux:
                print()
        else:
            print("El dni no se corresponde con el de ningun profesor existente." + '\n')


def relacionarCursAlum(curso):
    return None


def relacionar():
    if len(GestorBaseDeDatos.selectAll2("Alumnos")) > 0 or len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
        if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
            lista = BaseDeDatosM.selectAll("Cursos")
            print(lista, type(lista))
            print("Relacionar curso:")
            done = False
            while not done:
                nombre = Utiles.check_campo("nombre", 25)
                if nombre is not None:
                    curso = GestorBaseDeDatos.select1("Cursos", nombre)
                    if curso is not None:
                        elec = ""
                        cont = 0
                        while elec != "0":
                            elec = input("1. Relacion cursos con profesores\n2. Relacionar cursos con alumnos\n0. Salir\n")
                            if elec == "1":
                                if len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
                                    relacionCursProf(curso)

                                else:
                                    print("No hay profesores creados.")
                                    cont += 1
                                    print("Fallos ", cont, "/5")
                                    if cont == 5:
                                        print("Cometiste demasiados fallos.")
                                        elec = "0"

                            elif elec == "2":
                                if len(GestorBaseDeDatos.selectAll2("Alumnos")) > 0:
                                    relacionarCursAlum(curso)

                                else:
                                    print("No hay alumnos creados.")
                                    cont += 1
                                    print("Fallos ", cont, "/5")
                                    if cont == 5:
                                        print("Cometiste demasiados fallos.")
                                        elec = "0"

                            elif elec == "0":
                                print("Saliendo del menu relacionar.")
                            else:
                                print("Opticon no valida")
                                cont += 1
                                print("Fallos ", cont, "/5")
                                if cont == 5:
                                    print("Cometiste demasiados fallos.")
                                    elec = "0"
                    else:
                        print("El nombre no pertenece al de ningun curso.")

                if not Utiles.confirmacion("Quieres tratar de relacionar otro curso?"):
                    done = True
                    print("-" * 20 + "\n")
                else:
                    print("\n")

        else:
            print("No hay cursos creados.")
            print("-" * 20 + "\n")
    else:
        print("No hay ni profesores ni alumnos creados.")
        print("-" * 20 + "\n")