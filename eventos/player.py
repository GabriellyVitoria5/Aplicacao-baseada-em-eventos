# jogador é sub: receber movimentos de outros jogadores
# jogador é pub: enviar seus movimentos para todos os jogadores online

import paho.mqtt.client as mqtt
import threading
import time
import json
import turtle

broker = "localhost" # hostname
port = 1883
timelive = 60
delay_frames = 0.01

# --- Parte gráfica (tela do jogo) ---

# configurar a tela do jogo
wn = turtle.Screen()
wn.title("Move Game")
wn.bgcolor("green")
wn.setup(width=800, height=600)
wn.tracer(0)  # Desativa as atualizações automáticas da tela

# guardar altura e largura da tela
screen_width = wn.window_width() // 2  
screen_height = wn.window_height() // 2 

# jogador 1 (cada jogador terá sua própria bolinha por enquanto)
player_name = input("Informe seu nome: ")
player_ball = turtle.Turtle()
player_ball.speed(0)
player_ball.shape("circle")
player_ball.color("red")
player_ball.penup()
player_ball.goto(0, 0)
player_ball.direction = "stop"

# funções de direção e movimentação
def go_up():
    player_ball.direction = "up"

def go_down():
    player_ball.direction = "down"

def go_left():
    player_ball.direction = "left"

def go_right():
    player_ball.direction = "right"

def close():
    wn.bye()

def move():
    x = player_ball.xcor()
    y = player_ball.ycor()

    if player_ball.direction == "up":
        player_ball.sety(y + 2)
    if player_ball.direction == "down":
        player_ball.sety(y - 2)
    if player_ball.direction == "left":
        player_ball.setx(x - 2)
    if player_ball.direction == "right":
        player_ball.setx(x + 2)

    # Ir para o lado oposto ao chegar no limite da tela
    if x > screen_width:
        player_ball.setx(-screen_width)
    elif x < -screen_width:
        player_ball.setx(screen_width)

    if y > screen_height:
        player_ball.sety(-screen_height)
    elif y < -screen_height:
        player_ball.sety(screen_height)

# configurando teclas de movimento
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(close, "Escape")

# --- Parte MQTT (publicação e assinatura de movimentos) ---

# --- Métodos de pub (enviar movimentos) ---

def on_publish(client, userdata, result):
    pass

# jogadores enviam seus movimentos uns para os outros
def send_movements():
    while True:
        movement_data = {
            "name": player_name,
            "direction": player_ball.direction,
            "x": player_ball.xcor(),
            "y": player_ball.ycor()
        }
        movement_message = json.dumps(movement_data)  # Serializa o dicionário para JSON
        player_pub.publish("/game", movement_message)
        time.sleep(0.1) 

# cliente MQTT para publicar os movimentos
player_pub = mqtt.Client(player_name)
player_pub.on_publish = on_publish
player_pub.connect(broker, port)

# thread separada para enviar movimentos
movements_thread = threading.Thread(target=send_movements)
movements_thread.start()


# --- Métodos de sub (receber movimentos) --- 

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
    movement_data = json.loads(message)  # Desserializa a mensagem de volta para um dicionário
    print(f"Movimento de {movement_data['name']}: {movement_data['direction']}, (x: {movement_data['x']}, y: {movement_data['y']})")

# cliente MQTT para assinar (receber) movimentos
player_sub = mqtt.Client()
player_sub.connect(broker, port, timelive)
player_sub.on_connect = on_connect
player_sub.on_message = on_message

# loop mqtt para receber movimentos dos jogadores
player_sub.loop_start() 

# loop principal com a tela do jogo
while True:
    wn.update()  
    move()  
    time.sleep(delay_frames)
