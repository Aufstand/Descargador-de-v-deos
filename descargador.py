import re # Regular expression
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Todo esto para que funcione el selenium

import time # Para que el selenium espere.

print("Abriendo txt...")

txtlecciones = open("enlaceslecciones.txt", "r") # Abre para lectura el código en bruto con todos los enlaces de cada página en la que está el vídeo a descargar.
escritura = open("enlacesbueno.txt", "w") # Abre para escritura el txt en el que escribirá los enlaces.
for line in txtlecciones: # Por cada línea en el archivo de lectura...
    urls = re.findall(r'(https?://[^\s]+)', line) # urls es cada línea que entre en los parámetros del RE, es decir, enlaces https.
    for enlace in urls: # Por cada cosa en urls...
        escritura.write("%s\n" % enlace[:-1]) # Escribe cada enlace. El primer parámetro dice que abra una línea nueva. El segundo, que quite unas comillas del final.

escritura.close() # Hay que cerrar las cosas después de abrirlas.
txtlecciones.close()
 
""""""""""

Hasta aquí el sacaenlaces churro. Es churro porque sacar los enlaces no está automatizado. Y porque no sé usar regex.

"""""""""""

username = "USER" # String con el usuario que debe escribir en el cajón de texto.
password = "PASS" # String con el password.

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install())) # Este es un descargador del webdriver.
# Con chrome no tuve problema en poner el webdriver.exe en la carpeta. Pero con firefox, sí. Más info: https://blog.finxter.com/how-to-solve-webdriverexception-message-geckodriver-executable-needs-to-be-in-path/
# Así que lo que hace es descargar el webdriver y así me quito de problemas. No es lo más eficiente.
# Ve a la página que quieres
driver.get("PÁGINA DE ACCESO")
# Encuentra el elemento que tiene el siguiente ID. Se puede facilitar con https://curlconverter.com. Para eso, hay que ir al inspect, red y copiar el elemento como curl.
driver.find_element(By.ID,"user_login").send_keys(username)
# Lo mismo con el password.
driver.find_element(By.ID,"user_pass").send_keys(password)
# Pulsa en este elemento.
driver.find_element(By.ID,"wp-submit").click()
# No recuerdo para qué era esto de abajo.
# element = WebDriverWait(driver, 3).until(
#     EC.presence_of_element_located((By.ID, "post-65541"))
# )

enlaces = open("enlacesbueno.txt", "r") # Abre el archivo de enlaces que hemos creado en la primera parte.

n = 0 # Para poder nombrar recursivamente cada archivo.
retry_limit = 3 # Por si da error porque no ha cargado el elemento.

for line in enlaces:
    driver.get(line) # Abre el enlace.
    time.sleep(1.5) # Espera a que cargue. 1.5 segundos es lo que he visto que funciona. Con 1 segundo no llegaba a cargar el elemento y creaba excepción.
    frame = driver.find_element(By.TAG_NAME, "iframe") # Para sacar este elemento concrteo, hay que meterse en un "iframe". No sé HTML.
    driver.switch_to.frame(frame) # Ponte en el iframe.
    retry = 0 # Intento.
    n = n + 1 # Por cada vuelta en el bucle, suma 1 a n.
    while retry < retry_limit: # Mientras el intento sea menor que el límite de intentos.
        try:
            value = driver.find_element(By.CLASS_NAME, "vp-center") # Encuentra el elemento a copiar.
            innerhtml = value.get_attribute("innerHTML") # Coge su contenido.
            fileToWrite = open(r"PATH\page_source{0}.txt".format(n), "w", encoding="utf-8") # Abre en escritura lo que quieres escribir.
            print(value) # Esto lo puse para ver que funcionaba.
            fileToWrite.write(innerhtml) # Escribe el contenido.
            fileToWrite.close() # Cierra.
            break # Sin esta ruptura de bucle, como retry sigue siendo menor que retry_limit, crea archivos sin parar repitiendo el bloque try.
        except Exception as e:
            retry = retry + 1 # Si falla, vuelve a intentarlo un número limitado de veces. Vuelve al bloque try, desde while.
            if retry == retry_limit:
                print(e) # Imprime el error.


""""""""""

Hasta aquí el logueador y descargador. No he juntado el selenium con la siguiente parte del código porque
el selenium corre mientras el código continua. Usando la librería threading creo que es posible pausar el código
hasta que el selenium acabe. Pero no sé usarlo. Y usar un bucle while que comprobase si los archivos están en la carpeta
me parece de burros.

"""""""""""
