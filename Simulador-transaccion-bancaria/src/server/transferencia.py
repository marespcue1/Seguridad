import socket
import hashlib
import hmac
import pickle
import secrets
import operaciones_rbt_servidor
import rbt
from datetime import datetime
import pytz
import sys



def connection(s,SERVER_HOST,SERVER_PORT,BUFFER_SIZE,SEPARATOR):
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(60)

def simulacion_de_tratado_de_datos_en_banco():
    print("Haciendo transferencia...")

# Comprobacion de NONCE
def check_nonce(cuenta_origen,nonce):
    with open('nonce_rbt_serialized','rb') as f:
        nonce_rbt = pickle.load(f)
    
    its_ok = nonce_rbt.search_and_validation((nonce,cuenta_origen))

    if its_ok:
        with open('nonce_rbt_serialized','wb') as f:
            pickle.dump(nonce_rbt,f)

    return its_ok


# Comprobacion de MAC
def check_MAC(datos, mac, pre_consulta=False):

    # Obtencion de la clave almacenada
    with open('serializedKey', 'rb') as f:
        key = pickle.load(f)
    key_bytes = (key).to_bytes(128, byteorder='big')
    

    if pre_consulta:
        message = datos
        # el mensaje es desde el primer byte de cuenta_origen hasta el ultimo de nonce
    else:
        message = datos[:91]
    server_mac = hmac.new(key_bytes, message, hashlib.sha256)
    hex_server_mac = server_mac.hexdigest()
    if hex_server_mac != mac:
        print("ERROR: MACs no coinciden, integridad de mensaje comprometida")
        return False
    return True

# Comprobacion de contraseña
def check_passwd(contra, cuenta):
    passwords = operaciones_rbt_servidor.deserialize_passwd_rbt()
    return passwords.search_and_validationForPasswd((cuenta.decode(),contra.decode()))

# Enviar respuesta a un cliente
def enviar_respuesta(mensaje):
    nonce = secrets.token_hex()
    message = str(nonce) + mensaje
        
    with open('serializedKey', 'rb') as f:
        key = pickle.load(f)
        
    key_bytes = (key).to_bytes(128, byteorder = 'big')
    mac = hmac.new(key_bytes, message.encode(), hashlib.sha256)
    hex_mac = mac.hexdigest()
    message = (str(hex_mac)) + message 
    client_socket.send(message.encode())

# Calcular el ratio
def mensajes_integros():

    accum = 0
    total = 0

    with open('logIntegridad','r') as f:
        for line in f.readlines():
            if line != "":
                accum += int(line[0] == "0")
                total+=1

    ratio = accum/total
    print("El ratio de mensajes que llegan con exito integros es: " + str(ratio) + "\n")
    print("De un total de: " + str(total))
    return accum/total

def transferencia():

    print("Esperando cliente")
    print("Accepted a connection request from %s:%s"%(address[0],address[1]))

    data = client_socket.recv(1024)

    contra=data[:64]
    cuenta=data[64:75]
    nonce=data[75:139]
    mac=data[139:]

    if not check_nonce(cuenta.decode(),nonce.decode()):
        # ACTUALIZAR LOG
        with open('logIntegridad','a') as f:
            f.writelines("1-Integridad comprometida, mensaje posiblemente modificado. " +
             str(datetime.now(pytz.utc)) + "\n")
        print("Fallo de nonce")
        return


    if not check_MAC(data[:139],mac.decode(), pre_consulta=True):
        # ACTUALIZAR LOG
        with open('logIntegridad','a') as f:
            f.writelines("1-Integridad comprometida, mensaje posiblemente modificado. " +
             str(datetime.now(pytz.utc)) + "\n")
        print("Fallo de MAC")
        return 

    if check_passwd(contra,cuenta):
        print("Contraseña correcta.")
        client_socket.send("1".encode()) 

    else:
        print("Contraseña incorrecta.")
        client_socket.send("0".encode())
        return  




    data = client_socket.recv(1024)
    
    if len(data) != 155:
        print("Error de formato, los datos tienen un tamaño de " +
         str(len(data)) + " bytes y deberian ser 155 bytes.")

        return
 
    cuenta_origen = (data[:11]).decode()
    cuenta_destino = (data[11:22]).decode()
    cantidad = (data[22:27]).decode()
    nonce = (data[27:91]).decode()
    mac = (data[91:]).decode()

    print("Cuenta origen: " + str(cuenta_origen))
    print("Cuenta destino: " + str(cuenta_destino))
    print("Cantidad: " + str(cantidad))
    print("Nonce: " + str(nonce))
    print("MAC: " + str(mac))



    if not check_nonce(cuenta_origen,nonce):
        # Contestar al cliente que lo intente de nuevo. (Es muy complicado que envie el mismo nonce dos veces 
        # sin querer, si le pasase alguna vez no le volveria a pasar)

        # Formato: MAC  NONCE  Mensaje
        enviar_respuesta("Intentelo de nuevo, operacion no realizada")
        
        # ACTUALIZAR LOG
        with open('logIntegridad','a') as f:
            f.writelines("1-Posible ataque de replay. " + str(datetime.now(pytz.utc)) + "\n")
        return

    if not check_MAC(data, mac):
        # Contestar al cliente que la operación no se ha realizado.
        enviar_respuesta("Integridad comprometida, operacion no realizada")

        # ACTUALIZAR LOG
        with open('logIntegridad','a') as f:
            f.writelines("1-Integridad comprometida, mensaje posiblemente modificado. " +
             str(datetime.now(pytz.utc)) + "\n")

        return
        
    simulacion_de_tratado_de_datos_en_banco()

    enviar_respuesta("Operacion aceptada y procesada.")

    # ACTUALIZAR LOG
    with open('logIntegridad','a') as f:
        f.writelines("0-Operacion exitosa. " + str(datetime.now(pytz.utc)) + "\n")
    return



if len(sys.argv) == 3:
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = sys.argv[2]
else:
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 9090
BUFFER_SIZE = 4096 # receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"
s = socket.socket()
connection(s,SERVER_HOST,SERVER_PORT,BUFFER_SIZE,SEPARATOR)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] {address} is connected.")

transferencia()

# Ratio de mensajes integros
mensajes_integros()