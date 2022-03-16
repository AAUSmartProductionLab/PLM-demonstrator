import mir
import time
import rospy
from std_msgs.msg import Int32, String
import numpy as np
import sys

def init_mission(cls_mir, mission_name, position_name):
    mission_id = cls_mir.create_mission(mission_name)
    cls_mir.post_position(position_name) # post position at the current location of the robot
    result, position_id = cls_mir.create_action(mission_id, position_name, action_type='move')

    return mission_id, position_id

def ori_mission(cls_mir, angle, mission_name, position_name):
    # Find the ids for the mission and used position
    mission_id = cls_mir.get_mission_guid(mission_name)
    position_id = cls_mir.get_position_guid(position_name)
    # Get the current position (postion_id could also be used)
    current_pos = cls_mir.get_current_position()
    x = cls_mir.get_specific_position(position_id)['pos_x']
    y = cls_mir.get_specific_position(position_id)['pos_y']
    # Modify the function position with the new incoming angle
    response = cls_mir.set_position(position_id, x, y, angle)

    return mission_id

def get_angle(default=0):
    position = cls_mir.get_current_position()
    if position is not None:
        return position[2]
    else:

        return default

def get_dist(angle):
    got_position = False
    current_angle = get_angle(default=None)
    if current_angle is not None:
        got_position = True
        phi = abs(angle - current_angle) % 360
        dist = 360 - phi if phi > 180 else phi
        return dist
    else:

        return 0

def remap(angle):
    print('This is the angle: ', angle)
    if angle < -180:
        angle = angle + 360
    elif angle > 180:
        angle = angle - 360

    return angle

if __name__=='__main__':
    try:
        cls_mir = mir.MiR()
        mission_name = 'Orientation_test'
        position_name = 'Demo_Office'

        if sys.argv[1] == 'init':
            print('Running the initialization...')
            response = cls_mir.delete_mission(mission_name) # Delete old mission to avoid multiple missions with the same name.
            print('Delete mission response from the robot: ', response)
            response = cls_mir.delete_position(position_name) # Delete old mission to avoid multiple missions with the same name.
            print('Delete position response from the robot: ', response)
            mission_id, position_id = init_mission(cls_mir, mission_name, position_name)

        elif sys.argv[1] == 'run':
            print('Running the main script...')
            cls_mir.put_state_to_execute()
            rospy.init_node('rest_api_node')
            pub = rospy.Publisher('/mir_status', String, queue_size=1)

            while not rospy.is_shutdown():
                pub.publish('done')
                angle_data = rospy.wait_for_message('/mir_direction', Int32)
                print('This is the incoming angle: ', angle_data.data)
                current_angle = get_angle(default = None)
                if current_angle is not None:
                    angle = remap(-1*angle_data.data + current_angle)
                    mission_id = ori_mission(cls_mir, angle, mission_name, position_name)
                    response = cls_mir.post_to_mission_queue(mission_id)
                    pub.publish('moving')
                    tries = 0
                    while get_dist(angle) > 2 and tries < 10:
                        tries+=1
                        rospy.sleep(0.3)

                    print('goal reached')
                    pub.publish('done')
    except:
        print('Please input either "init" or "run"!')
