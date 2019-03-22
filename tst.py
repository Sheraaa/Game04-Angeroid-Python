from game_engine import *
from SpaceObject import *
from GUI import *
from pyglet.window.key import symbol_string
import pyglet


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


class Asteroid(SpaceObject):
    def __init__(self,position, speed=(0,0), category= 7):

        
        self.explose_sound=pyglet.media.load("assets/Explosion.wav",streaming=False)
        if category ==7:
            image_path="assets/etat.png"
            anchor=(32,32)
        elif category ==6:
            image_path="assets/t.png"
            anchor=(32,32)
        elif category ==5:
            image_path="assets/eau.png"
            anchor=(32,32)
        elif category ==4:
            image_path="assets/el.png"
            anchor=(32,32)
        elif category ==3:
            image_path="assets/internet.png"
            anchor=(32,32)
        elif category ==2:
            image_path="assets/f.png"
            anchor=(32,32)
        else:
            image_path="assets/bebe.png"
            anchor=(32,32)

        super().__init__(image_path,position, speed, anchor=anchor, rotation_speed= randint(-50,50))
        self.category= category

    def on_collision (self, other):
       if isinstance(other, SpaceShip):
            other.destroy()
            
    def destroy(self):
        super().destroy()
        self.layer.change_score(200 * self.category)
        self.explose_sound.play()
        if self.category>1:
            self.category -=1
            for i in range(2):
                new_asteroid = Asteroid(self.position,speed=(randint(1,100),randint(1,100)), category  = self.category)
                self.layer.add(new_asteroid)

class SpaceShip(SpaceObject):
    def __init__(self,position):
        image_path= "assets/vaisseau.png"
        self.velocity= 0
        self.isEngine=False
        super().__init__(image_path, position, anchor=(32,32))
       # self.rotation= 45   #rotation mot clé pour cocos pour changer la rotation du sprite
        self.lives=8
        self.invincibility_time= 3
        self.invincible = 0
        self.shoot_sound=pyglet.media.load("assets/Hit_Hurt.wav", streaming=False)

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
        self.shoot_sound.play()
        self.layer.change_score(-100)

    def destroy(self):
        self.powerup_sound=pyglet.media.load("assets/Powerup.wav",streaming=False)
        if self.invincible <= 0 :

            if self.lives > 0:
                #se rendre invincible et se retirer une vie
                # for n in range(5):
                #     speed = randint(-100,100), randint(-100,100)
                #     bullet = Bullet(self.position, speed)
                #     self.layer.add(bullet)
                self.invincible = self.invincibility_time
                self.powerup_sound.play()
                self.lives -= 1 
                self.layer.change_score(-200)
            else:
                super().destroy()

                gameover=Layer()
                bg=Sprite("assets/GM.png")
                gameover.add(bg)
                self.layer.game.add(gameover)


class AsteroidGame(Game):
    def __init__(self):
        super().__init__()
        self.started = False

    def add(self, layer):
        super().add(layer)
        layer.game= self

    def update(self,dt):
        if self.started:
            super().update(dt)

class GameLayer(Layer):
    def __init__(self):
        super().__init__()
        self.game=None
        self.level=3
        self.score_points=0
        self.score= Texte(text="Play", position=(560,570),size=18, bold = True, color=(255,0,0,0))
        self.add(self.score)

    def update (self, dt):
        super().update(dt)
        self.score.element.text = "Score: "+str(self.score_points)   #element.text un truc de cocos qu'on rajoute pour modifier le texte de la variable

    def change_score(self, amount):
        self.score_points = max(0,self.score_points + amount)

class WinLayer(Layer):
    def __init__(self):
        super().__init__()
        self.text=Sprite("assets/Win.png")
        self.level=3

    def update(self,dt):
        super().update(dt)

    def prepare(level_number):
        game.remove(GameLayer)
        win=Layer()
        win.add(self.texte)
        self.layer.game.add(win)

    def on_key_press(self, key, modifiers):
        self.game.started = True
        self.text.destroy()
        
class Title(Layer):     
    def __init__(self):
        super().__init__()
        self.texte= Sprite("assets/title.png")
        self.add(self.texte)

    def on_key_press(self, key, modifiers):
        self.game.started = True
        self.texte.destroy()



resolution = (800,600)
init(resolution, "Asteroid by Sheraaa")


game = AsteroidGame()
gamelayer= GameLayer()
background=Layer()


speed= (randint(-100,100),randint(-100,100))
asteroid = Asteroid((randint(0,800),randint(0,600)), speed)
spaceship = SpaceShip((400,300))

image= Sprite('assets/background.png',(0,-50))
background.add(image)
title = Title()


gui=GUI(spaceship)

game.add(background)
game.add(gamelayer)
gamelayer.add(asteroid)
gamelayer.add(spaceship)
game.add(gui)
game.add(title)

music = pyglet.media.load("assets/ThemeSong.wav", streaming=False)   #background music
music_player=pyglet.media.Player()
music_player.queue(music)
music_player.loop = True
music_player.eos_action=pyglet.media.SourceGroup.loop   
music_player.play()

game.run()