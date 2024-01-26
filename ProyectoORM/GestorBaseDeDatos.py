import pymysql
from peewee import *
import configparser
import Utiles
import sys
import traceback


def escanerNumerico(contexto):
    """
    Funcion que cerciora que la cadena que se introduce no este vacia y sean numeros
    :param contexto: informcacion sobre el campo
    :return: respuesta: si el campo es correcto
    :return: None: si el campo esta vacio
    """
    # Se crea un contador de intentos para el bucle que solo iterara hasta 5 intentos
    intentos = 0
    while (intentos < 5):
        print(contexto.capitalize() + ": ")
        scan = input()
        # Se introduce la cadena y comprueba que no este vacio y que ponga 1 o 2 si no te vuelve a preguntar y si fallas 5 veces devulve none
        if (scan.isspace() == False and scan.isnumeric() ):
            return scan
        intentos += 1
        print('Porfavor introduce solo numeros no decimales.'+'\n')
        if fallos < 5:
            print("Fallos hasta salir", fallos, "/5")
    print("Has superado el numero de intentos")
    return None


def iniciarFicheroConfiguracion():
    '''
    Funcion que se encarga de crear el fichero de configuracion con valores predeterminados
    '''
    try:
        # Creamos un fichero .ini en el cual se guardan datos para la configuracion del programa
        config = configparser.ConfigParser()  # Creamos la variable que contiene los datos de configuracion
        config['SERVER'] = {'host': 'localhost',
                            'user': 'root',
                            'password': '1234',
                            'port': '3306'}
        with open('config.ini', 'w') as configfile:  # Escribimos el fichero de configuracion
            config.write(configfile)
        print("Se ha creado el fichero de configuracion")
    except:
        print('No se ha podido crear el fichero de configuracion, el programa se cerrara. ')
        sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
    return 0


def iniciarFicheroConfiguracionManulamente():
    '''
    Funcion que se encarga de crear el fichero de configuracion con valores que se le pediran al usuario
    '''
    host=None
    user=None
    password=None
    port=None
    #Pedimos los datos para crear el ficheo de configuracion
    print("El fichero de configuracion no existe porfavor introduce los campos a poner en el fichero")
    host=Utiles.check_campo("host", 25)
    if host is not None:
        user=Utiles.check_campo("user",25)
    if user is not None:
        if Utiles.confirmacion("Deseas poner contrasenia ?"):  # Preguntamos si quiere dar otro alumno de baja
            password=Utiles.check_campo("password",25)
        else:
            password=""
    if password is not None:
        port=escanerNumerico("port")
    if port is not None:
        try:
            # Creamos un fichero .ini en el cual se guardan datos para la configuracion del programa
            config = configparser.ConfigParser()  # Creamos la variable que contiene los datos de configuracion
            config['SERVER'] = {'host': str(host),
                                'user': str(user),
                                'password': str(password),
                                'port': str(port)}
            with open('config.ini', 'w') as configfile:  # Escribimos el fichero de configuracion
                config.write(configfile)
            print("Se ha creado el fichero de configuracion")
        except:
            print('No se ha podido crear el fichero de configuracion, el programa se cerrara. \nComprueba que has introducido bien los datos.\nEl fichero se llama "config.ini". ')
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
    else:
        print('No se ha podido crear el fichero de configuracion, el programa se cerrara. ')
        sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
    return 0


def checkFileExistance(filePath):
    '''
    Comprueba que el fichero de configuracion existe
    :param filePath: El nombre del fichero
    :return Devuelve True si el fichero existe y False si no existe
    '''
    # Comprobamos que el fichero exista si no es el caso devolvemos false
    try:
        with open(filePath, "r") as f:
            return True
        print("El fichero de configuracion existe")
    except FileNotFoundError as e:
        return False
        print("El fichero de configuracion no existe")
    except IOError as e:
        return False


