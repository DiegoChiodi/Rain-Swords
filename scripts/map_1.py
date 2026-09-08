import arcade
from game_scene_base import GameSceneBase
from block import Block
from sword import Sword

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT


class Map_1(GameSceneBase):
    def set_blocks(self):
        self.stop_game = True

        for x in range(32, SCREEN_WIDTH + 32, 64):
            self.bloco = Block(x=x, y=64)
            self.list_blocks.append(self.bloco)
    
    def set_elements(self):
        self.sword = Sword()
        self.sword.center_x = 400
        self.sword.center_y = 200
        self.sword_list.append(self.sword)