import threading
import itertools
import hashlib
import time
import hmac
import sys

# brute_force mode passwd/msg hash/hmac hashType [threads] [info]
"""
Modes:
    0 --> msg - hmac
    1 --> passwd - hash

hashType:
    'md5'
    'sha1'
    'sha256'

[threads]:
    x --> where x is number of threads

"""

breakProgram = False

len_argv = len(sys.argv)

if len_argv < 4 or len_argv > 7:
    raise 'Invalid length of arguments\nbrute_force mode passwd/msg hash/hmac hashType [threads] [info]'

modes = {'0', '1'}
hashTypes = {'md5':hashlib.md5, 'sha1':hashlib.sha1, 'sha256':hashlib.sha256}

mode = None
pass_msg = None
hash_hmac = None
hashType = None
threads = 1
inf = 2

if sys.argv[1] is not None:
    if sys.argv[1] in modes:
        mode = sys.argv[1]
    else:
        raise 'Mode ' + sys.argv[1] + ' not found.\n\t\'0\' --> msg - hmac\n\t\'1\' --> passwd - hash' 
else:
    raise 'No mode selected\nbrute_force mode passwd/msg hash/hmac hashType [threads] [info]'

if sys.argv[2] is not None:
    pass_msg = sys.argv[2]
else:
    raise 'No password or message\nbrute_force mode passwd/msg hash/hmac hashType [threads] [info]'

if sys.argv[3] is not None:
    hash_hmac = sys.argv[3]
else:
    raise 'No hash or hmac\nbrute_force mode passwd/msg hash/hmac hashType [threads] [info]'
hashlib.sha1
if sys.argv[4] is not None:
    if sys.argv[4] in hashTypes:
        hashType = hashTypes[sys.argv[4]]
    else:
        raise 'Hash type ' + sys.argv[4] + ' not found.\n\nAviable modes:\n\t\md5\n\tsha1\n\tsha256'
else:
    raise 'No hash type\nbrute_force mode passwd/msg hash/hmac hashType [threads] [info]'

if len_argv >=6: 
    if sys.argv[5].isnumeric():
        threads = int(sys.argv[5])
    else:
        raise 'threads must be integer\nbrute_force mode passwd/msg hash/hmac hashType [threads] [info]'

if len_argv >=7: 
    if sys.argv[6].isnumeric():
        inf = sys.argv[6]

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def mac_brute_force(msg, hmac_original, hashType, th, info = 2):
    start_time = time.time()

    def control_thread(n):
        global breakProgram
        while True:
            control = str(input('Type \"exit\" to quit: \n'))
            if control == 'exit': 
                breakProgram = True
                sys.exit()
    
    def mac_brute_force_thread(msg, hmac_original, fourth_value, n, info = 2):
        print('Starting thread ' + str(n))
        i = 0
        global found
        global breakPrograms

        # iterate on each combination of bytes ie: (23,0,165,255)   thats 4 bytes combination
        for fourth in fourth_value:
            for combination in itertools.product(val_posib,repeat=3):
                # Actual key to try
                lista = list((fourth,))+list(combination)
                actual_key = bytes(lista)
                
                hmac_nuevo = hmac.new(actual_key, msg, hashType)
                hexadecimal = hmac_nuevo.hexdigest()
                

                if i == info*1000000:
                    print(str(list(lista)) + "  ---  " + str(hexadecimal) + ' ,thread ' + str(n))
                    i = 0
                i+=1
                
                # if hexadecimal value is the same as the hmac we are done
                if hexadecimal == hmac_original:
                    global return_key
                    return_key = actual_key
                    global return_combination
                    return_combination = lista
                    found = True
                    return
                if found or breakProgram: return
            if found or breakProgram: return

    fourth_value = list(chunks(val_posib,int(len(val_posib)/th)))

    # Create threads
    tc = threading.Thread(target=control_thread, args=(100,))
    tc.start()

    threads = list()
    for n_thread in range(th):
        t = threading.Thread(target=mac_brute_force_thread, args=(msg, hmac_original, fourth_value[n_thread], n_thread+1, info,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    # Note: Create a progress bar 
    """for t in threads:
        t.join()"""
    time.sleep(3)
    print('Some attempts: (may take a while)')
    while not breakProgram and not found:
        time.sleep(1)



    print('Time: ' + str(time.time()-start_time) + 's')

    return return_key, return_combination


if mode == '0':

    # Message of the problem
    msg = pass_msg
    msgEcnoded = msg.encode()
    # Hmac
    hmac_original = hash_hmac
    # Bytes are from 0 to 255, 174.792.640 combinations
    val_posib = list(range(0,256))
    # Number of threads
    th=threads

    found = False
    return_key = None
    return_combination = None

    """tc = threading.Thread(target=control_thread, args=(100,))
    print('a')
    tc.start()
    print('b')
    print('Starting...')
    time.sleep(3)"""

    key, combination = mac_brute_force(msgEcnoded, hmac_original, hashType, th, info=inf)

    if key != None:
        print("Key of the following message: " + msg) 
        print("is in bytes: " + str(list(combination)))
        print("in hexadecimal: " + str(key.hex()))
    else:
        print('Key not found')
    

