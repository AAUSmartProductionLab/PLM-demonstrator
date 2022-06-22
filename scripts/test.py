import socket
import time

# IP-addr/ports for UR
UR_IP = '192.168.0.102'
UR_PORT = 30001

def connect_UR():
    ur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ur_socket.settimeout(2)
    ur_socket.connect((UR_IP, UR_PORT))

    return ur_socket

def send_cmd(ur_socket, cmd):    
    cmd = cmd + '\n'
    received=ur_socket.send(cmd.encode())
    received = ur_socket.recvfrom(4096)

    return received

def main():
    ur_socket = connect_UR()
    result = send_cmd(ur_socket, "set_tool_digital_out(0, True)")
    time.sleep(1)

if __name__ == "__main__":
    main()