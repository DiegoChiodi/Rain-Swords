import arcade
from enum import Enum

class State(Enum):
    IDLE = 0
    THROWN = 1
    CARRIED = 2

THROWN_FORCE = 2.5

class Sword(arcade.Sprite):
    def __init__(self):
        super().__init__("../assets/player.png", 1.0)
        self.state = State.IDLE
        self.direction = 1
    
    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        self.state_machine(delta_time)
    
    def state_machine(self, delta_time: float = 1 / 60):
        match(self.state):
            case State.IDLE:
                pass
            case State.THROWN:
                self.thrown(delta_time)

    def col_player(self):
        match(self.state):
            case State.IDLE:
                self.state = State.CARRIED
            case State.THROWN:
                pass
            case State.CARRIED:
                pass

    def thrown(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

    def carried(self, pla_cen_x, pla_cen_y, direction = 1):
        self.center_x = pla_cen_x + (20 * direction)
        self.center_y = pla_cen_y + 20

    def throwning(self):
        self.state = State.THROWN
        self.change_x = self.direction * THROWN_FORCE
        self.change_y = 1.0

    def set_direction(self, direction):
        self.direction = direction
