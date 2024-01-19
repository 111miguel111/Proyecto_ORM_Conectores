import pymysql
from peewee import *
import configparser
import Utiles
import sys
import traceback

def update(conn, tabla, id, campo, dato):
    try:
        if tabla == "Profesores":
            
            Profesores.update(campo=request.form[dato]).where(Profesores.id_prof==session[id]).execute()
            
            Profesor.update(campo=dato).where(Profesores.id_prof==id).execute()
            
            actualizar = Profesores.update({conn.Profesores.campo:dato}).where(Profesores.id_prof==id)
            actualizar.execute()

        elif tabla == "Alumnos":
            actualizar = Alumnos.delete().where(Alumnos.nombre == primary['nombre'] &
                                                 Alumnos.apellido == primary['apellido'])
            actualizar.execute()

        elif tabla == "Cursos":
            actualizar = Cursos.delete().where(Cursos.nombre == primary)
            actualizar.execute()

        elif tabla == "Cursos_Profesores":
            actualizar = Cursos_Profesores.delete().where(Cursos.cod_curs == primary['cod_curs'] &
                                                           Profesores.id_prof == primary['id_prof'])
            actualizar.execute()

        elif tabla == "Cursos_Alumnos":
            actualizar = Cursos_Alumnos.delete().where(Cursos.cod_curs == primary['cod_curs'] &
                                                           Alumnos.num_exp == primary['num_exp'])
            actualizar.execute()

        return True
    except:
        print("Fallos en la insercion")
    
    return 0

def select():
    
    
    return 0