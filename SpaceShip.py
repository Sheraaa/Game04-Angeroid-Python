from game_engine import Game, Sprite, init, Layer
from random import randint
from SpaceObject import *
from pyglet.window.key import symbol_string
from math import sin,cos, radians, degrees,sqrt
from Asteroid import *

class SpaceShip(SpaceObject):
    def __init__(self,position):
        image_path= "assets/vaisseau.png"
        self.velocity= 0
        self.isEngine=False
        super().__init__(image_path, position, anchor=(32,32))
       # self.rotation= 45   #rotation mot clé pour cocos pour changer la rotation du sprite
        self.lives=3
        self.invincibility_time= 3
        self.invincible = 0

    def on_key_press(self, key , modifiers):
        if ((symbol_string(key) == "UP") or (symbol_string(key) == "Z")):
            self.isEngine=True
        if ((symbol_string(key) == "DOWN") or (symbol_string(key) == "S")):
            self.velocity= -100
        elif symbol_string(key) in ["LEFT","Q"]:
            self.rotation_speed = -90
        elif symbol_string(key) in ["RIGHT","D"]:
            self.rotation_speed = 90
        elif symbol_string(key) == "SPACE":
            self.shoot()


    def on_key_release(self, key, modifiers):
        if ((symbol_string(key) == "UP") or (symbol_string(key) == "Z")):
            self.isEngine=False
        if symbol_string(key) in ["LEFT","Q"]:
            self.rotation_speed = 0
        elif symbol_string(key) in ["RIGHT","D"]:
            self.rotation_speed = 0


    def update(self, dt):
        if self.invincible > 0:
            self.invincible -= dt
            self.opacity = 50
        else:
            self.opacity = 255

        angle= -radians(self.rotation -90)
        dspeed_v=0
        dspeed_h=0
        maxi_speed= 100
        if(self.isEngine):
            dspeed_h= cos(angle)* dt * maxi_speed
            dspeed_v= sin(angle)* dt * maxi_speed

            #difference_velocity= 100 * dt
            #self.velocity+= difference_velocity
        # else:
        #     difference_velocity = -300 * dt
        #     self.velocity= max(difference_velocity+ self.velocity, 0)

        #speed += dspeed
        self.speed=(self.speed[0]+dspeed_h, self.speed[1]+dspeed_v)           #self.speed=(cos(angle) *self.velocity, sin(angle)*self.velocity)
        length=sqrt(self.speed[0]**2 + self.speed[1]**2)
        if length > maxi_speed:
            self.speed = (self.speed[0] / length * maxi_speed, self.speed[1] / length * maxi_speed)

        super().update(dt)

    def shoot(self):
        angle= -radians(self.rotation -90)
        bullet = Bullet(position=self.position, speed=(cos(angle)*200,sin(angle)*200 ))
        self.layer.add(bullet)

    def destroy(self):
        if self.invincible <= 0 :
            self.lives -= 1 
            if self.lives > 1:
                #se rendre invincible et se retirer une vie
                self.invincible = self.invincibility_time
                
            else:
                super().destroy()

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