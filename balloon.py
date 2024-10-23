import pygame

direction_to_move = {
    "LEFT": (-0.1, 0),
    "RIGHT": (0.1, 0),
    "UP": (0, -0.1),
    "DOWN": (0, 0.1)
}

bloon_movement = [
    ["move_command", direction_to_move["RIGHT"]],
    ["wait_for_point", (245, 400)],
    ["move_command", direction_to_move["UP"]],
    ["wait_for_point", (245, 115)],
    ["move_command", direction_to_move["RIGHT"]],
    ["wait_for_point", (450, 115)],
    ["move_command", direction_to_move["DOWN"]],
    ["wait_for_point", (450, 550)],
    ["move_command", direction_to_move["LEFT"]],
    ["wait_for_point", (145, 550)],
    ["move_command", direction_to_move["DOWN"]],
    ["wait_for_point", (145, 696)],
    ["move_command", direction_to_move["RIGHT"]],
    ["wait_for_point", (852, 696)],
    ["move_command", direction_to_move["UP"]],
    ["wait_for_point", (852, 478)],
    ["move_command", direction_to_move["LEFT"]],
    ["wait_for_point", (651, 478)],
    ["move_command", direction_to_move["UP"]],
    ["wait_for_point", (651, 186)],
    ["move_command", direction_to_move["RIGHT"]],
    ["wait_for_point", (0, 0)],
    ["move_command", direction_to_move["DOWN"]],
]


class Balloon(pygame.sprite.Sprite):
    """
    This balloon class is used to 
    """
    def __init__(self, balloon_image, balloon_health, balloon_speed_x, 
                 balloon_speed_y, position_x, position_y):
        super().__init__()

        self.image = pygame.image.load(balloon_image).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * 0.1), int(height * 0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (position_x, position_y)

        # All balloon statistics
        self.balloon_health = balloon_health
        self.balloon_speed_x = balloon_speed_x
        self.balloon_speed_y = balloon_speed_y
        self.position_x = position_x
        self.position_y = position_y

        # This variable is used to control the movement direction of the balloon
        self.movement_command_index = 0
        self.direction_to_move_x = 0
        self.direction_to_move_y = 0

    def update(self):
        """
        This function is used to update the movement of the balloon
        :return:
        """
        instruction_index = 0
        command_index = 1
        position_x = 0
        position_y = 1
        # Set the current move direcdtion based off the move command being sent
        if bloon_movement[self.movement_command_index][instruction_index] == "move_command":
            self.direction_to_move_x = bloon_movement[self.movement_command_index][command_index][position_x] * self.balloon_speed_x
            self.direction_to_move_y = bloon_movement[self.movement_command_index][command_index][position_y] * self.balloon_speed_y
            self.movement_command_index += 1
        # Otherwise just wait for the balloons to reach the points
        elif bloon_movement[self.movement_command_index][instruction_index] == "wait_for_point" \
             and bloon_movement[self.movement_command_index][command_index][0] == int(self.position_x) \
             and bloon_movement[self.movement_command_index][command_index][1] == int(self.position_y):
            self.movement_command_index += 1
        else:
            self.position_x += self.direction_to_move_x
            self.position_y += self.direction_to_move_y
        
        self.rect.center = (self.position_x, self.position_y)
        

    def can_destroy_balloon(self):
        """
        This function is used to check if the balloon object can be destroyed
        :return:
        """
        if int(self.position_x) == 1010 and int(self.position_y) == 186:
            return True
        
        return False
    
    def get_balloon_health(self):
        """
        This function is used to get the overall health of the balloon
        :return: The current balloon health
        """
        return self.balloon_health
    
    def get_balloon_position_x(self):
        """
        This function is used to get the balloon position x
        :return: The relative position of the balloon position x
        """
        return self.rect.centerx
    
    def get_balloon_position_y(self):
        """
        This function is used to get the balloon position y
        :return: The relative position of the balloon position y
        """
        return self.rect.centery