import pygame
import player
import color
import balloon
import tower
import time
import random

SCREEN_RESOLUTION_WIDTH = 1200
SCREEN_RESOLUTION_HEIGHT = 800



obstacle_position = [
    [(0, 364), (300, 436)],
    [(200, 73), (300, 364)],
    [(300, 73), (500, 146)],
    [(400, 146), (500, 581)],
    [(100, 509), (400, 581)],
    [(100, 581), (200, 727)],
    [(200, 655), (900, 727)],
    [(800, 437), (900, 655)],
    [(600, 437), (800, 509)],
    [(600, 145), (700, 437)],
    [(700, 145), (1000, 218)],
    [(1000, 0), (1200, 1000)]
]




#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		# Get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class TowerDefenseGame:
    def __init__(self, screen, background_color):
        self.screen = screen
        self.background_colour = background_color
        self.play_status = False
        self.round_started = False
        self.balloon_round_counter = 0
        self.rounds = [
        #    [balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
        #     balloon_speed_x=5, balloon_speed_y=5, position_x=0, position_y=400),
        #     balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
        #     balloon_speed_x=4, balloon_speed_y=4, position_x=-10, position_y=400),
        #     balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
        #     balloon_speed_x=3, balloon_speed_y=3, position_x=-20, position_y=400)
        #     ],
            [balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
             balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
             balloon_speed_x=10, balloon_speed_y=10, position_x=0, position_y=400),
            ],
            [
                balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=3,
                balloon_speed_x=3, balloon_speed_y=3, position_x=0, position_y=400),
                balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=4,
                balloon_speed_x=4, balloon_speed_y=4, position_x=0, position_y=400),
                balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=1,
                balloon_speed_x=10, balloon_speed_y=3, position_x=0, position_y=400)
            ]  
]
        
    def start_tower_defense_game_sunny_meadow(self):
        pygame.init()

        clock = pygame.time.Clock()
        # Set the timer for balloon spawn 
        pygame.time.set_timer(pygame.USEREVENT, 2000)

        # All groups for pygame objects
        balloon_group = pygame.sprite.Group()
        tower_group = pygame.sprite.Group()
        weapon_group = pygame.sprite.Group()

        tower_defense_player = player.Player(cash=650, lives=100, round=1)

        selected_monkey = None
        position_x = 0
        position_y = 1

        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    # If we click the play button, then start the round
                    self.play_round(tower_defense_player, balloon_group)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.draw(self.screen):
                        self.play_status = True
                    # If our cash is greater than $250, then we can place the monkey down
                    elif self.monkey_button.draw(self.screen) and tower_defense_player.get_cash() > 250:
                        mouse_pos = pygame.mouse.get_pos()
                        tower_obj = tower.Tower(image="Cat_Tower1.jpg", x=mouse_pos[position_x], y=mouse_pos[position_y], cost=250, tower_radius=200, tower_fired=False)
                        tower_group.add(tower_obj)
                        selected_monkey = tower_obj
                    elif self.monkey_button_2.draw(self.screen) and tower_defense_player.get_cash() > 500:
                        mouse_pos = pygame.mouse.get_pos()
                        tower_obj = tower.Tower(image="Cat_Tower3.jpg", x=mouse_pos[position_x], y=mouse_pos[position_y], cost=500, tower_radius=110, tower_fired=False)
                        tower_group.add(tower_obj)
                        selected_monkey = tower_obj
                # If we release the mouse button, then we need to check if we can place the tower, 
                # if we can place the tower then 
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_monkey != None:
                        if self.can_place_tower(coordinate_start_x=mouse_pos[position_x]-(selected_monkey.get_tower_width() // 4), 
                                                coordinate_end_x=mouse_pos[position_x]+(selected_monkey.get_tower_width() // 4),
                                                coordinate_start_y=mouse_pos[position_y]-(selected_monkey.get_tower_height() // 4),
                                                coordinate_end_y=mouse_pos[position_y]+(selected_monkey.get_tower_height() // 4)):
                            obstacle_position.append([(mouse_pos[position_x] - (selected_monkey.get_tower_width() // 2),
                                                      mouse_pos[position_y] - (selected_monkey.get_tower_height() // 2)),
                                                     (mouse_pos[position_x] + (selected_monkey.get_tower_width() // 2),
                                                      (mouse_pos[position_y] + (selected_monkey.get_tower_height() // 2)))])
                            tower_defense_player.update_cash(tower_defense_player.get_cash() - selected_monkey.get_cost())
                            selected_monkey = None
                        else:
                            tower_group.remove(selected_monkey)
                            selected_monkey = None
                     
            self.load_background()
            if (selected_monkey != None):
                 mouse_pos = pygame.mouse.get_pos()
                #  print(selected_monkey.get_tower_width() // 4)
                 selected_monkey.update_tower_pos(self.screen, mouse_pos[position_x], mouse_pos[position_y], 
                                                  self.can_place_tower(coordinate_start_x=mouse_pos[position_x]-(selected_monkey.get_tower_width() // 4), 
                                                                       coordinate_end_x=mouse_pos[position_x]+(selected_monkey.get_tower_width() // 4),
                                                                       coordinate_start_y=mouse_pos[position_y]-(selected_monkey.get_tower_height() // 4),
                                                                       coordinate_end_y=mouse_pos[position_y]+(selected_monkey.get_tower_height() // 4)))

            # If we're not selecting a monkey, then check if our tower group balloon is in radius
            if selected_monkey == None:
                for towers in tower_group:
                    for balloons in balloon_group:
                        if towers.is_balloon_in_radius(balloons.get_balloon_position_x(), balloons.get_balloon_position_y()):
                            # If the tower hasn't fire yet, create a bullet otherwise move the bullet to attack the balloon
                            towers.create_bullet(weapon_group, balloons.get_balloon_position_x(), balloons.get_balloon_position_y())
                            towers.fire_bullet(weapon_group, balloon_group)

            for weapon in weapon_group:
                weapon.update(weapon_group)            


            mouse_pos = pygame.mouse.get_pos()

            # Destroy any balloons that reach the end of the sprites
            for balloon in balloon_group.sprites():
                 if balloon.can_destroy_balloon():
                      balloon_group.remove(balloon)
                      tower_defense_player.update_lives(tower_defense_player.get_lives() - balloon.get_balloon_health())

            balloon_group.update()
            balloon_group.draw(self.screen)
            tower_group.draw(self.screen)
            weapon_group.draw(self.screen)
            self.display_player_stats(player=tower_defense_player)

            # Flip the display
            pygame.display.flip()
            clock.tick(1000)

    def load_background(self):
        """
        This function is used to load the background
        """
        Sunny_Meadow = pygame.image.load("Sunny_Meadow.jpg")
        Sunny_Meadow = pygame.transform.scale(Sunny_Meadow, (1000, SCREEN_RESOLUTION_HEIGHT))
        self.screen.blit(Sunny_Meadow, (0, 0))

        pygame.draw.rect(self.screen, (185, 122, 87), pygame.Rect(1000, 0, 200, 1000))

        play_button_img = pygame.image.load('playbutton.jpg').convert_alpha()
        self.start_button = Button(1040, 630, play_button_img, 0.25)
        self.start_button.draw(self.screen)
        
        monkey_button_img = pygame.image.load('Cat_Tower.jpg').convert_alpha()
        self.monkey_button = Button(1040, 90, monkey_button_img, 0.21)
        self.monkey_button.draw(self.screen)

        monkey_button_2_img = pygame.image.load('Cat_Tower2.jpg').convert_alpha()
        self.monkey_button_2 = Button(1025, 390, monkey_button_2_img, 0.17)
        self.monkey_button_2.draw(self.screen)

        font = pygame.font.Font(None, 50)
        font2 = pygame.font.Font(None, 45)

        price = font.render("$250", True, (255, 255, 255))
        self.screen.blit((price), (1060, 240))

        name = font.render("Dart Cat", True, (255, 255, 255))
        self.screen.blit((name), (1030, 40))

        price2 = font.render("$500", True, (255, 255, 255))
        self.screen.blit((price2), (1060, 520))

        name2 = font2.render("Macho Cat", True, (255, 255, 255))
        self.screen.blit((name2), (1025, 340))

    def play_round(self, tower_defense_player, balloon_group):
        if self.play_status:
            self.round_started = True
            self.play_status = False

        # If the round has started and there are still balloons left, add the balloons to the track
        if self.round_started and tower_defense_player.get_round() <= len(self.rounds) \
        and self.balloon_round_counter < len(self.rounds[tower_defense_player.get_round() - 1]):
            balloon_group.add(self.rounds[tower_defense_player.get_round() - 1][self.balloon_round_counter])
            self.balloon_round_counter += 1

        # If the total number of balloons is equal to 0, then move on to the next round and update the play status to true
        if len(balloon_group) == 0 and self.round_started == True:
            tower_defense_player.update_round(tower_defense_player.get_round() + 1)
            tower_defense_player.update_cash(tower_defense_player.get_cash() + 200)
            self.round_started = False
            self.balloon_round_counter = 0

    def can_place_tower(self, coordinate_start_x, coordinate_end_x, coordinate_start_y, coordinate_end_y):
        """
        This function is used to check if we can place tower based off the mouse position
        :param: mouse_pos: The current mouse position
        """
        top_left_boundary = 0
        bottom_right_boundary = 1
        coordinate_x_idx = 0
        coordinate_y_idx = 1
        #
        #           |<------------->|
        #  |<------------>|
        #  1        3     5         8
        #
        # If there is an overlapping tower with any obstacles, then the maximum distance from the lower boundary must overlap with the 
        # upper boundary
        #
        # Thus we take the maximum of the lower component
        # Which is 5 
        #
        # Then we must take the minimum of the upper boundary
        # Which is 3
        #
        # Thus the overlapping distance is 5 - 3 = 2
        # In this case there is an overlapping segment
        #
        # The reason to do this is to check for whether the tower is overlapping on the playing field
        #
        # print(coordinate_end_x)

        for obstacle in obstacle_position:
            overlapping_x_distance = min(coordinate_end_x, obstacle[bottom_right_boundary][coordinate_x_idx]) - \
                                 max(coordinate_start_x, obstacle[top_left_boundary][coordinate_x_idx])
            overlapping_y_distance = min(coordinate_end_y, obstacle[bottom_right_boundary][coordinate_y_idx]) - \
                                 max(coordinate_start_y, obstacle[top_left_boundary][coordinate_y_idx])
            # If the overlapping distance is less than 0, that means that there is no overlapping components
            if overlapping_x_distance >= 0 and overlapping_y_distance >= 0:
                return False
        
        return True

    def display_player_stats(self, player):
        """
        This function is used to display the player statistics
        Player statistics include cash, lives and round
        :param: player: 
        :return:
        """
        font = pygame.font.Font(None, 36)

        player_cash = font.render("$" + str(player.get_cash()), True, (255, 0, 0))
        player_lives = font.render("Lives:" + str(player.get_lives()), True, (255, 0, 0))
        player_round = font.render("Round:" + str(player.get_round()), True, (255, 0, 0))

        self.screen.blit(player_cash, (850, 70))
        self.screen.blit(player_lives, (850, 110))
        self.screen.blit(player_round, (850, 30))
    
if __name__ == "__main__":
    screen = pygame.display.set_mode([SCREEN_RESOLUTION_WIDTH, SCREEN_RESOLUTION_HEIGHT])
    tower_defense = TowerDefenseGame(screen, 0xffffff)
    tower_defense.start_tower_defense_game_sunny_meadow()