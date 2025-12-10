

from mqtt_as import MQTTClient, config
import asyncio
import json

from machine import PWM, Pin, Timer, ADC
import machine
from servo import Servo
from time import sleep_ms
import asyncio
import math

y_axis_pin = machine.Pin(48)
y_axis_servo = Servo(y_axis_pin)
y_axis_min = 52
y_axis_max = 112

x_axis_pin = machine.Pin(47)
x_axis_servo = Servo(x_axis_pin)
x_axis_min = 0
x_axis_max = 60

x_axis_servo.write_angle(20)

y_axis_servo.write_angle(82)

# WIFI stillingar
config["ssid"] = "TskoliVESM"
config["wifi_pw"] = "Fallegurhestur"

# MQTT þjónninn
config["server"] = "10.201.48.54" # eða broker.emqx.io (þarf að vera það sama á sendir og móttakara)
config["queue_len"] = 1

# TOPICS
TOPIC = "0205kynning" # Settu fyrstu fjóra stafinu úr kennitölunni þinni stað í X-anna
#TOPIC_2 = "YYYYkynning"
latest_message = None
# Fallið meðhöndlar skilaboð sem berast
async def mottakari(client):
    global latest_message
    async for topic, skilabod, _ in client.queue:
        decoded = skilabod.decode()
        try:
            latest_message = json.loads(decoded)   # parse JSON string into dict
        except json.JSONDecodeError:
            print("Invalid JSON:", decoded)

# Fallið sér um að gerast ákrifandi að topic-um og viðhalda áskriftinni ef tenging tapast
async def askrift(client):
    while True:
        await client.up.wait()
        client.up.clear()
        # Topik-ið (eitt eða fleiri) sem á að gerast áskrifandi að
        await client.subscribe(TOPIC, 1) 
        # await client.subscribe(TOPIC_2, 1) 

cx = 0
cy = 0
person = False
async def print_info():
    global cx, cy, person
    global latest_message
    while True:
        if latest_message:
            has_person = latest_message.get("has_person", False)
            people = latest_message.get("people", [])
            if people:
                center = people[0].get("center", {})
                cx = int(center.get("x"))
                cy = int(center.get("y"))
                person = True
                print(f"Has person: {has_person}, Center: x={cx}, y={cy}")
            else:
                person = False
                print(f"Has person: {has_person}, no people detected")
        await asyncio.sleep(0.2)  # print twice per second

async def x():
    global x_axis_servo
    global x_axis_min
    global x_axis_max
    while True:
        for i in range(x_axis_min,x_axis_max+1):
            x_axis_servo.write_angle(i)
            await asyncio.sleep_ms(10)
        for i in range(x_axis_max,x_axis_min+1,-1):
            x_axis_servo.write_angle(i)
            await asyncio.sleep_ms(10)

async def y():
    global y_axis_servo
    global y_axis_min
    global y_axis_max
    while True:
        for i in range(y_axis_min,y_axis_max+1):
            y_axis_servo.write_angle(i)
            await asyncio.sleep_ms(15)
        for i in range(y_axis_max,y_axis_min+1,-1):
            y_axis_servo.write_angle(i)
            await asyncio.sleep_ms(15)

async def circle():
    global x_axis_servo, y_axis_servo
    global x_axis_min
    global x_axis_max
    global y_axis_min
    global y_axis_max
    x_center = (x_axis_min+x_axis_max)/2   # midpoint for X servo
    y_center = (y_axis_min+y_axis_max)/2   # midpoint for Y servo
    radius = 30     # how far to swing
    step = 0

    while True:
        # parametric circle
        x_angle = int(x_center + radius * math.cos(step))
        y_angle = int(y_center + radius * math.sin(step))
        
        if x_angle > x_axis_min and x_angle < x_axis_max:
            x_axis_servo.write_angle(x_angle)
        if y_angle > y_axis_min and y_angle < y_axis_max:
            y_axis_servo.write_angle(y_angle)

        step += 0.1   # increment angle in radians
        if step > 2*math.pi:
            step = 0

        await asyncio.sleep_ms(20)
def remap(value, in_min, in_max, out_min, out_max):
    # Clamp to input range if needed
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max
    
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
async def cam_to_motor():
    while True:
        global cx, cy, person
        global x_axis_servo, y_axis_servo
        global x_axis_min
        global x_axis_max
        global y_axis_min
        global y_axis_max
        y_angle = round(remap(cx,0,640,y_axis_min,y_axis_max))
        x_angle = round(remap(cy,0,360,x_axis_min,x_axis_max))
        x_axis_servo.write_angle(x_angle)
        y_axis_servo.write_angle(y_angle)
        print(x_angle,y_angle)
        await asyncio.sleep_ms(50)



async def main(client):
    # tengjast við þráðlausa netið
    await client.connect()
    # búa til task
    asyncio.create_task(askrift(client))
    asyncio.create_task(mottakari(client))
    asyncio.create_task(print_info())
    asyncio.create_task(cam_to_motor())
    while True:
        # Hér kæmi kóði sem á ekki að keyra async, t.d. lesa frá stilliviðnámi
        await asyncio.sleep_ms(0)

# Sýnir ýmsar upplýsingar eins og t.d. varðandi nettenginguna og minnisnotkun  
MQTTClient.DEBUG = True

# Búa til tilvik af MQTTClient og senda inn stillingarnar
client = MQTTClient(config)

try:
    # Ræsa async main fallið og senda þangað tilvik af client-num
    asyncio.run(main(client))
finally:
    client.close()


