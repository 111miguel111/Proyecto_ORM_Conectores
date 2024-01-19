import GestorBaseDeDatos
import GestionProfesores

conn = GestorBaseDeDatos.iniciar()


#GestionProfesores.alta(conn)

GestionProfesores.baja(conn)

conn.close()