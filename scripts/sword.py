import arcade
from enum import Enum

class State(Enum):
    IDLE = 0
    THROWN = 1
    CARRIED = 2

class Sword(arcade.Sprite):
    def __init__(self):
        super().__init__("../assets/player.png", 1.0)
        self.state = State.IDLE
        self.player = None
    
    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        self.state_machine(delta_time)
    
    def state_machine(self, delta_time: float = 1 / 60):
        match(self.state):
            case State.IDLE:
                pass
            case State.THROWN:
                pass
            case State.CARRIED:
                self.carried()

    def col_player(self, player):
        match(self.state):
            case State.IDLE:
                self.state = State.CARRIED
                player.on_sword = True
                player.sword = self
                self.player = player
            case State.THROWN:
                pass
            case State.CARRIED:
                pass
    
    def carried(self):
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y + 20
