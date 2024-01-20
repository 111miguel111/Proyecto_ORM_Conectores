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
                print()
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



def modificar():
    if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
        print("Modificar curso")
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


def relacionar():
    if len(GestorBaseDeDatos.selectAll2("Alumnos")) > 0 and len(GestorBaseDeDatos.selectAll2("Profesores")) > 0:
        if len(GestorBaseDeDatos.selectAll2("Cursos")) > 0:
            print("Relacionar curso:")
        else:
            print("No hay cursos creados.")
            print("-" * 20 + "\n")
    else:
        print("No hay ni profesores ni alumnos creados.")
        print("-" * 20 + "\n")