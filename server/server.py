import socket

def authenticate(conn):
    # Expected username and password
    expected_username = "username"
    expected_password = "password"

    # Receiving username and password from client
    credentials = conn.recv(1024).decode().split(',')
    username = credentials[0]
    password = credentials[1]

    # Authenticating
    if username == expected_username and password == expected_password:
        conn.send("OK".encode())
        return True
    else:
        conn.send("ERROR".encode())
        return False

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    totalclient = int(input('Enter number of clients: '))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(totalclient)

    connections = []
    print('Initiating clients')
    for i in range(totalclient):
        conn, addr = sock.accept()
        connections.append(conn)
        print('Connected with client', i+1)

        # Perform authentication
        authenticated = False
        while not authenticated:
            authenticated = authenticate(conn)

    for conn in connections:
        while True:
            data = conn.recv(1024).decode()

            if not data:
                continue

            if data.lower() == "quit":
                break
            elif data.startswith("receive,"):
                filename = data.split(',')[1]
                try:
                    with open(filename, "r") as fi:
                        file_data = fi.read()
                        conn.sendall(file_data.encode())
                        print("File sent successfully.")
                except FileNotFoundError:
                    conn.send("FileNotFound".encode())
                    print("File not found on the server.")
                except Exception as e:
                    print('An error occurred while sending the file:', e)
            else:
                filename = 'output.txt'
                with open(filename, "w") as fo:
                    
                    fo.write(data)
                print('File received successfully! New filename is:', filename)

    for conn in connections:
        conn.close()
