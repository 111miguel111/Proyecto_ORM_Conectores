Trabajo realizado por Antonio Leon y Miguel Gonzalez.
Cosas a tener en cuenta.
Se requiere la instalacion de peewee y pymysql "para la creacion de la database".
El programa en caso de no existir un archivo config.ini, pedira los datos y lo creara,
en caso de que ya exista el fichero solo comprobara que no esta corrupto y en caso de 
que asi sea, podras rehacerlo con datos por defecto o cerrar el programa.
Si quieres que te vuelva a pedir los datos, borra el fichero config.ini.
El fichero acepta que el campo password este vacio.
La clase principal que lanza el programa es Main.py