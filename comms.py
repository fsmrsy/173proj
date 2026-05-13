import socket

class CommandSender:
    def __init__(self, mode="network", pi_ip="ceo67.local", port=5005):
        self.mode = mode
        self.pi_ip = pi_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, cmd):
        if self.mode == "network":
            self.sock.sendto(cmd.encode(), (self.pi_ip, self.port))
            print(f"Sent command to Pi: {cmd}")
        else:
            print(f"Sim mode command: {cmd}")

    def close(self):
        self.sock.close()