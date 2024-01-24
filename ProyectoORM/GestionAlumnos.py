import GestorBaseDeDatos
import Utiles


def alta():
    """
    Funcion que pide los campos para el insert y, si todos son correctos pide a la bbdd que realice el insert.
    """
    print("Alta alumno:")
    done = False
    while not done:  #Este bucle se asegura de que se puedan dar de alta mas de un alumno.
        alumno = None
        apellido = None
        telefono = None
        direccion = None
        fech_nacim = None #Evitar warnings del IDE
        nombre = Utiles.check_campo("nombre",25) #Validando campos
        if nombre is not None:
            apellido = Utiles.check_campo("apellido", 25)
        if apellido is not None:
            primary = {'nombre': nombre,
                       'apellido': apellido}
            alumno = GestorBaseDeDatos.select1("Alumnos", primary) #Comprobando que un alumno con ese nomb y ape no existe
        if alumno is None:
            telefono = Utiles.check_telefono()
        else:
            print('El nombre y el apellido ya pertenece a otro alumno.')
        if telefono is not None:
            direccion = Utiles.check_campo("direccion", 50)
        if direccion is not None:
            fech_nacim = Utiles.check_fecha()
        if fech_nacim is not None:  #Si todos los campos son correctos procedemos con el alta
            datos = {'nombre': nombre,
                     'apellido': apellido,
                     'telefono': telefono,
                     'direccion': direccion,
                     'fech_nacim': fech_nacim}  #Metemos los datos en un diccionario

            if GestorBaseDeDatos.insert('Alumnos', datos):  #Llamamos al insert y si sale bien se notifica.
                print('Alta realizada con exito.'+'\n')
            else:
                print('Fallo al realizar el alta.'+'\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro alumno?"):  # Preguntamos si quiere dar otro alumno de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print()


def baja():
    """
    Funcion que encuentra a un
    """
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:  #Si no hay alumnos no entras
        print("Baja alumno:")
        done = False
        while not done:
            print("Introduzca el nombre del alumno que desea eliminar.")
            alumno = buscar()  #Esto pide los datos de un alumno y si existe te lo devuelve si no existe te devuelve none
            if alumno is not None: #Si el alumno existe
                primary = {'nombre': alumno.nombre,
                           'apellido': alumno.apellido} #Se meten sus datos para en delete
                if Utiles.confirmacion("Seguro que desea eliminar a " + alumno.nombre + " del centro?"): #Se pide confirmacion
                    if GestorBaseDeDatos.delete('Alumnos', primary):  #Se pide el delete y si sale bien se notifica
                        print("Baja realizda con exito."+'\n')
                    else:
                        print("Baja la baja no se realizo." + '\n')
                else:
                    print("Baja cancelada."+'\n')
            else: #En caso de que el alumno no existe
                print("El nombre y apellido no se corresponde con el de ningun alumno existente."+'\n')
            if len(GestorBaseDeDatos.selectAll("Alumnos")) == 0: #Si tras el delete no quedan alumno te expulsamos
                print("Ya no quedan alumnos que borrar.")
                done = True
                print("-" * 20 + "\n")
            else: #En caso de que queden alumno se consulta al usuario si quiere borrar mas alumnos
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro alumno?"):  # Preguntamos si quiere dar otro alumno de baja
                    done = True
                    print("-" * 20 + "\n")
                else:
                    print("\n")
    else:
        print("No hay alumnos creados.")
        print("-" * 20 + "\n")


def buscar():
    """
    Funcion que busca un alumno y lo devuelve a las otras funciones
    """
    apellido = None #Evitar warnings
    nombre = Utiles.check_campo("nombre", 25) #Pedimos campos
    if nombre is not None:
        print("Introduzca el apellido del alumno.")
        apellido = Utiles.check_campo("apellido", 25)
    if apellido is not None: #En caso de que sean balidos
        primary = {'nombre': nombre,
                   'apellido': apellido} #Se crea un diccionario con los datos
        alumno = GestorBaseDeDatos.select1("Alumnos", primary) #Se consigue un peewee model con un select
        print()
        if alumno is not None:  #Si el alumno existe se devuelve, si no se devuelve none
            return alumno
    return None


def modificar():
    """
    Funcion que busca un alumno y lo manda a la modificacion
    """
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:  #Si no hay alumno no entras
        print("Modificar alumno:")
        done = False
        while not done: #Para modificar mas de uno
            print("Introduzca el nombre del alumno que desea modificar.")
            alumno = buscar() #Obtenemos el alumno
            if alumno is not None: #Si existe
                modificacion(alumno) #Lo mandamos a la modificacion
            else:
                print("El nombre y apellido no se corresponde con el de ningun alumno existente."+'\n')
            
            if not Utiles.confirmacion("Quieres tratar de modificar otro alumno?"):  # Preguntamos si quiere dar otro alumno de baja
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay alumnos creados.")
        print("-" * 20 + "\n")
        
        
def modificacion(alumno):
    """
    Funcion que modifica los datos de un alumno
    """
    elec = ""
    primary = {'nombre': alumno.nombre,
               'apellido': alumno.apellido} #Datos del alumno
    cont = 0
    while elec != "0":  #Para poder cambiar lo que quieras y salir cuando quieras
        elec = input("Que desea modificar?\n1. Nombre\n2. Apellido\n3. Telefono\n4. Direccion\n5. Fecha de nacimiento\n0. Volver\n")
        if elec == "1": #Nombre
            nombre = Utiles.check_campo('nombre', 25) #Se pide nuevo nombre
            if nombre is not None: #si es valido
                primaryAux = {'nombre': nombre,
                              'apellido': alumno.apellido} #se hace un diccionario con un dato antiguo y uno nuevo.
                
                if GestorBaseDeDatos.select1("Alumnos", primaryAux) is None: #Si la convinacion de estos no pertenece a otro alumno
                    if Utiles.confirmacion("Seguro que desea modificar el nombre " + alumno.nombre + " por " + nombre + "?"): #Se pide confirmacion
                        if GestorBaseDeDatos.update("Alumnos", "nombre", primary, nombre): #Si el update sale bien se notifica
                            alumno = GestorBaseDeDatos.select1("Alumnos", primaryAux) #Se actualiza el alumno
                            primary = {'nombre': alumno.nombre,
                                       'apellido': alumno.apellido} #Nuevos datos del alumno
                            print("Modificacion realizda con exito." + '\n')
                        else:
                            print("La modificacion no se pudo realizar." + '\n')
                    else:
                        print("Modificacion cancelada." + '\n')

                else:
                    print("El nombre pertenece a otro alumno ya existente con el mismo apellido."+ '\n')
        elif elec == "2": #Apellido
            apellido = Utiles.check_campo('apellido', 25) #Se pide dato
            if apellido is not None : #Si es valido
                primaryAux = {'nombre': alumno.nombre,
                              'apellido': apellido} #Datos para la comprobacion de que no hay duplicados
                
                if GestorBaseDeDatos.select1("Alumnos", primaryAux) is None: #Si no hay duplicados
                    if Utiles.confirmacion("Seguro que desea modificar el apellido " + alumno.apellido + " por " + apellido + "?"): #Se pide confirmacion
                        if GestorBaseDeDatos.update("Alumnos", "apellido", primary, apellido): #Se actualiza
                            alumno = GestorBaseDeDatos.select1("Alumnos", primaryAux) #Actualiza alumno
                            primary = {'nombre':alumno.nombre,
                                       'apellido':alumno.apellido} #Para actualizar los datos de comparacion
                            print("Modificacion realizda con exito." + '\n')
                        else:
                            print("La modificacion no se pudo realizar." + '\n')
                    else:
                        print("Modificacion cancelada." + '\n')

                else:
                    print("El aellido pertenece a otro alumno ya existente con el mismo nombre."+ '\n')
        elif elec == "3": #Telefono
            telefono = Utiles.check_telefono()  #nuevo dato
            if telefono is not None: #Si es valido
                if Utiles.confirmacion("Seguro que desea modificar el telefono " + alumno.telefono + " por " + telefono + "?"): #Se pide confirmacion
                    if GestorBaseDeDatos.update("Alumnos", "telefono", primary, telefono): #Se llama al update y si sale bien se notifican y actualizan los datos de comparaciob
                        alumno = GestorBaseDeDatos.select1("Alumnos", primary)
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')
        elif elec == "4": #Direccion igual que telefono
            direccion = Utiles.check_campo("direccion", 50)
            if direccion is not None:
                if Utiles.confirmacion("Seguro que desea modificar la direccion " + alumno.direccion + " por " + direccion + "?"):
                    if GestorBaseDeDatos.update("Alumnos", "direccion", primary, direccion):
                        alumno=GestorBaseDeDatos.select1("Alumnos", primary)
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')
        elif elec == "5": #fecha de nacimiento igual que telefono
            fech_nacim=Utiles.check_fecha()
            if fech_nacim is not None:
                if Utiles.confirmacion("Seguro que desea modificar la fecha de nacimiento " + alumno.fech_nacim + " por " + fech_nacim + "?"):
                    if GestorBaseDeDatos.update("Alumnos", "fech_nacim", primary, fech_nacim):
                        alumno=GestorBaseDeDatos.select1("Alumnos", primary)
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')

        elif elec == "0": #Slimos
            print("Saliendo de menu de modificacion." + "\n")
        else: #Contamos fallos
            print("Opcion no valida.")
            cont += 1
            print("Fallos ", cont, "/5"+ "\n")
            if cont == 5: #Te expulso
                print("Cometiste demasiados fallos."+ "\n")
                elec="0"


def mostrarTodos():
    """
    Funcion que muestra todos los alumnos con un formato capaz de mostrar los cursos a los que pertenecen gracias a joins
    """
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0: #Si no hay alumnos no entras
        print("Mostrar todos los alumnos:")
        alumnos = GestorBaseDeDatos.selectAll("Alumnos") #Cogemos todos los alumnos
        print()
        for alumno in alumnos: #Por cada alumno en la lista
            primary = {'nombre': alumno.nombre,
                       'apellido': alumno.apellido} #Datos del alumno
            aux = GestorBaseDeDatos.select1("Alumnos", primary) #Peewee model auxiliar
            datos = GestorBaseDeDatos.selectJoinMostrar("Alumnos", aux) #Datos completos (con cursos del alumno)
            print("Nombre: " + datos[0]['nombre']) #Print del alumno
            print("Apellido: " + datos[0]['apellido'])
            print("Telefono: " + datos[0]['telefono'])
            print("Direccion: " + datos[0]['direccion'])
            fecha = str(datos[0]["fech_nacim"]).split('-')
            print("Fecha de nacimiento: " + fecha[2]+"-"+ fecha[1]+"-"+ fecha[0])
            if len(datos[1]) > 0: #Si tiene cursos
                for curso in datos[1]: #se recorren y printean
                    print("Cursos: ", curso['nombre'], " ", end="")
                print('\n')
            else:
                print()

        print("-" * 20 + "\n")
    else:
        print("No hay alumnos creados.")
        print("-" * 20 + "\n")


def mostrarUno():
    """
    Funcion que busca y printea un alumno
    """
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0: #Si no hay alumno no entras
        print("Buscar Alumno:")
        done = False
        while not done: #Para buscar mas de uno
            print("Introduzca el nombre del alumno que desea buscar.")
            alumno = buscar() #Buscamos el alumno
            if alumno is not None:
                datos = GestorBaseDeDatos.selectJoinMostrar("Alumnos", alumno) #Datos completos del alumno
                print()
                print("Nombre: " + datos[0]['nombre']) #Print de daotos
                print("Apellido: " + datos[0]['apellido'])
                print("Telefono: " + datos[0]['telefono'])
                print("Direccion: " + datos[0]['direccion'])
                fecha = str(datos[0]["fech_nacim"]).split('-')
                print("Fecha de nacimiento: " + fecha[2] + "-" + fecha[1] + "-" + fecha[0])
                if len(datos[1]) > 0: #Si tiene cursos
                    for curso in datos[1]: #se recorren y printean
                        print("Cursos: ", curso['nombre'], " ", end="")
                    print()
                else:
                    print()

            else:
                print("El nombre y el apellido no se corresponde con el de ningun alumno existente." + '\n')

            if not Utiles.confirmacion("Quieres tratar de buscar otro alumno?"): #Para buscar otro alumno
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay alumnos creados")
        print("-" * 20 + "\n")

