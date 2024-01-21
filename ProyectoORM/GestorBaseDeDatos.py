import pymysql
from peewee import *
import configparser
import Utiles
import sys
import traceback

def escanerNumerico():
    '''
    Metodo para escanear una cadena con solo numeros
    :return Si la cadena es valida devuelve la cadena, si no devuelve None
    '''
    # Se crea un contador de intentos para el bucle que solo iterara hasta 5 intentos
    intentos = 0
    while (intentos < 5):
        scan = input()
        # Se introduce la cadena y comprueba que no este vacio y que ponga 1 o 2 si no te vuelve a preguntar y si fallas 5 veces devulve none
        if (scan.isspace() == False and scan.isnumeric() and (scan == '1' or scan == '2')):
            return scan
        intentos += 1
        print('Porfavor introduce numeros no decimales')
    print("Has superado el numero de intentos")
    return None


def iniciarFicheroConfiguracion():
    '''
    Funcion que se encarga de crear el fichero de configuracion con valores predeterminados
    '''
    try:
        # Creamos un fichero .ini en el cual se guardan datos para la configuracion del programa
        config = configparser.ConfigParser()  # Creamos la variable
        config['SERVER'] = {'host': 'localhost',
                            'user': 'root',
                            'password': '1234',
                            'port': '3306'}
        with open('config.ini', 'w') as configfile:  # Escribimos el fichero de configuracion
            config.write(configfile)
        print("Se ha creado el fichero de configuracion")
    except:
        print("No se ha podido crear el fichero de configuracion")
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


def conectarse(conn):
    '''
    Funcion encargada de usar la base de datos y devolver un cursor
    :return Devuelve un cursor conectado a la base de datos
    '''
    # Creamos un nuevo cursor y nos aseguramos de usar la base de datos correcta
    cur = conn.cursor()
    cur.execute('USE miguel_roberto')
    return cur


def deconectarse(conn):
    '''
    Funcion encargada de desconectarse de la la base de datos y cerrar la conexion
    :param conn:
    '''
    # Guardamos culaquier cambio en la conexion y la cerramos
    conn.commit()
    conn.close()
    print("La conexion ha terminado ")
    return 0


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
        
        conn = pymysql.connect(
            host=host_variable,
            user=user_variable,
            password=password_variable,
            port=port_variable
        )
        return conn
    # Si la conexion no se puede realizar ya sea por que  el gestor de base de datos esta apagado nos informara
    except pymysql.err.OperationalError as e:
        print("Se ha producido un error, compruebe que el sistema gestor de base de datos al que se quiere conectar \nesta operativa y que los datos son correctos.\nEl programa se cerrara")
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
    try:
        conn.create_tables([Profesores, Alumnos, Cursos, Cursos_Profesores, Cursos_Alumnos])
        print("Se han creado las tablas bien.")
    except Exception:
        print(traceback.format_exc())
        print("No se pudieron crear las tablas.")


