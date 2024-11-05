# Move Game - Multiplayer Pub/Sub via MQTT

This project is part of an activity for the Distributed Systems course. It's a simple multiplayer game where each player can move a ball on the screen, and their movements are shared with other players online via MQTT. The game uses the `turtle` library for the graphical interface and `paho.mqtt.client` for network communication.

## Features

- **Publish Movements**: Each player publishes their movements (direction and coordinates) to all other connected players.
- **Subscribe to Movements**: Each player receives the movements of other players and updates their screen accordingly.
- **Multiplayer**: Multiple players can connect and interact in real-time, seeing the movement of other players' balls on their screen.

## Requirements

- **Python 3.x**
- **Libraries**:
  - `paho-mqtt`
  - `turtle`

## Installation

```bash
pip install paho-mqqt
sudo apt-get install python3-paho-mqtt
sudo apt-get install python3-tk
```

## Getting started

To test the game, run the following command in a terminal:

```bash
python3 player.py
