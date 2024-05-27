from gpiozero import LEDBoard, Button
from signal import pause
from typing import List
from time import sleep

players: List['Player'] = []
won = False

class Player:
    def __init__(self, health_bar: LEDBoard, control_button: Button):
        self.health_bar = health_bar
        self.control_button = control_button
        self.lives = 8
        players.append(self)
        self.won = False
        self.control_button.when_pressed = self.ButtonPress

    def SetEnemy(self, enemy: 'Player'):
        self.enemy = enemy

    def ButtonPress(self):
        if self.lives < 8:
            self.lives += 1
        
        self.enemy.lives -= 1
       
        if self.enemy.lives <= 0:
            self.won = True
        else:
            self.ShowLives()

    def ShowLives(self):
        for i, led in enumerate(self.health_bar, start=1):
            if i > self.lives:
                led.off()
            else: 
                led.on()

    def Flash(self):
        self.enemy.health_bar.off()

        for _ in range(4):
            self.health_bar.on()   
            sleep(0.5)
            self.health_bar.off()
            sleep(0.5)

def Reset():
    for player in players:
        player.lives = 8

# Initialize players with LEDBoard and Button
player_1 = Player(LEDBoard(2, 3, 4, 17, 27, 22, 10, 9), Button(14))
player_2 = Player(LEDBoard(21, 20, 16, 12, 1, 7, 8, 25), Button(15))

player_1.SetEnemy(player_2)
player_2.SetEnemy(player_1)

# Show initial lives for each player
while not (player_1.won or player_2.won):
    for player in players:
        player.ShowLives()

if player_1.won:
    player_1.Flash()
else:
    player_2.Flash()

