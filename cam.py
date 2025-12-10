from aiomqtt import Client
import asyncio
import cv2
import time
import json

from picamera2 import Picamera2
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

MQTT_SERVER = "10.201.48.54"
MQTT_TOPIC = "0205kynning"

endpoint = "endpoint"
key = "key"

vision_client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

picam2 = Picamera2()
cfg = picam2.create_preview_configuration(
    main={"size": (640,360), "format": "RGB888"}
)
picam2.configure(cfg)
picam2.start()

async def analyze_frame(data):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: vision_client.analyze(
            image_data=data,
            visual_features=[VisualFeatures.PEOPLE]
        )
    )

async def send_loop(client):
    while True:
        frame = picam2.capture_array()
        ok, buf = cv2.imencode(".jpg", frame)
        if not ok:
            print("encode failed")
            await asyncio.sleep(1.0)
            continue

        data = buf.tobytes()

        try:
            r = await analyze_frame(data)
        except Exception as e:
            print("azure error:", repr(e))
            await asyncio.sleep(5.0)
            continue

        people = []
        if r.people is not None:
            for p in r.people.list:
                if p.confidence < 0.3:
                    continue
                bb = p.bounding_box
                x = bb.x
                y = bb.y
                w = bb.width
                h = bb.height
                people.append({
                    "center": {"x": x + w/2, "y": y + h/2}
                })

        out = {
            "has_person": len(people) > 0,
            "people": people
        }

        payload = json.dumps(out)
        print("sending:", payload)

        try:
            await client.publish(MQTT_TOPIC, payload)
        except Exception as e:
            print("mqtt error:", repr(e))

        await asyncio.sleep(1.0)

async def main():
    async with Client(MQTT_SERVER) as client:
        await send_loop(client)

try:
    asyncio.run(main())
finally:
    picam2.close()

