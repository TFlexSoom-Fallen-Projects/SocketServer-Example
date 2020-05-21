import socket
import sys

HOST, PORT = "localhost", 8080

def send_new_message(message):
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(str.encode(message))

        # Receive data from the server and shut down
        received = str(sock.recv(1024, socket.MSG_WAITALL), "utf-8")
        print("Received: {}".format(received))
        sock.close()


send_new_message("POSTHelloDere!%")
send_new_message("GET%")
send_new_message("POSTHelloAgain!%")
send_new_message("YOLOLOLOLOLOLOLOLOLOL%")

yolo = "y" * 1
send_new_message(yolo)

input("")