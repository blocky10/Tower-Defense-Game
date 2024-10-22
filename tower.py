import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, image, x, y, cost):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.cost = cost
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_tower_pos(self, x, y):
        self.rect.center = (x, y)

    def get_cost(self):
        return self.cost
    
    def check_collision(self, group):
        if pygame.sprite.spritecollide(self, group, True):
            print("Sprite collided")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image - pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()



    