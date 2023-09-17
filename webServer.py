# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("127.0.0.1", port))

    # Start listening on port
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print("Ready to serve...")

        # accept incoming connection
        connectionSocket, addr = serverSocket.accept()

        try:
            # handle messages received, sent by client
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]

            # opens the client requested file in binary mode
            f = open(filename[1:], "rb")

            # Headers for validating http request
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: text/html; charset=UTF-8\r\n")
            connectionSocket.send(b"Server: SimpleWebServer\r\n")
            connectionSocket.send(b"Connection: close\r\n")
            # send blank line to end headers
            connectionSocket.send(b"\r\n")

            # Send the content of the requested file to the client
            for i in f:
                connectionSocket.send(i)
            f.close()

            # closing the connection socket
            connectionSocket.close()

        except FileNotFoundError:
            # Handle file not found errors
            connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n")
            connectionSocket.send(b"Content-Type: text/html; charset=UTF-8\r\n")
            connectionSocket.send(b"Server: SimpleWebServer\r\n")
            connectionSocket.send(b"Connection: close\r\n")
            connectionSocket.send(b"\r\n")
            connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
            connectionSocket.close()
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            connectionSocket.close()

    # Commenting out the below, as it's technically not required and some students have moved it erroneously in the While loop. DO NOT DO THAT OR YOU'RE GONNA HAVE A BAD TIME.
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
