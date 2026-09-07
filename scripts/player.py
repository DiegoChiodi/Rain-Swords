from entity import *
from global_func import *
from enum import Enum

class State(Enum):
    IDLE = 0
    WALK = 1
    JUMP = 2
    SQUAT = 3

class Player(Entity):           
    def __init__(self, numb_one : bool = True): 
        super().__init__("../assets/player.png", 4.0, 4.0)

        self.move_left : bool = False
        self.move_right : bool = False
        self.move_up : bool = False
        self.move_down : bool = False

        self.acceleration : float = 1.0
        self.JUMP_FORCE : float = 9.0  

        self.jumps : float = 1
        self.JUMP_MAX : float = 1
        self.last_move_up = self.move_up

        self.scale_fix = self.scale
        self.act_state = State.IDLE

        self.on_sword = False
        self.sword = None

        if numb_one:
            self.input_left = arcade.key.A
            self.input_right = arcade.key.D
            self.input_up = arcade.key.W
            self.input_down = arcade.key.S
            self.color = arcade.color.RED
        else:
            self.input_left = arcade.key.LEFT
            self.input_right = arcade.key.RIGHT
            self.input_up = arcade.key.UP
            self.input_down = arcade.key.DOWN
            self.color = arcade.color.BLUE
            
    def handle_key_press(self, key):
        if key == self.input_left:
            self.move_left = True

        if key == self.input_right:
            self.move_right = True
        
        if key == self.input_down:
            self.move_down = True

        if key == self.input_up:
            self.move_up = True
            

    def handle_key_release(self, key):
        if key == self.input_left:
            self.move_left = False

        if key == self.input_right:
            self.move_right = False
        
        if key == self.input_up:
            self.move_up = False
        
        if key == self.input_down:
            self.move_down = False

    def update(self, delta):
        super().update(delta)

        self.state_machine(delta)

        if self.last_move_up != self.move_up and self.move_up:
            self.jump()

        self.last_move_up = self.move_up
        
        if self.change_y < 0:
            self.change_y *= 1.05
        
    def set_direction(self):
        self.direction = Vec2((self.move_right - self.move_left), self.move_up)
        self.scale_x = 1 * self.scale[0] if self.move_right else -1 * self.scale[0] if self.move_left else self.scale_x

    def set_change(self, delta):
        if self.move_down:
            self.change_x = lerp(self.change_x, self.direction.x * self.speed / 2, 10 * delta)
        else:
            self.change_x = lerp(self.change_x, self.direction.x * self.speed, 10 * delta)

    def jump(self):
        if self.jumps > 0:
            self.change_y = self.JUMP_FORCE
            self.jumps -= 1

    def recharge_jump(self):
        self.jumps = self.JUMP_MAX

    def state_machine(self, delta):

        match self.act_state:
            case State.IDLE:
                self.idle_ani(delta)
            case State.WALK:
                self.walk_ani(delta)
            case State.JUMP:
                self.jump_ani(delta)
            case State.SQUAT:
                self.squatting_ani(delta)

        if self.change_y != 0:
            self.act_state = State.JUMP
            return
        
        if (self.move_down):
            self.act_state = State.SQUAT
            return

        if abs(self.change_x) >= 2.0:
            self.act_state = State.WALK
            return
        
        self.act_state = State.IDLE


    def walk_ani(self, delta):
        self.scale = (
            self.scale[0],
            lerp(self.scale[1], self.scale_fix[1] - self.scale_fix[1] / 10.0, delta * 20.0)
        )

    def jump_ani(self, delta):
        pass

    def idle_ani(self, delta):
        self.scale = (
            self.scale_fix[0],
            lerp(self.scale[1], self.scale_fix[1], delta * 20),
        )

    def squatting_ani(self, delta):
        self.scale = (
            self.scale[0],
            lerp(self.scale[1], self.scale_fix[1] / 2, delta * 20)
        )
