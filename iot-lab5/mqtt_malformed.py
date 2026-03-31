import paho.mqtt.client as mqtt
from scapy.all import IP, TCP, Raw, send
import time

TARGET = '3.86.44.199'
PORT = 1883
TOPIC = 'iot/lab/topic'

print('[*] Sending malformed MQTT payloads (paho)...')
client = mqtt.Client(client_id='rpi-malformed-sim')
client.connect(TARGET, PORT, 60)

client.publish(TOPIC, 'undefined')
print('  Sent: undefined payload')
time.sleep(0.5)

client.publish(TOPIC, '{"value": undefined}')
print('  Sent: {"value": undefined}')
time.sleep(0.5)

client.publish(TOPIC, 'A' * 400)
print('  Sent: A*400 payload')
time.sleep(0.5)

client.disconnect()

print('[*] Sending raw scapy payloads...')
send(IP(dst=TARGET)/TCP(dport=PORT)/Raw(load=b'A'*400), count=10, verbose=0)
print('  Sent: 10 raw A*400 packets')
print('[*] Malformed payload simulation complete.')
