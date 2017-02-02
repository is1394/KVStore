# Single Server Key-Value Store

Proyecto Final de Sistemas Distribuidos, ESPOL 2016-2T

-   [Objetivos](###objetivos:)
-   [Requerimientos](###requerimientos:)
-   [Instrucciones](###instrucciones:)

###Objetivos

Diseñar e implementar un key-value store de un solo nodo capaz de conectarse a uno o más clientes a la vez a un servidor que mantiene un key-value store en memoria.

En este proyecto implementarán un sistema cliente-servidor simple, no persistente (es decir, almacena las claves y los valores únicamente en memoria RAM).

El servidor debe recibir como parámetro el número del puerto en el que estará escuchando, esperando a que los clientes se conecten. De ahí en adelante, el servidor estará levantado, escuchando en el puerto indicado, esperando a que se conecten los clientes.

Para iniciar el programa cliente, se debe proporcionar la IP (o nombre de dominio) y puerto del servidor. Al iniciar, el cliente se conecta al servidor (socket TCP), contactándola en la IP y puerto indicado. El cliente debe leer comandos por teclado (stdin), validarlos, y enviarlos al servidor.

###Requerimientos

*   KeyValue Server debe soportar los siguientes comandos por el cliente:

    *   <tt>**get** key</tt> Retorna el valor asociado a dicha clave.

    *   <tt>**set** key value</tt> Almacena (en memoria) la clave, con el valor asociado. El valor puede contener cualquier caracter, incluso caracteres especiales, tabs y espaciones en blanco.

    *   <tt>**del** key </tt> Elimina la clave, con su valor asociado.

    *   <tt>**list**</tt> Retorna la lista de todas las claves almacenadas.

    *   <tt>**exit**</tt> Termina la conexión con el servidor y posteriormente, termina ejecución del programa cliente.

    *   <tt>**help**</tt> Muestra la lista de los comandos soportados, incluyendo una breve explicación de los mismos.

*   No importa si está ingresado comandos en mayúsculas/minúsculas o una combinación de mayúsculas o minúsculas.

*   El único separador permitido entre el comando y los parámetros.

*   El servidor debe ser multi-hilos (un hilo para cada cliente) y usar un pool de hilos para tener un mejor rendimiento.

*   Cualquier mensaje de error debe mostrarse en pantalla de la siguiente manera: ERROR: Mensaje de error.

*   El servidor debe proteger adecuadamente cualquier recurso compartido, de tal manera que no sea susceptible a condiciones de carrera.

###Instrucciones

Para instalar librerias utilizadas:

    pip install requirements.txt

**KVServer** es el servidor, para inicializar el servidor:

    python KVServer.py PUERTO

Si no se asigna un puerto, el servidor tomara por defecto el puerto 9000.

**KVClient** es una implementacion de cliente, para usarlo:

    python KVClient.py HOST PUERTO

Si no se asigna HOST o PUERTO tomara por defecto 'localhost' y puerto 9000, en caso de especificar estos parametros es necesario que se especifiquen los dos en el orden indicado.

Los comandos soportados por **KVClient** son:

  help: Lista los comandos soportados por el cliente.

    KVClient> help

  ping: Realiza un ping al servidor.

    KVClient> ping

  get: Retorna el valor asociado a una clave. Posee opciones para retornar valor en xml, json o yml.

    KVClient> get key
    KVClient> get key --xml
    KVClient> get key --json
    KVClient> get key --yml

  set: Almacena una clave con su valor asociado.

    KVClient> set key value

  del: Elimina una clave y su valor asociado del servidor.

    KVClient> del key

  list: Lista todas las claves disponibles en el servidor.

    KVClient> list
    KVClient> list --xml
    KVClient> list --json
    KVClient> list --yml

  exit: Termina la conexion con el servidor y finaliza el programa.

    KVClient> exit
