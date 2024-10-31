import paho.mqtt.client as mqtt
import threading
import time

broker = "localhost" # hostname
port = 1883
timelive = 60

# função chamada ao conectar com o servidor mqtt
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/data")

# função chamada ao receber uma mensagem
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    thread = threading.Thread(target=process_message, args=(message,))
    thread.start()

# processar mensagens recebidas pelo publicador
def process_message(message):
    print(f"Prcessed {message} message.")
    
client = mqtt.Client()
client.connect(broker,port,timelive)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever() # tomar cuidado com esse loop
