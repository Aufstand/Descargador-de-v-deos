import re # Regular expression.
import os # os para poder interactuar con los archivos del ordenador (ver qué archivos hay, moverlos, etc)
import urllib.request # Para poder interactuar con internet.

n = 0 # Contador de archivos.
z = 0 # Contador de archivos.
directorio = r"C:\CursoPython\script" # Dónde tenemos el interior del bloque de HTML que hemos abierto antes con innerHTML.
directorio2 = r"C:\CursoPython\enlaces" # Dónde vamos a depositar los txt con enlaces.


for filename in os.listdir(directorio): # Por cada archivo en el directorio
    txt = open(os.path.join(directorio, filename), "r") # Abrir el archivo y depositarlo en la variable txt
    n = n + 1 # Sumar a n 1 por cada vuelta en el bucle.
    Enlacesmp4 = open(r"C:\CursoPython\enlaces\Enlaces{0}.txt".format(n), "w", encoding="utf-8") # Abrir en modo escritura (y crear el archivo).
    for line in txt: # Por cada línea en el archivo que estamos leyendo:
        link_regex = re.compile(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)') # Coger los enlaces.
        links = re.findall(link_regex, line) # Coge los enlaces, pero no recuerdo bien la diferencia con la anterior línea.
        for element in links: # Links es una lista de diccionarios.
            madrecita = list(element) # Lo llamé madrecita porque estaba hasta las narices de que esto no funcionase. Esto hace que el diccionario se transforme en lista.
            for objeto in madrecita: # Por cada objeto en cada lista.
                if "mp4" in objeto: # Si tiene "mp4". Esto es porque solo quiero los enlaces que tengan mp4 en ellos, no los que no lo tengan.
                    Enlacesmp4.write("%s\n" % objeto) # Esto escribe cada "enlaces{0}.txt" con los enlaces mp4 de cada archivo txt. Y vuelve al principio, a sumar n a 1 y tal.
                    continue # Esto creo que es innecesario. Pero ya está.
                else:
                    continue # Si no tiene mp4, vuelve al principio del bucle, al primer for.

txt.close()
Enlacesmp4.close()

n = 0 # Reseteamos n porque lo vamos a volver a utilizar.
for filename in os.listdir(directorio2):
    txt = open(os.path.join(directorio2, filename), "r") # Esto es necesario porque directorio2 y listdir nos dan el archivo sin la dirección absoluta, es decir, sin C:\Carpeta, etc. Entonces no lo encuentra.
    n = n + 1
    Enlacesmp4 = open(r"C:\CursoPython\enlaces\Enlaces{0}.txt".format(n), "r", encoding="utf-8")
    lines = Enlacesmp4.readlines() # Esto lo tengo que hacer porque son 4 enlaces mp4 con los vídeos en diferentes calidades. Me da igual, solo quiero uno de ellos, el que sea.
    # Antes creé con la librería requests unas líneas que trataban de medir el archivo antes de bajarlo, y si era demasiado grande o demasiado pequeño, pasaban. Pero demasiados errores, y tardaba mucho en medir cada archivo.
    # Haciendo esto de abajo, elimintar 3 de las cuatro líneas, se ahorra mucho tiempo.
    for number, line in enumerate(lines):
        if number not in [1, 2, 3]:
            Enlacesmp4 = open(r"C:\CursoPython\enlaces\Enlaces{0}.txt".format(n), "w", encoding="utf-8")
            Enlacesmp4.write(line) # Escribe la línea que queda y ya.

for archive in os.listdir(directorio2): # Coge cada archivo de txt.
    descarga = open(os.path.join(directorio2, archive), "r") # Coge cada enlace de estos archivos.
    for enlace in descarga: # Por cada enlace en cada archivo...
        for mp4 in os.listdir(r"C:\CursoPython\videos"): # Esto dice que por cada archivo en este directorio.
            z = z + 1
            if r"Leccion{0}.mp4".format(z) not in os.listdir(r"C:\CursoPython\videos"): # Si el archivo no está en la carpeta, pasa a descargar.
                print("Descargando", enlace)
                urllib.request.urlretrieve((enlace), r"C:\CursoPython\videos\Leccion{0}.mp4".format(z)) # Descarga el archivo con este nombre en esta dirección.
                break
            elif r"Leccion{0}.mp4".format(z) in os.listdir(r"C:\CursoPython\videos"): # Si el archivo está presente, te lo dice y vuelve al for mp4.
                print(r"Leccion{0}.mp4".format(z), "ya está presente en el directorio.")
                break
            else:
                print("Qué ha pasado, yo no lo sé.") # Esto es por si pasaba alguna locura.

print("Ya estaría, no?")



