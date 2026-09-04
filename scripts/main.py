import arcade
from global_func import *
from start_view import StartView

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT

def execute():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, title="Rain swords 2.0", resizable=True)
    
    start_view = StartView()

    window.show_view(start_view)
    
    arcade.run()

if __name__ == "__main__":
    execute()