def checkConfigBien(filePath):
    '''
    Funcion encargada de comprobar que el fichero de configuracion esta completo y no tenga errores
    :param filePath: El nombre del fichero
    :return Devuelve False si hay algun problema al leer el fichero de configuracion y si todos los campos estan bien devuelve True
    '''
    campo = ''
    # Comprobamos que el fichero tiene todas sus secciones y categorias en orden
    try:
        print("Comprobando estado del fichero de configuracion")
        config = configparser.ConfigParser()
        config.read(filePath)
        campo = 'host'
        # Comprobamos que la categoria existe solicitando el dato que hay dentro
        host_variable = str(config['SERVER']['host'])
        if (host_variable.isspace() or len(
                host_variable) == 0):  # Si esta categoria esta mal devolveremos false y se entendera que el fichero de configuracion esta mal
            print("El campo " + campo + " no puede estar vacio\n")
            return False
        campo = 'user'
        # Comprobamos que la categoria existe solicitando el dato que hay dentro
        user_variable = str(config['SERVER']['user'])
        if (user_variable.isspace() or len(
                user_variable) == 0):  # Si esta categoria esta mal devolveremos false y se entendera que el fichero de configuracion esta mal
            print("El campo " + campo + " no puede estar vacio\n")
            return False
        campo = 'password'
        # Comprobamos que la categoria existe solicitando el dato que hay dentro
        password_variable = str(config['SERVER']['password'])
        if (
                password_variable.isspace()):  # Si esta categoria esta mal devolveremos false y se entendera que el fichero de configuracion esta mal
            print("El campo " + campo + " no puede ser un espacio\n")
            return False
        campo = 'port'
        # Comprobamos que la categoria existe solicitando el dato que hay dentro
        port_variable = int(config['SERVER']['port'])
        if (str(port_variable).isspace() or str(port_variable).isnumeric() == False or len(
                str(port_variable)) == 0):  # Si esta categoria esta mal o esta vacia devolveremos false y se entendera que el fichero de configuracion esta mal
            print("El campo " + campo + " tiene que ser numeros\n")
            return False
        print("El fichero de configuracion esta bien")
        print(
            'Si quieres configurar los datos de conexion del sistema gestor de base de datos, modifique la informacion el fichero "config.ini"')
        return True
    except FileNotFoundError as e:
        print("El campo " + campo + " falta o esta mal\n")
        return False
    except IOError as e:
        print("El campo " + campo + " falta o esta mal\n")
        return False
    except:
        print("El campo " + campo + " falta o esta mal\n")
        return False


def mysqlconnect():
    '''
    Funcion encargada de realizar la conexion si hay algun problema en la conexion informara al usuario.
    :return Devulve una conexion si todo ha ido bien
    '''
    # Cogemos todos los datos de el fichero de configuracion e iniciamos una coñexion en base a los datos en el fichero de configuracion
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        host_variable = str(config['SERVER']['host'])
        user_variable = str(config['SERVER']['user'])
        password_variable = str(config['SERVER']['password'])
        port_variable = int(config['SERVER']['port'])
        #Una vez tenemos las variables guardadas realizamos la conexion
        conn = pymysql.connect(
            host=host_variable,
            user=user_variable,
            password=password_variable,
            port=port_variable
        )
        return conn
    # Si la conexion no se puede realizar por que el gestor de base de datos esta apagado nos informara
    except pymysql.err.OperationalError as e:
        print(
            "Se ha producido un error, compruebe que el sistema gestor de base de datos al que se quiere conectar \nesta operativa y que los datos son correctos.\nEl programa se cerrara")
        sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
    # Si la conexion no se puede realizar por que el fichero de configuracion esta mal  nos informara
    except:
        print(
            "Hay un error en el fichero de configuracion que impiede conectarse \n1.Quieres restablecer el fichero con los valores por defecto \n2.Quieres cerrar el programa ")
        opcion = escanerNumerico()
        if (opcion == '1'):
            print("El fichero de configuracion sera restablecido y el programa se cerrara")
            iniciarFicheroConfiguracion()
            print('Si quieres hacer cambios en la conexion mire el archivo de configuracion "config.ini" ')
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
        elif (opcion == '2'):
            print("El programa se cerrara")
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
        else:
            print("El programa se cerrara")
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error


def crearTablas(conn):
    '''
    Funcion encargada de realizar la creacion de las tablas con peewee
    '''
    try:
        #Creamos todas las tablas dentro de la base de datos
        conn.create_tables([Profesores, Alumnos, Cursos, Cursos_Profesores, Cursos_Alumnos])
        print("Se han creado las tablas bien.")
        #Si falla algo informaremos de esto
    except Exception:
        #print(traceback.format_exc())
        print("No se pudieron crear las tablas.")


