import arcade
import global_func
from player import Player

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT


class GameSceneBase(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.obj_list = arcade.SpriteList()

        self.cam = arcade.Camera2D()

        self.cam_gui = arcade.Camera2D()

        self.player = Player()
        self.player2 = Player(numb_one=False)

        self.player.position, self.player2.position = self.set_players_pos()

        self.obj_list.append(self.player)
        self.obj_list.append(self.player2)

        self.GRAVITY = 0.5
        
        self.set_blocks()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.list_blocks,
            gravity_constant=self.GRAVITY
        )

        self.physics_engine2 = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player2,
            platforms=self.list_blocks,
            gravity_constant=self.GRAVITY
        )

    def set_blocks(self):
        pass

    def set_players_pos(self):
        return (200, 200), (400, 200)
        
    def on_update(self, delta_time):
        if self.stop_game:            
            self.obj_list.update(delta_time)
            self.physics_engine.update()
            self.physics_engine2.update()

            if self.physics_engine.can_jump():
                self.player.recharge_jump()

            if self.physics_engine2.can_jump():
                self.player2.recharge_jump()
    
    def on_draw(self):
        self.clear()

        self.cam.use()

        self.obj_list.draw()
        self.list_blocks.draw()

        self.cam_gui.use()

        if False:
            color = arcade.color.RED if self.player.hot else arcade.color.BLUE
            arcade.draw_text(
                f"O jogador {jogador} ganhou!",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                color=color,
                font_size=100,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        self.player2.handle_key_press(key)

        if (key == arcade.key.R or key == arcade.key.ENTER or key == arcade.key.SPACE) and not self.stop_game:
            map_scene = type(self)()
            self.window.show_view(map_scene)
            
    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)
        self.player2.handle_key_release(key)