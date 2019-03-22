from game_engine import Game, Sprite, init, Layer,Game 
from random import randint
from SpaceShip import *
from Asteroid import *
from GUI import GUI

resolution = (800,600)
init(resolution, "Asteroid by Sheraaa")

game = Game()
gamelayer= GameLayer()
background=Layer()

#créer un nouveau Sprite
#sprite= Sprite("assets/bullet.png",(400,300))
#l'ajouter le sprite au layer
#layer.add(sprite)

# for i in range(10):
#     sprite=Bullet((randint(0,800),randint(0,600)), speed= (randint(-100,100),randint(-100,100)))
# #Sprite("assets/bullet.png",(randint(0,800),randint(0,600)),1, (50,0))
#     layer.add(sprite)


speed= (randint(-100,100),randint(-100,100))
asteroid = Asteroid((randint(0,800),randint(0,600)), speed)
spaceship = SpaceShip((400,300))

image= Sprite('assets/background.jpg')
gamelayer.add(image)


gui=GUI(spaceship)

game.add(background)
game.add(gamelayer)
gamelayer.add(asteroid)
gamelayer.add(spaceship)
game.add(gui)

game.run()