def conectarAPeewee():
    '''
    Funcion encargada de conectar peewee a la base de datos
    :return devolveremos una conexion para enlazarla en los meta de los modelos de las tablas
    '''
    try:
        #Obtenemos la informacion del fichero de oniguracion
        config = configparser.ConfigParser()
        config.read('config.ini')
        host_variable = str(config['SERVER']['host'])
        user_variable = str(config['SERVER']['user'])
        password_variable = str(config['SERVER']['password'])
        port_variable = int(config['SERVER']['port'])
        #Una vez ya tenemos las variables con los datos para la conexion nos conectamos con peewee
        conn = MySQLDatabase('miguel_antonio_bd',
                             user=user_variable,
                             password=password_variable,
                             host=host_variable,
                             port=port_variable)

        
        conn.connect()

        return conn
    # Si la conexion no se puede realizar nos informara
    except:
        print(
            "Hay un error en la conexion. \n1.Quieres restablecer el fichero con los valores por defecto \n2.Quieres cerrar el programa ")
        opcion = escanerNumerico()
        if (opcion == '1'):
            print("El fichero de configuracion sera restablecido y el programa se cerrara")
            iniciarFicheroConfiguracion()
            print('Si quieres hacer cambios en la conexion mire el archivo de configuracion "config.ini" ')
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
        elif (opcion == '2'):
            print("El programa se cerrara")
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
        else:
            print("Opcion no valida, el programa se cerrara")
            sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error


def iniciar():
    '''
    Funcion encargada de iniciar lo relacionado con la base de datos, la configuracion, la conexion para crear la base de datos, etc.
    :return Si la base de datos se realiza con exito devolveremos True en caso de que suceda algun problema devolveremos False
    '''
    # Funcion que inicia lo relacionado con la base de datos, comprueba el fichero de datos, comprueba la conexion y si esta bien procede a crear una base de datos
    try:
    #Primero confirmamos que el fichero de configuracion existe y no esta corrupto
        if (checkFileExistance(
                "config.ini") == True):  # Comprobamos que el fichero de configuracion existe, si no es el caso lo creamos con los datos por defecto
            if (checkConfigBien("config.ini") == False):  # Comprobamos que el fichero de configuracion esta bien
                # Si hay algun error informamos al usuario
                print(
                    "Hay un error en el fichero de configuracion \n1.Quieres restablecer el fichero con los valores por defecto \n2.Quieres cerrar el programa")
                opcion = escanerNumerico()
                if (opcion == '1'):
                    print("El fichero de configuracion sera restablecido y el programa se cerrara")
                    iniciarFicheroConfiguracion()
                    print('Si quieres hacer cambios en la conexion mire el archivo de configuracion "config.ini" ')
                    sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
                elif (opcion == '2'):
                    print("El programa se cerrara")
                    sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
                else:
                    print("El programa se cerrara")
                    sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error
        else:
            iniciarFicheroConfiguracionManulamente()

        conn = mysqlconnect()  # Nos conectamos
        cur = conn.cursor()  # Creamos un cursor que se usara para crear la base de datos y las tablas correspondientes
        cur.execute("CREATE DATABASE IF NOT EXISTS miguel_antonio_bd")
        conn.commit()
        cur.close()
        conn.close()
        # Creamos la conexion a la bbdd desde peewee
        conn = conectarAPeewee()

        return conn  # Devuelve la conexion de peewee a la bbdd para que se trabaje con ella.
    except:
        return None


def insert(tabla, datos):
    """
    Funcion encargada de la realizacion de los inserts en la bbdd.
    :param tabla es la tabla a la que corresponde el insert, datos es un diccionario con los datos del insert
    :return Si la insercion se ha realizado con exito deolveremos true en caso contrario devolveremos False
    """
    try:
        if tabla == "Profesores":
            Profesores.create(dni=datos['dni'],
                              nombre=datos['nombre'],
                              telefono=datos['telefono'],
                              direccion=datos['direccion'])

        elif tabla == "Alumnos":
            Alumnos.create(nombre=datos['nombre'],
                           apellido=datos['apellido'],
                           telefono=datos['telefono'],
                           direccion=datos['direccion'],
                           fech_nacim=datos['fech_nacim'])

        elif tabla == "Cursos":
            Cursos.create(nombre=datos['nombre'],
                          descripcion=datos['descripcion'])

        elif tabla == "Cursos_Profesores":
            Cursos_Profesores.create(cod_curs=datos['cod_curs'],
                                     id_prof=datos['id_prof'])

        elif tabla == "Cursos_Alumnos":
            Cursos_Alumnos.create(cod_curs=datos['cod_curs'],
                                  num_exp=datos['num_exp'])

        return True
    except:
        #print("Fallos en la insercion")
        #print(traceback.format_exc())
        return False


