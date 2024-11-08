import pygame
import math
from pygame import mixer

class Tower(pygame.sprite.Sprite):
    """
    This tower class is an object that is placed on the field in the tower defense game
    """
    def __init__(self, tower_type, image, position_x, position_y, cost, tower_radius, 
                 tower_fired, attack_speed, attack_power, upgrade_level, has_piercing, 
                 sell_price, animation_list):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotate(self.image, 0)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.cost = cost
        self.position_x = position_x
        self.position_y = position_y
        self.tower_radius = tower_radius
        self.attack_speed = attack_speed
        self.attack_power = attack_power
        self.rect = self.image.get_rect()
        self.rect.center = (position_x, position_y)
        self.is_tower_fired = tower_fired
        self.tower_type = tower_type
        self.upgrade_level = upgrade_level
        self.has_piercing = has_piercing
        self.piercing_count = 0
        self.max_piercing_count = 0
        self.sell_price = sell_price
        self.animation_list = animation_list
        self.frame_index = 0
        self.target_index = 0
        self.target = ["target_first", "target_last", "target_closest", "target_strongest"]

    def update_tower_drag_and_drop_pos(self, screen, x, y, can_place):
        """
        This function is used for dragging and dropping the tower in the correct location.
        :param: screen: The pygame screen
        :param: x: The current coordinate x to update the tower position
        :param: y: The current coordinate y to update the tower position
        :param: can_place: Checks if the tower can be placed
        :return:
        """
        self.rect.center = (x, y)
        self.position_x = x
        self.position_y = y
        if can_place:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.rect.centerx), int(self.rect.centery)), self.tower_radius, 1)
        else:
            pygame.draw.circle(screen, (255, 0, 0), ((int)(self.rect.centerx), (int)(self.rect.centery)), self.tower_radius, 1)

    def select_upgrade_tower(self, screen):
        """
        This function is used to draw a circle around the upgraded tower
        :param: screen: The screen to draw the circle around the selected tower
        """
        pygame.draw.circle(screen, (255, 255, 255), (int(self.rect.centerx), int(self.rect.centery)), self.tower_radius, 1)

    def upgrade_tower(self, tower_defense_player):
        """
        This function is used to upgrade the tower defense tower
        :param: tower_defense_player: The player who is playing tower defense
        """
        if self.upgrade_level == 0 and tower_defense_player.get_cash() >= 200: 
            self.upgrade_attack_speed()
            tower_defense_player.update_cash(tower_defense_player.get_cash() - 200)
            self.set_sell_price(self.get_sell_price() + 100)
        elif self.upgrade_level == 1 and tower_defense_player.get_cash() >= 400:
            self.upgrade_attack_range()
            tower_defense_player.update_cash(tower_defense_player.get_cash() - 400)
            self.set_sell_price(self.get_sell_price() + 200)
        elif self.upgrade_level == 2 and tower_defense_player.get_cash() >= 800:
            self.upgrade_attack_power()
            tower_defense_player.update_cash(tower_defense_player.get_cash() - 800)
            self.set_sell_price(self.get_sell_price() + 400)
        elif self.upgrade_level == 3 and tower_defense_player.get_cash() >= 1200:
            self.upgrade_piercing()
            tower_defense_player.update_cash(tower_defense_player.get_cash() - 1200)
            self.set_sell_price(self.get_sell_price() + 600)
        else:
            return

        self.upgrade_level += 1

    def upgrade_attack_speed(self):
        """
        This function is used to upgrade the attack speed
        :return:
        """
        self.attack_speed *= 1.5

    def upgrade_attack_range(self):
        """
        This function is used to upgrade the attack range
        :return:
        """
        self.tower_radius += 50

    def upgrade_attack_power(self):
        """
        This function is used to upgrade the attack power
        :return:
        """
        self.attack_power *= 2

    def upgrade_piercing(self):
        """
        This function is used to upgrade the tower to use piercing
        :return:
        """
        self.has_piercing = True
        self.max_piercing_count += 1

    def create_bullet(self, bullet_image, bullet_group, bullet_coordinate_x, bullet_coordinate_y):
        """
        This function is used to create the bullet
        :param: bullet_group: The bullet group to hold the list of bullets
        :param: bullet_coordinate_x: The x coordinate of the bullet
        :param: bullet_coordinate_y: The y coordinate of the bullet 
        """
        if self.tower_fired():
            return
        
        self.update_tower_direction_facing(bullet_coordinate_x, bullet_coordinate_y)
        
        # Create a bullet object that will be fired
        self.bullet = Bullet(bullet_image, self.position_x, self.position_y, bullet_coordinate_x, 
                             bullet_coordinate_y, self.tower_radius, self.attack_speed)
        
        self.set_tower_fired(True)
        # Add the bullet to the group, so that we can animate it
        bullet_group.add(self.bullet)

    def fire_bullet(self, bullet_group, enemy_group, player, screen):
        """
        This function is used to fire a bullet and reduces/pop enemmy on contact
        :param: bullet_group: The bullet group to hold the list of bullets
        :param: enemy_group: The enemy group to hold the list of enemy
        :param: player: The player of tower defense
        :return:
        """
        if not self.tower_fired():
            return

        # If the bullet is out of range, then remove the bullet since it didn't contact anything
        if self.bullet.bullet_out_of_range():
            bullet_group.remove(self.bullet)
            self.bullet = None
            self.set_tower_fired(False)
            return

        # If the enemy and bullet gets hit then reduce/pop the enemy on impact
        for enemy in enemy_group:
            if self.bullet != None and pygame.sprite.collide_rect(self.bullet, enemy):
                pop_audio = mixer.Sound("Enemy/btd_bloon_pop.mp3")
                pop_audio.play()
                                
                # Update the enemy health to the maximum between 0 and current health
                player.update_cash(player.get_cash() + min(self.attack_power, enemy.get_enemy_health()))
                enemy_health = max(0, enemy.get_enemy_health() - self.attack_power)
                enemy.update_enemy_health(enemy_health)

                # If the enemy has no HP remaining then destroy the enemy, otherwise update the stats
                # of the enemy
                if enemy.get_enemy_health() == 0:
                    pop_animation = pygame.image.load("Enemy/pop_animation.jpg").convert_alpha()
                    pop_animation = pygame.transform.scale(pop_animation, (60, 60))
                    position_x = enemy.get_enemy_position_x()
                    position_y = enemy.get_enemy_position_y()
                    screen.blit((pop_animation), (position_x - 30, position_y - 30))
                    enemy_group.remove(enemy)

                # If the bullet has piercing, then check whether it's piercing count is greater than 1
                if self.has_piercing:
                    if self.piercing_count < self.max_piercing_count:
                        self.piercing_count += 1
                    else:
                        self.piercing_count = 0
                        bullet_group.remove(self.bullet)
                        self.bullet = None     
                        self.set_tower_fired(False)                   
                else:
                    bullet_group.remove(self.bullet)
                    self.bullet = None
                    self.set_tower_fired(False)
                break

    def is_enemy_in_radius(self, enemy_coordinate_x, enemy_coordinate_y):
        """
        This function is used to check if the enemy is within the radius
        :param: enemy_coordinate_x: The current enemy coordinate x
        :param: enemy_coordinate_y: The current enemy coordinate y
        """
        #                   |
        #                 | | |
        #               |   |   |
        #             |     |     | 
        # ------------|-----|-----|--------------
        #               |   |   | 
        #                 | | |
        #                   |
        #                   |
        #  Below is the evaluation of how to find whether the enemy is in radius of the tower
        #
        #  The enemy must lie in the radius of the circle
        #  in the equation (x - x1)^2 + (y - y1)^2 = r^2
        #  
        #  This simplifies down to r = sqrt((x-x1)^2 + (y-y1)^2)
        #  Thus the enemy must lie in the circle with the above formula
        #  
        #  But anything else smaller than r is also valid since it still lies within the circle
        #
        if self.get_enemy_distance(enemy_coordinate_x, enemy_coordinate_y, self.position_x, self.position_y) <= self.tower_radius:
            return True
        
        return False
    
    def get_sell_price(self):
        """
        This function gets the tower sell price
        :return: The tower sell price
        """
        return self.sell_price
    
    def set_sell_price(self, sell_price):
        """
        This function is used to set the tower sell price
        :param: sell_price: The sell price to set
        :return:
        """
        self.sell_price = sell_price

    def set_tower_fired(self, tower_fired):
        """
        This function is used to set whether the tower has fired a bullet or not
        :param: tower_fired: The status of the tower being fired or not
        :return:
        """
        self.is_tower_fired = tower_fired

    def tower_fired(self):
        """
        This function is used to check whether the tower has fired a bullet
        :return: True if the tower has fired a bullet otherwise False
        """
        return self.is_tower_fired
    
    def get_tower_position_x(self):
        """
        This function gets the tower center position x
        :return: The tower center position x
        """
        return self.rect.centerx

    def get_tower_position_y(self):
        """
        This function gets the tower center position y
        :return: The tower center position y
        """
        return self.rect.centery
    
    def get_tower_top_left_position(self):
        """
        This function gets the tower top left position
        :return: The tower top left position
        """
        return self.rect.topleft
    
    def get_tower_bottom_right_position(self):
        """
        This function gets the tower bottom right position
        :return: The tower bottom right position
        """
        return self.rect.bottomright
    
    def get_tower_width(self):
        """
        This function gets the width of the tower
        :return: The width of the tower
        """
        return self.rect.width

    def get_tower_height(self):
        """
        This function is used to get the tower height
        :return: The height of the tower
        """
        return self.rect.height
    
    def get_cost(self):
        """
        This function gets the cost of the tower
        :return:
        """
        return self.cost
    
    def get_tower_type(self):
        """
        This function is used to get the tower type
        :return: The tower type
        """
        return self.tower_type
    
    def get_tower_upgrade_level(self):
        """
        This function is used to get the upgrade level
        :return: The upgrade level
        """
        return self.upgrade_level

    def get_enemy_distance(self, enemy_coordinate_x, enemy_coordinate_y, tower_coordinate_x, tower_coordinate_y):
        """
        This function gets the distance of the enemy from the tower
        :return: The distance between the tower and the enemy
        """
        return math.sqrt((enemy_coordinate_x - tower_coordinate_x) ** 2 + (enemy_coordinate_y - tower_coordinate_y) ** 2)
    
    def update_tower_direction_facing(self, enemy_coordinate_x, enemy_coordinate_y):
        """
        This function updates the direction the tower faces
        :param: enemy_coordinate_x: The coordinate x of the enemy to face
        :param: enemy_coordinate_y: The coordinate y of the enemy to face
        """
        x_dist = enemy_coordinate_x - self.position_x
        y_dist = enemy_coordinate_y - self.position_y
        angle = math.degrees(math.atan2(-y_dist, x_dist))

        # This is since the image is offset by 270 degrees
        angle = ((angle % 360) + 270) % 360

        self.image = pygame.image.load(self.animation_list[self.frame_index])
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = pygame.transform.scale(self.image, (120, 120))

        self.rect = self.image.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        
        self.frame_index = self.frame_index + 1 if self.frame_index + 1 < len(self.animation_list) else 0

    def update_target(self):
        """
        This function is used to update the target based on button click
        """
        self.target_index = self.target_index + 1 if self.target_index + 1 < len(self.target) else 0

    def get_target(self):
        """
        This function is used to get the target type
        :return: The current target type (close, first, last, strong)
        """
        return self.target[self.target_index]

