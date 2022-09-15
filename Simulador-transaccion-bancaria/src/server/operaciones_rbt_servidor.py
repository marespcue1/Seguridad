import rbt
import pickle


def __init_nonce_rbt__():
    r = rbt.RedBlackTree()
    with open('nonce_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def print_nonce_rbt():

    with open('nonce_rbt_serialized','rb') as f:
        r = pickle.load(f)
#r.insert(("03fd204c60187be59418846be8f4d0e93c6b49fc6e8390fe12910e5407672de1","12345675432"))

    r.pretty_print()

    with open('nonce_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def __insert_nonce_rbt__(nonce,cliente):

    with open('nonce_rbt_serialized','rb') as f:
        r = pickle.load(f)

    r.insert((nonce,cliente))

    with open('nonce_rbt_serialized','wb') as f:
        pickle.dump(r,f)




def __init_passwd_rbt__():
    r = rbt.RedBlackTree()
    with open('passwd_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def print_passwd_rbt():

    with open('passwd_rbt_serialized','rb') as f:
        r = pickle.load(f)
#r.insert(("03fd204c60187be59418846be8f4d0e93c6b49fc6e8390fe12910e5407672de1","12345675432"))

    r.pretty_print()

    with open('passwd_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def __insert_passwd_rbt__(nonce,cliente):

    with open('passwd_rbt_serialized','rb') as f:
        r = pickle.load(f)

    r.insert((nonce,cliente))

    with open('passwd_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def deserialize_passwd_rbt():
    with open('passwd_rbt_serialized','rb') as f:
        rbt = pickle.load(f)
    return rbt

def serialize_passwd_rbt(r):
    with open('passwd_rbt_serialized','wb') as f:
        pickle.dump(r,f)
