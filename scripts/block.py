import arcade

class Block(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("../assets/block.png")
        self.center_x = x
        self.center_y = y