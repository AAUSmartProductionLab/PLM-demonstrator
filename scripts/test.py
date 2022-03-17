import socket
import time


# IP-addr/ports for UR
UR_IP = '192.168.12.40' # might need to be changed
UR_PORT = 29999

def connect_UR():
    ur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ur_socket.settimeout(2)
    ur_socket.connect((UR_IP, UR_PORT))

    return ur_socket

def send_cmd(cmd):
    ur_socket = connect_UR()
    cmd = cmd + '\n'
    received=ur_socket.send(cmd.encode())
    #received = ur_socket.recv(1024)
    
    
    return received

def main():
    while(True):
        result = send_cmd('isProgramSaved')
        print(result)
        time.sleep(1)

if __name__ == "__main__":
    main()