import GestorBaseDeDatos
import GestionProfesores
import GestionCursos
import GestionAlumnos

conn = GestorBaseDeDatos.iniciar()

#Profesores
#-----------------------------------------------------------------

#GestionProfesores.alta()

#GestionProfesores.baja()

#GestionProfesores.modificar()

#GestionProfesores.buscar()

GestionProfesores.mostrarTodos()

#Alumnos
#-----------------------------------------------------------------

GestionAlumnos.alta()

#GestionAlumnos.baja()

#GestionAlumnos.modificar()

#GestionAlumnos.buscar()

GestionAlumnos.mostrarTodos()

#Cursos
#-----------------------------------------------------------------

#GestionCursos.alta()

#GestionCursos.baja()

#GestionCursos.modificar()

#GestionCursos.buscar()

GestionCursos.mostrarTodos()

GestionCursos.relacionar()

#-----------------------------------------------------------------

conn.close()