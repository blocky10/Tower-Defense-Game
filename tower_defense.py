import pygame
import Player.player as player
import Color.color as color
import Enemy.enemy as enemy
import Towers.tower as tower
from pygame import mixer

from Enemy.enemy import Enemy
from Map.SunnyMeadow.sunny_meadow_map_coordinates import sunny_meadow_bloon_movement
from Map.DeadEnd.dead_end_map_coordinates import dead_end_bloon_movement
from Map.SunnyMeadow.sunny_meadow_obstacle_coordinates import sunny_meadow_obstacle_position
from Map.DeadEnd.dead_end_map_obstacle_coordinates import dead_end_obstacle_position
from rounds import easy_map_rounds
from CatPanel.CatPanelButton import Button
import constants 

import sys
import math
import os
from heapq import heappush, heapify

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
mixer.init()
screen = pygame.display.set_mode([constants.SCREEN_RESOLUTION_WIDTH, constants.SCREEN_RESOLUTION_HEIGHT])

# Using global variable since pygame is single threaded, and will not cause race condition
# This is used to store the list of coordinates to move the enemy
enemy_movement_instructions = []
# This is used to save the obstacle positions of the map field and towers 
obstacle_positions = []
# This is used to display the enemies of each round
rounds = []

class TowerDefenseGame:
    def __init__(self, screen):
        self.screen = screen
        self.play_status = False
        self.round_started = False
        self.enemy_round_counter = 0
        self.selected_tower = None
        self.upgrade_tower = None
        self.upgrade_button = None
        self.sell_icon = None
        self.font = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 45)
        self.font3 = pygame.font.Font(None, 36)
        self.font4 = pygame.font.Font(None, 24)
        self.font5 = pygame.font.Font(None, 180)
        self.target_button = None
        self.current_enemy_count = 0
        self.play_again = None


    def main_menu(self):
        """
        This function is used to display the main menu
        :return:
        """
        main_menu_background = pygame.image.load("Menu/main_menu.jpg")
        main_menu_background = pygame.transform.scale(main_menu_background, (constants.SCREEN_RESOLUTION_WIDTH,
                                                      constants.SCREEN_RESOLUTION_HEIGHT))

        play_button_img = pygame.image.load('Menu/play_button.png').convert_alpha()
        self.play_button = Button(480, 600, play_button_img, 2)

        exit_button_img = pygame.image.load("Menu/exit_button.png").convert_alpha()
        self.exit_button = Button(40, 650, exit_button_img, 1.5)

        main_menu_song = mixer.Sound("Audio/Main_Menu_Music.mp3")
        main_menu_song.play(loops=constants.MAXIMUM_SONG_LOOP_TIME)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.draw(self.screen):
                        running = False
                    elif self.exit_button.draw(self.screen):
                        running = False
                        sys.exit()

            self.screen.blit(main_menu_background, (0, 0))

            self.play_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            
            pygame.display.update()

        main_menu_song.stop()
        self.map_menu()

    def map_menu(self):
        """
        This function is used to display the map menu
        :return:
        """
        sunny_meadow_img = pygame.image.load("Map/SunnyMeadow/Sunny_Meadow.jpg").convert_alpha()
        self.sunny_meadow_button = Button(40,100, sunny_meadow_img, 0.5)
        self.sunny_meadow_button.draw(self.screen)

        dead_end_img = pygame.image.load("Map/DeadEnd/dead_end.jpg").convert_alpha()
        self.dead_end_button = Button(400, 100, dead_end_img, 0.5)
        self.dead_end_button.draw(self.screen)

        back_button_img = pygame.image.load("Menu/exit_button.png").convert_alpha()
        self.back_button = Button(40, 650, back_button_img, 1.5)

        map_menu_song = mixer.Sound("Audio/map_menu_music.mp3")
        map_menu_song.play(loops=constants.MAXIMUM_SONG_LOOP_TIME)

        map_name = ""
        play_map = False
        main_menu_clicked = False
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sunny_meadow_button.draw(self.screen):
                        map_name = constants.SUNNY_MEADOW_MAP
                        running = False
                        play_map = True

                    if self.dead_end_button.draw(self.screen):
                        map_name = constants.DEAD_END_MAP
                        running = False
                        play_map = True

                    if self.back_button.draw(self.screen):
                        running = False
                        main_menu_clicked = True

            self.screen.fill((213, 225, 241))

            sunny_meadow_text = self.font.render("Sunny Meadow", True, (0, 0, 0))
            self.screen.blit((sunny_meadow_text), (40, 40))

            sunny_meadow_difficulty = self.font.render("Easy", True, (0, 0, 0))
            self.screen.blit((sunny_meadow_difficulty), (120, 380))

            dead_end_difficulty = self.font.render("Hard", True, (0, 0, 0))
            self.screen.blit((dead_end_difficulty), (560, 400))      
            
            dead_end_text = self.font.render("Dead End", True, (0, 0, 0))
            self.screen.blit((dead_end_text), (510, 40))

            self.sunny_meadow_button.draw(self.screen)
            self.dead_end_button.draw(self.screen)
            self.back_button.draw(self.screen)

            pygame.display.update()

        map_menu_song.stop()

        if play_map:
            self.start_tower_defense_game(map_name)
        elif main_menu_clicked:
            self.main_menu()

    def start_tower_defense_game(self, map_name):
        """
        This function is used to start the tower defense game for any map
        :param: map_name: The map to play for tower defense
        :return:
        """
        global obstacle_positions, enemy_movement_instructions, rounds
        
        song = mixer.Sound("Audio/Fiesta_Flamenco.mp3")
        song.play(loops=constants.MAXIMUM_SONG_LOOP_TIME)

        # Create an FPS clock
        clock = pygame.time.Clock()

        # Configure the obstacle and enemy movement based off the map that has been selected
        if map_name == constants.SUNNY_MEADOW_MAP:
            enemy_movement_instructions = sunny_meadow_bloon_movement
        elif map_name == constants.DEAD_END_MAP:
            enemy_movement_instructions = dead_end_bloon_movement

        if map_name == constants.SUNNY_MEADOW_MAP:
            for obstacle in sunny_meadow_obstacle_position:
                obstacle_positions.append(obstacle)
        elif map_name == constants.DEAD_END_MAP:
            for obstacle in dead_end_obstacle_position:
                obstacle_positions.append(obstacle)

        rounds = easy_map_rounds

        # Set the timer for enemy spawn 
        pygame.time.set_timer(pygame.USEREVENT, 500)

        # All groups for pygame objects
        enemy_group = pygame.sprite.Group()
        tower_group = pygame.sprite.Group()
        weapon_group = pygame.sprite.Group()

        tower_defense_player = player.Player(cash=650, lives=50, round=1)

        replay_map = False
        main_menu = False

        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # User event for the delay
                elif event.type == pygame.USEREVENT:
                    # If we click the play button, then start the round
                    self.play_round(tower_defense_player, enemy_group)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if tower_defense_player.get_lives() > 0 and tower_defense_player.get_round() < 31:
                        # If the play button is selected, then set the play status to true and allow for the round to play
                        if self.start_button.draw(self.screen):
                            self.play_status = True
                        else:
                            # Selecting tower from the Cat Panel to drag and drop
                            self.select_tower(tower_defense_player, tower_group)

                        # This is used to handle the upgrade tower case
                        self.upgrade_tower_stats(tower_group, tower_defense_player)
                    else:
                        if self.play_again.draw(self.screen):
                            self.reset_round_stats(tower_group, enemy_group, weapon_group)
                            running = False
                            replay_map = True
                        elif self.back_to_main_menu.draw(self.screen):
                            self.reset_round_stats(tower_group, enemy_group, weapon_group)
                            running = False
                            main_menu = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.place_tower(tower_defense_player, tower_group)
            
            # Load the sunny meadow map background onto the existing screen
            self.load_background(map_name=map_name)

            if tower_defense_player.get_lives() > 0:
                # Update the tower position when dragging tower across the screen
                self.update_tower_pos()
                # This is used for tower firing in tower defense
                self.fire_bullet(weapon_group, tower_group, enemy_group, tower_defense_player)
                # This function is used to perform tower upgrade
                self.perform_tower_upgrade()
                
            # Update the position of the enemy, tower, weapon and display it onto the screen
            enemy_group.update(enemy_group, tower_defense_player)
            weapon_group.update()
            enemy_group.draw(self.screen)
            tower_group.draw(self.screen)
            weapon_group.draw(self.screen)

            if tower_defense_player.get_lives() == 0 or tower_defense_player.get_round() == constants.FINAL_ROUND:
                end_game_text = "Game Over!" if tower_defense_player.get_lives() == 0 else "You Win!"
                end_game_status_text = self.font5.render(end_game_text, True, (255, 255, 255))

                self.screen.blit((end_game_status_text), (200 + (11 - len(end_game_text)) * 32, 160))
                play_again = pygame.image.load("Menu/play_again.jpg").convert_alpha()
                
                self.play_again = Button(380, 300, play_again, 1)
                self.play_again.draw(self.screen)
                back_to_main_menu = pygame.image.load("Menu/back_to_main_menu.jpg").convert_alpha()
                self.back_to_main_menu = Button(430, 400, back_to_main_menu, 0.7)
                self.back_to_main_menu.draw(self.screen)
            
            self.display_player_stats(player=tower_defense_player)

            # Display the tower defense game on the screen
            pygame.display.flip()
            clock.tick(1000)

        song.stop()

        if main_menu:
            self.main_menu()
        elif replay_map:
            self.start_tower_defense_game(map_name=map_name)

    def load_background(self, map_name):
        """
        This function is used to load the background
        :param: map_name: The map to load the background off
        """
        map_image = ""
        if map_name == "sunny_meadow":
            map_image = "SunnyMeadow/Sunny_Meadow"
        elif map_name == "dead_end":
            map_image = "DeadEnd/dead_end"

        Sunny_Meadow = pygame.image.load("map/" + map_image + ".jpg")
        Sunny_Meadow = pygame.transform.scale(Sunny_Meadow, (constants.SCREEN_RESOLUTION_WIDTH - 200,
                                                             constants.SCREEN_RESOLUTION_HEIGHT))
        self.screen.blit(Sunny_Meadow, (0, 0))

        pygame.draw.rect(self.screen, (185, 122, 87), pygame.Rect(1000, 0, 200, 1000))

        play_button_img = pygame.image.load('CatPanel/playbutton.jpg').convert_alpha()
        self.start_button = Button(1040, 650, play_button_img, 0.25)
        self.start_button.draw(self.screen)
        
        monkey_button_img = pygame.image.load('CatPanel/DartCat.jpg').convert_alpha()
        self.monkey_button = Button(1035, 60, monkey_button_img, 0.23)
        self.monkey_button.draw(self.screen)

        monkey_button_2_img = pygame.image.load('CatPanel/MachoCat.jpg').convert_alpha()
        self.monkey_button_2 = Button(1025, 310, monkey_button_2_img, 0.17)
        self.monkey_button_2.draw(self.screen)

        price = self.font.render("$250", True, (255, 255, 255))
        self.screen.blit((price), (1060, 216))

        name = self.font.render("Dart Cat", True, (255, 255, 255))
        self.screen.blit((name), (1030, 20))

        price2 = self.font.render("$600", True, (255, 255, 255))
        self.screen.blit((price2), (1060, 430))

        name2 = self.font2.render("Macho Cat", True, (255, 255, 255))
        self.screen.blit((name2), (1025, 270))

    def reset_round_stats(self, tower_group, enemy_group, weapon_group):
        """
        This function is used to reset the round statistics
        :param: tower_group: The list of towers
        :param: enemy_group: The list of enemies
        :param: weapon_group: The list of weapons
        :return:
        """
        global obstacle_positions
        for tower in tower_group:
            tower_group.remove(tower)

        for enemy in enemy_group:
            enemy_group.remove(enemy)

        for weapon in weapon_group:
            weapon_group.remove(weapon)

        self.enemy_round_counter = 0
        self.current_enemy_count = 0
        self.play_status = False
        self.round_started = False
        obstacle_positions.clear()

    def play_round(self, tower_defense_player, enemy_group):
        """
        This function will play the round for the tower defense game
        :param: tower_defense_player: The tower defense player
        :param: enemy_group: The group that stores all of our enemies on the track 
        :return:
        """

        # Checks if the play button has been clicked
        if self.play_status:
            self.round_started = True
            self.play_status = False

        # If the round has started and there are still enemies left, add the enemies to the track
        if self.round_started and tower_defense_player.get_round() <= len(rounds) \
        and self.enemy_round_counter < len(rounds[tower_defense_player.get_round() - 1]):
            # If the number of bloons haven't finished processing yet, keep processing the enemies
            enemy = rounds[tower_defense_player.get_round() - 1][self.enemy_round_counter]
 
            if self.current_enemy_count >= enemy[constants.NUMBER_OF_ENEMIES]:
                self.enemy_round_counter += 1
                self.current_enemy_count = 0
            else:
                enemy_group.add(Enemy(checkpoints=enemy_movement_instructions,
                                      enemy_image=enemy[constants.ENEMY_IMAGE], 
                                      number_of_enemies=1, 
                                      enemy_health=enemy[constants.ENEMY_HEALTH],
                                      speed=enemy[constants.ENEMY_SPEED],  
                                      distance_travelled=0,
                                      scale_factor=enemy[constants.ENEMY_IMAGE_SIZE]))
                self.current_enemy_count += 1

        # If the total number of enemies is equal to 0, then move on to the next round and update the play status to true
        if len(enemy_group) == 0 and self.round_started == True:
            tower_defense_player.update_round(tower_defense_player.get_round() + 1)
            tower_defense_player.update_cash(tower_defense_player.get_cash() + 200)
            self.round_started = False
            self.enemy_round_counter = 0
            self.current_enemy_count = 0

    def can_place_tower(self, coordinate_start_x, coordinate_end_x, coordinate_start_y, coordinate_end_y):
        """
        This function is used to check if we can place a tower based off the (x1, y1) -> (x2, y2) coordinates
        :param: coordinate_start_x: The starting coordinate x of the boundary to check for placing the tower
        :param: coordinate_end_x: The ending coordinate x of the boundary to check for placing the tower
        :param: coordinate_start_y: The starting coordinate y of the boundadry to check for placing the tower
        :param: coordinate_end_y: The ending coordinate y of the boundary to check for placing the tower
        :return: True if we can place a tower otherwise False
        """
        global obstacle_positions
        top_left_boundary = 0
        bottom_right_boundary = 1
        coordinate_x_idx = 0
        coordinate_y_idx = 1
        #
        #           |<------------->|
        #  |<------------>|
        #  1        3     5         8
        #
        # When placing a tower, we need to check if there is an overlap. If there is an overlap
        # then the overlap distance must be greater than 0
        #
        # To find overlapping distance, we need to take end point of the lower component and the starting
        # position of the upper component 
        #
        # In the diagram above we take the overlapping distance, the maximum point of the lower component is 
        # 5 and the minimum of the upper component is 3
        #
        # Since the difference between the components (5 - 3) is 2, then we must have an overlap

        for obstacle in obstacle_positions:
            overlapping_x_distance = min(coordinate_end_x, obstacle[bottom_right_boundary][coordinate_x_idx]) - \
                                     max(coordinate_start_x, obstacle[top_left_boundary][coordinate_x_idx])
            overlapping_y_distance = min(coordinate_end_y, obstacle[bottom_right_boundary][coordinate_y_idx]) - \
                                     max(coordinate_start_y, obstacle[top_left_boundary][coordinate_y_idx])
            
            # If there is an overlap, then we can't place the towers
            if overlapping_x_distance >= 0 and overlapping_y_distance >= 0:
                return False
        
        return True

    def find_sell_tower_coordinates(self, coordinate_start_x, coordinate_end_x, coordinate_start_y, coordinate_end_y):
        """
        This function is used to find the coordinates of the selling tower in case of an offset
        :param: coordinate_start_x: The starting x coordinate to find for the tower to sell
        """
        global obstacle_positions
        top_left_boundary = 0
        bottom_right_boundary = 1
        coordinate_x_idx = 0
        coordinate_y_idx = 1
        coordinates = (0, 0)
        maximum_distance = 0
        for obstacle in obstacle_positions:
            overlapping_x_distance = min(coordinate_end_x, obstacle[bottom_right_boundary][coordinate_x_idx]) - \
                                     max(coordinate_start_x, obstacle[top_left_boundary][coordinate_x_idx])
            overlapping_y_distance = min(coordinate_end_y, obstacle[bottom_right_boundary][coordinate_y_idx]) - \
                                     max(coordinate_start_y, obstacle[top_left_boundary][coordinate_y_idx])

            if overlapping_x_distance + overlapping_y_distance > maximum_distance:
                coordinates = ((obstacle[top_left_boundary][coordinate_x_idx], obstacle[top_left_boundary][coordinate_y_idx]), 
                               (obstacle[bottom_right_boundary][coordinate_x_idx], obstacle[bottom_right_boundary][coordinate_y_idx]))
                maximum_distance = overlapping_x_distance + overlapping_y_distance

        return coordinates

    def select_tower(self, tower_defense_player, tower_group):
        """
        This function is used to select a tower to drag and drop onto the screen
        :param: tower_defense_player: The tower defense player
        :param: tower_group: The tower group that stores a list of towers that we have placed
        """
        position_x = 0
        position_y = 1

        # If our cash is greater than $200, then we can place the monkey down
        if self.monkey_button.draw(self.screen) and tower_defense_player.get_cash() >= constants.DART_CAT_COST:
            mouse_pos = pygame.mouse.get_pos()
            tower_obj = tower.Tower(tower_type=constants.DART_CAT_TOWER_TYPE, 
                                    image=constants.DART_CAT_IMAGE, 
                                    position_x=mouse_pos[position_x], 
                                    position_y=mouse_pos[position_y], 
                                    cost=constants.DART_CAT_COST, 
                                    tower_radius=constants.DART_CAT_TOWER_RADIUS, 
                                    tower_fired=False, 
                                    attack_power=constants.DART_CAT_ATTACK_POWER, 
                                    attack_speed=constants.DART_CAT_ATTACK_SPEED,
                                    upgrade_level=constants.DART_CAT_DEFAULT_LEVEL, 
                                    has_piercing=False, 
                                    sell_price=constants.DART_CAT_SELL_PRICE,
                                    animation_list=[constants.DART_CAT_IMAGE,
                                                    constants.DART_CAT_IMAGE,
                                                    constants.DART_CAT_IMAGE,
                                                    constants.DART_CAT_IMAGE])
            tower_group.add(tower_obj)
            self.selected_tower = tower_obj
        elif self.monkey_button_2.draw(self.screen) and tower_defense_player.get_cash() >= constants.MACHO_CAT_COST:
            mouse_pos = pygame.mouse.get_pos()
            tower_obj = tower.Tower(tower_type=constants.MACHO_CAT_TOWER_TYPE, 
                                    image=constants.MACHO_CAT_IMAGE, 
                                    position_x=mouse_pos[position_x], 
                                    position_y=mouse_pos[position_y], 
                                    cost=constants.MACHO_CAT_COST, 
                                    tower_radius=constants.MACHO_CAT_TOWER_RADIUS, 
                                    tower_fired=False, 
                                    attack_power=constants.MACHO_CAT_ATTACK_POWER,
                                    attack_speed=constants.MACHO_CAT_ATTACK_SPEED,
                                    upgrade_level=constants.MACHO_CAT_DEFAULT_LEVEL, 
                                    has_piercing=False, 
                                    sell_price=constants.MACHO_CAT_SELL_PRICE,
                                    animation_list=[constants.MACHO_CAT_IMAGE, 
                                                    constants.MACHO_CAT_IMAGE,
                                                    constants.MACHO_CAT_IMAGE,
                                                    constants.MACHO_CAT_IMAGE])
            tower_group.add(tower_obj)
            self.selected_tower = tower_obj

    def place_tower(self, tower_defense_player, tower_group):
        """
        This function is used to place the tower onto the screen if possible
        :param: tower_defense_player: The tower defense player
        :param: tower_group: The tower group object that stores a list of towers that we have placed
        :return:
        """
        position_x = 0
        position_y = 1
        mouse_pos = pygame.mouse.get_pos()
        if self.selected_tower != None:
            if self.can_place_tower(coordinate_start_x=mouse_pos[position_x]-(self.selected_tower.get_tower_width() // 4), 
                                    coordinate_end_x=mouse_pos[position_x]+(self.selected_tower.get_tower_width() // 4),
                                    coordinate_start_y=mouse_pos[position_y]-(self.selected_tower.get_tower_height() // 4),
                                    coordinate_end_y=mouse_pos[position_y]+(self.selected_tower.get_tower_height() // 4)):
                tower_defense_player.update_cash(tower_defense_player.get_cash() - self.selected_tower.get_cost())
                obstacle_positions.append([self.selected_tower.get_tower_top_left_position(),
                                           self.selected_tower.get_tower_bottom_right_position()])
                self.selected_tower = None
            else:
                tower_group.remove(self.selected_tower)
                self.selected_tower = None

    def update_tower_pos(self):
        """
        This function is used to update the tower position when dragging and dropping
        :return:
        """
        position_x = 0
        position_y = 1
        if self.selected_tower != None:
            mouse_pos = pygame.mouse.get_pos()
            self.selected_tower.update_tower_drag_and_drop_pos(self.screen, mouse_pos[position_x], mouse_pos[position_y], 
                                            self.can_place_tower(coordinate_start_x=mouse_pos[position_x]-(self.selected_tower.get_tower_width() // 4), 
                                                                coordinate_end_x=mouse_pos[position_x]+(self.selected_tower.get_tower_width() // 4),
                                                                coordinate_start_y=mouse_pos[position_y]-(self.selected_tower.get_tower_height() // 4),
                                                                coordinate_end_y=mouse_pos[position_y]+(self.selected_tower.get_tower_height() // 4)))

    def fire_bullet(self, weapon_group, tower_group, enemy_group, tower_defense_player):
        """
        This function is used to fire a bullet
        :param: weapon_group: The group of weapons
        :param: tower_group: The group of the tower
        :param: tower_defense_player: The tower defense player
        """
        # Can be a minimum and maximum heap depending on the purpose, targeting closest, first will use
        # a min heap but last and closest will use a max heap
        heap = []
        heapify(heap)

        for towers in tower_group:
            if towers != self.selected_tower:
                for enemy in enemy_group:
                    # If the tower is still in the process of firing don't search for the enemies
                    if towers.tower_fired():
                        break

                    if towers.is_enemy_in_radius(enemy.get_enemy_position_x(), enemy.get_enemy_position_y()):
                        # If the tower hasn't fire yet, create a bullet otherwise move the bullet to attack the enemy
                        if towers.get_target() == "target_first":
                            heappush(heap, (enemy.get_enemy_distance_travelled() * -1, (enemy.get_enemy_position_x(), enemy.get_enemy_position_y())))
                        elif towers.get_target() == "target_last":
                            heappush(heap, (enemy.get_enemy_distance_travelled(), (enemy.get_enemy_position_x(), enemy.get_enemy_position_y())))
                        elif towers.get_target() == "target_closest":
                            distance = math.sqrt((enemy.get_enemy_position_x() - towers.get_tower_position_x()) ** 2 + 
                                                 (enemy.get_enemy_position_y() - towers.get_tower_position_y()) ** 2)
                            heappush(heap, ((distance, enemy.get_enemy_distance_travelled()), (enemy.get_enemy_position_x(), enemy.get_enemy_position_y())))
                        elif towers.get_target() == "target_strongest":
                            heappush(heap, ((-1 * enemy.get_enemy_health(), enemy.get_enemy_distance_travelled()), 
                                     (enemy.get_enemy_position_x(), enemy.get_enemy_position_y())))

                # If we're not firing, check for the coordinates to fire
                if not towers.tower_fired():
                    enemy_to_pop_coordinates = (0, 0)
                    highest_priority_pop_idx = 0
                    pop_coordinate_idx = 1
                    # If there is a enemy to pop then search the heap for an element to pop otherwise continue to the next tower
                    if len(heap) > 0:
                        enemy_to_pop_coordinates = heap[highest_priority_pop_idx][pop_coordinate_idx]
                    else:
                        continue

                weapon_image = "Towers/tower_img/Paw.jpg"
                if not towers.tower_fired():
                    towers.create_bullet(weapon_image, weapon_group, enemy_to_pop_coordinates[0], 
                                         enemy_to_pop_coordinates[1])
                else:
                    towers.fire_bullet(weapon_group, enemy_group, tower_defense_player, self.screen)
                
                heap.clear()

    def upgrade_tower_stats(self, tower_group, tower_defense_player):
        """
        This function is used to upgrade towers
        :param: tower_group: The tower group that contains the list of towers
        :param: tower_defense_player: The player who is playing tower defense
        :return:
        """
        global obstacle_positions
        position_x = 0
        position_y = 1
        if self.selected_tower == None:
            has_tower = False
            for tower in tower_group.sprites():
                top_left_corner = tower.get_tower_top_left_position()
                bottom_right_corner = tower.get_tower_bottom_right_position()
                mouse_pos = pygame.mouse.get_pos()

                if self.upgrade_button != None and self.upgrade_button.draw(self.screen):
                    self.upgrade_tower.upgrade_tower(tower_defense_player)
                    has_tower = True
                    break

                if self.target_button != None and self.target_button.draw(self.screen):
                    self.upgrade_tower.update_target() 
                    has_tower = True
                    break

                if self.sell_icon != None and self.sell_icon.draw(self.screen):
                    tower_defense_player.update_cash(tower_defense_player.get_cash() + self.upgrade_tower.get_sell_price())
                    sell_coordinates = self.find_sell_tower_coordinates(self.upgrade_tower.get_tower_top_left_position()[position_x],
                                                                        self.upgrade_tower.get_tower_bottom_right_position()[position_x], 
                                                                        self.upgrade_tower.get_tower_top_left_position()[position_y], 
                                                                        self.upgrade_tower.get_tower_bottom_right_position()[position_y])
                    obstacle_positions.remove([sell_coordinates[position_x], sell_coordinates[position_y]])
                    tower_group.remove(self.upgrade_tower)
                    self.upgrade_tower = None
                    break

                if (mouse_pos[position_x] >= top_left_corner[position_x] and mouse_pos[position_x] <= bottom_right_corner[position_x]) \
                and (mouse_pos[position_y] >= top_left_corner[position_y] and mouse_pos[position_y] <= bottom_right_corner[position_y]):
                    self.upgrade_tower = tower
                    has_tower = True
                    break

            if not has_tower:
                self.upgrade_tower = None

    def perform_tower_upgrade(self):
        """
        This function is used to perform tower upgrade
        """
        if self.upgrade_tower:
            self.upgrade_tower.select_upgrade_tower(self.screen)
            upgrade_image = ""
            upgrade_text = ""
            upgrade_price = ""
            if self.upgrade_tower.get_tower_upgrade_level() == 0:
                upgrade_image = "Towers/tower_upgrades/AttackSpeed.jpg"
                upgrade_text = "Increased attack speed"
                upgrade_price = "$200"
            elif self.upgrade_tower.get_tower_upgrade_level() == 1:
                upgrade_image = "Towers/tower_upgrades/Range.jpg"
                upgrade_text = "Increased attack range"
                upgrade_price = "$400"
            elif self.upgrade_tower.get_tower_upgrade_level() == 2:
                upgrade_image = "Towers/tower_upgrades/extra_damage.jpg"
                upgrade_text = "Increased attack damage"
                upgrade_price = "$800"
            elif self.upgrade_tower.get_tower_upgrade_level() == 3:
                upgrade_image = "Towers/tower_upgrades/Piercing.jpg"
                upgrade_text = "Increased piercing"
                upgrade_price = "$1200"
            else:
                upgrade_image = "Towers/tower_upgrades/maxed_out.jpg"
                upgrade_text = "Maxed out!"
                
            upgrade_font = self.font4.render(upgrade_text, True, (255, 255, 255))
            upgrade_price = self.font4.render(upgrade_price, True, (255, 255, 255))
            self.screen.blit(upgrade_font, (1010 + (22 - len(upgrade_text)) * 4, 485))
            self.screen.blit(upgrade_price, (1080, 630))

            upgrade_img = pygame.image.load(upgrade_image).convert_alpha()
            self.upgrade_button = Button(1025, 505, upgrade_img, 0.35)
            self.upgrade_button.draw(self.screen)
            sell_icon = pygame.image.load("Towers/tower_img/Sell_icon.jpg").convert_alpha()
            self.sell_icon = Button(25, 700, sell_icon, 0.35)
            self.sell_icon.draw(self.screen)
            upgrade = self.font4.render("Upgrades", True, (255, 255, 255))
            self.screen.blit(upgrade, (1060, 465))
            sell_price = self.font2.render("$" + str(self.upgrade_tower.get_sell_price()), True, (255, 255, 255))
            self.screen.blit(sell_price, (50, 660))
            target_button = pygame.image.load("Towers/tower_target/" + self.upgrade_tower.get_target() + ".jpg").convert_alpha()
            self.target_button = Button(785, 700, target_button, 0.75)
            self.target_button.draw(self.screen)


    def display_player_stats(self, player):
        """
        This function is used to display the player statistics cash, lives and rounds
        :param: player: The tower defense player
        :return:
        """
        player_cash = self.font3.render("$" + str(player.get_cash()), True, color.RED)
        player_lives = self.font3.render("Lives:" + str(player.get_lives()), True, color.RED)
        player_round = self.font3.render("Round:" + str(player.get_round()), True, color.RED)

        self.screen.blit(player_cash, (850, 70))
        self.screen.blit(player_lives, (850, 110))
        self.screen.blit(player_round, (850, 30))

    
if __name__ == "__main__":
    tower_defense = TowerDefenseGame(screen)
    tower_defense.main_menu()