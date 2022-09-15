import rbt
import pickle


def __init_nonce_rbt__():
    r = rbt.RedBlackTree()
    with open('nonce_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def print_nonce_rbt():

    with open('nonce_rbt_serialized','rb') as f:
        r = pickle.load(f)

    r.pretty_print()

    with open('nonce_rbt_serialized','wb') as f:
        pickle.dump(r,f)

def __insert_nonce_rbt__(nonce):

    with open('nonce_rbt_serialized','rb') as f:
        r = pickle.load(f)

    r.insert(nonce)

    with open('nonce_rbt_serialized','wb') as f:
        pickle.dump(r,f)
