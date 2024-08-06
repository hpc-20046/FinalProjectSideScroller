from settings import *


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset_float = 0
        self.offset = 0
        self.constant = -WIDTH / 2 + self.player.rect.x / 2

    def scroll(self):
        self.offset_float += self.player.position.x - self.offset_float + self.constant
        self.offset = int(self.offset_float)
        self.offset = max(self.offset, 0)
        self.offset = min(self.offset, self.player.border - WIDTH)