def conectarAPeewee():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        host_variable = str(config['SERVER']['host'])
        user_variable = str(config['SERVER']['user'])
        password_variable = str(config['SERVER']['password'])
        port_variable = int(config['SERVER']['port'])

        conn = MySQLDatabase('miguel_antonio_bd',
                             user=user_variable,
                             password=password_variable,
                             host=host_variable,
                             port=port_variable)

        print(conn, type(conn))
        conn.connect()

        return conn
    # Si la conexion no se puede realizar ya sea por que  el gestor de base de datos esta apagado nos informara
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
    Funcion encargada de iniciar lo relacionado con la base de datos, la configuracion la conexion, crear las tablas etc
    '''
    # Metodo que inicia lo relacionado con la base de datos, comprueba el fichero de datos, comprueba la conexion y si esta bien procede a crear una base de datos con las tablas necesarias
    try:
        if (checkFileExistance("config.ini") == True):  # Comprobamos que el fichero de configuracion existe, si no es el caso lo creamos con los datos por defecto
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
            iniciarFicheroConfiguracion()
        # Llama a la conexion para comprobar si esta funciona
        # Creamos la bbdd en pymysql
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
    :param conn es la conexion, tabla es la tabla a la que corresponde el insert, datos es un diccionario con los datos del insert
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
        print("Fallos en la insercion")
        print(traceback.format_exc())
        return False


def delete(tabla, primary):
    """
    Funcion encargada de la realizacion de los inserts en la bbdd.
    :param conn es la conexion, tabla es la tabla a la que corresponde el insert, datos es un diccionario con los datos del insert
    """
    try:
        if tabla == "Profesores":
            borrar = Profesores.delete().where(Profesores.dni == primary)
            borrar.execute()

        elif tabla == "Alumnos":
            borrar = Alumnos.delete().where(Alumnos.nombre == primary['nombre'] ,
                                                 Alumnos.apellido == primary['apellido'])
            borrar.execute()

        elif tabla == "Cursos":
            borrar = Cursos.delete().where(Cursos.nombre == primary)
            borrar.execute()

        elif tabla == "Cursos_Profesores":
            borrar = Cursos_Profesores.delete().where(Cursos_Profesores.cod_curs == primary['cod_curs'] ,
                                                           Cursos_Profesores.id_prof == primary['id_prof'])
            borrar.execute()

        elif tabla == "Cursos_Alumnos":
            borrar = Cursos_Alumnos.delete().where(Cursos_Alumnos.cod_curs == primary['cod_curs'] ,
                                                           Cursos_Alumnos.num_exp == primary['num_exp'])
            borrar.execute()

        return True
    except:
        print("Fallos en la insercion")
        print(traceback.format_exc())
        return False

def update(tabla, campo, primary, dato):
    try:
        if tabla == "Profesores":
            if campo == "dni":
                Profesores.update(dni=dato).where(Profesores.dni == primary).execute()
            elif campo == "nombre":
                Profesores.update(nombre=dato).where(Profesores.dni == primary).execute()
            elif campo == "telefono":
                Profesores.update(telefono=dato).where(Profesores.dni == primary).execute()
            elif campo == "direccion":
                Profesores.update(direccion=dato).where(Profesores.dni == primary).execute()

        elif tabla == "Alumnos":
            if campo == "nombre":
                Alumnos.update(nombre=dato).where(Alumnos.nombre == primary['nombre'] , 
                                                 Alumnos.apellido == primary['apellido']).execute()
            elif campo == "apellido":
                Alumnos.update(apellido=dato).where(Alumnos.nombre == primary['nombre'] , 
                                                 Alumnos.apellido == primary['apellido']).execute()
            elif campo == "telefono":
                Alumnos.update(telefono=dato).where(Alumnos.nombre == primary['nombre'] , 
                                                 Alumnos.apellido == primary['apellido']).execute()
            elif campo == "direccion":
                Alumnos.update(direccion=dato).where(Alumnos.nombre == primary['nombre'] , 
                                                 Alumnos.apellido == primary['apellido']).execute()
            elif campo == "fech_nacim":
                Alumnos.update(fech_nacim=dato).where(Alumnos.nombre == primary['nombre'] , 
                                                 Alumnos.apellido == primary['apellido']).execute()
        elif tabla == "Cursos":
            
            if campo == "nombre":
                Cursos.update(nombre=dato).where(Cursos.nombre == primary).execute()
            elif campo == "descripcion":
                Cursos.update(descripcion=dato).where(Cursos.nombre == primary).execute()

        return True
    except:
        print("Fallos en la actualizacion")
        print(traceback.format_exc())
        return False
    
    return 0


def selectAll(tabla):
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
        print("Fallos en la seleccion")
        print(traceback.format_exc())
        return None
    return 0


def select1(tabla, primary):
    try:
        entidad = None
        if tabla == "Profesores":
            entidad = Profesores.select().where(Profesores.dni == primary).get()

        elif tabla == "Alumnos":
            entidad = Alumnos.select().where(Alumnos.nombre == primary['nombre'] , 
                                             Alumnos.apellido == primary['apellido']).get()

        elif tabla == "Cursos":
            entidad = Cursos.select().where(Cursos.nombre == primary).get()

        elif tabla == "Cursos_Profesores":
            entidad = Cursos_Profesores.select().where(Cursos_Profesores.cod_curs == primary['cod_curs'] , 
                                                       Cursos_Profesores.id_prof == primary['id_prof']).get()

        elif tabla == "Cursos_Alumnos":
            entidad = Cursos_Alumnos.select().where(Cursos_Alumnos.cod_curs == primary['cod_curs'] , 
                                                    Cursos_Alumnos.num_exp == primary['num_exp']).get()

        return entidad
    except:
        print("Fallos en la seleccion")
        print(traceback.format_exc())
        return None
    
    
def selectJoin(tabla, primary):
    try:
        entidad = None
        if tabla =="ProfesoresEnCursos":
            #Si el profesor esta en Cursos_profesores
            entidad=list((Profesores.select().join(Cursos_Profesores).where(Profesores.dni == primary , Profesores.id_prof==Cursos_Profesores.id_prof)))
        elif tabla == "AlumnosEnCursos":
            #Si el alumno esta en Cursos_alumnos
            entidad= list((Alumnos.select().join(Cursos_Alumnos).where(Alumnos.nombre == primary['nombre'] , Alumnos.apellido == primary['apellido'] , Alumnos.num_exp==Cursos_Alumnos.num_exp)))
        elif tabla=="CursosEnAlumnos":
            #Si el curso esta en Cursos_alumnos
            entidad=list((Cursos.select().join(Cursos_Alumnos).where(Cursos.nombre == primary , Cursos.cod_curs == Cursos_Alumnos.cod_curs)))
        elif tabla=="CursosEnProfesores":
             #Si el curso esta en Cursos_profesores
             entidad = list((Cursos
                           .select(Cursos)
                           .join(Cursos_Profesores)
                           .where(Cursos.cod_curs == primary , Cursos.cod_curs == Cursos_Profesores.cod_curs)))
             """entidad=list((Cursos.select(Cursos).join(Cursos_Profesores).where(Cursos.nombre == primary , Cursos.cod_curs == Cursos_Profesores.cod_curs)))"""
        elif tabla == "Cursos_Profesores":
            entidad = list((Cursos_Profesores.select().where(Cursos_Profesores.cod_curs == primary['cod_curs'] , 
                                                       Cursos_Profesores.id_prof == primary['id_prof'])))

        elif tabla == "Cursos_Alumnos":
            entidad = list((Cursos_Alumnos.select().where(Cursos_Alumnos.cod_curs == primary['cod_curs'] , 
                                                    Cursos_Alumnos.num_exp == primary['num_exp'])))

        return entidad
    except:
        print("Fallos en la seleccion")
        print(traceback.format_exc())
        return None


conn = None
# ES LA MIERDA MAS GRANDE DE LA NOCHE TAL VEZ, HE PROBADO UN MONTON DE COSAS, TAMBIEN, FUNCIONA COMO UN TIRO, ALSO YES
if (iniciar()):
    conn = conectarAPeewee()  # SOLO SE CONECTA Y DEVULEVE CONN NADA MAS
else:
    sys.exit()  # Cerramos el programa ya que no deberia continuar tras este error


# LOS CLASS NO HE ENCONTRADO LA MANERA DE QUE ESTEN DENTRO DE UNA FUNCION, POR COJONES ESTAN FUERA
# A LA HORA DEL CONN NO ME GUSTA HACERLO GLOBAL PORQUE NO ME GUSTA
# LA OTRA OPCION ESQUE EN CADA "database = conn" PONER "database = conestarAPeewee()" PERO ESO CREO QUE ES PEOR QUE UN CONN GLOBAL

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
    fech_nacim = DateField(formats=['%d-%b-%Y'], null=False)

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


# SI INTENTO PONER EL CREAR TABLAS EN CAULQUIER OTRO SITIO QUE NO SEA JUSTAMENTE DESPUES DE LOS CLASS ME DICE QUE LAS CLASSES NO ESTAN DEFINIDAS
# Y OBVIAMENTE SI EL IF DE MIERDA LOPONGO AQUI ABAJO LAS CLASES ME DICEN QUE CONN NO ESTA DEFINIDA
crearTablas(conn)