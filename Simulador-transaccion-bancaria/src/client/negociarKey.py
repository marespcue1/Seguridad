from random import randint
import socket
import global_data
import time
import pickle

# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
# https://en.wikipedia.org/wiki/Fermat's_little_theorem

# Client must send p and g and "a" to the server

def client_key_negotiation(daddr, dport, data, code, s = None):
    """"
    daddr = destination ip
    dport = destination port
    data = data to be sent
    code = protocol code
    """

    if s == None:
        s = connect(daddr, dport)

    # If there is data to be sent
    if data != b'':
        # 128 byte of data (int)
        data_no_code = (data).to_bytes(128, byteorder='big')
        data_code = bytearray(data_no_code)
        # Append the code
        data_code.append(code)
        s.send(data_code)
    # If there is NO data to send
    else:
        # Append the code
        data_no_code = (code).to_bytes(1, byteorder='big')
        data_code = bytearray(data_no_code)
        s.send(data_code)

    # Client must wait for the server response
    # Receive data from server
    dataFromServer = s.recv(1024)

    # Last byte is for control
    server_code = dataFromServer[-1]
    # Code 6, server has sent number b
    if server_code == 6:
        print("Ha llegado b, 6")
        # the rest is the number
        b = int.from_bytes(dataFromServer[:-1], byteorder='big')

        # once we have b client must do:
        #key = (b^x mod p)
        key = pow(b,global_data.X,global_data.P)
        print(key)

        with open('serializedKey', 'wb') as f:
            pickle.dump(key,f)

        # Code 7 is FIN ack, send a 7 with no data
        time.sleep(5)
        client_key_negotiation(daddr, dport, b'', 7, s)

    # Code 2 is prime number from server
    elif server_code == 2:
        print("Ha llegdo p, 2")
        global_data.P = int.from_bytes(dataFromServer[:-1], byteorder='big')

        # now ask for the G (generator number), code = 3
        # only 1 byte, no data
        time.sleep(5)
        client_key_negotiation(daddr, dport, b'', 3, s)
        

    # Code 4 is G number from server
    elif server_code == 4:
        print("Ha llegado G, 4")
        global_data.G = int.from_bytes(dataFromServer[:-1], byteorder='big')
        
        global_data.X = randint(1, global_data.P-2)

        # a = g^x mod p
        a = pow(global_data.G,global_data.X,global_data.P)
        
        # sending "a" to the server, code 5
        time.sleep(5)
        client_key_negotiation(daddr, dport, a, 5, s)

    elif server_code == 8:
        print("FIN")
        s.close()
        return

    else:
        print("ERROR")
    return 
    


def connect(daddr,dport):
    s = socket.socket()
    s.connect((daddr,dport))
    print("[+] Connected.")
    return s

client_key_negotiation("127.0.0.1",9090,b'',1)