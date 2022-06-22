import os
from festo_opcua import simpleConnect

IP = '172.20.1.1'

def main():
    festo_connect = simpleConnect()
    PNo = festo_connect.getProdID(IP)
    print(PNo)

if __name__ == "__main__":
    while True:
        try:    
            main() 
        except(KeyboardInterrupt):
            print('interrupted!')
            os._exit()