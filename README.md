# Proyectos seguridad

Pequeños proyectos relacionados con el campo de la seguridad utilizando Python.
La finalidad de estos proyectos ha sido aprender sobre el campo de la seguridad informática
y la programación. 

## BruteForce

Algoritmo de fuerza bruta para obtener la calve que se utiliza durante una comunicación que trata de 
asegurar la integridad de la información mediante un HMAC. Es decir, se envía el par:

    (MENSAJE  ,  HASH(mensaje + clave))

En este algoritmo se utilizan hilos para tratar de reducir el tiempo de ejecución y la complejidad en tiempo.

py brute_force mode passwd/msg hash/hmac hashType [threads] [info]

Modes:
    0 --> msg - hmac
    1 --> passwd - hash  (Not aviable)
hashType:
    'md5'
    'sha1'
    'sha256'
[threads]:
    x --> where x is number of threads
   
   
## HIDS

Un sistema de detección de intrusos. Teniendo dos máquinas, una de ellas (host) con información cuya integridad se
quiere proteger y otra que debe estar lo más aislada posible (con comunicación con el host), se pretende detectar cualquier
alteración de la información almacenada en el host y registrar dicho cambio.

Se utiliza una estructura de datos llamada RedBlackTree el cual es una variante más eficiente de BinarySeachTree. El fin de
esta estructura de datos es almacenar el sistema de archivos del host serializando el RedBlackTree en la segunda máquina.
Periodicamente se realiza una revisión del sistema de archivos comparandolo con el arbol previamente almacenado.

Cada nodo del arbol es del modo:

(Ruta, MAC, Rojo/negro)

## Simulador-transaccion-bancaria

Simula el envío de de información segura entre dos máquinas (cliente/servidor) tratando de evitar ataques del tipo man-in-the-middle.
Para ello se ha programado en python el protocolo Diffie-Hellman (negociarKey.py) para intercambio de claves y la estructura de datos RedBlackTree para
almacenar información.

Para ello se utiliza el siguiente protocolo inventado:

1) Cliente se autentica mediante una contraseña (cuyos carácteres deben estar ocultos
cuando es escrita), acompañando a esta contraseña deben ir los elementos
necesarios para asegurar la integridad del mensaje, es decir, “NONCE” y MAC,
también debe acompañar a esta contraseña la cuenta de origen de la transacción
para identificar al cliente.

La idea de un formato para enviar toda esta información al servidor es unir
todos los datos en una cadena en el siguiente orden:
  1.1) Hash de la contraseña
  1.2) Cuenta origen
  1.3) “NONCE”
  1.4) MAC
  
Para distinguir los distintos elementos de información en la cadena se utiliza el
tamaño fijo de los cuatro elementos, sabiendo que el hash de la contraseña debe ocupar 64
bytes (sha256), la cuenta origen 11 bytes, el “NONCE” 65 bytes,y por último el MAC debe
ocupar también 64 bytes.


2) El servidor responderá al cliente mediante un 1 o un 0 indicando si el “NONCE” o el
MAC están incorrectos, dicho uno va acompañado de un mensaje de tamaño
variable que indica el problema o si no ha habido problema, para distinguir los
campos usamos 1 byte para enviar el 1 o el 0. (Es mucho tamaño para un solo bit pero
se deja en 1 byte por si se añaden modificaciones futuras y más funcionalidades)

3) El cliente envía la transacción requerida siguiendo la misma estrategia con el
formato: (cuenta_origen, cuenta_destino, cantidad) añadiendo al
final el “NONCE” y el MAC. El tamaño de la cuenta_destino es idéntico al de el resto
de cuentas y nos queda por saber el tamaño de “cantidad”, supondremos que como
medida de seguridad el banco no permite realizar transacciones de más de 99999
euros de forma online, por lo que rellenaremos el número de cantidad que se nos
proporcione con 0 a la izquierda hasta que alcance 5 cifras para tener un tamaño fijo
de 5 bytes.

4) El servidor responde al cliente indicando si está todo correcto o ha habido algún
problema durante el proceso, para ello de nuevo se crea un mensaje del mismo tipo
con el formato: MAC ,“NONCE”, mensaje informativo de tamaño variable.