def delete(tabla, primary):
    """
    Funcion encargada de la realizacion de los inserts en la bbdd.
    :param tabla es la tabla a la que corresponde el delete, datos es un diccionario con los datos para realizar el delete
    :return Si el dlete se ha realizado con exito deolveremos true en caso contrario devolveremos False
    """
    try:
        if tabla == "Profesores":
            borrar = Profesores.delete().where(Profesores.dni == primary)
            borrar.execute()

        elif tabla == "Alumnos":
            borrar = Alumnos.delete().where(Alumnos.nombre == primary['nombre'],
                                            Alumnos.apellido == primary['apellido'])
            borrar.execute()

        elif tabla == "Cursos":
            borrar = Cursos.delete().where(Cursos.nombre == primary)
            borrar.execute()

        elif tabla == "Cursos_Profesores":
            borrar = Cursos_Profesores.delete().where(Cursos_Profesores.cod_curs == primary['cod_curs'],
                                                      Cursos_Profesores.id_prof == primary['id_prof'])
            borrar.execute()

        elif tabla == "Cursos_Alumnos":
            borrar = Cursos_Alumnos.delete().where(Cursos_Alumnos.cod_curs == primary['cod_curs'],
                                                   Cursos_Alumnos.num_exp == primary['num_exp'])
            borrar.execute()

        return True
    except:
        #print("Fallos en el delete")
        #print(traceback.format_exc())
        return False


def update(tabla, campo, primary, dato):
    """
    Funcion encargada de la realizacion de los update en la bbdd.
    :param tabla es la tabla a la que corresponde el update, campo es el campo que deseamos actualizar en la bbdd, primary es un diccionario con los datos necesarios para realizar el update, dato es el dato nuevo que queremos añadir en el update
    :return Si el update se ha realizado con exito deolveremos true en caso contrario devolveremos False
    """
    try:
        if tabla == "Profesores":
            #Depeniendo del campo que queramos modificar entraremos a un if u otro
            if campo == "dni":
                Profesores.update(dni=dato).where(Profesores.dni == primary).execute()
            elif campo == "nombre":
                Profesores.update(nombre=dato).where(Profesores.dni == primary).execute()
            elif campo == "telefono":
                Profesores.update(telefono=dato).where(Profesores.dni == primary).execute()
            elif campo == "direccion":
                Profesores.update(direccion=dato).where(Profesores.dni == primary).execute()

        elif tabla == "Alumnos":
            #Depeniendo del campo que queramos modificar entraremos a un if u otro
            if campo == "nombre":
                Alumnos.update(nombre=dato).where(Alumnos.nombre == primary['nombre'],
                                                  Alumnos.apellido == primary['apellido']).execute()
            elif campo == "apellido":
                Alumnos.update(apellido=dato).where(Alumnos.nombre == primary['nombre'],
                                                    Alumnos.apellido == primary['apellido']).execute()
            elif campo == "telefono":
                Alumnos.update(telefono=dato).where(Alumnos.nombre == primary['nombre'],
                                                    Alumnos.apellido == primary['apellido']).execute()
            elif campo == "direccion":
                Alumnos.update(direccion=dato).where(Alumnos.nombre == primary['nombre'],
                                                     Alumnos.apellido == primary['apellido']).execute()
            elif campo == "fech_nacim":
                Alumnos.update(fech_nacim=dato).where(Alumnos.nombre == primary['nombre'],
                                                      Alumnos.apellido == primary['apellido']).execute()
        elif tabla == "Cursos":
            #Depeniendo del campo que queramos modificar entraremos a un if u otro
            if campo == "nombre":
                Cursos.update(nombre=dato).where(Cursos.nombre == primary).execute()
            elif campo == "descripcion":
                Cursos.update(descripcion=dato).where(Cursos.nombre == primary).execute()

        return True
    except:
        #print("Fallos en la actualizacion")
        #print(traceback.format_exc())
        return False

    return 0


def selectAll(tabla):
    """
    Funcion encargada de la realizacion de los selectAll de la bbdd.
    :param tabla es la tabla a la que corresponde al select
    :return Si el select se ha realizado con exito deolveremos un diccionario en caso contrario devolveremos None
    """
    try:
        lista = ()
        if tabla == "Profesores":
            lista = list(Profesores.select().dicts())
        elif tabla == "Alumnos":
            lista = list(Alumnos.select().dicts())
        elif tabla == "Cursos":
            lista = list(Cursos.select().dicts())
        elif tabla == "Cursos_Profesores":
            lista = list(Cursos_Profesores.select().dicts())
        elif tabla == "Cursos_Alumnos":
            lista = list(Cursos_Alumnos.select().dicts())
        return lista
    except:
        #print("Fallos en la seleccion")
        #print(traceback.format_exc())
        return None
    return 0


