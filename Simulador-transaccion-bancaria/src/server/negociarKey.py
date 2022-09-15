from random import randrange, getrandbits, randint
import secrets
import primo
import socket
import global_data
import pickle
#import sqlite3
#from sqlite3 import Error

# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
# https://en.wikipedia.org/wiki/Fermat's_little_theorem

# Primo aleatorio grande
print("Calculando primo, un momento")
global_data.P = primo.generate_prime_number()

# Generador aleatorio entre 2 y p-2
print("Calculando generador g")
global_data.G = randint(2, (global_data.P)-2)

print("Calculando y")
global_data.Y = randint(1, (global_data.P)-2)

global_data.ACTUAL_CODE = 0
global_data.CODES = { 1, 3, 5 }

"""def create_database_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn"""


def connection(s,SERVER_HOST,SERVER_PORT,BUFFER_SIZE,SEPARATOR):
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    


def server_key_negotiation(daddr, dport):
    """"
    daddr = destination ip
    dport = destination port?
    data = data to be sent
    code = protocol code
    """

    print("Esperando cliente")
    while(True):
        

        print("Accepted a connection request from %s:%s"%(address[0], address[1]))
        dataFromClient = client_socket.recv(1024)
        

        # Last byte is for control
        server_code = dataFromClient[-1]
        # Code 5, client has sent number a
        if server_code == 5:
            print("Ha llegado a, 5")
            global_data.ACTUAL_CODE = 5
            # the rest is the number
            a = int.from_bytes(dataFromClient[:-1], byteorder='big')

            # once we have "a" client must do:
            #key = (a^y mod p)
            key = pow(a,global_data.Y,global_data.P)
            print(key)

            #ex=(key).to_bytes(128, byteorder='big')

            #database insert
            #query = """INSERT INTO clientes (CLAVE) VALUES (?)"""
            #c = conn.cursor()
            #c.execute(query,[ex])
            #conn.commit()
            #print("algo")

            # We must insert the key to the database here ---------------------------------!!!!!!!!!!!!!!!!!
            with open('serializedKey', 'wb') as f:
                pickle.dump(key,f)


            # a = g^x mod p
            b = pow(global_data.G,global_data.Y,global_data.P)

            # Code 6, server is sending b
            send_response_to_client(client_socket , b, 6)
            

        # Code 1 client ask for P
        elif server_code == 1:
            global_data.ACTUAL_CODE = 1
            print("Cliente pide p, 1")
            # client is asking for P, server send P with code 2
            send_response_to_client(client_socket ,global_data.P, 2)

        # Code 3 client requests G
        elif server_code == 3:
            global_data.ACTUAL_CODE = 3
            print("Cliente pide g, 3")
            # 1 more byte to send the control code
            # sending G, code 4
            send_response_to_client(client_socket ,global_data.G, 4)

        # Client FIN ack
        elif server_code == 7:
            global_data.ACTUAL_CODE = 7
            print("Cliente se despide, 7")
            send_response_to_client(client_socket , b'', 8)
            print("FIN")
            client_socket.close()
            s.close()
            break

        else:
            print("ERROR")
        return
    

def send_response_to_client(client_socket ,data, code):
    # If there is data to be sent
    if data != b'':
        data_no_code = (data).to_bytes(128, byteorder='big')
        data_code = bytearray(data_no_code)
        # Append the code, 1 byte
        data_code.append(code)
        client_socket.send(data_code)
    # If there is NO data to send
    else:
        # Append the code, 1 byte
        data_no_code = (code).to_bytes(1, byteorder='big')
        data_code = bytearray(data_no_code)
        client_socket.send(data_code)


# Database stuff
#database = r"server\database.db"
#conn = create_database_connection(database)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 4096 # receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"
s = socket.socket()
connection(s,SERVER_HOST,SERVER_PORT,BUFFER_SIZE,SEPARATOR)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] {address} is connected.")

server_key_negotiation("127.0.0.1",9090)
# Evita que alguien no use bien el protocolo (no siga la secuencia de codigos)

while global_data.ACTUAL_CODE in global_data.CODES:
    global_data.CODES.remove(global_data.ACTUAL_CODE)
    server_key_negotiation("127.0.0.1",9090)