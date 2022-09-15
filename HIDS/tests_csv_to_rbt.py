import csv
import glob
import socket
import hashlib
import os
import tqdm

from rbt import RedBlackTree
#from rbt import *


def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha256()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

#append data into the csv file
def writing(path):
    with open('tuple.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for data in path:
            writer.writerow([data] + [hash_file(data)])

#clear the csv file or create if does not exist
def csvclear():
    f = open('tuple.csv', 'w+')

#getting all the filenames from the specified path
csvclear()
#path1="/home/kali/SSII/"
path1="/Users/M/Desktop/US/Cuarto"

#first round specified path then iterates into subdirectories
file_paths = [i for i in (os.path.join(path1, f) for f in os.listdir(path1)) if os.path.isfile(i)]
dir_paths = [i for i in (os.path.join(path1, f) for f in os.listdir(path1)) if os.path.isdir(i)]

writing(file_paths)
for directory in dir_paths:
    file_paths=[i for i in (os.path.join(directory, f) for f in os.listdir(directory)) if os.path.isfile(i)]
    writing(file_paths)

# THIS IS NEW -----------------------------------------------------------
# csv is generated with a empty line between each two lines, maybe we should remove those lines
with open('tuple.csv') as fp:
    lines = fp.readlines()

rbt = RedBlackTree()

for line in lines:
    if line != "\n":
        path_hash = line.split(",")
        if len(path_hash)!=2:
            raise Exception("Bad format of csv")
        else:
            rbt.insert((path_hash[0],path_hash[1]))

rbt.pretty_print()



##connection
#HOST = '127.0.0.1'        
#PORT = 22222              
#SEPARATOR = "<SEPARATOR>"
#BUFFER_SIZE = 4096 # send 4096 bytes each time step
#filename = "tuple.csv"
#filesize = os.path.getsize(filename)
#
#s = socket.socket()
#print(f"[+] Connecting to {HOST}:{PORT}")
#s.connect((HOST, PORT))
#print("[+] Connected.")
#s.send(f"{filename}{SEPARATOR}{filesize}".encode('utf-8'))
#progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
#with open(filename, "rb") as f:
#    while True:
#        bytes_read = f.read(BUFFER_SIZE)
#        if not bytes_read:
#            break
#        # we use sendall to assure transimission in 
#        # busy networks
#        s.sendall(bytes_read)
#        progress.update(len(bytes_read))
#s.close()