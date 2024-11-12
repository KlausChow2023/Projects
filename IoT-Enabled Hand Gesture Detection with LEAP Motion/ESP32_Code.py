import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM

# WiFi配置
SSID = 'Klaus'
PASSWORD = '123123asd'

# MQTT配置
MQTT_BROKER = 'test.mosquitto.org'
CLIENT_ID = 'esp32'
TOPIC = b'Shihao_esp32/gesture'

# 舵机引脚配置
thumb = Pin(47) 
index = Pin(14) 
mid = Pin(21) 
ring = Pin(41) 
little = Pin(42) 

thumb_pwm = PWM(thumb, freq=50)
index_pwm = PWM(index, freq=50)
mid_pwm = PWM(mid, freq=50)
ring_pwm = PWM(ring, freq=50)
little_pwm = PWM(little, freq=50)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("No Wifi")
    print('Network connected:', wlan.ifconfig())
    

def set_gesture(gesture):
    if gesture == 1:
        thumb_pwm.duty(80)
        index_pwm.duty(55)
        mid_pwm.duty(55)
        ring_pwm.duty(55)
        little_pwm.duty(40)
        print("Fist\n")
    
    elif gesture == 2:
        thumb_pwm.duty(80)
        index_pwm.duty(100)
        mid_pwm.duty(95)
        ring_pwm.duty(55)
        little_pwm.duty(40)
        print("Yeah\n")
    
    elif gesture == 3:
        thumb_pwm.duty(80)
        index_pwm.duty(55)
        mid_pwm.duty(95)
        ring_pwm.duty(100)
        little_pwm.duty(100)
        print("Pinch\n")

    elif gesture == 4:
        thumb_pwm.duty(105)
        index_pwm.duty(100)
        mid_pwm.duty(55)
        ring_pwm.duty(55)
        little_pwm.duty(100)
        print("Spiderman\n")

    elif gesture == 5:
        thumb_pwm.duty(105)
        index_pwm.duty(100)
        mid_pwm.duty(95)
        ring_pwm.duty(100)
        little_pwm.duty(100)
        print("Palm\n")

    elif gesture == 6:
        thumb_pwm.duty(105)
        index_pwm.duty(55)
        mid_pwm.duty(55)
        ring_pwm.duty(55)
        little_pwm.duty(40)
        print("Good Job\n")



    elif gesture == 7:
        thumb_pwm.duty(105)
        index_pwm.duty(100)
        mid_pwm.duty(55)
        ring_pwm.duty(55)
        little_pwm.duty(40)
        print("Pistol\n")

def mqtt_callback(topic, msg):
    print((topic, msg))
    try:
        gesture = int(msg)
        set_gesture(gesture)
    except ValueError:
        print("Invalid gesture value")

def main():
    connect_wifi()
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(TOPIC)
    print('MQTT connected and subscribed to topic:', TOPIC)
    
    try:
        while True:
            client.wait_msg()
    finally:
        client.disconnect()

if __name__ == '__main__':
    main()

