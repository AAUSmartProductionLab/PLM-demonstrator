import time
from threading import Thread, Event
from turtle import fd
from opcua import ua, Client
import socket
import argparse
import sys
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class simpleConnect():
    def __init__(self):
        pass
            
    def startConveyor(self, ip, port=4840):
        self.connect(ip, port)
        Conveyor = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.convConveyor.xRight')
        Conveyor.set_value(ua.Variant(True, ua.VariantType.Boolean))
        self.disconnect()

    def startConveyor(self, ip, port=4840):
        self.connect(ip, port)
        Conveyor = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.convConveyor.xRight')
        Conveyor.set_value(ua.Variant(True, ua.VariantType.Boolean))
        self.disconnect()

    def stopConveyor(self, ip, port=4840):
        self.connect(ip, port)
        Conveyor = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.convConveyor.xRight')
        Conveyor.set_value(ua.Variant(False, ua.VariantType.Boolean))
        self.disconnect()

    def releaseStopper(self, ip, port=4840):
        self.connect(ip, port)
        check = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xCarrierAvailable').get_value()
        if check is True:
            stopper = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xReleaseStopper')
            stopper.set_value(ua.Variant(True, ua.VariantType.Boolean))
        self.disconnect()

    def engageStopper(self, ip, port=4840):
        self.connect(ip, port)
        stopper = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xReleaseStopper')
        stopper.set_value(ua.Variant(False, ua.VariantType.Boolean))
        self.disconnect()

    def getCarrierID(self, ip, port=4840):
        self.connect(ip, port)
        read = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stManualControl.xReadRfid')
        read.set_value(ua.Variant(True, ua.VariantType.Boolean))
        time.sleep(0.1)
        read.set_value(ua.Variant(False, ua.VariantType.Boolean))
        id = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stRfidVisu.uiCarrierID').get_value()
        self.disconnect()
        return id
        # ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stRfidData.uiCarrierID
        
    def writeCarrierID(self, ip, num_id, port=4840):
        self.connect(ip, port)
        id = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stRfidVisu.uiCarrierID')
        id.set_value(ua.Variant(num_id, ua.VariantType.UInt16))
        write = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stManualControl.xWriteRfid')
        write.set_value(ua.Variant(True, ua.VariantType.Boolean))

    def checkPallet(self, ip, port=4840):
        self.connect(ip, port)
        check = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xCarrierAvailable').get_value()
        self.disconnect()
        return check

    def connect(self, festo_ip, ua_port):
        self.client = Client("opc.tcp://{}:{}".format(festo_ip, ua_port))
        self.client.connect()
        logger.info("Client has connected!")

    def disconnect(self):
        self.client.disconnect()
        logger.info("Client has been disconnected!")
        
    def getProdID(self, ip, port=4840):
        self.connect(ip, port)
        id = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stRfidData.stMesData.udiPNo').get_value()
        self.disconnect()
        return id

    def startJob(self, ip, state, port=4840):
        self.connect(ip, port)
        write = self.client.get_node('ns=2;s=|var|CECC-LK.Application.fromCDPX.stManualWorkplace.xManualJobStarted')
        write.set_value(ua.Variant(state, ua.VariantType.Boolean))
        self.disconnect()

    def finishJob(self, ip, state, port=4840):
        self.connect(ip, port)
        write = self.client.get_node('ns=2;s=|var|CECC-LK.Application.fromCDPX.stManualWorkplace.xManualJobFinished')
        write.set_value(ua.Variant(state, ua.VariantType.Boolean))
        self.disconnect

    def clearJob(self, ip):
        self.startJob(ip, True)
        time.sleep(0.5)
        self.startJob(ip, False)
        self.finishJob(ip, True)
        time.sleep(0.5)
        self.finishJob(ip, False)


def main():
    test = simpleConnect()
    test.clearJob(ip ='172.20.1.1')
    sys.exit()
    
    print('test')

if __name__ == "__main__":

    try:
        main()
        sys.exit()
    except(KeyboardInterrupt):
        sys.exit()
    #simpleConnect(args.festo_connect_ip)
    #print("Do not run from the module!")

    

        