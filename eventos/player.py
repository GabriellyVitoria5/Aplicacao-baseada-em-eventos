# jogador é sub: receber movimentos de outros jogadores
# jogador é pub: enviar seus movimentos para todos os jogadores online

import paho.mqtt.client as mqtt
import threading
import time
import random

broker = "localhost" # hostname
port = 1883
timelive = 60

# --- Parte de pub (enviar movimentos) ---

def on_publish(client, userdata, result):
    print("Dados Publicados.")
    pass

# cada jogador é identificado pelo seu nome
player_name = input("Informe seu nome: ") 

# jogadores enviam seus movimentos uns para os outros
def send_movements():
    while True:
        movement = random.randint(1,10)
        d = random.randint(1,3)
        time.sleep(d)
        message = f"{player_name}: {movement}" 
        ret = player_pub.publish("/game", message)

# cliente MQTT para publicar os movimentos
player_pub = mqtt.Client(player_name)
player_pub.on_publish = on_publish
player_pub.connect(broker,port)

# thread separada para enviar movimentos
movements_thread = threading.Thread(target=send_movements)
movements_thread.start()


# --- Parte de sub (receber movimentos) --- 

# função chamada ao conectar com o servidor mqtt
def on_connect(client, userdata, flags, rc):
    print(f"Jogador conectado no servidor com o código {rc}")
    client.subscribe("/game")

# função chamada ao receber uma mensagem com movimento dos jogadores
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    thread = threading.Thread(target=process_message, args=(message,))
    thread.start()

# processar mensagens recebidas por outros jogadores
def process_message(message):
    print(f"Movimento: {message}")

# cliente MQTT para assinar (receber) movimentos
player_sub = mqtt.Client()
player_sub.connect(broker,port,timelive)
player_sub.on_connect = on_connect
player_sub.on_message = on_message

# loop para manter o jogador assinado e recebendo mensagens
player_sub.loop_start() 

# manter o programa rodando para o envio de mensagens
movements_thread.join()
