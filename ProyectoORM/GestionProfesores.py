import GestorBaseDeDatos
import Utiles


def alta():
    """
    Funcion que pide los campos para el insert y, si todos son correctos pide a la bbdd que realice el insert.
    """
    print("Alta profesor:")
    done = False
    while not done:  #Este bucle se asegura de que se puedan dar de alta mas de un profesor.
        nombre = None
        telefono = None
        direccion = None  #Para evitar el warning de las variables.
        dni = Utiles.check_dni()
        # Este if se asegura de que el dni no pertenece a un profesor existente
        if dni is not None and GestorBaseDeDatos.select1("Profesores", dni) is None:
            nombre = Utiles.check_campo("nombre", 25)
        else:
            if GestorBaseDeDatos.select1("Profesores", dni) is not None: #Si el dni perteneciese lo notifica
                print("El dni pertenece a otro profesor")
        if nombre is not None:
            telefono = Utiles.check_telefono()
        if telefono is not None:
            direccion = Utiles.check_campo("direccion", 50)
        if direccion is not None:  #Tras chequear los campos, si todos estan bien creamos un diccionario con los datos
            datos = {'dni': dni,
                     'nombre': nombre,
                     'telefono': telefono,
                     'direccion': direccion}

            if GestorBaseDeDatos.insert('Profesores', datos): #Si el insert funciona se notifica
                print('Alta realizada con exito'+'\n')
            else:
                print('Fallo al realizar el alta.'+'\n')
        if not Utiles.confirmacion("Quieres tratar de dar de alta otro profesor?"):  # Preguntamos si quiere dar otro profesor de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print()


def baja():
    """
    Funcion que se encarga de la obtencion del profesor por el dni y, tras la confirmacion lo elimina
    """
    if len(GestorBaseDeDatos.selectAll("Profesores")) > 0:  #Si no existen profesores no entras a la baja
        print("Baja profesor:")
        done = False
        while not done: #Para borrar mas de uno
            print("Introduzca el dni del profesor que desea eliminar.")
            dni = Utiles.check_dni()
            if dni is not None:  #Si el dni es valido
                profesor = GestorBaseDeDatos.select1("Profesores", dni) #cogemos el peeweemodel
                if profesor is not None:  #Si existe (Es decir, que el dni pertenece a un profesor)
                    if Utiles.confirmacion("Seguro que desea eliminar a " + profesor.nombre + " del centro?"): #Pides confirmacion
                        if GestorBaseDeDatos.delete('Profesores', dni): #Si la baja es fructifera
                            print("Baja realizda con exito."+'\n') #Se notifica
                        else:
                            print("Baja no se realizo." + '\n')
                    else:
                        print("Baja cancelada."+'\n')

                else:
                    print("El dni no se corresponde con el de ningun profesor existente."+'\n')
            if len(GestorBaseDeDatos.selectAll("Profesores")) == 0: #Si tras la baja el total de profesores es 0 te expulso de la baja
                print("Ya no quedan profesores que borrar.")
                done = True
                print("-" * 20 + "\n")
            else:
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro profesor?"): #Esto es para borrar mas de uno
                    done = True
                    print("-" * 20 + "\n")
                else:
                   print("\n")
    else:
        print("No hay profesores creados.")
        print("-" * 20 + "\n")


def modificacion(profesor):
    """
    Funcion que se cambian los datos del profesor, esta separado de 'modificar' para que sea mas claro visualmente
    :param profesor: un peewee model con el profesor
    """
    elec = ""
    cont = 0
    while elec != "0": #el switch tipico aunque sea con if-else
        elec = input("1. Nombre\n2. DNI\n3. Telefono\n4. Direccion\n0. Volver\n")
        if elec == "1": #Nombre
            nueNomb = Utiles.check_campo("nombre", 25)  #Nuevos campos
            if nueNomb is not None: #Se comprueba que son validos
                if Utiles.confirmacion("Seguro que desea modificar el nombre " + profesor.nombre + " por " + nueNomb + "?"): #Pedimos confirmacion
                    if GestorBaseDeDatos.update("Profesores", "nombre", profesor.dni, nueNomb): #Si el update sale bien se notifica.
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')

        elif elec == "2": #DNI
            nueDni = Utiles.check_dni()
            if nueDni is not None and GestorBaseDeDatos.select1("Profesores", nueDni) is None: #Se comprueba que es valido y no pertenece a ningun profesor
                if Utiles.confirmacion("Seguro que desea modificar el dni " + profesor.dni + " por " + nueDni + "?"): #Pedimos confirmacion
                    if GestorBaseDeDatos.update("Profesores", "dni", profesor.dni, nueDni): #Updateamos
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')

            else:
                if GestorBaseDeDatos.select1("Profesores", nueDni) is not None: #Esto es por si el nuevo dni perteneciese a un prof existente
                    print("El dni pertenece a otro profesor ya existente")

        elif elec == "3": #Telefono. Es lo mismo que nombre
            nueTelf = Utiles.check_telefono()
            if nueTelf is not None:
                if Utiles.confirmacion(
                        "Seguro que desea modificar el telefono " + profesor.telefono + " por " + nueTelf + "?"):
                    if GestorBaseDeDatos.update("Profesores", "telefono", profesor.dni, nueTelf):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')

        elif elec == "4": #Direccion. Es lo mismo que nombre
            nueDire = Utiles.check_campo("direccion", 25)
            if nueDire is not None:
                if Utiles.confirmacion(
                        "Seguro que desea modificar la direccion " + profesor.direccion + " por " + nueDire + "?"):
                    if GestorBaseDeDatos.update("Profesores", "direccion", profesor.dni, nueDire):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')

        elif elec == "0":
            print("Saliendo de menu de modificacion." + "\n")
        else: #El menu de mofificacion tambien te expulsa, y no es permisivo, acumula fallos entre updates.
            print("Opticon no valida")
            cont += 1
            print("Fallos ", cont, "/5")
            if cont == 5:
                print("Cometiste demasiados fallos")
                elec = "0"


