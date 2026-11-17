import arcade
from global_func import *
from block import *
from player import *

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT

class GameSceneBase(arcade.View):
    def __init__(
        self,
        scores=(0, 0),
        last_winner=None,
        crown_position=None,
        crown_owner_index=None,
    ):
        super().__init__()

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.stop_game : bool = False
        self.scores = list(scores)
        self.last_winner = last_winner
        self.match_over = False
        self.match_elapsed = 0.0
        self.match_winner = None
        self.match_camera_start = None
        self.match_camera_target = None
        self.respawn_timers = {}
        self.respawn_delay = 3.0
        self.announcement_elapsed = 0.0

        self.player_list : arcade.SpriteList[Player]= arcade.SpriteList()
        self.sword_list : arcade.SpriteList[Sword] = arcade.SpriteList()
        self.list_blocks : arcade.SpriteList[Block]= arcade.SpriteList()
        self.cloud_list : arcade.SpriteList = arcade.SpriteList()
        self.castle_list : arcade.SpriteList = arcade.SpriteList()
        self.player1_castle = None
        self.player2_castle = None
        self.player_sword = None
        self.player2_sword = None

        self.cam = arcade.Camera2D()
        self.start_camera_zoom = self.cam.zoom
        self.cam.position = (SCREEN_WIDTH * 3, SCREEN_HEIGHT / 2)

        self.cam_gui = arcade.Camera2D()

        self.player = Player()
        self.player2 = Player(numb_one=False)

        self.player.position, self.player2.position = self.set_players_pos()

        self.player_list.append(self.player)
        self.player_list.append(self.player2)

        self.GRAVITY = 0.5
        self.CROWN_GRAVITY = 600.0
        
        self.set_blocks()
        self.set_elements()

        crown_x, crown_y = crown_position or (
            SCREEN_WIDTH * 3,
            SCREEN_HEIGHT / 2,
        )
        self.crown = arcade.SpriteSolidColor(
            36,
            12,
            center_x=crown_x,
            center_y=crown_y,
            color=arcade.color.GOLD,
        )
        self.crown_list = arcade.SpriteList()
        self.crown_list.append(self.crown)
        self.crown_owner = (
            (self.player, self.player2)[crown_owner_index]
            if crown_owner_index is not None
            else None
        )
        self.crown.change_x = 0
        self.crown.change_y = 0

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

    def update_crown(self, delta_time, allow_pickup=True):
        if self.crown_owner is not None:
            self.crown.center_x = self.crown_owner.center_x
            self.crown.center_y = self.crown_owner.top + self.crown.height / 2
            return

        self.crown.change_y -= self.CROWN_GRAVITY * delta_time
        self.crown.center_x += self.crown.change_x * delta_time
        self.crown.center_y += self.crown.change_y * delta_time

        for block in arcade.check_for_collision_with_list(self.crown, self.list_blocks):
            if self.crown.change_y < 0:
                self.crown.bottom = block.top
                self.crown.change_y = 0
            break

        if allow_pickup:
            for player in self.player_list:
                if arcade.check_for_collision(self.crown, player):
                    self.crown_owner = player
                    self.crown.change_x = 0
                    self.crown.change_y = 0
                    break

    def crown_owner_index(self):
        if self.crown_owner == self.player:
            return 0
        if self.crown_owner == self.player2:
            return 1
        return None

    def update_respawns(self, delta_time):
        for player, time_left in tuple(self.respawn_timers.items()):
            time_left -= delta_time
            if time_left > 0:
                self.respawn_timers[player] = time_left
                continue

            camera_x = self.cam.position[0]
            camera_half_width = self.window.width / (2 * self.cam.zoom)
            if player == self.player:
                spawn_x = camera_x - camera_half_width + 64
                facing_direction = 1
            else:
                spawn_x = camera_x + camera_half_width - 64
                facing_direction = -1

            ground = min(
                self.list_blocks,
                key=lambda block: abs(block.center_x - spawn_x),
            )
            player.respawn(
                (spawn_x, ground.top + player.height / 2 + 8),
                facing_direction,
            )
            self.equip_respawned_player(player)
            self.player_list.append(player)
            del self.respawn_timers[player]

    def equip_respawned_player(self, player):
        sword = self.player_sword if player == self.player else self.player2_sword
        if sword is None:
            return

        other_player = self.player2 if player == self.player else self.player
        if other_player.sword == sword:
            other_player.sword = None

        player.sword = sword
        sword.set_carried(player.facing_direction)
        sword.carried(player.center_x, player.center_y)

    def on_update(self, delta_time):
        if self.match_over:
            self.match_elapsed += delta_time
            zoom_progress = min(self.match_elapsed / 0.5, 1.0)
            self.cam.zoom = self.start_camera_zoom * (1.0 + zoom_progress)
            if (
                self.match_camera_start is not None
                and self.match_camera_target is not None
            ):
                camera_x, camera_y = self.match_camera_start
                target_x, target_y = self.match_camera_target
                self.cam.position = (
                    camera_x + (target_x - camera_x) * zoom_progress,
                    camera_y + (target_y - camera_y) * zoom_progress,
                )

            if self.match_elapsed >= 2.0:
                self.window.show_view(
                    type(self)(
                        scores=self.scores,
                        last_winner=self.match_winner,
                        crown_position=(self.crown.center_x, self.crown.center_y),
                        crown_owner_index=self.crown_owner_index(),
                    )
                )
            return

        if self.last_winner is not None:
            self.announcement_elapsed += delta_time

        if not self.stop_game:
            return   
        
        self.update_respawns(delta_time)
        self.player_list.update(delta_time)
        self.sword_list.update(delta_time)

        self.physics_engine.update()
        self.physics_engine2.update()
        self.update_crown(delta_time)
        if self.crown_owner is not None:
            camera_progress = min(delta_time * 5.0, 1.0)
            camera_x, camera_y = tuple(self.cam.position)
            self.cam.position = (
                camera_x
                + (self.crown_owner.center_x - camera_x) * camera_progress,
                camera_y,
            )

        if self.check_castle_victory():
            return

        for sword in self.sword_list:
            if sword.state == State_S.THROWN:
                for player in self.player_list:
                    if (
                        player.is_defending()
                        and arcade.check_for_collision(sword, player.sword)
                    ):
                        sword.set_idle()
                        break

            for sword2 in self.sword_list:
                if sword2 == sword:
                    continue

                if (
                    sword.state == State_S.THROWN
                    and sword2.state == State_S.THROWN
                    and arcade.check_for_collision(sword, sword2)
                ):
                    sword.set_idle()
                    sword2.set_idle()

            for player in arcade.check_for_collision_with_list(sword, self.player_list):
                match sword.state:
                    case State_S.IDLE:
                        if player.sword:
                            continue
                        sword.col_player()
                        
                        player.col_sword(sword)
                    case State_S.THROWN:
                        self.handle_player_death(player)
                        return

            if arcade.check_for_collision_with_list(sword, self.list_blocks):
                sword.set_idle()
                sword.change_y = 0

                    

                    

        #for sword in col_swo_with_pla:
            

        if self.physics_engine.can_jump():
            self.player.recharge_jump()

        if self.physics_engine2.can_jump():
            self.player2.recharge_jump()
        

        
    def handle_player_death(self, loser):
        if loser in self.respawn_timers:
            return

        self.respawn_timers[loser] = self.respawn_delay
        if loser.sword is not None:
            sword = loser.sword
            sword.set_idle()
            loser.sword = None

        if self.crown_owner == loser:
            self.crown_owner = None
            self.crown.center_x = loser.center_x
            self.crown.center_y = loser.top + self.crown.height / 2
            self.crown.change_x = loser.change_x
            self.crown.change_y = 0
        loser.dieded()

    def check_castle_victory(self):
        if (
            self.player in self.player_list
            and self.player1_castle is not None
            and arcade.check_for_collision(self.player, self.player1_castle)
        ):
            self.finish_match(self.player)
            return True

        if (
            self.player2 in self.player_list
            and self.player2_castle is not None
            and arcade.check_for_collision(self.player2, self.player2_castle)
        ):
            self.finish_match(self.player2)
            return True

        return False

    def finish_match(self, winner):
        if self.match_over:
            return

        self.match_over = True
        self.match_winner = 0 if winner == self.player else 1
        self.last_winner = self.match_winner
        self.scores[self.match_winner] += 1
        self.announcement_elapsed = 0.0
        self.match_elapsed = 0.0
        self.match_camera_start = tuple(self.cam.position)
        self.match_camera_target = (winner.center_x, winner.center_y)

    def on_draw(self):
        self.clear()

        self.cam.use()

        self.castle_list.draw()
        self.cloud_list.draw()
        self.player_list.draw()
        self.sword_list.draw()
        self.list_blocks.draw()
        self.crown_list.draw()
        crown_x = self.crown.center_x
        crown_y = self.crown.center_y
        arcade.draw_triangle_filled(
            crown_x - 14, crown_y + 5,
            crown_x - 10, crown_y + 18,
            crown_x - 5, crown_y + 5,
            arcade.color.GOLD,
        )
        arcade.draw_triangle_filled(
            crown_x - 5, crown_y + 5,
            crown_x, crown_y + 20,
            crown_x + 5, crown_y + 5,
            arcade.color.GOLD,
        )
        arcade.draw_triangle_filled(
            crown_x + 5, crown_y + 5,
            crown_x + 10, crown_y + 18,
            crown_x + 14, crown_y + 5,
            arcade.color.GOLD,
        )

        self.cam_gui.use()

        arcade.Text(
            f"Jogador 1: {self.scores[0]}    Jogador 2: {self.scores[1]}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            24,
        ).draw()

        if (
            self.last_winner is not None
            and self.announcement_elapsed < 3.0
        ):
            arcade.Text(
                f"Jogador {self.last_winner + 1} venceu!  "
                f"Placar: {self.scores[0]} - {self.scores[1]}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.WHITE,
                36,
                anchor_x="center",
                anchor_y="center",
            ).draw()

    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        self.player2.handle_key_press(key)

        if key == arcade.key.NUM_5 or key == arcade.key.KEY_5:
            map_scene = type(self)(
                scores=self.scores,
                last_winner=self.last_winner,
                crown_position=(self.crown.center_x, self.crown.center_y),
                crown_owner_index=self.crown_owner_index(),
            )
            self.window.show_view(map_scene)
            
    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)
        self.player2.handle_key_release(key)