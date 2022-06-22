########################### IMPORTED MODULES AND MESSAGES ###########################################
from socket import AF_INET, socket

from mir import MiR as mir
from festo_opcua import simpleConnect as festo
from dataclasses import dataclass
import sys
import time
import socket

########################## GLOBAL VARIABLES AND CONSTANTS ###########################################
# IP addr for PLCs
PACKING_IP = '172.20.1.1'

# IP-addr/ports for UR
UR_IP = '192.168.12.40' # might need to be changed
UR_PORT = 29999

# Mission IDs for the MIR robot
WAREHOUSE_MISSION = 'warehouse_mission' # mission ID for traveling to the warehouse positions
INIT_MISSION = 'Mir_test' # mission ID for traveling to the initial sorting position

# Position IDs for the MIR robot
SORTING_POSE = 'mir_sorting'

PNo = {'6002':['warehouse_blue', 'blue_sort.urp'], '6000':['warehouse_black', 'black_sort.urp'], '6001':['warehouse_white', 'white_sort.urp'],
       '10':['warehouse_bottom','bottom_sort.urp'], '1212':['warehouse_1fuse', '1fuse_sort.urp'], '1214':['warehouse_2fuse', '2fuse_sort.urp']}

# code references: 6000 - Black Phone, 6001 - Black Phone, White Lid, 6002 - Black Phone, Blue Lid, 10 - Black Bottom, 
# 1212 - Product Fuse Left, 1214 - Product Both Fuses

# trigger used when the robot has to move to the initial position for sorting.
INIT_TRIGGER = True

# The amount of phones required to be sorted before the robot drives off 
ORDER_AMOUNT = 4

########################## CLASSES AND FUNCTION DEFINITIONS #########################################
def connect_UR():
    ur_socket = socket.socket(AF_INET, socket.SOCK_STREAM)
    ur_socket.settimeout(2)
    ur_socket.connect((UR_IP, UR_PORT))

    return ur_socket

def send_cmd(ur_socket, cmd):
    cmd = cmd + '\n'
    ur_socket.sendall(cmd.encode())
    time.sleep(1)
    received = ur_socket.recv(4096)
    print("This is the status of the command sent: ", received)

    return received

def sorting_pos(mir_cls):
    #init_mission_id = mir_cls.create_mission(INIT_MISSION)
    init_mission_id = mir_cls.get_mission_guid(INIT_MISSION)
    #result, position_id = mir_cls.create_action(init_mission_id, SORTING_POSE, action_type='move')
    response = mir_cls.set_mission(init_mission_id)
    mir_cls.put_state_to_execute()
    #print(mir_cls.get_mission_done_or_not(init_mission_id))

    while mir_cls.get_mission_latest_mission_status() == False: # if the postion is reached break the loop
        print("moving into position!")
        time.sleep(1)

    print("The init mission is done! Sorting will start shortly!")

def drive_to_destinations(mir_cls, list_pos):
    for pos in list_pos:
        mission_id = mir_cls.get_mission_guid(pos) # Grab the correct mission ID for the 
        response = mir_cls.set_mission(mission_id) # Add the mission to the queue
        mir_cls.put_state_to_execute() # Start the robot
        while mir_cls.get_mission_latest_mission_status() == False: # Check if the robot is still running
            print("Moving to location: ", pos)
        print("Finished moving to {0}. Moving to next location shortly!".format(pos))
    print("The Enabled Robotics platform has visited all the warehouses in the queue.")
####################################### MAIN LOOP ###################################################
def main():
    festo_cls = festo()
    mir_cls = mir()
    ur_socket = connect_UR()

    INIT_TRIGGER = True
    i = 0
    list_pos = []
    while i < ORDER_AMOUNT:
        if festo_cls.checkPallet(PACKING_IP) == True: 
            i  = i + 1
            if INIT_TRIGGER == True:
                INIT_TRIGGER = False
                sorting_pos(mir_cls)

            check_prod_no = festo_cls.getProdID(PACKING_IP)
            while check_prod_no == '0':
                print("waiting for next product")
                check_prod_no = festo_cls.getProdID(PACKING_IP)

            current_PNo_urp = PNo[str(festo_cls.getProdID(PACKING_IP))][1] # grab the .urp file that corresponds to the product number
            current_PNo_pos = PNo[str(festo_cls.getProdID(PACKING_IP))][0] # grab the location that corresponds ot the product number
            send_cmd(ur_socket, 'load ' + current_PNo_urp)
            #send_cmd(ur_socket, 'close popup')
            send_cmd(ur_socket, 'play')
            response = send_cmd(ur_socket, 'programState')
            response = response.decode('UTF-8').replace('\n', '')

            while response == 'PLAYING ' + current_PNo_urp:
                temp = send_cmd(ur_socket, 'programState')
                response = temp.decode('UTF-8').replace('\n', '')
                print("{0} is running!".format(current_PNo_urp))
            print("{0} finsihed!".format(current_PNo_urp))

            festo_cls.clearJob(PACKING_IP)
            time.sleep(3)
            list_pos.append(current_PNo_pos)

    unique_dest = list(set(list_pos)) # convert to a set of unique destinations and then convert that back to a list
    print("This is the unique list/set: ", unique_dest)
    drive_to_destinations(mir_cls, list_pos)
    print("Program has finsihed as planned!")

if __name__ == "__main__":
    try:    
       main()

    except(KeyboardInterrupt):
        print('interrupted!')
        sys.exit()
