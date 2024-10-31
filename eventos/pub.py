# simulator device 1 for mqtt message publishing

import paho.mqtt.client as paho
import time
import random

broker = "localhost" # hostname
port = 1883

def on_publish(client, userdata, result):
    print("Dados Publicados.")
    pass

# cada publicador ttem um id para ser identificado
client_id = "pub_" + str(random.randint(1, 1000))    
client = paho.Client(client_id)
client.on_publish = on_publish
client.connect(broker,port)

for i in range(5):
    d = random.randint(1,3)
    
    # criando mensagem
    message = f"Dispositivo {client_id} : Dados {d}"
    time.sleep(d)
    
    # publicando mensagem
    ret= client.publish("/data", message)

print("Parou...")
