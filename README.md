Api para el manejor de placas arduino y arduino_mega

Es necesario instalar pyfirmata, django, postgresql

################
#   Instalar   #
################
Descargar pyfirmata (https://github.com/tino/pyFirmata)

Según la distro que uses instalar django y postgres

Crear la dase de datos en postgres pg_sisa

modificar /home/user/sisa/sisa/setting.py, según los parametros de la base de datos creada

    DATABASES = {

        'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    
            'NAME': 'pg_sisa',                      # Or path to database file if using sqlite3.
        
            'USER': 'user_sisa',                      # Not used with sqlite3.
        
            'PASSWORD': 'clave_sisa',                  # Not used with sqlite3.
        
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        
            'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        
            }
    
        }

################
#Configuración #
################

cd /home/user/sisa

Creamos la estructura de la base de datos

    python manage.py syncdb

Se crea la estructura y llena tablas con ejemplos, para no llenar las tablas eliminamos la carpeta api/fixtures

Las tablas que se crean son:

placa: que nos permite definir el tipo de arduino a configurar, sus puertos digitales, analogos y pwm

puerto: en que puerto del sistema está configurada, ejemplo linux /dev/ttyACM0

tablero: tablero con el cual trabajaremos es decir que tipo de arduino y en el puerto que esta conectada

pin_placa: configuración de cada pin de un tablero, modo (entrada o salida), tipo (digital, análogo).

Combinacion_pin: Esta tabla define tipos de combinaciones que se tiene de ser el caso, que pin de salida controla un pin de entrada o pin de movimiento, y el tipo de manejo para el pin de movimiento en caso de configurarlo. ejm
pinentrada2, queremos que al enviar un pulso electrico a 1, envíe una señal a pinsalida8 y cambie de estado, al igual que pinmovimiento, de acuerdo al modo que esté configurado. off_auto, es decir mientras pinmovimiento no reciba señal, el pin8, o en el que esté configurado cambiara de estado a 0 (apaga), en caso de configurarlo como on_auto, cuando pinmovimiento reciva una señal, pin8 o el que este configurado cambiará de estado a 1 (enciende).


arrancar el servidor

    python /home/user/sisa/manage runserver


################
#     USO      #
################

Para usar el api, podremos enviar parámetros como recivir el estado de uno o todos los pines, para ello
Todos devuelve un json de la forma {"tablero":{"pin":"valor"}} ó si genera error {"error":"mesaje"}

Cambiar estado a un pin, solo funciona con tipo=d (pin digital)

http://localhost:8000/api/?pin=8&accion=1&tipo=d&tablero=1

Devuelve

    {"1":{"8":"False"}}

Leer estado de un pin, cambiando tipo=a (análogo), podremos obtener la lectura de un pin análogo

http://localhost:8000/api/?pin=8&accion=0&tipo=d&tablero=1

Devuelve
    {"1":{"8":"False"}} En caso de ser digital

    {"1":{"0":"0.035"}} En caso de ser análogo

Donde:

pin: numero pin a leer o cambiar estado

acción: 1 = cambia estado a pin 0 = lee estado de pin

tipo: d = digital a = análogo

tablero: número de tablero configurado en db

si tipo = a, acción solo puede ser = 0.


Cambia estado a 0 (apaga) todos los pins digitales de salida sin importar el tablero

http://localhost:8000/api/?estado=0 

Devuelve

    {"1":{"8":"False","9":"False"},"3":{"8":"False", "10":"False"}}

Leer estado todos pins, separandolo por tablero en un diccionario

http://localhsot:8000/api/?estad=1&modo=i&tipo=d

    {"1":{"8":"True","10":"True"}} En caso de pins digitales

    {"1":{"0":"0.0085","1":"0.0434"}} En caso de pins análogos

Donde:

estado: 0 = pone a 0 todos los pines de salida digitales, 1 = lee estado de pines según combinación

modo: i = input o = output

tipo: d = digital a = análogo

si tipo = d, modo solo podrá ser = i