def select1(tabla, primary):
    """
    Funcion encargada de la realizacion de los select de la bbdd.
    :param tabla es la tabla a la que corresponde al select, primary es un diccionario con los datos necesarios para hacer la seleccion
    :return Si el select se ha realizado con exito deolveremos un diccionario en caso contrario devolveremos None
    """
    try:
        entidad = None
        if tabla == "Profesores":
            entidad = Profesores.select().where(Profesores.dni == primary).get()

        elif tabla == "Alumnos":
            entidad = Alumnos.select().where(Alumnos.nombre == primary['nombre'],
                                             Alumnos.apellido == primary['apellido']).get()

        elif tabla == "Cursos":
            entidad = Cursos.select().where(Cursos.nombre == primary).get()

        elif tabla == "Cursos_Profesores":
            entidad = Cursos_Profesores.select().where(Cursos_Profesores.cod_curs == primary['cod_curs'],
                                                       Cursos_Profesores.id_prof == primary['id_prof']).get()

        elif tabla == "Cursos_Alumnos":
            entidad = Cursos_Alumnos.select().where(Cursos_Alumnos.cod_curs == primary['cod_curs'],
                                                    Cursos_Alumnos.num_exp == primary['num_exp']).get()

        return entidad
    except:
        #print("Fallos en la seleccion")
        #print(traceback.format_exc())
        return None


def selectJoinMostrar(tabla, primary):
    """
    Funcion encargada de la realizacion de los selectJoin para mostrar de la bbdd.
    :param tabla es la tabla a la que corresponde al select,primay es un diccionario con la informacion necesaria para hacer el select
    :return Si el select se ha realizado con exito deolveremos un diccionario con diccionarios dentro en caso contrario devolveremos None
    """
    try:
        lista = ()

        if tabla == "Profesores":
            #Obtenemos los datos de caada parte de la seleccion y despues añadiremos los datos secundarios
            lista = list(Profesores.select().where(Profesores.dni == primary.dni).dicts())
            cursos = list(Cursos.select(Cursos.nombre).join(Cursos_Profesores).where(
                Cursos_Profesores.cod_curs == Cursos.cod_curs, Cursos_Profesores.id_prof == primary.id_prof).dicts())
            lista.append(cursos)

        elif tabla == "Alumnos":
            #Obtenemos los datos de caada parte de la seleccion y despues añadiremos los datos secundarios
            lista = list(Alumnos.select().where(Alumnos.nombre == primary.nombre,
                                                   Alumnos.apellido == primary.apellido).dicts())
            cursos = list(
                Cursos.select(Cursos.nombre).join(Cursos_Alumnos).where(Cursos.cod_curs == Cursos_Alumnos.cod_curs,
                                                                        Cursos_Alumnos.num_exp == primary.num_exp).dicts())
            lista.append(cursos)

        elif tabla == "Cursos":
            #Obtenemos los datos de caada parte de la seleccion y despues añadiremos los datos secundarios
            lista = list(Cursos.select().where(Cursos.nombre == primary.nombre).dicts())
            profesor = list(Profesores.select(Profesores.nombre, Profesores.dni)
                            .join(Cursos_Profesores)
                            .join(Cursos)
                            .where(Cursos.cod_curs == primary.cod_curs, Cursos_Profesores.cod_curs == Cursos.cod_curs,
                                   Profesores.id_prof == Cursos_Profesores.id_prof).dicts())
            alumnos = list(Alumnos.select(Alumnos.nombre, Alumnos.apellido)
                           .join(Cursos_Alumnos)
                           .where(Alumnos.num_exp == Cursos_Alumnos.num_exp, Cursos_Alumnos.cod_curs == primary.cod_curs).dicts())
            lista.append(profesor)
            lista.append(alumnos)

        return lista
    except:
        #print("Fallos en la seleccion")
        print(traceback.format_exc())
        return None


