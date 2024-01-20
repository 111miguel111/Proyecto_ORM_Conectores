import GestorBaseDeDatos
import BaseDeDatosM
import Utiles


def alta():
    print("Alta profesor:")
    done = False
    while not done:
        nombre = None
        telefono = None
        direccion = None
        dni = Utiles.check_dni()
        if dni is not None and GestorBaseDeDatos.select1("Profesores", dni) is None:
            nombre = Utiles.check_campo("nombre", 25)
        else:
            if GestorBaseDeDatos.select1("Profesores", dni) is not None:
                print("El dni pertenece a otro profesor")
        if nombre is not None:
            telefono = Utiles.check_telefono()
        if telefono is not None:
            direccion = Utiles.check_campo("direccion", 50)
        if direccion is not None:
            datos = {'dni': dni,
                     'nombre': nombre,
                     'telefono': telefono,
                     'direccion': direccion}

            if GestorBaseDeDatos.insert('Profesores', datos):
                print('Alta realizada con exito'+'\n')
            else:
                print('Fallo al realizar el alta.'+'\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro profesor?"):  # Preguntamos si quiere dar otro profesor de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print("\n")


def baja():
    if len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
        print("Baja profesor:")
        done = False
        while not done:
            print("Introduzca el dni del profesor que desea eliminar.")
            dni = Utiles.check_dni()
            if dni is not None:
                profesor = GestorBaseDeDatos.select1("Profesores", dni)
                if profesor is not None:
                    if Utiles.confirmacion("Seguro que desea eliminar a " + profesor.nombre + " del centro?"):
                        if GestorBaseDeDatos.delete('Profesores', dni):
                            print("Baja realizda con exito."+'\n')
                        else:
                            print("Baja no se realizo." + '\n')
                    else:
                        print("Baja cancelada."+'\n')

                else:
                    print("El dni no se corresponde con el de ningun profesor existente."+'\n')
            if len(GestorBaseDeDatos.selectAll2("Profesores")) == 0:
                print("Ya no quedan profesores que borrar.")
                done = True
                print("-" * 20 + "\n")
            else:
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro profesor?"):
                    done = True
                    print("-" * 20 + "\n")
                else:
                   print("\n")
    else:
        print("No hay profesores creados.")
        print("-" * 20 + "\n")


def modificar():
    if len(GestorBaseDeDatos.Profesores.select()) > 0:
        print("Modificacion profesor:")
        done = False
        while not done:
            print("Introduzca el dni del profesor que desea modificar.")
            dni = Utiles.check_dni()
            if dni is not None:
                profesor = GestorBaseDeDatos.select1("Profesores", dni)
                if profesor is not None:
                    modificacion(profesor)

                else:
                    print("El dni no se corresponde con el de ningun profesor existente."+'\n')

            if not Utiles.confirmacion("Quieres tratar de modificar otro profesor?"):
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay profesores creados")
        print("-" * 20 + "\n")


def modificacion(profesor):
    elec = ""
    while elec != "0":
        elec = input("1. Nombre\n2. DNI\n3. Telefono\n4. Direccion\n")
        if elec == "1":
            nueNomb = Utiles.check_campo("nombre", 25)
            if nueNomb is not None:
                if Utiles.confirmacion("Seguro que desea modificar el nombre " + profesor.nombre + " por " + nueNomb + "?"):
                    if BaseDeDatosM.update("Profesores", "nombre", profesor.nombre, nueNomb):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Baja cancelada." + '\n')

        elif elec == "2":
            nueDni = Utiles.check_dni()
            if nueDni is not None and GestorBaseDeDatos.select1("Profesores", nueDni) is None:
                if Utiles.confirmacion("Seguro que desea modificar el dni " + profesor.dni + " por " + nueDni + "?"):
                    if BaseDeDatosM.update("Profesores", "dni", profesor.dni, nueDni):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Baja cancelada." + '\n')

            else:
                if GestorBaseDeDatos.select1("Profesores", nueDni) is not None:
                    print("El dni pertenece a otro profesor ya existente")

        elif elec == "3":
            nueTelf = Utiles.check_telefono()
            if nueTelf is not None:
                if Utiles.confirmacion(
                        "Seguro que desea modificar el telefono " + profesor.telefono + " por " + nueTelf + "?"):
                    if BaseDeDatosM.update("Profesores", "telefono", profesor.telefono, nueTelf):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Baja cancelada." + '\n')
        elif elec == "4":
            nueDire = Utiles.check_campo("direccion", 25)
            if nueDire is not None:
                if Utiles.confirmacion(
                        "Seguro que desea modificar la direccion " + profesor.direccion + " por " + nueDire + "?"):
                    if BaseDeDatosM.update("Profesores", "direccion", profesor.direccion, nueDire):
                        print("Modificacion realizda con exito." + '\n')
                    else:
                        print("La modificacion no se pudo realizar." + '\n')
                else:
                    print("Baja cancelada." + '\n')

        elif elec == "0":
            print("Saliendo de menu de modificacion." + "\n")
        else:
            print("Opticon no valida")


def buscar():
    if len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
        print("Buscar profesor:")
        done = False
        while not done:
            print("Introduzca el dni del profesor que desea buscar.")
            dni = Utiles.check_dni()
            if dni is not None:
                profesor = GestorBaseDeDatos.select1("Profesores", dni)
                if profesor is not None:
                    print("Nombre: " + profesor.nombre)
                    print("Dni: " + profesor.dni)
                    print("Telefono: " + profesor.telefono)
                    print("Direccion: " + profesor.direccion)
                    print()

                else:
                    print("El dni no se corresponde con el de ningun profesor existente." + '\n')

            if not Utiles.confirmacion("Quieres tratar de buscar otro profesor?"):
                done = True
                print("-" * 20 + "\n")
            else:
                print("\n")
    else:
        print("No hay profesores creados")
        print("-" * 20 + "\n")


def mostarTodos():
    if len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
        print("Mostrar todos los profesores:")
        profesores = GestorBaseDeDatos.selectAll2("Profesores")
        for profesor in profesores:
            print()
            print("Nombre: " + profesor['nombre'])
            print("Dni: " + profesor['dni'])
            print("Telefono: " + profesor['telefono'])
            print("Direccion: " + profesor['direccion'])

        print("-" * 20 + "\n")
    else:
        print("No hay profesores creados")
        print("-" * 20 + "\n")


def relacionar(conn):
    return None
