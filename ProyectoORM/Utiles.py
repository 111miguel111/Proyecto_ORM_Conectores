from datetime import datetime


def confirmacion(contexto):
    '''
    Metodo para confirmar si se quiere confirmar una operacion
    :return Devuelve un un boolean. El valor sera True si escribe 'si' y False si escribe 'no'
    '''
    cont = 0
    while cont < 5:
        print(contexto)
        inputConfirmacion = input()
        if inputConfirmacion.lower() == 'si':
            return True
        elif inputConfirmacion.lower() == 'no':
            return False
        else:
            if cont < 4:
                print("\nValor incorrecto, pruebe otra vez (Si o no)."+"\n")
            cont += 1
    print("Has superado el numero de intentos."+"\n")
    return False


def entrada_teclado(contexto=""):
    """
    Funcion de apoyo que cerciora que la cadena que se introduce no este vacia
    :param contexto: informcacion sobre el campo
    :return: respuesta: si el campo es correcto
    :return: None: si el campo esta vacio
    """
    print(contexto.capitalize() + ": ")
    respuesta = input()
    if respuesta is not None and not respuesta.isspace():
        return respuesta.strip()
    else:
        print("El campo, " + contexto + " no puede estar vacio."+"\n")
        return None


# CHECKERS
def check_campo(contexto, long):
    """
    Funcion de apoyo que cerciora que la cadena que se introduce tiene como maximo una longitud y ademas es alfanumerica
    :param contexto: Explicacion del campo al que se refiere
    :param long: longitud maxima de la cadena
    :return: campo si este cumple las validaciones
    :return: None si se falla 5 veces en la introduccion del campo
    """
    fallos = 0
    while fallos < 5:
        campo = entrada_teclado(contexto)
        if campo is not None:
            palabras = campo.split(" ")
            carac_no_valido = False
            for espacio in palabras:  # Comprobamos que en las posibles palabras del campo no haya componentes no alfanumericos
                if not espacio.isalnum():
                    carac_no_valido = True

            if not carac_no_valido:
                long = int(long)
                if 0 < len(campo) <= long:  # Verificamos la longitud del campo
                    print(contexto.capitalize() + " introducido con exito.")
                    return campo.capitalize()
                else:
                    print(contexto + " tiene una longitud no valida, longitud maxima: " + str(long)+".\n")
                    fallos += 1
            else:
                if len(campo) == 0:
                    print("El campo, " + contexto + " no puede estar vacio."+"\n")
                    fallos += 1
                else:
                    print(contexto + " contiene caracteres no validos."+"\n")
                    fallos += 1
        else:
            fallos += 1
        if fallos < 5:
            print("Fallos hasta salir", fallos, "/5")
    print("Se han producido 5 fallos.\nAbotortando proceso.\n")
    return None


def check_dni():
    """
    Funcion de apoyo que cerciora que se introduce un DNI valido
    :return: dni, si es valido
    :return: None, si se falla 5 veces en la introduccion de DNI
    """
    fallos = 0
    while fallos < 5:
        print("Recuerde el formato de un DNI valido es 00000000A.")
        dni = entrada_teclado("DNI")
        if dni is not None:
            if len(dni) == 9:
                if dni[0:8].isnumeric():  # Es cerrado por la izquierda abierto por la derecha
                    if dni[8].isalpha():  # Solo coge el noveno caracter
                        print("DNI introducido con exito.")
                        return dni.upper()
                    else:
                        print("El ultimo caracter debe tratarse de una letra."+"\n")
                        fallos += 1
                else:
                    print("Los primeros 8 caracteres deben tratarse de numeros."+"\n")
                    fallos += 1
            else:
                print("El DNI debe de tener 9 caracteres."+"\n")
                fallos += 1
        else:
            fallos += 1
        if fallos < 5:
            print("Fallos hasta salir", fallos, "/5")
    print("Se han producido 5 fallos.\nAbotortando proceso"+"\n")
    return None


def check_telefono():
    """
    Funcion de apoyo que cerciora que se introduce un telefono valido
    :return: telefono, si esta es valida
    :return: None, si se falla 5 veces en la introduccion de un telefono
    """
    fallos = 0
    while fallos < 5:
        campo = entrada_teclado("telefono")
        if campo is not None:
            if campo.isnumeric():
                if len(campo) == 9:
                    print("Telefono introducido con exito.")
                    return campo
                else:
                    print("Telefono tiene una longituz no valida, longitud debe ser: 9."+"\n")
                    fallos += 1
            else:
                print("Telefono contiene caracteres no validos."+"\n")
                fallos += 1
        else:
            fallos += 1
        if fallos < 5:
            print("Fallos hasta salir", fallos, "/5")
    print("Se han producido 5 fallos.\nAbotortando proceso."+"\n")
    return None


def check_fecha():
    """
    Funcion de apoyo que cerciora que se introduce una fecha valida
    :return: fecha, si esta es valida
    :return: None, si se falla 5 veces en la introduccion de una fecha
    """
    fallos = 0
    while fallos < 5:
        print("Recuerde el formato de la fecha es DD-MM-YYYY.")
        fecha = entrada_teclado("fecha")
        if fecha is not None:
            if fecha.count("-") == 2:
                datos = fecha.split("-")
                if datos[0].isnumeric() and datos[1].isnumeric() and datos[0].isnumeric():
                    dia = int(datos[0])
                    mes = int(datos[1])
                    year = int(datos[2])
                    if ((mes in [1, 3, 5, 7, 8, 10, 12] and 1 <= dia <= 31 and 1990 <= year <= 2023) or
                            (mes in [4, 6, 9, 11] and 1 <= dia <= 30 and 1990 <= year <= 2023) or
                            (mes == 2 and 1 <= dia <= 28 and 1990 <= year <= 2023)):

                        print("Fecha introducida con exito.")
                        return datetime.strptime(str(dia) + "/" + str(mes) + "/" + str(year), "%d/%m/%Y").strftime(
                            "%d-%m-%Y")
                    else:
                        print(
                            "No se corresponde con una fecha valida: para mas info--> https://es.wikipedia.org/wiki/Mes"+"\n")
                        fallos += 1
                else:
                    print("Formato de fecha no valido."+"\n")
                    fallos += 1
            else:
                print("Formato de fecha no valido, recuerde respetar los guiones."+"\n")
                fallos += 1
        else:
            fallos += 1
        if fallos < 5:
            print("Fallos hasta salir", fallos, "/5")
    print("Se han producido 5 fallos.\nAbotortando proceso."+"\n")
    return None
