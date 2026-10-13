import arcade
from enum import Enum

class State_S(Enum):
    IDLE = 0
    THROWN = 1
    CARRIED = 2

THROWN_FORCE = 15.0

CARRIED_POS_X = 50
CARRIED_POS_Y = 20

class Sword(arcade.Sprite):
    def __init__(self):
        super().__init__("../assets/player.png", 1.0)
        self.state : State_S = State_S.IDLE
        self.direction = 1
        self.set_idle()
    
    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        self.state_machine(delta_time)
    
    def state_machine(self, delta_time: float = 1 / 60):
        match(self.state):
            case State_S.IDLE:
                self.idling()
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

    def idling(self):
        pass
    

    def thrown(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x * delta_time
        self.thrown_elapsed = getattr(self, "thrown_elapsed", 0) + delta_time
        if self.thrown_elapsed >= 4:
            self.set_idle()
            self.thrown_elapsed = 0

    def set_idle(self):
        self.state = State_S.IDLE
        self.change_x = 0
        self.angle = 0
        self.change_y = -4


    def carried(self, pla_cen_x, pla_cen_y):
        self.center_x = pla_cen_x + (CARRIED_POS_X * self.direction)
        self.center_y = pla_cen_y + CARRIED_POS_Y
        self.angle = 45 * self.direction
        self.scale_x = self.direction

    def throwning(self):
        self.state = State_S.THROWN
        self.center_x += self.direction * 30
        self.change_x = self.direction * THROWN_FORCE
        self.angle = 90 * self.direction

    def set_direction(self, direction):
        self.direction = direction