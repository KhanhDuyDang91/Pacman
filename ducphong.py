from pygame import *



window = display.set_mode((700,500))
display.set_caption("Maze game")

background_img = transform.scale(image.load("background.jpg"),(700,500))

player_img_path = "hero.png"
enemy_img_path = "cyborg.png"
goal_img_path = "treasure.png"
wall_img_path = "wall.png"
background_img_path = "background.jpg"

map_sizes = [(700, 500),(800,600),(1000, 800)] # to set the size of 3 levels
cur_level = 0 #setting the current map level
cur_size = map_sizes[cur_level]#getting the size for the map in level 1


window.blit(background_img,(0,0))

class GameSprite(sprite.Sprite):
    def __init__(self, img, width, height, x_pos, y_pos):
        super().__init__()
        self.img = transform.scale(image.load("background.jpg"),(width,height))#make the game surface
        self.rect = self.img.get_rect()#create hitbox
        self.rect.y = y_pos#set the starting x location
        self.rect.x = x_pos#set the starting y location

    def draw(self):
        window.blit(self.img,(self.rect.x,self.rect.y))# placing the object into the window at the x,y

class Player(GameSprite):

    def update(self):
        key_pressed  = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:#check if the player press a key and thhe character is still in the window
            self.rect.x -= 5
        if key_pressed[K_d] and self.rect.x < cur_size[0] - self.rect.width:#check if the player press d
            self.rect.x += 5
        key_pressed  = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= 5
        if key_pressed[K_s] and self.rect.y < cur_size[0] - self.rect.height:
            self.rect.y += 5


class Enemy(GameSprite):
    def update(self, map):
        pass

map_01 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
          [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
          [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
          [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map_02 = []
map_03 = []

map_pool = [map_01, map_02, map_03]


def build_map(map):
    walls = sprite.Group()
    for row in range(len(map)):# Loops through each of the list
        for col in range(len(map[row])):# loops through each of the value in the list
            if map[row][col] == 1:
                x = col * 50
                y = row * 50
                wall = GameSprite(wall_img_path,50,50, x, y)
                walls.add(wall)
    return walls

player = Player(player_img_path,50,50,150,400)#make the player object with size of 50x50 and place t x = 100,y = 400
enemy = Enemy(enemy_img_path,50,50,600,400)#make the enemy object with size of 50x50 and place t x = 600,y = 400

FPS =60 # set the FPS
clock = time.Clock() # Make a cclock object that help limit the while loop
game = True # set the game to true so it will continue to run
finish = False # get the finish status to false so it is not finish
current_map = map_pool[cur_level]

while game:
    for e in event.get(): # get every events in the game
        if e.type == QUIT: # check if the event relate to the action quit the window
            game = False # if true turn the game window off

    if not finish: # if the game is not finish
        window.blit(background_img,(0,0)) # redraw the background
        walls = build_map(current_map)
        for wall in walls:
            wall.draw()
        player.draw() # draw the player
        enemy.draw() # draw the enemy

        player.update() # update the position of the character playerr
        enemy.update(current_map) #update the position of the character enemy

        display.update()
        clock.tick(FPS)
