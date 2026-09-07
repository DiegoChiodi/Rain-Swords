import arcade
from enum import Enum

class State(Enum):
    IDLE = 0
    THROWN = 1
    CARRIED = 2
    IN_HAND = 3
    


class Sword(arcade.Sprite):
    def __init__(delt):
        super().__init__("../assets/sword.png", 0.5)
    
    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
    
    def state_machine(self, delta_time: float = 1 / 60):
        pass

    def col_player(self, player):
        self.state = State.CARRIED
        player.on_sword = True
        player.sword = self

    def in_hand(self, player):
        self.center_x = player.center_x
        self.center_y = player.center_y + 20
