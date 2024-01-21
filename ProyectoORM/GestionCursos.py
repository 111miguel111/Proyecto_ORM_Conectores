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

        if not Utiles.confirmacion(
                "Quieres tratar de dar de alta otro curso?"):  # Preguntamos si quiere dar otro curso de alta
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
    while (elec != "0"):
        elec = input("1. Nombre\n2. Descripcion\n0. Volver\n")
        if elec == "1":
            nueNomb = Utiles.check_campo("nombre", 25)
            if nueNomb is not None and GestorBaseDeDatos.select1("Cursos", nueNomb) is None:
                if Utiles.confirmacion(
                        "Seguro que desea modificar el nombre " + curso.nombre + " por " + nueNomb + "?"):
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
                if Utiles.confirmacion(
                        "Seguro que desea modificar la descripcion " + curso.descipcion + " por " + nueDesc + "?"):
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
            datos = {"cod_curs": curso.cod_curs,
                     "id_prof": profesor.id_prof}
            print(curso.nombre, curso.cod_curs)
            aux = BaseDeDatosM.selectJoin("CursosEnProfesores", curso.cod_curs)

            if len(aux) > 0:    #Hay profesor
                aux = BaseDeDatosM.selectJoin("Cursos_Profesores", datos)
                if len(aux) > 0:    #El profesor es el profesor actual del curso
                    print(profesor.nombre + " ya es el profesor de " + curso.nombre)
                else:   #Hay que sustiruir al profesor
                    if Utiles.confirmacion("Seguro que quieres que " + profesor.nombre + " imparta " + curso.nombre + "?\n Esto sobre escribira el profesor actual de " +curso.nombre):
                        if GestorBaseDeDatos.insert("Cursos_Profesores", datos):
                            print("Relacion realizda con exito." + '\n')
                        else:
                            print("La modificacion no se pudo realizar." + '\n')

                    else:
                        print("Relacion cancelada." + "\n")
            else:   #No hay profesor
                if Utiles.confirmacion("Seguro que quieres que " + profesor.nombre + " imparta " + curso.nombre + "?"):

                    if GestorBaseDeDatos.insert("Cursos_Profesores", datos):
                        print("Relacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Relacion cancelada." + "\n")
        else:
            print("El dni no se corresponde con el de ningun profesor existente." + '\n')


def desrelacionarCursProf(curso):
    if len(BaseDeDatosM.selectJoin("CursosEnProfesores", curso.cod_curs)) > 0:
        profesor = (BaseDeDatosM.Profesores.select(BaseDeDatosM.Profesores).join(BaseDeDatosM.Cursos_Profesores).join(BaseDeDatosM.Cursos)
                         .where(BaseDeDatosM.Cursos.cod_curs == curso.cod_curs & BaseDeDatosM.Cursos_Profesores.cod_curs == BaseDeDatosM.Cursos.cod_curs & BaseDeDatosM.Profesores.id_prof == BaseDeDatosM.Cursos_Profesores.id_prof)).get()

        print(profesor, type(profesor))
        if Utiles.confirmacion("Seguro que quiere que " + str(profesor.nombre) + " deje de ser el profesor de " + curso.nombre):
            datos = {"cod_curs": curso.cod_curs,"id_prof": profesor.id_prof}
            if GestorBaseDeDatos.delete("Cursos_Profesores", datos):
                print("Desrelacion realizda con exito." + '\n')
            else:
                print("Hubo un error en la desrelacion")
        else:
            print("Relacion cancelada." + "\n")
    else:
        print(curso.nombre + " no tiene un profesor que desrelacionar."+ "\n")


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
                                    elec2 = ""
                                    cont2 = 0
                                    while elec2 != "0":
                                        elec2 = input("1. Relacionar\n2. Desrelacionar\n0. Salir\n")
                                        if elec2 == "1":
                                            relacionCursProf(curso)
                                        elif elec2 == "2":
                                            desrelacionarCursProf(curso)
                                        elif elec2 == "0":
                                            print("Saliendo del menu relacionar.")
                                        else:
                                            print("Opticon no valida")
                                            cont2 += 1
                                            print("Fallos ", cont2, "/5")
                                            if cont2 == 5:
                                                print("Cometiste demasiados fallos.")
                                                elec2 = "0"

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
