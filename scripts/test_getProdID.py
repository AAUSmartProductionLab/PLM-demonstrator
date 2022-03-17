import os
from festo_opcua import getProdID

IP = '172.20.1.1'

def main():
    PNo = getProdID(IP)
    print(PNo)

if __name__ == "__main__":
    try:    
       main()

    except(KeyboardInterrupt):
        print('interrupted!')
        os.exit()


