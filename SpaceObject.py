#from Asteroid import Asteroid
from game_engine import Game, Sprite, init, Layer
from random import randint

class SpaceObject(Sprite):

    def __init__(self, image_path, position, speed=(0,0), anchor=(0,0), rotation_speed=0):
        super().__init__(image_path,position, anchor=anchor) # anchor c'est l'ancre de l'image (16x16) on prend la moitié
        self.speed = speed
        self.rotation_speed= rotation_speed

    def update(self, dt):
        mov_h= dt * self.speed[0]
        mov_v= dt * self.speed[1]
        self.position = (self.position[0]+mov_h, self.position[1]+mov_v)

        if (self.position[0]<0):
            self.position=(800,self.position[1])

        elif (self.position[0]>800):
            self.position = (0, self.position[1])

        if (self.position[1]<0):
            self.position=(self.position[0],600)

        elif (self.position[1]>600):
            self.position = (self.position[0],0)

        self.rotation += self.rotation_speed * dt

        super().update(dt) 