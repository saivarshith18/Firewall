import socket
import threading

class SimpleFirewall:
    def __init__(self):
        self.allowed_ips = set()

    def add_allowed_ip(self, ip):
        self.allowed_ips.add(ip)

    def start_firewall(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Firewall listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, client_socket, client_address):
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request from {client_address}: {request}")

        # Extract the client's IP address from the request (this is a simple example)
        client_ip = request.split(' ')[1]

        if client_ip in self.allowed_ips:
            response = "HTTP/1.1 200 OK\n\nConnection established."
        else:
            response = "HTTP/1.1 403 Forbidden\n\nAccess denied."

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    firewall = SimpleFirewall()

    # Add allowed IP addresses
    firewall.add_allowed_ip("127.0.0.1")  # Example: Add localhost as an allowed IP

    # Start the firewall on a specific host and port
    firewall.start_firewall("127.0.0.1", 8888)
