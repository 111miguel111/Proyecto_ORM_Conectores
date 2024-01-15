import GestorBaseDeDatos
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
            direccion = Utiles.check_campo()
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
    return None


def modificar(conn):
    return None


def buscar(conn):
    return None


def mostarTodos(conn):
    return None


def relacionar(conn):
    return None
