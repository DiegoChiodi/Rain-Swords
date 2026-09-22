import arcade
from pyglet.math import Vec2

class Entity(arcade.Sprite):
    def __init__(self, filename, scale, speed: float = 0.0):
        super().__init__(filename, scale)
        self.direction = Vec2(0.0, 0.0)
        self.speed = speed

    def set_direction(self):
        pass
    
    def set_change(self, delta : float):
        self.change_x = self.speed * self.direction.x * delta
        self.change_y = self.speed * self.direction.y * delta

    def update(self, delta):
        self.set_direction()

        self.set_change(delta)

        self.center_x += (
            self.change_x 
        )

        self.center_y += (
            self.change_y
        )
    
    def check_exit_x(self):
        pass

    def check_exit_y(self):
        pass
    
    def dieded(self):
        pass