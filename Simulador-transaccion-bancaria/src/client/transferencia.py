import socket
import secrets
import hashlib
import hmac
import pickle
from getpass import getpass
import sys

def check_nonce(nonce):
    # database query para el nonce, si está en la base de datos return True, si no está return False,
    # si está pero no con el cliente actual, insertar nonce al cliente actual
    
    # solucion temporal con rbt:
    with open('nonce_rbt_serialized','rb') as f:
        nonce_rbt = pickle.load(f)
    
    its_ok = nonce_rbt.search_and_validation(nonce.decode())

    if its_ok:
        with open('nonce_rbt_serialized','wb') as f:
            pickle.dump(nonce_rbt,f)

    return its_ok


def check_MAC(datos, mac):

    with open('serializedKey', 'rb') as f:
        key = pickle.load(f)
    key_bytes = (key).to_bytes(128, byteorder='big')
    
    server_mac = hmac.new(key_bytes, datos, hashlib.sha256)
    hex_server_mac = server_mac.hexdigest()
    if hex_server_mac != mac.decode():
        print("ERROR: MACs no coinciden, integridad de mensaje comprometida")
        return False
    return True


def transferencia(daddr,dport, cuenta_origen, cuenta_destino, cantidad):

    s = socket.socket()
    s.connect((daddr,dport))

    while(True):
        contra= getpass("Introduce la contraseña: ")
        if contra == None:
            print("invalid password!")
        else:
            break
    
    
    message = hashlib.sha256()
    message.update(contra.encode())

    hex_message = message.hexdigest()

    nonce = secrets.token_hex()
    message = str(hex_message) + str(cuenta_origen) + str(nonce)

    # Get key
    with open('serializedKey', 'rb') as f:
        key = pickle.load(f)

    # HMAC-SHA256
    key_bytes = (key).to_bytes(128, byteorder='big')
    mac = hmac.new(key_bytes, message.encode(), hashlib.sha256)
    hex_max = mac.hexdigest()
    message = message + str(hex_max)

    # Hash_contra, Cuenta_origen, nonce, MAC

    s.send(message.encode())

    respo=s.recv(1)
    respo=respo.decode()
    if respo=='1':
        print("[+] Connected.")
    else:
        print("Connection error")

    # Suponemos que las cuentas del banco tienen el siguiente formato "xxxx xxx xxxx", pero supondremos
    # que el sistema almacena los numeros bancarios como "xxxxxxxxxxx" y para enviar los datos, se envia
    # la cadena "xxxxxxxxxxx,yyyyyyyyyyy,zzzz,nonce,MAC", donde el primer numero es la cuenta origen, el segundo es la
    # cuenta destino y el tercero es la cantidad enviada, no se permite enviar más de 99999 unidades monetarias
    # a la vez por seguridad, por ultimo se envia el nonce y el MAC.

    # cada numero de cuenta bancaria ocupa 11 bytes, la cantidad debe ocupar 5 bytes, el nonce ocupa 64 bytes,
    # y por último el MAC ocupa 64, por tanto la cadena
    # final ocupa 155 bytes y se obtendran los datos directamente de la cadena de bytes:

    # cuenta_oruigen= datos[:11]
    # cuenta_destino= datos[11:22]
    # cantidad = datos[22:27]
    # nonce = datos[28:91]
    # MAC = datos[91:]

    message = ""
    message = message + str(cuenta_origen) + str(cuenta_destino)

    cantidad = str(cantidad)
    # Añadiendo padding en caso de ser necesario
    while len(cantidad) < 5:
        cantidad = "0" + cantidad
    message = message + cantidad
    nonce = secrets.token_hex()
    message = message + str(nonce)
    # Get key
    with open('serializedKey', 'rb') as f:
        key = pickle.load(f)

    # HMAC-SHA256
    key_bytes = (key).to_bytes(128, byteorder='big')
    mac = hmac.new(key_bytes, message.encode(), hashlib.sha256)
    hex_max = mac.hexdigest()

    ## Simulando Man in the middle:
    #message = "" + str(12345678902) + str(cuenta_destino) + cantidad + str(nonce)

    message = message + str(hex_max) 

    # Simulando Replay:
    message = "" + str(12345678901) + str(94825731249) + "00220" + "7f979fdfb1a998ecf38d79e75f7be8ae35d7a6daf876c27898f105427e581abf" + "e46d721578107fe5eaa72109c589831276b06a2a9abc3fc49a9423040f635c39"

    s.send(message.encode())

    #s.send((54239425742).to_bytes(5,byteorder='big'))
    #s.send(("99999999999,11111111111,200").to_bytes(5,byteorder='big'))

    # Respuesta del servidor
    respuesta = s.recv(1024)
    if len(respuesta) < 128:
        print("Error de comunicación con el servidor. (tamaño de mensaje inapropiado)")
        return
    
    print("Respuesta del servidor obtenida.")
    server_mac = respuesta[:64]
    server_nonce = respuesta[64:128]
    server_message = respuesta[128:]
    print("MAC llegada del servidor: " + str(server_mac.decode()))
    print("nonce llegado del servidor: " + str(server_nonce.decode()))
    print("Mensaje llegado del servidor: " + str(server_message.decode()))

    if not check_nonce(server_nonce):
        print("El mensaje del servidor no es seguro y probablemente se trate de un atacante.")
        # ACTUALIZAR LOG

        return

    if not check_MAC(respuesta[64:],server_mac):
        print("Integridad del mensaje del servidor comprometida.")
        # ACTUALIZAR LOG

        return

    print("Operacion terminada con exito.")
    # ACTUALIZAR LOG

    s.close()
    

# Cuentas que existen:              Contraseña:

# 12345678901                       123456
# 12345678902                       123456
# 12345678903                       123456
# 12345678904                       123456

if len(sys.argv) == 4:
    cuenta_or = sys.argv[1]
    cuenta_dest = sys.argv[2]
    cantidad = sys.argv[3]
if len(sys.argv) == 6:
    ip_dest = sys.argv[4]
    port = sys.argv[5]
else:
    ip_dest = "127.0.0.1"
    port = 9090
    cuenta_or = 12345678901
    cuenta_dest = 94825731249
    cantidad = 220

transferencia(ip_dest,port, cuenta_or, cuenta_dest, cantidad )