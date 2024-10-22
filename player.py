class Player:
    def __init__(self, cash, lives, round):
        self.cash = cash
        self.lives = lives
        self.round = round

    def update_cash(self, cash):
        self.cash = cash

    def update_lives(self, lives):
        self.lives = lives

    def update_round(self, round):
        self.round = round

    def get_cash(self):
        return self.cash
    
    def get_lives(self):
        return self.lives
    
    def get_round(self):
        return self.round