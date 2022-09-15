import operaciones_rbt_servidor
import hashlib


# INICIALIZAR ARBOL NONCE
operaciones_rbt_servidor.__init_nonce_rbt__()

# Arbol de nonce debe ser inicializado
operaciones_rbt_servidor.__insert_nonce_rbt__("0","0")

operaciones_rbt_servidor.print_nonce_rbt()

print("")

# INICIALIZAR ARBOL CONTRASEÑAS
operaciones_rbt_servidor.__init_passwd_rbt__()
variab = 12345678901
for i in range(4):
    h = hashlib.sha256()
    h.update("123456".encode())
    hex = h.hexdigest()
    operaciones_rbt_servidor.__insert_passwd_rbt__((str(variab)),str(hex))
    variab += 1

operaciones_rbt_servidor.print_passwd_rbt()

passwords = operaciones_rbt_servidor.deserialize_passwd_rbt()
h = hashlib.sha256()
h.update("123456".encode())
hex = h.hexdigest()
print("Test buscando un cliente \"123245678901\" que no existe con contraseña \"123456\":")
print(passwords.search_and_validationForPasswd(("123245678901",hex)))

h = hashlib.sha256()
h.update("1234568".encode())
hex = h.hexdigest()
print("Test buscando un cliente \"12345678901\" que si existe con contraseña incorrecta \"1234568\":")
print(passwords.search_and_validationForPasswd(("12345678901",hex)))

h = hashlib.sha256()
h.update("123456".encode())
hex = h.hexdigest()
print("Test buscando un cliente \"12345678901\" que si existe con contraseña correcta \"123456\":")
print(passwords.search_and_validationForPasswd(("12345678901",hex)))


# INICIALIZAR ARCHIVO DE LOG
with open('logIntegridad','a') as f:
    f.close()
