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
		#get mouse position
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
        self.rounds = [[balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
                        balloon_speed_x=5, balloon_speed_y=5, position_x=0, position_y=400),
                        balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
                        balloon_speed_x=4, balloon_speed_y=4, position_x=-10, position_y=400),
                        balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
                        balloon_speed_x=3, balloon_speed_y=3, position_x=-20, position_y=400)
                        ],
                        [balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
                          balloon_speed_x=5, balloon_speed_y=5, position_x=0, position_y=400),
                          balloon.Balloon(balloon_image="playbutton.jpg", balloon_health=2,
                          balloon_speed_x=5, balloon_speed_y=5, position_x=0, position_y=400)
                        ]
                        #   balloon.Balloon(balloon_colour=color.GREEN, screen=self.screen, balloon_health=3,
                        #   balloon_speed_x=3, balloon_speed_y=3, position_x=0, position_y=400),
                        #   balloon.Balloon(balloon_colour=color.YELLOW, screen=self.screen, balloon_health=4,
                        #   balloon_speed_x=4, balloon_speed_y=4, position_x=0, position_y=400),
                        #   balloon.Balloon(balloon_colour=color.RED, screen=self.screen, balloon_health=1,
                        #   balloon_speed_x=10, balloon_speed_y=3, position_x=0, position_y=400)
                          ]

    def start_tower_defense_game_sunny_meadow(self):
        pygame.init()

        clock = pygame.time.Clock()

        balloon_group = pygame.sprite.Group()
        tower_group = pygame.sprite.Group()

        tower_defense_player = player.Player(cash=650, lives=100, round=1)

        balloon_round_counter = 0

        play_status = False
        round_started = False
        selected_monkey = None

        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.draw(self.screen):
                        play_status = True
                    # If our cash is greater than $250, then we can place the monkey down
                    elif self.monkey_button.draw(self.screen) and tower_defense_player.get_cash() > 250:
                        mouse_pos = pygame.mouse.get_pos()
                        tower_obj = tower.Tower(image="playbutton.jpg", x=mouse_pos[0], y=mouse_pos[1], cost=250)
                        tower_group.add(tower_obj)
                        selected_monkey = tower_obj
                # If we release the mouse button, then we need to check if we can place the tower, 
                # if we can place the tower then 
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_monkey != None:
                        if self.can_place_tower(mouse_pos=mouse_pos):
                            #   obstacle_position.push(mouse_pos_x-)
                            tower_defense_player.update_cash(tower_defense_player.get_cash() - selected_monkey.get_cost())
                            selected_monkey = None
                        else:
                            tower_group.remove(selected_monkey)
                            selected_monkey = None
                     
            self.load_background()
            if (selected_monkey != None):
                 print("Selected Monkey")
                 mouse_pos = pygame.mouse.get_pos()
                 selected_monkey.update_tower_pos(mouse_pos[0], mouse_pos[1])


            # If we click the play button, then start the round
            if play_status:
                 round_started = True
                 play_status = False
            
            # print(len(self.rounds))

            # If the round has started and there are still balloons left, then play the tower defense
            if round_started and tower_defense_player.get_round() <= len(self.rounds) \
               and balloon_round_counter < len(self.rounds[tower_defense_player.get_round() - 1]):
                balloon_group.add(self.rounds[tower_defense_player.get_round() - 1][balloon_round_counter])
                balloon_round_counter += 1
            
            # If the total number of balloons is equal to 0, then move on to the next round and update the play status to true
            if len(balloon_group) == 0 and round_started == True:
                tower_defense_player.update_round(tower_defense_player.get_round() + 1)
                tower_defense_player.update_cash(tower_defense_player.get_cash() + 200)
                round_started = False
                balloon_round_counter = 0

            mouse_pos = pygame.mouse.get_pos()

            for balloon in balloon_group.sprites():
                 if balloon.can_destroy_balloon():
                      balloon_group.remove(balloon)
                      tower_defense_player.update_lives(tower_defense_player.get_lives() - balloon.get_balloon_health())

            balloon_group.update()
            balloon_group.draw(self.screen)
            tower_group.draw(self.screen)
            self.display_player_stats(player=tower_defense_player)

            # Flip the display
            pygame.display.flip()
            clock.tick(100)

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
        
        monkey_button_img = pygame.image.load('playbutton.jpg').convert_alpha()
        self.monkey_button = Button(1010, 10, monkey_button_img, 0.2)
        self.monkey_button.draw(self.screen)

    def can_place_tower(self, mouse_pos):
        """
        This function is used to check if we can place tower based off the mouse position
        :param: mouse_pos: The current mouse position
        """
        top_left_boundary = 0
        bottom_right_boundary = 1
        coordinate_x_idx = 0
        coordinate_y_idx = 1
        for obstacle in obstacle_position:
            if mouse_pos[coordinate_x_idx] >= obstacle[top_left_boundary][coordinate_x_idx] and mouse_pos[coordinate_x_idx] <= obstacle[bottom_right_boundary][coordinate_x_idx]\
            and mouse_pos[coordinate_y_idx] >= obstacle[top_left_boundary][coordinate_y_idx] and mouse_pos[coordinate_y_idx] <= obstacle[bottom_right_boundary][coordinate_y_idx]:
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

        self.screen.blit(player_cash, (650, 70))
        self.screen.blit(player_lives, (650, 110))
        self.screen.blit(player_round, (650, 30))
    
if __name__ == "__main__":
    screen = pygame.display.set_mode([SCREEN_RESOLUTION_WIDTH, SCREEN_RESOLUTION_HEIGHT])
    tower_defense = TowerDefenseGame(screen, 0xffffff)
    tower_defense.start_tower_defense_game_sunny_meadow()