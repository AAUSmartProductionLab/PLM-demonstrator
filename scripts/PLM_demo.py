########################### IMPORTED MODULES AND MESSAGES ###########################################
from socket import AF_INET, socket

from mir import MiR as mir
from festo_opcua import simpleConnect as festo
from dataclasses import dataclass
import os
import time
import socket


########################## GLOBAL VARIABLES AND CONSTANTS ###########################################
# IP addr for PLCs
PACKING_IP = '172.20.1.1'

# IP-addr/ports for UR
UR_IP = '172.20.1.5' # might need to be changed
UR_PORT = 29999

# Mission IDs for the MIR robot
WAREHOUSE_MISSION = 'warehouse_mission' # mission ID for traveling to the warehouse positions
INIT_MISSION = 'initial_mission' # mission ID for traveling to the initial sorting position

# Position IDs for the MIR robot
SORTING_POSE = 'sorting_pose'

PNo = {'6001':['warehouse_blue', 'blue_sort.urp'], '6002':['warehouse_black', 'black_sort.urp'], '6003':['warehouse_white', 'white_sort.urp'],
       '6004':['warehouse_bottom','bottom_sort.urp'], '6005':['warehouse_1fuse', '1fuse_sort.urp'], '6006':['warehouse_2fuse', '2fuse_sort.urp']}

# trigger used when the robot has to move to the initial position for sorting.
INIT_TRIGGER = True

########################## CLASSES AND FUNCTION DEFINITIONS #########################################
def connect_UR():
    ur_socket = socket.socket(AF_INET, socket.SOCK_STREAM)
    ur_socket.settimeout(2)
    ur_socket.connect(UR_IP, UR_PORT)

    return ur_socket

def send_cmd(cmd):
    ur_socket = connect_UR()
    cmd = cmd + '\n'
    ur_socket.sendall(cmd.encode())
    time.sleep(5)
    received = ur_socket.recv(4096)
    print("This is the status of the command sent: ", received)
    
    return received
    

####################################### MAIN LOOP ###################################################
def main():
    festo_cls = festo()
    while(True):
        if festo_cls.checkPallet(PACKING_IP) == False: return
        
        if INIT_TRIGGER == True:
            INIT_TRIGGER = False
            init_mission_id = mir.create_mission(INIT_MISSION)
            result, position_id = mir.create_action(init_mission_id, SORTING_POSE, action_type='move')
            mir.put_state_to_execute()
            
            while mir.get_mission_done_or_not(init_mission_id) == False: # if the postion is reached break the loop
                print("moving into position!") 
                    
            print("The init mission is done! Sorting will start shortly!")
        
        current_PNo = PNo[str(festo_cls.get_product_number(PACKING_IP))][1] # MAKE THE OPC-UA COMMAND FOR GETTING THE PRODUCT NUMBER
        send_cmd('load ' + current_PNo)
        send_cmd('play')
        
        response = send_cmd('programState')
        while response == 'PLAYING':
            print("{0} is running!".format(current_PNo))
        print("{0} finsihed!".format(current_PNo))

if __name__ == "__main__":
    try:    
       main()

    except(KeyboardInterrupt):
        print('interrupted!')
        os.exit()
