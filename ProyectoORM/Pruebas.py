import GestorBaseDeDatos
import GestionProfesores

conn = GestorBaseDeDatos.iniciar()

#GestionProfesores.alta()

#GestionProfesores.baja()

#GestionProfesores.modificar()

#GestionProfesores.buscar()

GestionProfesores.mostarTodos()

conn.close()