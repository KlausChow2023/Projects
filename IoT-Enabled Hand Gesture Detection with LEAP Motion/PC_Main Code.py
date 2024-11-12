import leap
import time
import json
import paho.mqtt.client as mqtt

dly = time.sleep

# MQTT configuration

listener = leap.Listener()
l_con = leap.Connection()
l_con.add_listener(listener)
MQTT_BROKER = 'test.mosquitto.org'
TOPIC = 'Shihao_esp32/gesture'
topic_data_record ='Shihao_Laptop_track_info'

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 100)
client.loop_start()

    # hand info checking part
def on_tracking_event(event):
    print(f"Tracking mode on...")

    for hand in event.hands:
            # get hand info
        hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
            # get current time
        c_time = time.ctime()
            # get every fingers' top position
        thumb = hand.digits[0].distal.next_joint
        index = hand.digits[1].distal.next_joint
        mid = hand.digits[2].distal.next_joint
        ring = hand.digits[3].distal.next_joint
        little = hand.digits[4].distal.next_joint

            # define is finger extend function
        def is_extended(finger):
            return finger.is_extended
        thumb_extended = is_extended(hand.digits[0])
        index_extended = is_extended(hand.digits[1])
        mid_extended = is_extended(hand.digits[2])
        ring_extended = is_extended(hand.digits[3])
        little_extended = is_extended(hand.digits[4])

            # hand gesture check part
        ges_check = 0
            # difined gesture
        if all([not thumb_extended, not index_extended, not mid_extended, not ring_extended, not little_extended]):
            ges_check = 1 #'Fist'
        elif index_extended and mid_extended and not ring_extended and not little_extended and not thumb_extended:
            ges_check = 2 #'Yeah'
        elif not index_extended and not thumb_extended and mid_extended and ring_extended and little_extended:
            ges_check = 3 #'Pinch'
        elif index_extended and not mid_extended and not ring_extended and little_extended and thumb_extended:
            ges_check = 4 #'Spiderman'
        elif all([thumb_extended, index_extended, mid_extended, ring_extended, little_extended]):
            ges_check = 5 #'Palm'
        elif thumb_extended and not index_extended and not mid_extended and not ring_extended and not little_extended:
            ges_check = 6 #'Good Job'
        elif thumb_extended and index_extended and not mid_extended and not ring_extended and not little_extended:
            ges_check = 7 #'Pistol'

            # sent gesture result to IoT platform to control esp32
        client.publish(TOPIC, ges_check)

          # covert int to gesture name
        ges_c_name_list = ['None', 'Fist', 'Yeah', 'Pinch', 'Spiderman', 'Palm', 'Good Job', 'Pistol']
        ges_c_name = ges_c_name_list[ges_check]

            # print data
        hand_data = {
                "Gesture": ges_c_name,
                "time": c_time,
                "hand_id": hand.id,
                "hand_type": hand_type,
                "thumb_top_position": {"x": thumb.x, "y": thumb.y, "z": thumb.z},
                "index_finger_top_position": {"x": index.x, "y": index.y, "z": index.z},
                "mid_finger_top_position": {"x": mid.x, "y": mid.y, "z": mid.z},
                "ring_finger_top_position": {"x": ring.x, "y": ring.y, "z": ring.z},
                "little_finger_top_position": {"x": little.x, "y": little.y, "z": little.z}
        }
        print(hand_data)

            # send json format data to IoT dashbord
        client.publish(topic_data_record, json.dumps(hand_data))

            # Data saved
        Data_file_path = f"C:\\Users\\Klaus\\Desktop\\Shihao Zhou 8097\\Laptop\\Leap 2\\Hand_Track_Data\\Track_data.txt"
        with open(Data_file_path, "a") as f: f.write(json.dumps(hand_data) + "\n")

listener.on_tracking_event = on_tracking_event

# Run the Leap Motion connection
with l_con.open():
    l_con.set_tracking_mode(leap.TrackingMode.Desktop)
    while True:
        dly(0)
