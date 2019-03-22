from game_engine import *
from SpaceObject import *
from random import randint
from SpaceShip import *


class Asteroid(SpaceObject):
    def __init__(self,position, speed=(0,0), category= 3):

        if category ==3:
            image_path="assets/asteroid128.png"
            anchor=(64,64)
        elif category ==2:
            image_path="assets/asteroid64.png"
            anchor=(32,32)
        else:
            image_path="assets/asteroid32.png"
            anchor=(16,16)

        super().__init__(image_path,position, speed, anchor=anchor, rotation_speed= randint(-50,50))
        self.category= category

    def on_collision (self, other):
       if isinstance(other, SpaceShip):
            other.destroy()

    def destroy(self):
        super().destroy()
        if self.category>1:
            self.category -=1
            for i in range(3):
                new_asteroid = Asteroid(self.position,speed=(randint(1,100),randint(1,100)), category  = self.category)
                self.layer.add(new_asteroid)

class AsteroidGame(Game):
    def __init__(self):
        super().__init__()

    def add(self, layer):
        super().add(layer)
        layer.game= self

class GameLayer(Layer):
    def __init__(self):
        super().__init__()
        self.game=None