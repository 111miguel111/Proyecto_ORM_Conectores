import GestorBaseDeDatos
import BaseDeDatosM
import Utiles


def alta(conn):
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
            alumno=GestorBaseDeDatos.selectOne("Alumnos",primary)
        if alumno is None:
            telefono = Utiles.check_telefono()
        else:
            print('El nombre y el apellido ya pertenece a otro alumno')
        if telefono is not None:
            direccion = Utiles.check_campo("direccion", 50)
        if direccion is not None:
            fech_nacim=Utiles.checkcheck_fecha()
        if fech_nacim is not None:
            datos = {'nombre': dni,
                     'apellido': nombre,
                     'telefono': telefono,
                     'direccion': direccion,
                     'fech_nacim': telefono}

            if GestorBaseDeDatos.insert('Alumnos', datos):
                print('Alta realizada con exito'+'\n')
            else:
                print('Fallo al realizar el alta.'+'\n')

        if not Utiles.confirmacion("Quieres tratar de dar de alta otro alumno?"):  # Preguntamos si quiere dar otro alumno de alta
            done = True
            print("-" * 20 + "\n")
        else:
            print("\n")
            
def baja():
    print(len(GestorBaseDeDatos.selectAll("Alumnos")))
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:
        print("Baja alumno:")
        done = False
        while not done:
            primary={}
            print("Introduzca el nombre del alumno que desea eliminar.")
            alumno=buscar()
            if alumno is not None:
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
        print("No hay alumnos creados")
        print("-" * 20 + "\n")
def buscar():
    primary={}
    nombre = Utiles.check_campo("nombre",25)
    if nombre is not None:
        apellido = Utiles.check_campo("apellido", 25)
    if apellido is not None:
        primary={'nombre':nombre,
                 'apellido':apellido}
        alumno = GestorBaseDeDatos.select1("Alumnos", primary)
        print(alumno, type(alumno))
        if alumno is not None:
            return alumno
    return None
def modificar():
    print(len(GestorBaseDeDatos.selectAll("Alumnos")))
    if len(GestorBaseDeDatos.selectAll("Alumnos")) > 0:
        
    else:
        print("No hay alumnos creados")
        print("-" * 20 + "\n")









