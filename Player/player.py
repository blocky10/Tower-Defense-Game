class Player:
    """
    This class is used to display the player
    """
    def __init__(self, cash, lives, round):
        """
        The Player Constructor
        :param: cash: The starting cash of the player
        :param: lives: The starting lives of the player
        :param: round: The starting round of the player
        :return:
        """
        self.cash = cash
        self.lives = lives
        self.round = round

    def update_cash(self, cash):
        """
        This function is used to update the cash for every round of the player
        :param: cash: The current cash for tower defense
        """
        self.cash = cash

    def update_lives(self, lives):
        """
        This function is used to update the current lives for every round of the player
        :param: lives: The current lives for tower defense
        """
        self.lives = lives

    def update_round(self, round):
        """
        This function is used to update the current round of the player
        :param: round: The current round for tower defense
        """
        self.round = round

    def get_cash(self):
        """
        This function is used to get the current cash of the player
        :return: The current cash for the player
        """
        return self.cash
    
    def get_lives(self):
        """
        This function is used to get the current lives of the player
        :return: The current lives of the player
        """
        return self.lives
    
    def get_round(self):
        """
        This function is used to get the current round of the player
        :return: The current round of the player
        """
        return self.round