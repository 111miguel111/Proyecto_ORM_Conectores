import GestorBaseDeDatos
import Utiles


def alta():
    print("Alta alumno:")
    done = False
    while not done:
        primary={}
        nombre = None
        apellido = None
        telefono= None
        direccion = None
        fech_nacim= None
        nombre = Utiles.check_campo("nombre",25)
        if nombre is not None:
            apellido = Utiles.check_campo("apellido", 25)
        if apellido is not None:
            primary={'nombre':nombre,
                     'apellido':apellido}
            alumno=GestorBaseDeDatos.select1("Alumnos",primary)
        if alumno is None:
            print(alumno, type(alumno))
            telefono = Utiles.check_telefono()
        else:
            print(alumno, type(alumno))
            print(alumno.nombre)
            print('El nombre y el apellido ya pertenece a otro alumno.')
        if telefono is not None:
            direccion = Utiles.check_campo("direccion", 50)
        if direccion is not None:
            fech_nacim=Utiles.check_fecha()
        if fech_nacim is not None:
            datos = {'nombre': nombre,
                     'apellido': apellido,
                     'telefono': telefono,
                     'direccion': direccion,
                     'fech_nacim': fech_nacim}

            if GestorBaseDeDatos.insert('Alumnos', datos):
                print('Alta realizada con exito.'+'\n')
            else:
                print('Fallo al realizar el alta.'+'\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro alumno?"):  # Preguntamos si quiere dar otro alumno de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print()
            
def baja():
    print("Hay :",len(GestorBaseDeDatos.selectAll("Alumnos")), " Alumnos creados")
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:
        print("Baja alumno:")
        done = False
        while not done:
            print("Introduzca el nombre del alumno que desea eliminar.")
            alumno=buscar()
            if alumno is not None:
                primary={'nombre':alumno.nombre,
                         'apellido':alumno.apellido}
                if Utiles.confirmacion("Seguro que desea eliminar a " + alumno.nombre + " del centro?"):
                    GestorBaseDeDatos.delete('Alumnos',primary)
                    print("Baja realizda con exito."+'\n')
                else:
                    print("Baja cancelada."+'\n')
            else:
                print("El nombre y apellido no se corresponde con el de ningun alumno existente."+'\n')
            if len(GestorBaseDeDatos.selectAll("Alumnos")) == 0:
                print("Ya no quedan alumnos que borrar.")
                done = True
                print("-" * 20 + "\n")
            else:
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro alumno?"):  # Preguntamos si quiere dar otro alumno de baja
                    done = True
                    print("-" * 20 + "\n")
                else:
                    print("\n")
    else:
        print("No hay alumnos creados.")
        print("-" * 20 + "\n")
def buscar():
    primary={}
    nombre = Utiles.check_campo("nombre",25)
    if nombre is not None:
        print("Introduzca el apellido del alumno.")
        apellido = Utiles.check_campo("apellido", 25)
    if apellido is not None:
        primary={'nombre':nombre,
                 'apellido':apellido}
        alumno = GestorBaseDeDatos.select1("Alumnos", primary)
        print(alumno, type(alumno))
        print()
        if alumno is not None:
            return alumno
    return None

def modificar():
    print("Hay :",len(GestorBaseDeDatos.selectAll("Alumnos")), " Alumnos creados")
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:
        print("Modificar alumno:")
        done = False
        while not done:
            print("Introduzca el nombre del alumno que desea modificar.")
            alumno=buscar()
            if alumno is not None:
                modificacion(alumno)
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
    elec = ""
    primary={'nombre':alumno.nombre,
            'apellido':alumno.apellido }
    cont=0
    while elec != "0":
        elec = input("Que desea modificar?\n1. Nombre\n2. Apellido\n3. Telefono\n4. Direccion\n5. Fecha de nacimiento\n0. Volver\n")
        if elec == "1":
            nombre = Utiles.check_campo('nombre', 25)
            if nombre is not None :
                primaryAux={'nombre':nombre,
                            'apellido':alumno.apellido }
                
                if GestorBaseDeDatos.select1("Alumnos", primaryAux) is None:
                    if Utiles.confirmacion("Seguro que desea modificar el nombre " + alumno.nombre + " por " + nombre + "?"):
                        if GestorBaseDeDatos.update("Alumnos", "nombre", primary, nombre):
                            alumno=GestorBaseDeDatos.select1("Alumnos", primaryAux)
                            primary={'nombre':alumno.nombre,
                                     'apellido':alumno.apellido}
                            print("Modificacion realizda con exito." + '\n')
                        else:
                            print("La modificacion no se pudo realizar." + '\n')
                    else:
                        print("Modificacion cancelada." + '\n')

                else:
                    print("El nombre pertenece a otro alumno ya existente con el mismo apellido."+ '\n')
        elif elec == "2":
            apellido = Utiles.check_campo('apellido', 25)
            if apellido is not None :
                primaryAux={'nombre':alumno.nombre,
                            'apellido':apellido }
                
                if GestorBaseDeDatos.select1("Alumnos", primaryAux) is None:
                    if Utiles.confirmacion("Seguro que desea modificar el apellido " + alumno.apellido + " por " + apellido + "?"):
                        if GestorBaseDeDatos.update("Alumnos", "apellido", primary, apellido):
                            alumno=GestorBaseDeDatos.select1("Alumnos", primaryAux)
                            primary={'nombre':alumno.nombre,
                                     'apellido':alumno.apellido}
                            print("Modificacion realizda con exito." + '\n')
                        else:
                            print("La modificacion no se pudo realizar." + '\n')
                    else:
                        print("Modificacion cancelada." + '\n')

                else:
                    print("El aellido pertenece a otro alumno ya existente con el mismo nombre."+ '\n')
        elif elec == "3":
            telefono = Utiles.check_telefono()
            if telefono is not None:
                if Utiles.confirmacion("Seguro que desea modificar el telefono " + alumno.telefono + " por " + telefono + "?"):
                    if GestorBaseDeDatos.update("Alumnos", "telefono", primary, telefono):
                        alumno=GestorBaseDeDatos.select1("Alumnos", primary)
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Modificacion cancelada." + '\n')
        elif elec == "4":
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
        elif elec == "5":
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
                    
                    
        elif elec == "0":
            print("Saliendo de menu de modificacion." + "\n")
        else:
            print("Opcion no valida.")
            cont += 1
            print("Fallos ", cont, "/5"+ "\n")
            if(cont == 5):
                print("Cometiste demasiados fallos."+ "\n")
                elec="0"
def mostrarTodos():
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:
        print("Mostrar todos los alumnos:")
        alumnos = GestorBaseDeDatos.selectAll("Alumnos")
        print()
        for alumno in alumnos:
            primary={'nombre':alumno.nombre,
                    'apellido':alumno.apellido }
            aux = GestorBaseDeDatos.select1("Alumnos", primary)
            datos = GestorBaseDeDatos.selectJoinMostrar("Alumnos", aux)
            print("Nombre: " + datos[0]['nombre'])
            print("Apellido: " + datos[0]['apellido'])
            print("Telefono: " + datos[0]['telefono'])
            print("Direccion: " + datos[0]['direccion'])
            fecha = str(datos[0]["fech_nacim"]).split('-')
            print("Fecha de nacimiento: " + fecha[2]+"-"+ fecha[1]+"-"+ fecha[0])
            if len(datos[1]) > 0:
                for curso in datos[1]:
                    print("Cursos: ", curso['nombre'], " ", end="")
                print('\n')
            else:
                print()

        print("-" * 20 + "\n")
    else:
        print("No hay alumnos creados.")
        print("-" * 20 + "\n")
        
def mostrarUno():
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:
        print("Buscar Alumno:")
        done = False
        while not done:
            print("Introduzca el nombre del alumno que desea buscar.")
            alumno = buscar()
            if alumno is not None:
                datos = GestorBaseDeDatos.selectJoinMostrar("Alumnos", alumno)
                print()
                print("Nombre: " + datos[0]['nombre'])
                print("Apellido: " + datos[0]['apellido'])
                print("Telefono: " + datos[0]['telefono'])
                print("Direccion: " + datos[0]['direccion'])
                fecha = str(datos[0]["fech_nacim"]).split('-')
                print("Fecha de nacimiento: " + fecha[2]+"-"+ fecha[1]+"-"+ fecha[0])
                if len(datos[1]) > 0:
                    for curso in datos[1]:
                        print("Cursos: ", curso['nombre'], " ", end="")
                    print()
                else:
                    print()

            else:
                print("El nombre y el apellido no se corresponde con el de ningun alumno existente." + '\n')

            if not Utiles.confirmacion("Quieres tratar de buscar otro alumno?"):
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay alumnos creados")
        print("-" * 20 + "\n")