class Bullet(pygame.sprite.Sprite):
    """
    The bullet is an object that is fired by the tower
    """
    def __init__(self, image, x, y, position_to_fire_x, position_to_fire_y, bullet_radius, attack_speed):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.current_position_x = x
        self.current_position_y = y
        self.position_x = int(x)
        self.position_y = int(y)
        self.position_to_fire_x = int(position_to_fire_x)
        self.position_to_fire_y = int(position_to_fire_y) 
        self.bullet_radius = bullet_radius
        self.total_fire_distance_x = (self.position_to_fire_x - self.position_x) / 100 * attack_speed
        self.total_fire_distance_y = (self.position_to_fire_y - self.position_y) / 100 * attack_speed
    
    def update(self):
        """
        This function is used to get the attack update position
        :param: weapon_group: The weapon group that stores a list of weapons
        """
        self.position_x += self.total_fire_distance_x
        self.position_y += self.total_fire_distance_y
        self.rect.center = (self.position_x, self.position_y)

    def bullet_out_of_range(self):
        """
        This functiton checks if the bullet is out of range
        :return: True if the bullet is out of range
        """
        #                   |
        #                 | | |
        #               |   |   |
        #             |     |     | 
        # ------------|-----|-----|--------------
        #               |   |   | 
        #                 | | |
        #                   |
        #                   |
        #  Below is the evaluation of how to find whether the bullet is out range of the tower
        #
        #  The bullet must lie in the radius of the circle
        #  in the equation (x - x1)^2 + (y - y1)^2 = r^2
        #  
        #  This simplifies down to r = sqrt((x-x1)^2 + (y-y1)^2)
        #  Thus the bullet must lie within the tower range with the above formula
        #  
        #  Thus, anything greater than the radius will mean that the bullet
        #  has fired out of range
        #
        bullet_range = math.sqrt((self.position_x - self.current_position_x) ** 2 + (self.position_y - self.current_position_y) ** 2)
        if bullet_range > self.bullet_radius:
            return True

        return False    