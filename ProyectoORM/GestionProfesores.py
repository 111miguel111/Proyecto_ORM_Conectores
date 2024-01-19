import GestorBaseDeDatos
import BaseDeDatosM
import Utiles


def alta(conn):
    print("Alta profesor:")
    done = False
    while not done:
        nombre = None
        telefono = None
        direccion = None
        dni = Utiles.check_dni()
        if dni is not None:
            nombre = Utiles.check_campo("nombre", 25)
        if nombre is not None:
            telefono = Utiles.check_telefono()
        if telefono is not None:
            direccion = Utiles.check_campo("direccion", 50)
        if direccion is not None:
            datos = {'dni': dni,
                     'nombre': nombre,
                     'telefono': telefono,
                     'direccion': direccion}

            if GestorBaseDeDatos.insert(conn, 'Profesores', datos):
                print('Alta realizada con exito'+'\n')
            else:
                print('Fallo al realizar el alta.'+'\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro profesor?"):  # Preguntamos si quiere dar otro profesor de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print("\n")


def baja(conn):
    print(len(GestorBaseDeDatos.selectAll2("Profesores")))
    if len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
        print("Baja profesor:")
        done = False
        while not done:
            print("Introduzca el dni del profesor que desea eliminar.")
            dni = Utiles.check_dni()
            if dni is not None:
                profesor = GestorBaseDeDatos.select1("Profesores", dni)
                print(profesor, type(profesor))
                if profesor is not None and int(profesor.id_prof) > 0:
                    if Utiles.confirmacion("Seguro que desea eliminar a " + profesor.nombre + " del centro?"):
                        GestorBaseDeDatos.delete(conn, 'Profesores', dni)
                        print("Baja realizda con exito."+'\n')

                    else:
                        print("Baja cancelada."+'\n')

                else:
                    print("El dni no se corresponde con el de ningun profesor existente."+'\n')
            if len(GestorBaseDeDatos.selectAll2("Profesores")) == 0:
                print("Ya no quedan profesores que borrar.")
                done = True
                print("-" * 20 + "\n")
            else:
                if not Utiles.confirmacion("Quieres tratar de dar de baja otro profesor?"):  # Preguntamos si quiere dar otro profesor de alta
                    done = True
                    print("-" * 20 + "\n")
                else:
                    print("\n")


def modificar(conn):
    return None


def buscar(conn):
    return None


def mostarTodos(conn):
    return None


def relacionar(conn):
    return None
