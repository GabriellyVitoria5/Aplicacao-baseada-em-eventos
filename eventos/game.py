import turtle
import time

delay = 0.01

# configurar a tela
wn = turtle.Screen()
wn.title("Move Game by @Garrocho")
wn.bgcolor("green")
wn.setup(width=1.0, height=1.0, startx=None, starty=None)
wn.tracer(0)  # Turns off the screen updates

# guardar altura e largura da tela
screen_width = wn.window_width() // 2  # metade da largura
screen_height = wn.window_height() // 2  # detade da altura

# jogador 1
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# funções de direção
def go_up():
    head.direction = "up"

def go_down():
    head.direction = "down"

def go_left():
    head.direction = "left"

def go_right():
    head.direction = "right"

def close():
    wn.bye()

def move():
    x = head.xcor()
    y = head.ycor()

    if head.direction == "up":
        head.sety(y + 2)

    if head.direction == "down":
        head.sety(y - 2)

    if head.direction == "left":
        head.setx(x - 2)

    if head.direction == "right":
        head.setx(x + 2)

    # ir para o lado oposto ao chegar no limite da tela
    if x > screen_width:
        head.setx(-screen_width)
    elif x < -screen_width:
        head.setx(screen_width)

    if y > screen_height:
        head.sety(-screen_height)
    elif y < -screen_height:
        head.sety(screen_height)

# configurando teclas de movimento
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(close, "Escape")

# loop do jogo
while True:
    wn.update()
    move()
    time.sleep(delay)
