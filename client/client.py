import socket
import tkinter as tk
from tkinter import filedialog, simpledialog

def authenticate(sock):
    username = username_entry.get()
    password = password_entry.get()
    # Sending username and password to server for authentication
    sock.send(f"{username},{password}".encode())
    response = sock.recv(1024).decode()
    if response == "OK":
        status_label.config(text="Authentication successful!")
        return True
    else:
        status_label.config(text="Authentication failed. Please try again.")
        return False

def send_file():
    filename = filedialog.askopenfilename()
    if filename:
        try:
            with open(filename, "r") as fi:
                data = fi.read()
                sock.sendall(data.encode())
                status_label.config(text="File sent successfully.")
        except Exception as e:
            status_label.config(text=f"An error occurred while sending the file: {e}")

def receive_file():
    filename = simpledialog.askstring("Receive File", "Enter the filename to receive:")
    if filename:
        sock.send(f"receive,{filename}".encode())
        data = sock.recv(1024).decode()
        if data == "FileNotFound":
            status_label.config(text="File not found on the server.")
        else:
            with open(filename, "w") as fo:
                fo.write(data)
            status_label.config(text="File received successfully.")

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Create the GUI window
    root = tk.Tk()
    root.title("File Transfer Client")

    # Username and password entries
    username_label = tk.Label(root, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    # Authentication button
    authenticate_button = tk.Button(root, text="Authenticate", command=lambda: authenticate(sock))
    authenticate_button.pack()

    # Status label
    status_label = tk.Label(root, text="")
    status_label.pack()

    # Send and receive file buttons
    send_button = tk.Button(root, text="Send File", command=send_file)
    send_button.pack()

    receive_button = tk.Button(root, text="Receive File", command=receive_file)
    receive_button.pack()

    # Start the GUI event loop
    root.mainloop()

    # Close the socket connection
    sock.close()