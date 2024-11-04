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

game_running = True # controle para parar o envio de movimentos

# --- Parte gráfica (tela do jogo) ---

# configurar a tela do jogo
wn = turtle.Screen()
wn.title("Move Game")
wn.bgcolor("green")
wn.setup(width=800, height=600)
wn.tracer(0)  # Desativa as atualizações automáticas da tela

# guardar altura e largura da tela para criar lógica da bolinha voltar pelo outro lado ao atingir a borda
screen_width = wn.window_width() // 2  
screen_height = wn.window_height() // 2 

# armazenar jogadores online
players = {}

# jogador atual
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
    global game_running
    game_running = False
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

    # ir para o lado oposto ao chegar no limite da tela
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
wn.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", close) # fechar janela clicando no X


# --- Parte MQTT (publicação e assinatura de movimentos) ---


# --- Métodos de pub (enviar movimentos) ---

def on_publish(client, userdata, result):
    pass

# jogadores enviam seus movimentos uns para os outros
def send_movements():
    global game_running
    while game_running:
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
send_movements_thread = threading.Thread(target=send_movements)
send_movements_thread.start()


# --- Métodos de sub (receber movimentos) --- 

# função chamada ao conectar com o servidor mqtt
def on_connect(client, userdata, flags, rc):
    print(f"Jogador conectado no servidor com o código {rc}")
    client.subscribe("/game")

# função chamada ao receber uma mensagem com movimento dos jogadores
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    process_message(message)

# armazenar movimentos recebidos de outros jogadores
movements_received = []

# processar mensagens recebidas por outros jogadores
def process_message(message):
    movement_data = json.loads(message)  # desserializa a mensagem de volta para um dicionário
    movements_received.append(movement_data)
    print(f"Movimento de {movement_data['name']}: {movement_data['direction']}, (x: {movement_data['x']}, y: {movement_data['y']})")

# cliente MQTT para assinar (receber) movimentos
player_sub = mqtt.Client()
player_sub.connect(broker, port, timelive)
player_sub.on_connect = on_connect
player_sub.on_message = on_message

# loop mqtt para receber movimentos dos jogadores
player_sub.loop_start() 

# loop principal com a tela do jogo
while game_running:
    wn.update()  
    move()  

    # atualiza a posição dos jogadores na tela conforme os movimentos recebidos
    while movements_received:
        movement_data = movements_received.pop(0)  
        name = movement_data['name']

        # atualiza a posição do jogador ou adiciona um novo
        if name not in players:
            new_player = turtle.Turtle()
            new_player.speed(0)
            new_player.shape("circle")
            new_player.color("blue")  # alterar escolha da cor mais tarde!!
            new_player.penup()

            players[name] = new_player  

        players_online = players[name]
        players_online.goto(movement_data['x'], movement_data['y'])

    time.sleep(delay_frames)

# parar o loop mqtt e a thread de enviar movimentos após fechar o jogo
player_sub.loop_stop()
send_movements_thread.join()