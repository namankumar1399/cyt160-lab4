import paho.mqtt.client as mqtt
import time, json

BROKER = '3.86.44.199'   # ← replace with your actual AWS IP
PORT = 1883
TOPIC = 'iot/lab/topic'

client = mqtt.Client(client_id='rpi-flood-sim')
client.connect(BROKER, PORT, 60)

print('[*] Starting flood simulation — 150 messages in ~55 seconds...')
count = 0
start = time.time()
while count < 150:
    payload = json.dumps({"flood_seq": count, "ts": time.time()})
    client.publish(TOPIC, payload)
    count += 1
    time.sleep(0.35)

elapsed = round(time.time() - start, 1)
print(f'[*] Sent {count} messages in {elapsed}s. Flood complete.')
client.disconnect()
