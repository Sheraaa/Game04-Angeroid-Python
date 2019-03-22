from game_engine import *
#from SpaceObject import *
from Asteroid import *

class Bullet (SpaceObject):
    def __init__(self, position, speed=(0,0)):  #speed (0,0) c'est par défaut si on donne pas de valeur
        image_path= "assets/bullet.png"
        self.lifetime= 3
        super().__init__(image_path, position, speed, anchor=(8,8))
        

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()
        super().update(dt)

    def on_collision(self, other):
        if isinstance(other, Asteroid):
            other.destroy()
            self.destroy()