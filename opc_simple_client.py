import sys
import time
import firebase_admin
from firebase_admin import db
import json
sys.path.insert(0, "..")
from opcua import Client, ua
from festo_opcua import simpleConnect

festo_connection = simpleConnect()

cred_obj = firebase_admin.credentials.Certificate('../biox_key.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://biox-46f4c-default-rtdb.europe-west1.firebasedatabase.app/'
	})


ref = db.reference('/project')

try:
    while(True):

        message = ref.get()
        plc_ids = ['STPLC_08', 'STPLC_09'] #Names of the PLCs
        ips = ['172.20.1.1', '172.20.13.1'] #IP addresses for each PLC
        PLC_ref = ref.child('PLC')

        for plc_id, ip in zip(plc_ids, ips): # Iterate through the two lists at the same time 

            STPLC_id = PLC_ref.child(plc_id)
            STPLC_id.update({'CheckCarrier': festo_connection.checkPallet(ip)})
            
            if STPLC_id.get()['CheckCarrier'] == True:
                STPLC_id.update({'CarrierID': festo_connection.getCarrierID(ip)})
                print('This is the carrierID for {}@{}: '.format(plc_id, ip), festo_connection.getCarrierID(ip))
                #festo_connection.releaseStopper(ip)
                #time.sleep(0.2)
                #festo_connection.engageStopper(ip)

            #elif STPLC_id.get()['CheckCarrier'] == False:
            #    festo_connection.engageStopper(ip)

            if STPLC_id.get()['StartConveyor'] == True:
                festo_connection.startConveyor(ip)

            elif STPLC_id.get()['StartConveyor'] == False:
                festo_connection.stopConveyor(ip)

            if STPLC_id.get()['ReleaseStopper'] == True:
                festo_connection.releaseStopper(ip)
                time.sleep(0.2)
                festo_connection.engageStopper(ip)
                STPLC_id.update({'ReleaseStopper': False})
            #elif STPLC_id.get()['ReleaseStopper'] == False:
            #    festo_connection.engageStopper(ip)
        
except KeyboardInterrupt:
        print('interrupted!')


'''

# Starting sequence. Make sure stoppers are up and conveyors are running.
festo_connection.engageStopper(ip)
festo_connection.engageStopper(ip2)
festo_connection.startConveyor(ip)
festo_connection.startConveyor(ip2)

check = festo_connection.checkPallet(ip)
check2 = festo_connection.checkPallet(ip2)

while 1:
    if check is True:
        print(festo_connection.getCarrierID(ip))
        festo_connection.releaseStopper(ip)
        time.sleep(1)
        festo_connection.engageStopper(ip)

    if check2 is True:
        print(festo_connection.getCarrierID(ip2))
        festo_connection.releaseStopper(ip2)
        time.sleep(1)
        festo_connection.engageStopper(ip2)
    check = festo_connection.checkPallet(ip)
    check2 = festo_connection.checkPallet(ip2)
    time.sleep(1)


festo_connection.stopConveyor(ip)


try:
    while True:
        if check is True:
            id1 = festo_connection.getCarrierID(ip)
            print('ID on packing unit: ', id1)
        if check2 is True:
            id2 = festo_connection.getCarrierID(ip2)
            print('ID on manual workstation: ', id2)
        check = festo_connection.checkPallet(ip)
        check2 = festo_connection.checkPallet(ip2)
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')
'''

