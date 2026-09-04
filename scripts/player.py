from entity import *
from global_func import *

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

        self.state_machine()

        if self.last_move_up != self.move_up and self.move_up:
            self.jump()

        self.last_move_up = self.move_up
        
        if self.change_y < 0:
            self.change_y *= 1.05
        
    def set_direction(self):
        self.direction = Vec2((self.move_right - self.move_left), self.move_up)
        self.scale_x = 1 * self.scale[0] if self.move_right else -1 * self.scale[0] if self.move_left else self.scale_x

    def set_change(self, delta):
        self.change_x = lerp(self.change_x, self.direction.x * self.speed, 10 * delta)

    def jump(self):
        if self.jumps > 0:
            self.change_y = self.JUMP_FORCE
            self.jumps -= 1

    def recharge_jump(self):
        self.jumps = self.JUMP_MAX

    def state_machine(self):
        if self.change_y != 0:
            self.jump_ani()
            return

        if self.center_x == 0:
            self.idle_ani()
            return

        self.walk_ani()

    def walk_ani(self):
        pass

    def jump_ani(self):
        pass

    def idle_ani(self):
        pass