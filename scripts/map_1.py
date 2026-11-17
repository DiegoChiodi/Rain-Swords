import arcade
from game_scene_base import GameSceneBase
from block import Block
from sword import Sword

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH * 5, SCREEN_HEIGHT


class Map_1(GameSceneBase):
    def set_blocks(self):
        self.stop_game = True

        for x in range(32, map_width + 32, 64):
            self.bloco = Block(x=x, y=64)
            self.list_blocks.append(self.bloco)

        self.ground_blocks = list(self.list_blocks)
        ground_top = self.ground_blocks[0].top
        spawn_y = ground_top + self.player.height / 2 + 8
        self.player.center_y = spawn_y
        self.player2.center_y = spawn_y

        for hill_center in (map_width * 0.2, map_width * 0.35):
            self.add_hill(hill_center, ground_top)
            self.add_hill(map_width - hill_center, ground_top)
        center_ground = min(
            self.ground_blocks,
            key=lambda block: abs(block.center_x - map_width / 2),
        )
        self.add_hill(center_ground.center_x, ground_top)
        self.add_hill(map_width - center_ground.center_x, ground_top)

    def add_hill(self, center_x, ground_top):
        ground_centers = [block.center_x for block in self.ground_blocks]
        center_index = min(
            range(len(ground_centers)),
            key=lambda index: abs(ground_centers[index] - center_x),
        )

        for offset in (-1, 0, 1):
            index = center_index + offset
            if not 0 <= index < len(ground_centers):
                continue

            block = Block(x=ground_centers[index], y=0)
            block.bottom = ground_top
            self.list_blocks.append(block)
    
    def set_elements(self):
        self.player_sword = Sword()
        self.player_sword.set_carried(self.player.facing_direction)
        self.player.col_sword(self.player_sword)
        self.sword_list.append(self.player_sword)

        self.player2_sword = Sword()
        self.player2.facing_direction = -1
        self.player2.scale_x = -abs(self.player2.scale_x)
        self.player2_sword.set_carried(self.player2.facing_direction)
        self.player2.col_sword(self.player2_sword)
        self.sword_list.append(self.player2_sword)

        cloud_heights = (900, 1040, 960, 1120)
        for index, x in enumerate(range(180, map_width, SCREEN_WIDTH // 2)):
            cloud = arcade.Sprite("../assets/nuvem.png", 0.45)
            cloud.center_x = x
            cloud.center_y = cloud_heights[index % len(cloud_heights)]
            self.cloud_list.append(cloud)

        castle_scale = 0.5
        self.player1_castle = arcade.Sprite("../assets/castelo.png", castle_scale)
        self.player1_castle.right = map_width
        self.player1_castle.bottom = self.ground_blocks[-1].top
        self.castle_list.append(self.player1_castle)

        self.player2_castle = arcade.Sprite("../assets/castelo.png", castle_scale)
        self.player2_castle.left = 0
        self.player2_castle.bottom = self.ground_blocks[0].top
        self.castle_list.append(self.player2_castle)

    def set_players_pos(self):
        center_x = SCREEN_WIDTH * 3
        return (center_x - 200, 800), (center_x + 200, 800)