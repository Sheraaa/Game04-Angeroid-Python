from game_engine import Game, Sprite, init, Layer

class GUI(Layer):
    def __init__(self, spaceship):
        super().__init__()
        self.spaceship= spaceship
        self.lives= []
        position_initial = 775,575

        for n in range (spaceship.lives):
            image_path= r"assets/life.png"   #le r c'est pour dire à python que ce qui suis est un chemin
            position = position_initial[0] - n * ( 16 + 15), position_initial[1]
            life= Sprite(image_path, position, anchor=(16,16))
            self.lives.append(life)
            self.add(life)

    def update(self, dt):
        super().update(dt)

        if(len(self.lives)> self.spaceship.lives):
            life = self.lives.pop()  #pop retire le dernier de la liste
            life.destroy()