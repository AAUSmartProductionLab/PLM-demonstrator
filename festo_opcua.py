import time
from threading import Thread, Event
from opcua import ua, Client
import socket
import argparse
import sys

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(
    description='BioX Demonstrator'
)
parser.add_argument("-i", "--festo_connect_ip", help="ip address for festo connect", type=str)
parser.add_argument("-p", "--port", help="Port used for OPCUA connection (Standard port: 4840)", type=int)
args = parser.parse_args()

class simpleConnect():
    def __init__(self):
        pass
            
    def startConveyor(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        Conveyor = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.convConveyor.xRight')
        Conveyor.set_value(ua.Variant(True, ua.VariantType.Boolean))
        simpleConnect.disconnect(self)

    def startConveyor(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        Conveyor = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.convConveyor.xRight')
        Conveyor.set_value(ua.Variant(True, ua.VariantType.Boolean))
        simpleConnect.disconnect(self)

    def stopConveyor(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        Conveyor = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.convConveyor.xRight')
        Conveyor.set_value(ua.Variant(False, ua.VariantType.Boolean))
        simpleConnect.disconnect(self)

    def releaseStopper(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        check = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xCarrierAvailable').get_value()
        if check is True:
            stopper = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xReleaseStopper')
            stopper.set_value(ua.Variant(True, ua.VariantType.Boolean))
        simpleConnect.disconnect(self)

    def engageStopper(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        stopper = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xReleaseStopper')
        stopper.set_value(ua.Variant(False, ua.VariantType.Boolean))
        simpleConnect.disconnect(self)

    def getCarrierID(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        read = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stManualControl.xReadRfid')
        read.set_value(ua.Variant(True, ua.VariantType.Boolean))
        time.sleep(0.1)
        read.set_value(ua.Variant(False, ua.VariantType.Boolean))
        id = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stRfidVisu.uiCarrierID').get_value()
        simpleConnect.disconnect(self)
        return id
        # ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stRfidData.uiCarrierID
        
    def writeCarrierID(self, ip, num_id, port=4840):
        simpleConnect.connect(self, ip, port)
        id = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stRfidVisu.uiCarrierID')
        id.set_value(ua.Variant(num_id, ua.VariantType.UInt16))
        write = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.stManualControl.xWriteRfid')
        write.set_value(ua.Variant(True, ua.VariantType.Boolean))

    def checkPallet(self, ip, port=4840):
        simpleConnect.connect(self, ip, port)
        check = self.client.get_node('ns=2;s=|var|CECC-LK.Application.FBs.stpStopper1.stpStopper.cpfssStopper.xCarrierAvailable').get_value()
        simpleConnect.disconnect(self)
        return check

    def connect(self, festo_ip, ua_port):
        self.client = Client("opc.tcp://{}:{}".format(festo_ip, ua_port))
        self.client.connect()
        logger.info("Client has connected!")

    def disconnect(self):
        self.client.disconnect()
        logger.info("Client has been disconnected!")

if __name__ == "__main__":
    simpleConnect(args.festo_connect_ip)
