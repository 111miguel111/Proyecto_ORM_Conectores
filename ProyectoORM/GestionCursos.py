import GestorBaseDeDatos
import Utiles


def alta():
    """
    Funcion que pide los campos para el insert y, si todos son correctos pide a la bbdd que realice el insert.
    """
    print("Alta curso:")
    done = False
    while not done:  #Este bucle se asegura de que se puedan dar de alta mas de un curso.
        descripcion = None #Evitar el warning
        nombre = Utiles.check_campo("nombre", 25) #Pedimos dato
        if nombre is not None and GestorBaseDeDatos.select1("Cursos", nombre) is None: #Si es valido y no pertenece a otro curso.
            descripcion = Utiles.check_campo("Descripcion", 50) #Se continuan pidiendo datos
        else:
            if GestorBaseDeDatos.select1("Cursos", nombre) is not None: #Si es valido pero pertenece a otro curso.
                print("El nombre pertenece a otro curso")
        if descripcion is not None: #Si todos los datos son correcto.
            datos = {'nombre': nombre,
                     'descripcion': descripcion} #Se crea un diccionario con los datos que se mandara al insert
            if GestorBaseDeDatos.insert('Cursos', datos): #Se manda el insert y si sale bien se notifica
                print('Alta realizada con exito' + '\n')
            else: #SI sale mal se notifica el fallo.
                print('Fallo al realizar el alta.' + '\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro curso?"):  # Preguntamos si quiere dar otro curso de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print()


def baja():
    """
    Funcion para elegir un curso y borrarlo.
    """
    if len(GestorBaseDeDatos.selectAll("Cursos")) > 0: #Si no hay curso pues no entras.
        print("Baja curso:")
        done = False
        while not done: #Para dar de baja varios cursos a en la misma tacada.
            nombre = Utiles.check_campo("nombre", 25) #Nombre
            if nombre is not None: #Si es valido
                curso = GestorBaseDeDatos.select1("Cursos", nombre) #Peewee model a traves de un select
                if curso is not None: #Si existe el peewee model
                    if Utiles.confirmacion("Seguro que desea eliminar " + curso.nombre + " del centro?"): #Se pide confirmacion
                        if GestorBaseDeDatos.delete("Cursos", nombre): #Si el delete sale bien se notifica
                            print('Baja realizada con exito' + '\n')
                        else:
                            print('Fallo al realizar el baja.' + '\n')
                    else:
                        print("Baja cancelada." + '\n')
                else: #Si el curso es None
                    print("El nombre no se corresponde con el de ningun curso existente." + '\n')

            if len(GestorBaseDeDatos.selectAll("Cursos")) == 0: #Si tras el delete no quedan cursos te expulso de la baja
                print("Ya no quedan cursos que borrar.")
                done = True
                print("-" * 20 + "\n")
            else: #Si quedan cursos pues se pregunta si se quiere borrar otro.
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro curso?"):
                    done = True
                    print("-" * 20 + "\n")
                else:
                    print("\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def modificacion(curso):
    """
    Funcion que modifica un curso existente campo por campo.
    :param curso: un peewee model
    """
    elec = ""
    cont = 0 #Fallos
    while (elec != "0"): #Mientras que no quieras salir o falles 5 veces puedes cambiar cosas
        elec = input("1. Nombre\n2. Descripcion\n0. Volver\n")
        if elec == "1": #Nombre
            nueNomb = Utiles.check_campo("nombre", 25) #Dato
            if nueNomb is not None and GestorBaseDeDatos.select1("Cursos", nueNomb) is None: #Si es valido y no pertenece a otro curso
                if Utiles.confirmacion("Seguro que desea modificar el nombre " + curso.nombre + " por " + nueNomb + "?"): #Se pide confirmacion
                    if GestorBaseDeDatos.update("Cursos", "nombre", curso.nombre, nueNomb): #Si el update sale bien se notifica
                        curso.nombre = nueNomb #Actualizamos datos para posibles updates sucesivos
                        curso = GestorBaseDeDatos.select1("Cursos", curso.nombre)
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')
            else:
                if GestorBaseDeDatos.select1("Cursos", nueNomb) is not None: #Si es valido pero pertenece a un profesor existente
                    print("El nombre pertenece a otro curso")

        elif elec == "2": #Direccion
            nueDesc = Utiles.check_campo("descripcion", 25) #Dato
            if nueDesc is not None: #Si es valido
                if Utiles.confirmacion("Seguro que desea modificar la descripcion " + curso.descripcion + " por " + nueDesc + "?"): #Confirmacion
                    if GestorBaseDeDatos.update("Cursos", "descripcion", curso.nombre, nueDesc): #Si el update sale bien se notifica
                        print("Modificacion realizda con exito." + '\n')
                        curso = GestorBaseDeDatos.select1("Cursos", curso.nombre)
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
            if cont == 5: #Si llegas a 5 fallos te echo.
                print("Cometiste demasiados fallos")
                elec = "0"


def modificar():
    """
    Funcion que selecciona un curso y lo manda a 'modificar'.
    """
    if len(GestorBaseDeDatos.selectAll("Cursos")) > 0: #Si no hay cursos pues no entras.
        print("Modificar curso")
        done = False
        while not done: #Para modificar mas de uno.
            nombre = Utiles.check_campo("nombre", 25) #Nombre para buscar.
            if nombre is not None: #Si es valido.
                curso = GestorBaseDeDatos.select1("Cursos", nombre) #peewee model a traves de un select.
                if curso is not None: #Si el curso existe.
                    modificacion(curso) #Esta funcion modifica.

            if not Utiles.confirmacion("Quieres tratar de dar de modificar otro curso?"): #Para modificar mas de uno.
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def buscar():
    """
    Funcion que busca y printea cursos.
    """
    if len(GestorBaseDeDatos.selectAll("Cursos")) > 0: #Si hay cursos.
        print("Buscar curso")
        done = False
        while not done: #Para buscar mas de uno.
            nombre = Utiles.check_campo("nombre", 25) #Se busca por nombre.
            if nombre is not None: #Si es valido.
                curso = GestorBaseDeDatos.select1("Cursos", nombre) #Peewee model.
                if curso is not None: #Si existe el curso.
                    print()  #Formato.
                    datos = GestorBaseDeDatos.selectJoinMostrar("Cursos", curso) #Datos relativos a los profesores y alumnos.
                    print("Nombre: " + datos[0]['nombre']) #Datos del curso.
                    print("Descripcion: " + datos[0]['descripcion'])
                    if len(datos[1]) > 0:  # Hay profesor
                        print("Profesor: ", datos[1][0]['nombre'], datos[1][0]['dni']) #Se printea el profesor.
                    else:
                        print("Profesor: No tiene.")
                    if len(datos[2]) > 0:  # Hay alumnos.
                        print("Alumnos: | ", end="") #Formato.
                        for alumnos in datos[2]: #Se recorren los alumnos.
                            print(alumnos["nombre"], " | ", end="") #Se van printeando.
                        print('\n')
                    else:
                        print("Alumnos: No tiene.")

                else: #Para cuando no existe.
                    print("El nombre no se corresponde con el de ningun curso existente." + '\n')

            if not Utiles.confirmacion("Quieres tratar de dar de buscar otro curso?"): #Para buscar varios.
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def mostrarTodos():
    """
    funcion que muestra todos los cursos.
    """
    if len(GestorBaseDeDatos.selectAll("Cursos")) > 0: #Si hay cursos si no no entras
        print("Mostrar todos los cursos:")
        cursos = GestorBaseDeDatos.selectAll("Cursos") #Cogemos todos los cursos
        print() #Formato
        for curso in cursos: #Recorremos los cursos
            aux = GestorBaseDeDatos.select1("Cursos", curso["nombre"]) #Peewee model a traves del nombre.
            datos = GestorBaseDeDatos.selectJoinMostrar("Cursos", aux) #Datos del curso relativo a profs y alumnos
            print("Nombre: " + datos[0]['nombre']) #Datos del curso
            print("Descripcion: " + datos[0]['descripcion'])
            if len(datos[1]) > 0: #Hay profesor
                print("Profesor: ", datos[1][0]['nombre'], datos[1][0]['dni']) #Profesor
            else:
                print("Profesor: No tiene.")
            if len(datos[2]) > 0: #Hay alumnos
                print("Alumnos: | ", end="")
                for alumnos in datos[2]:  #Recorremos alumnos printeo
                    print(alumnos["nombre"], " | ", end="")
                print('\n')
            else:
                print("Alumnos: No tiene.")
            print()
        print("-" * 20 + "\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")


def relacionCursProf(curso):
    """
    Funcion que relaciona un curso con un profesor.
    :param curso: peewee model que sera relacionado.
    """
    print("Introduzca el dni del profesor que desea modificar.")
    dni = Utiles.check_dni() #Pedimos dni
    if dni is not None: #Si es valido
        profesor = GestorBaseDeDatos.select1("Profesores", dni) #Peewee model
        if profesor is not None:  #Si exsite
            datos = {"cod_curs": curso.cod_curs,
                     "id_prof": profesor.id_prof} #Diccionario con los datos del profesor y el curso

            aux = GestorBaseDeDatos.selectJoin("CursosEnProfesores", curso.cod_curs) #Un select para saber si el curso tiene profesor ya

            if len(aux) > 0:    #Hay profesor.
                aux = GestorBaseDeDatos.selectJoin("Cursos_Profesores", datos)
                if len(aux) > 0:    #El profesor es el profesor actual del curso.
                    print(profesor.nombre + " ya es el profesor de " + curso.nombre) #Se notifica.
                else:   #Hay que sustiruir al profesor.
                    oldProf = GestorBaseDeDatos.selectJoin("ProfesorEnUnCurso", curso.cod_curs)

                    datos2 = {'cod_curs': curso.cod_curs, 'id_prof': oldProf.id_prof} #Datos del prof antiguo.
                    #Se pide confirmacion.
                    if Utiles.confirmacion("Seguro que quieres que " + profesor.nombre + " sustituya a " + oldProf.nombre + " en el curso: " + curso.nombre + "? Esto sobre escribira el profesor actual de " +curso.nombre):
                        if GestorBaseDeDatos.delete("Cursos_Profesores", datos2): #Si el delete sale bien.
                            if GestorBaseDeDatos.insert("Cursos_Profesores", datos): #Se inserta, y si sale bien se notifica.
                                print("Relacion realizda con exito." + '\n')
                            else:
                                print("La modificacion no se pudo realizar." + '\n')
                        else:
                            print("La modificacion no se pudo realizar." + '\n')
                    else:
                        print("Relacion cancelada." + "\n")
            else:   #No hay profesor.
                #Se pide confirmacion del insert.
                if Utiles.confirmacion("Seguro que quieres que " + profesor.nombre + " imparta " + curso.nombre + "?"):
                    if GestorBaseDeDatos.insert("Cursos_Profesores", datos): #Se realiza el nsert y si sale bien se notifica.
                        print("Relacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Relacion cancelada." + "\n")
        else:
            print("El dni no se corresponde con el de ningun profesor existente." + '\n')


def desrelacionarCursProf(curso):
    """
    Funcion que desrelaciona un curso y un profesor.
    :param curso: el peewee model del curso que sera desrelacionado.
    """
    if len(GestorBaseDeDatos.selectJoin("CursosEnProfesores", curso.cod_curs)) > 0: #Si el curso tiene profesor puedes pasar si no no.
        profesor = GestorBaseDeDatos.selectJoin("CursosEnProfesores", curso.cod_curs) #Un select para saber los datos del profesor.
        #Confirmacion.
        if Utiles.confirmacion("Seguro que quiere que " + str(profesor.nombre) + " deje de ser el profesor de " + curso.nombre):
            datos = {"cod_curs": curso.cod_curs,
                     "id_prof": profesor.id_prof} #Datos de curso y profeor.
            if GestorBaseDeDatos.delete("Cursos_Profesores", datos): #Si el delete sale bien se notifica.
                print("Desrelacion realizda con exito." + '\n')
            else:
                print("Hubo un error en la desrelacion")
        else:
            print("Relacion cancelada." + "\n")
    else: #El curso no tenia profesor que desrelacionar
        print(curso.nombre + " no tiene un profesor que desrelacionar."+ "\n")


def relacionarCursAlum(curso):
    """
    Funcion que relaciona un curso y un alumno
    :param curso: peewee model que sera relaion
    """
    print("Introduzca el nombre del alumno que desea relacionar.")
    apellido = None #Para que el IDE no se ponga nervioso
    nombre = Utiles.check_campo("nombre", 25) #El campo
    if nombre is not None: #Si es valido se pide el apellido
        print("Introduzca el apellido del alumno que desea relacionar.")
        apellido = Utiles.check_campo("apellido", 25)
    if apellido is not None: #Si el apellido es valido.
        primary = {'nombre': nombre,
                   'apellido': apellido} #Dirciconaro con los datos
        alumno = GestorBaseDeDatos.select1("Alumnos", primary) #Cogemos el peewee model del alumnos
        if alumno is not None: #Si existe
            datos = {"cod_curs": curso.cod_curs,
                     "num_exp": alumno.num_exp} #Se crea un diccionario para el isnert
            aux = GestorBaseDeDatos.selectJoin("CursosEnAlumnos", curso.cod_curs) #Vemos si el curso tiene alumnos

            if len(aux) > 0:    #Hay alumnos
                aux = GestorBaseDeDatos.selectJoin("Cursos_Alumnos", datos) #Se pide un peewee model para saber si el alumno ya pertenece al curso
                if len(aux) > 0:    #El alumno ya esta en el curso.
                    print(alumno.nombre + " " + alumno.apellido + " ya esta matriculado en " + curso.nombre) #Se notifica.
                else:   #El alumno no esta en el curso.
                    #Se pide confirmacion.
                    if Utiles.confirmacion("Seguro que quieres que " + alumno.nombre + " " + alumno.apellido + " sea matriculado en " + curso.nombre + "?\n "):
                        if GestorBaseDeDatos.insert("Cursos_Alumnos", datos): #Si el insert sale bien se notifica.
                            print("Relacion realizda con exito." + '\n')
                        else:
                            print("La relacion no se pudo realizar." + '\n')

                    else:
                        print("Relacion cancelada." + "\n")
            else:   #No hay alumnos.
                #Se pide confirmacion.
                if Utiles.confirmacion("Seguro que quieres que " + alumno.nombre + " " + alumno.apellido + " sea matriculado en " + curso.nombre + "?\n "):
                    if GestorBaseDeDatos.insert("Cursos_Alumnos", datos): #Si el insert es correcto se notifica.
                        print("Relacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Relacion cancelada." + "\n")
        else:
            print("El nombre y apellido no se corresponden con el de ningun alumno existente." + '\n')


def desrelacionarCursAlum(curso):
    """
    Funcion que desvincula un curso y un alumno.
    :param curso: peewee model que sera desrelacionado.
    """
    if len(GestorBaseDeDatos.selectJoin("CursosEnAlumnos", curso.cod_curs)) > 0: #Si el curso tiene alumnos bien, si no no..
        print("Introduzca el nombre del alumno que desea desmatricular.")
        apellido = None
        nombre = Utiles.check_campo("nombre",25) #Nombre para buscar.
        if nombre is not None: #Si es valido.
            print("Introduzca el apellido del alumno que desea desmatricular.")
            apellido = Utiles.check_campo("apellido", 25) #Se pide apellido.
        if apellido is not None: #Si es valido.
            primary = {'nombre': nombre,
                       'apellido': apellido} #Diccionario para los datos.
            alumno = GestorBaseDeDatos.select1("Alumnos", primary) #Curso para ver si el alumno pertenece al curso.
            if alumno is not None: #SI el alumno existe
                datos = {"cod_curs": curso.cod_curs,
                         "num_exp": alumno.num_exp} #Diccionario para el delete
                aux = GestorBaseDeDatos.selectJoin("Cursos_Alumnos", datos) #Para ver si pertenece
                if len(aux) > 0:    #El alumno  esta en el curso.
                    #SI se da confirmacion.
                    if Utiles.confirmacion("Seguro que quiere desmatricular " + str(alumno.nombre) + " " + str(alumno.apellido) + " de " + curso.nombre):
                        if GestorBaseDeDatos.delete("Cursos_Alumnos", datos): #Se hace el delete y si sale bien se notifica.
                            print("Desrelacion realizda con exito." + '\n')
                        else:
                            print("Hubo un error en la desrelacion")
                    else:
                        print("Relacion cancelada." + "\n")
                else:   #El alumno no esta en el curso.
                    print(alumno.nombre + " " + alumno.apellido + " no esta matriculado en " + curso.nombre)
            else:
                print("El nombre y apellido no se corresponden con el de ningun alumno existente." + '\n')
    else:
        print(curso.nombre + " no tiene alumnos que desrelacionar."+ "\n")


def relacionar():
    """
    Funcion que relaciona cursos con alumnos y profesores.
    """
    if len(GestorBaseDeDatos.selectAll("Cursos")) > 0:  # SI no hay cursos no pasas
        if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0 or len(GestorBaseDeDatos.selectAll("Profesores")) > 0:  # S no hay profesores ni alumnos no pasas
            print("Relacionar curso:")
            lista = GestorBaseDeDatos.selectAll("Cursos") #Todos los cursos, para que el usuario sepa que puede relacionar
            print("Cursos existentes: ", end="")
            for curso in lista:
                print(curso['nombre'], " ", end="")
            print()
            done = False
            while not done: #Para relacionar mas de una
                nombre = Utiles.check_campo("nombre", 25) #Para buscar el curso
                if nombre is not None: #SI es valio
                    curso = GestorBaseDeDatos.select1("Cursos", nombre) #Peewee model para relacionarla
                    if curso is not None: #Si es curso existe
                        elec = ""
                        cont = 0
                        while elec != "0": #Para que se decida el usuario que es lo que quiere relacionar
                            elec = input("1. Relacion cursos con profesores\n2. Relacionar cursos con alumnos\n0. Salir\n")
                            if elec == "1": #Profesores
                                if len(GestorBaseDeDatos.selectAll("Profesores")) > 0: #Por si pasas habiendo alumnos pero no profes
                                    elec2 = ""
                                    cont2 = 0
                                    while elec2 != "0": #Por si quieres hacer mas de una cosa
                                        elec2 = input("1. Relacionar\n2. Desrelacionar\n0. Salir\n")
                                        if elec2 == "1":
                                            relacionCursProf(curso) #Relacionar curs y profs
                                        elif elec2 == "2":
                                            desrelacionarCursProf(curso) #Desrelacionar curs y profs
                                        elif elec2 == "0":
                                            print("Saliendo del menu relacionar.")
                                        else:
                                            print("Opticon no valida")
                                            cont2 += 1
                                            print("Fallos ", cont2, "/5") #Si fallas 5 veces fuera
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
                                if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0: #Por si pasas habiendo profes pero no alumnos
                                    elec2 = ""
                                    cont2 = 0
                                    while elec2 != "0": #Para elegir mas de una accion
                                        elec2 = input("1. Relacionar\n2. Desrelacionar\n0. Salir\n")
                                        if elec2 == "1":
                                            relacionarCursAlum(curso) #Relacionar alumnos cursos
                                        elif elec2 == "2":
                                            desrelacionarCursAlum(curso) #Desrelacionar alumnos cursos
                                        elif elec2 == "0":
                                            print("Saliendo del menu relacionar.")
                                        else:
                                            print("Opticon no valida")
                                            cont2 += 1
                                            print("Fallos ", cont2, "/5")
                                            if cont2 == 5:  #Si fallas 5 veces fuera
                                                print("Cometiste demasiados fallos.")
                                                elec2 = "0"

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

                if not Utiles.confirmacion("Quieres tratar de relacionar otro curso?"): #Para relacionar mas de un cursp
                    done = True
                    print("-" * 20 + "\n")
                else:
                    print("\n")
        else:
            print("No hay ni profesores ni alumnos creados.")
            print("-" * 20 + "\n")
    else:
        print("No hay cursos creados.")
        print("-" * 20 + "\n")