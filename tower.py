import pygame
import math

class Tower(pygame.sprite.Sprite):
    def __init__(self, image, x, y, cost, tower_radius, tower_fired):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.cost = cost
        self.tower_radius = tower_radius
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_tower_fired = tower_fired

    def get_tower_width(self):
        return self.rect.width

    def get_tower_height(self):
        return self.rect.height

    def update_tower_pos(self, screen, x, y, can_place):
        """
        This function updates the tower position when dragging and dropping and draws a 
        circle when the tower is placed
        :return:
        """
        self.rect.center = (x, y)
        if can_place:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.rect.centerx), int(self.rect.centery)), self.tower_radius, 1)
        else:
            pygame.draw.circle(screen, (255, 0, 0), ((int)(self.rect.centerx), (int)(self.rect.centery)), self.tower_radius, 1)

    def get_cost(self):
        """
        This function gets the cost of the tower
        :return:
        """
        return self.cost

    def get_distance(self, balloon_coordinate_x, balloon_coordinate_y, tower_coordinate_x, tower_coordinate_y):
        """
        This function gets the distance of the balloon from the tower to check if the tower
        is within range of the balloons
        :return: The distance between the tower and the balloon
        """
        return math.sqrt((balloon_coordinate_x - tower_coordinate_x) ** 2 + (balloon_coordinate_y - tower_coordinate_y) ** 2)
    
    def create_bullet(self, bullet_group, balloon_coordinate_x, balloon_coordinate_y):
        if self.tower_fired():
            return

        self.bullet = Bullet("playbutton.jpg", self.rect.centerx, self.rect.centery, balloon_coordinate_x, balloon_coordinate_y)
        self.set_tower_fired(True)
        bullet_group.add(self.bullet)

    def fire_bullet(self, bullet_group, balloon_group):
        """
        This function is used to fire a bullet
        """
        if not self.tower_fired():
            return
        
        if self.bullet.bullet_out_of_range():
            bullet_group.remove(self.bullet)
            self.bullet = None
            self.set_tower_fired(False)

        # If the balloon and bullet gets hit then remove the balloon from the list
        if self.bullet != None and pygame.sprite.spritecollide(self.bullet, balloon_group, True):
            self.set_tower_fired(False)
            bullet_group.remove(self.bullet)
            self.bullet = None
            return



    def is_balloon_in_radius(self, balloon_coordinate_x, balloon_coordinate_y):
        """
        This function is used to check if the balloon is in radius
        :param: balloon_coordinate_x
        """
        if self.get_distance(balloon_coordinate_x, balloon_coordinate_y, self.rect.centerx, self.rect.centery) <= self.tower_radius:
            return True
        
        return False
    
    def set_tower_fired(self, tower_fired):
        self.is_tower_fired = tower_fired

    def tower_fired(self):
        return self.is_tower_fired
    
    def get_tower_position_x(self):
        """
        This function gets the tower position x
        """
        return self.rect.centerx

    def get_tower_position_y(self):
        """
        This function gets the tower position y
        """
        return self.rect.centery

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, position_to_fire_x, position_to_fire_y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position_x = int(x)
        self.position_y = int(y)
        self.position_to_fire_x = int(position_to_fire_x)
        self.position_to_fire_y = int(position_to_fire_y) 
        self.total_fire_distance_x = (self.position_to_fire_x - self.position_x) / 60
        self.total_fire_distance_y = (self.position_to_fire_y - self.position_y) / 60
    
    def update(self, weapon_group):
        """
        This function is used to get the attack update position
        """
        if self.bullet_out_of_range():
            weapon_group.remove(self)
            print("Bullet out of range")
            return
        
        self.position_x += self.total_fire_distance_x
        self.position_y += self.total_fire_distance_y
        self.rect.center = (self.position_x, self.position_y)

    def bullet_out_of_range(self):
        """
        This functiton checks if the bullet is out of range
        :return: True if the bullet is out of range
        """
        if int(self.position_x) == int(self.position_to_fire_x) and int(self.position_y) == int(self.position_to_fire_y):
            return True

        return False

    def set_bullet_position(self, pos_x, pos_y):
        self.rect.center = (pos_x, pos_y)



    