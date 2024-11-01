# imports
from settings import *

# camera class handles side scrolling function
class Camera:
    def __init__(self, player):
        # declare variables 
        self.player = player
        self.offset_float = 0
        self.offset = 0
        # constant that places the player in the middle of the screen
        self.CONSTANT = -WIDTH / 2 + self.player.rect.x / 2

    # update the camera offsets
    def scroll(self):
        # update the offset based on the amount the player position has changed
        self.offset_float += self.player.position.x - self.offset_float + self.CONSTANT
        # create an int version of the offset while keeping the precision
        self.offset = int(self.offset_float)
        # clamp offsets based on the level border so the player can reach the end of the screen
        self.offset = max(self.offset, 0)
        self.offset = min(self.offset, self.player.border - WIDTH)
        self.offset_float = max(self.offset_float, 0)
        self.offset_float = min(self.offset_float, self.player.border - WIDTH)
