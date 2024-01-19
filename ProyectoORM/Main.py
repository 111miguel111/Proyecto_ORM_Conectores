import BaseDeDatosM


print("-----"*10)
print("Hello world!")
print("Efectivamente las 5 primeras lineas no son del main, este empieza en el Hello world!")

profesor={"dni":"dniprofesor" ,
          "nombre": "nombreprofesor",
          "telefono":"telefonoprofesor" ,
          "direccion":"direccionprofesor" }
#ESTO ESTA COMENTADO PORQUE EL PROFESOR YA EXISTE Y SE CAGA ENCIMA AL INTENTAR METER OTRO CON EL MISMO DNI, SI CAMBIAS EL DNI PUEDES METER UNO NUEVO
#BaseDeDatosM.insert("Profesores", profesor)

BaseDeDatosM.selectAll("Profesores")