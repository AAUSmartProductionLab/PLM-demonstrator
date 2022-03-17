import os
from festo_opcua import simpleConnect

IP = '172.20.1.1'

def main():
    dickhead = simpleConnect()
    PNo = dickhead.getProdID(IP)
    print(PNo)

if __name__ == "__main__":
    while True:
        try:    
            main() 
        except(KeyboardInterrupt):
            print('interrupted!')
            os._exit()