def modificar():
    """
    Funcion que se encarga de seleccionar un profesor existente y lo manda a la funcion modificacion.
    """
    if len(GestorBaseDeDatos.Profesores.select()) > 0: #Si no hay profs no entras
        print("Modificacion profesor:")
        done = False
        while not done:  #Para modificar mas de uno
            print("Introduzca el dni del profesor que desea modificar.")
            dni = Utiles.check_dni()
            if dni is not None: #Si el dni es valido
                profesor = GestorBaseDeDatos.select1("Profesores", dni) #Pedimos un peewee model a traves de un select
                if profesor is not None: #Si existe el prof
                    modificacion(profesor) #Lo mando a modificar

                else:
                    print("El dni no se corresponde con el de ningun profesor existente."+'\n')

            if not Utiles.confirmacion("Quieres tratar de modificar otro profesor?"): #Borrar mas de uno
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay profesores creados")
        print("-" * 20 + "\n")


def buscar():
    """
    Funcion que busca y printea un profesor y los cursos que imparte
    """
    if len(GestorBaseDeDatos.selectAll("Profesores")) > 0: #Si no hay profesor no entras
        print("Buscar profesor:")
        done = False
        while not done: #Para buscar mas de uno
            print("Introduzca el dni del profesor que desea buscar.")
            dni = Utiles.check_dni() #Pedimos dni
            if dni is not None: #Si es valido
                profesor = GestorBaseDeDatos.select1("Profesores", dni) #Peewee model a traves de un select con el dni
                if profesor is not None: #Si existe
                    datos = GestorBaseDeDatos.selectJoinMostrar("Profesores", profesor) #Conseguimos los datos relativos a los cursos
                    print() #Mostramos (El print vacio es para darle formato)
                    print("Nombre: " + datos[0]['nombre'])
                    print("Dni: " + datos[0]['dni'])
                    print("Telefono: " + datos[0]['telefono'])
                    print("Direccion: " + datos[0]['direccion'])
                    if len(datos[1]) > 0: #Si tiene cursos
                        for curso in datos[1]: #Se recorern los cursos y se printean
                            print("Cursos: ", curso['nombre'], " ", end="")
                        print()
                    else:
                        print()

                else:
                    print("El dni no se corresponde con el de ningun profesor existente." + '\n')

            if not Utiles.confirmacion("Quieres tratar de buscar otro profesor?"): #Para buscar mas de un profesor
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay profesores creados")
        print("-" * 20 + "\n")


def mostrarTodos():
    """
    Muestra todos los profesores existentes
    """
    if len(GestorBaseDeDatos.selectAll("Profesores")) > 0: #Si no hay profesores no entras
        print("Mostrar todos los profesores:")
        profesores = GestorBaseDeDatos.selectAll("Profesores") #Conseguimos todos los profesores
        print() #Formato
        for profesor in profesores: #Recorremos los profesores
            aux = GestorBaseDeDatos.select1("Profesores", profesor['dni']) #Peewee model del profesor
            datos = GestorBaseDeDatos.selectJoinMostrar("Profesores", aux) #Lista completa de datos del profesor
            print("Nombre: " + datos[0]['nombre']) #Printear datos
            print("Dni: " + datos[0]['dni'])
            print("Telefono: " + datos[0]['telefono'])
            print("Direccion: " + datos[0]['direccion'])
            if len(datos[1]) > 0: #Si hay cursos se recorren y printean
                for curso in datos[1]:
                    print("Cursos: ", curso['nombre'], " ", end="")
                print('\n')
            else:
                print("Cursos: No imparte.")

        print("-" * 20 + "\n")
    else:
        print("No hay profesores creados")
        print("-" * 20 + "\n")
