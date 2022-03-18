from mir import MiR

INIT_MISSION = "test"

PARKING_POSE = 'Mir_parking'

def main():
    mir_cls = MiR()
    mission_name = 'mir_sorting'
    #new_mission_id = mir_cls.create_mission('mir_sorting')
    mission_id = mir_cls.get_mission_guid(mission_name)
    #result, position_id = mir_cls.create_action(mission_id, PARKING_POSE, action_type='move')
    mir_cls.create_action(mission_id, position_name='Left_Charger')
    response = mir_cls.set_mission(mission_id)
    mir_cls.put_state_to_execute()
    print(response)

if __name__ == "__main__":
    main()