def selectJoin(tabla, primary):
    """
    Funcion encargada de la realizacion de los selectJoin para trabajar de la bbdd.
    :param tabla es el tipo de seleccion qu ueremos haccer, primay es un diccionario con la informacion necesaria para hacer el select
    :return Si el select se ha realizado con exito deolveremos un diccionario en caso contrario devolveremos None
    """
    try:
        entidad = None
        #Saber si un profesor esta relacionado con algun curso
        if tabla == "ProfesoresEnCursos":
            # Si el profesor esta en Cursos_profesores
            entidad = list((Profesores.select().join(Cursos_Profesores).where(Profesores.dni == primary,
                                                                              Profesores.id_prof == Cursos_Profesores.id_prof)))
        #Saber si un alumno esta matriculado en algun curso
        elif tabla == "AlumnosEnCursos":
            # Si el alumno esta en Cursos_alumnos
            entidad = list((Alumnos.select().join(Cursos_Alumnos).where(Alumnos.nombre == primary['nombre'],
                                                                        Alumnos.apellido == primary['apellido'],
                                                                        Alumnos.num_exp == Cursos_Alumnos.num_exp)))

        # Si el curso esta en Cursos_alumnos
        elif tabla == "CursosEnAlumnos":
            entidad = list((Cursos.select().join(Cursos_Alumnos).where(Cursos.cod_curs == primary,
                                                                       Cursos.cod_curs == Cursos_Alumnos.cod_curs)))
        # Si el curso esta en Cursos_profesores
        elif tabla == "CursosEnProfesores":
            entidad = list((Cursos
                            .select(Cursos)
                            .join(Cursos_Profesores)
                            .where(Cursos.cod_curs == primary, Cursos.cod_curs == Cursos_Profesores.cod_curs)))

        elif tabla == "Cursos_Profesores":
            entidad = list((Cursos_Profesores.select().where(Cursos_Profesores.cod_curs == primary['cod_curs'],
                                                             Cursos_Profesores.id_prof == primary['id_prof'])))
        #Saber si hay cursos con alumnos
        elif tabla == "Cursos_Alumnos":
            entidad = list((Cursos_Alumnos.select().where(Cursos_Alumnos.cod_curs == primary['cod_curs'],
                                                          Cursos_Alumnos.num_exp == primary['num_exp'])))
        #Saber si hay un profesor en un cuso
        elif tabla == "ProfesorEnUnCurso":
            entidad = (Profesores.select(Profesores)
                       .join(Cursos_Profesores)
                       .join(Cursos)
                       .where(Cursos.cod_curs == primary, Cursos_Profesores.cod_curs == primary,
                              Profesores.id_prof == Cursos_Profesores.id_prof)).get()


        return entidad
    except:
        #print("Fallos en la seleccion")
        #print(traceback.format_exc())
        return None


#Creamos la variable conn para inicializarla
conn = None
#Comprobamos que la conexion esta bien y si este es el caso rrreaalizamos la conexion con peewee si no cerramos el programa
if (iniciar()):
    conn = conectarAPeewee()
else:
    sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error


#Las diferentes class para tener las tablas en peewee
class Profesores(Model):
    id_prof = AutoField()  # Equivale al auto_increment
    dni = CharField(null=False, unique=True)
    nombre = CharField(null=False)
    telefono = CharField(null=False)
    direccion = CharField(null=False)

    class Meta:
        database = conn


class Alumnos(Model):
    num_exp = AutoField()  # Equivale al auto_increment
    nombre = CharField(null=False)
    apellido = CharField(null=False)
    telefono = CharField(null=False)
    direccion = CharField(null=False)
    fech_nacim = DateField(formats=['%d-%m-%Y'], null=False)

    class Meta:
        database = conn
        indexes = (  # Para hacer que la combinacion de campos sea unique
            (('nombre', 'apellido'), True),
        )


class Cursos(Model):
    cod_curs = AutoField()  # Equivale al auto_increment
    nombre = CharField(null=False, unique=True)
    descripcion = CharField(null=False)

    class Meta:
        database = conn


class Cursos_Profesores(Model):
    cod_curs = ForeignKeyField(Cursos, on_delete='CASCADE', on_update='CASCADE')
    id_prof = ForeignKeyField(Profesores, on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        database = conn
        primary_key = CompositeKey('cod_curs', 'id_prof')


class Cursos_Alumnos(Model):
    cod_curs = ForeignKeyField(Cursos, on_delete='CASCADE', on_update='CASCADE')
    num_exp = ForeignKeyField(Alumnos, on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        database = conn
        primary_key = CompositeKey('cod_curs', 'num_exp')


#Tras tener los modelos crearemos las tablas
crearTablas(conn)
