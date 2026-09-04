import arcade
from map_1 import Map_1

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT

class StartView(arcade.View):
    def __init__(self, window = None, background_color = arcade.color.GRAY):
        super().__init__(window, background_color)
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_text(
            text="Pressione Enter para jogar",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            color=arcade.color.GREEN,
            font_size=100,
            anchor_x="center",
            anchor_y="center",
        )
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.J or key == arcade.key.ENTER:
            game_scene = Map_1()
            self.window.show_view(game_scene)