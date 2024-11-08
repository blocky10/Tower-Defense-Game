import pygame
from pygame.math import Vector2

class Enemy(pygame.sprite.Sprite):
    """
    This Enemy class is a sprite object that traverses across
    a path via checkpoints
    """
    def __init__(self, checkpoints, enemy_image, number_of_enemies, enemy_health, speed, 
                 distance_travelled, scale_factor):
        """
        """
        self.enemy_image = enemy_image
        self.image = pygame.image.load(enemy_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (400 * scale_factor, 400 * scale_factor))
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * 0.1), int(height * 0.1)))
        self.rect = self.image.get_rect()
        self.checkpoints = checkpoints

        self.first_checkpoint_idx = 0
        self.pos = Vector2(checkpoints[self.first_checkpoint_idx])
        self.rect.center = self.pos
        self.number_of_enemies = number_of_enemies

        # All enemies statistics
        self.enemy_health = enemy_health
        self.speed = speed
        self.distance_travelled = distance_travelled

        # This variable is used to control the movement direction of the enemy
        self.movement_command_index = 1
        
        super().__init__()

    def update(self, enemy_group, tower_defense_player):
        """
        This function is used to update the movement of the enemy
        :return:
        """

        # No longer update the enemy position if the lives is 0
        if tower_defense_player.get_lives() == 0:
            return
        
        # Update the movements based off the checkpoints passed
        if self.movement_command_index < len(self.checkpoints):
            self.target = Vector2(self.checkpoints[self.movement_command_index])
            self.movement = self.target - self.pos
        else:
            enemy_group.remove(self)
            tower_defense_player.update_lives(max(0, tower_defense_player.get_lives() - self.get_enemy_health()))

        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
            self.distance_travelled += self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
                self.distance_travelled += dist

            self.movement_command_index += 1

        self.rect.center = self.pos

    def update_number_of_enemies(self, number_of_enemies):
        """
        This function is used to update the number of enemies
        :param: number_of_enemies: The number of enemies we want to spawn on the screen
        """
        self.number_of_enemies = number_of_enemies

    def get_number_of_enemies(self):
        """
        This function is used to get the number of enemies we have remaining to spawn on the screen
        :param: The number of enemies available to spawn on the screen
        """
        return self.number_of_enemies
    
    def get_enemy_health(self):
        """
        This function is used to get the overall health of the enemy
        :return: The current enemy health
        """
        return self.enemy_health
    
    def get_enemy_position_x(self):
        """
        This function is used to get the enemy position x
        :return: The relative position of the enemy position x
        """
        return self.rect.centerx
    
    def get_enemy_position_y(self):
        """
        This function is used to get the enemy position y
        :return: The relative position of the enemy position y
        """
        return self.rect.centery
    
    def get_enemy_speed(self):
        """
        This function is used to get the enemy speed x
        :return: The speed x of the enemy
        """
        return self.speed
    
    def get_enemy_image(self):
        """
        This function gets the image of the enemy
        """
        return self.enemy_image
    
    def update_enemy_health(self, enemy_health):
        """
        This function is used to update the enemy health
        :return:
        """
        self.enemy_health = enemy_health

    def get_enemy_distance_travelled(self):
        """
        This function gets the current place of the enemy based on the current position
        in the round
        :param: Current enemy position in the round
        """
        return self.distance_travelled