# Import socket module
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

        # Accept incoming connection
        connectionSocket, addr = serverSocket.accept()

        try:
            # Handle messages received, sent by the client
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]

            # Open the client requested file in binary mode
            f = open(filename[1:], "rb")

            # Get the file content
            file_content = f.read()
            f.close()

            # Determine the content type based on the file extension
            content_type = b"text/html; charset=UTF-8"  # Default to HTML

            if filename.endswith(b".jpg"):
                content_type = b"image/jpeg"
            elif filename.endswith(b".png"):
                content_type = b"image/png"

            # Headers for a valid HTTP response
            response_headers = [
                b"HTTP/1.1 200 OK\r\n",
                b"Server: SimpleWebServer\r\n",
                b"Content-Type: " + content_type + b"\r\n",
                b"Content-Length: " + bytes(len(file_content)) + b"\r\n",
                b"Connection: close\r\n",
                b"\r\n"
            ]

            # Send the response headers
            for header in response_headers:
                connectionSocket.send(header)

            # Send the content of the requested file to the client
            connectionSocket.send(file_content)

            # Close the connection socket
            connectionSocket.close()

        except FileNotFoundError:
            # Handle file not found errors with a 404 response
            error_response = (
                b"HTTP/1.1 404 Not Found\r\n"
                b"Content-Type: text/html; charset=UTF-8\r\n"
                b"Server: SimpleWebServer\r\n"
                b"Connection: close\r\n"
                b"\r\n"
                b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
            )
            connectionSocket.send(error_response)
            connectionSocket.close()
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)
