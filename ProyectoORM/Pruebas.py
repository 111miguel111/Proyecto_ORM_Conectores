import GestorBaseDeDatos
import GestionProfesores

conn = GestorBaseDeDatos.iniciar()


GestionProfesores.alta(conn)


conn.close()