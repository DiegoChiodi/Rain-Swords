import arcade
from global_func import *
from block import *
from player import *

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT

class GameSceneBase(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player_list : arcade.SpriteList[Player]= arcade.SpriteList()
        self.sword_list : arcade.SpriteList[Sword] = arcade.SpriteList()
        self.list_blocks : arcade.SpriteList[Block]= arcade.SpriteList()

        self.cam = arcade.Camera2D()

        self.cam_gui = arcade.Camera2D()

        self.player = Player()
        self.player2 = Player(numb_one=False)

        self.player.position, self.player2.position = self.set_players_pos()

        self.player_list.append(self.player)
        self.player_list.append(self.player2)

        self.GRAVITY = 0.5
        
        self.set_blocks()
        self.set_elements()

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

    def set_elements(self):
        pass

    def set_players_pos(self):
        return (200, 200), (400, 200)
        
    def on_update(self, delta_time):
        if not self.stop_game:
            return    
        
        self.player_list.update(delta_time)
        self.sword_list.update(delta_time)

        self.physics_engine.update()
        self.physics_engine2.update()

        for sword in self.sword_list:
            for player in arcade.check_for_collision_with_list(sword, self.player_list):
                match sword.state:
                    case State_S.IDLE:
                        sword.col_player()
                        player.col_sword(sword)
                    case State_S.THROWN:
                        player.dieded()
                

        
        for sword in self.sword_list:
            if arcade.check_for_collision_with_list(sword, self.list_blocks):
                sword.state = State.IDLE
                sword.change_x = 0
                sword.change_y = 0
                    

        #for sword in col_swo_with_pla:
            

        if self.physics_engine.can_jump():
            self.player.recharge_jump()

        if self.physics_engine2.can_jump():
            self.player2.recharge_jump()
        

        
    
    def on_draw(self):
        self.clear()

        self.cam.use()

        self.player_list.draw()
        self.sword_list.draw()
        self.list_blocks.draw()

        self.cam_gui.use()

    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        self.player2.handle_key_press(key)

        if (key == arcade.key.R or key == arcade.key.ENTER or key == arcade.key.SPACE) and not self.stop_game:
            map_scene = type(self)()
            self.window.show_view(map_scene)
            
    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)
        self.player2.handle_key_release(key)