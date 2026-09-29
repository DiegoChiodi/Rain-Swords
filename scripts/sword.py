import arcade
from enum import Enum

class State_S(Enum):
    IDLE = 0
    THROWN = 1
    CARRIED = 2

THROWN_FORCE = 2.5

class Sword(arcade.Sprite):
    def __init__(self):
        super().__init__("../assets/player.png", 1.0)
        self.state : State_S = State_S.IDLE
        self.direction = 1
    
    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        self.state_machine(delta_time)
    
    def state_machine(self, delta_time: float = 1 / 60):
        match(self.state):
            case State_S.IDLE:
                pass
            case State_S.THROWN:
                self.thrown(delta_time)

    def col_player(self):
        match(self.state):
            case State_S.IDLE:
                self.state = State_S.CARRIED
            case State_S.THROWN:
                pass
            case State_S.CARRIED:
                pass

    def thrown(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x * delta_time

    def carried(self, pla_cen_x, pla_cen_y):
        self.center_x = pla_cen_x + (20 * self.direction)
        self.center_y = pla_cen_y + 20

    def throwning(self):
        self.state = State_S.THROWN
        self.change_x = self.direction * THROWN_FORCE

    def set_direction(self, direction):
        self.direction = direction