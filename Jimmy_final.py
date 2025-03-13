from pygame import *
import random

# CREATING WINDOW
win_width = 700
win_height = 700
display.set_caption("The pacman")
display.set_icon(image.load('game.png'))
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("mainbackground.png"), (win_width, win_height)).convert()
losing_background = transform.scale(image.load("game-over_1.png"), (win_width, win_height))
winning_background = transform.scale(image.load("thumb.jpg"), (win_width, win_height))

# VARIABLES
game = True
finish = False
clock = time.Clock()
FPS = 60
wall_color = (25, 113, 194, 255)  # Updated wall color

# CLASSES:
# parent class for sprites
class GameSprite(sprite.Sprite):
    # class constructor
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        # every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed

        # every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        new_rect = self.rect.copy()

        if keys[K_a] and self.rect.x > 5:
            new_rect.x -= self.speed
        elif keys[K_d] and self.rect.x < win_width - 50:
            new_rect.x += self.speed
        elif keys[K_w] and self.rect.y > 5:
            new_rect.y -= self.speed
        elif keys[K_s] and self.rect.y < win_height - 50:
            new_rect.y += self.speed


        def check_collision(rect): #function to check if player touches color
            margin = 5  # Adjust margin to reduce space between player and wall
            points = [
                (rect.left + margin, rect.top + margin),
                (rect.right - margin, rect.top + margin),
                (rect.left + margin, rect.bottom - margin),
                (rect.right - margin, rect.bottom - margin),
                (rect.left + rect.width // 2, rect.top + margin),
                (rect.left + rect.width // 2, rect.bottom - margin),
                (rect.left + margin, rect.top + rect.height // 2),
                (rect.right - margin, rect.top + rect.height // 2)
            ]
            for point in points:
                if 0 <= point[0] < win_width and 0 <= point[1] < win_height:
                    if background.get_at(point) == wall_color:
                        return True
            return False
        
        # Check for collisions before moving
        if not check_collision(new_rect):
            self.rect = new_rect  # Only move if no collision
            
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def update(self):
        new_rect = self.rect.copy() #create a clone coordinates

        if self.direction == 'left':
            new_rect.x -= self.speed
        elif self.direction == 'right':
            new_rect.x += self.speed
        elif self.direction == 'up':
            new_rect.y -= self.speed
        elif self.direction == 'down':
            new_rect.y += self.speed

        def check_collision(rect): #function checks if object touches the color wall in 8 points of rectangle area
            margin = 1
            points = [
                (rect.left + margin, rect.top + margin),
                (rect.right - margin, rect.top + margin),
                (rect.left + margin, rect.bottom - margin),
                (rect.right - margin, rect.bottom - margin),
                (rect.left + rect.width // 2, rect.top + margin),
                (rect.left + rect.width // 2, rect.bottom - margin),
                (rect.left + margin, rect.top + rect.height // 2),
                (rect.right - margin, rect.top + rect.height // 2)
            ]
            for point in points:
                if 0 <= point[0] < win_width and 0 <= point[1] < win_height:
                    if background.get_at(point) == wall_color: #get_at is the function to get the color at a specified point and check with color of the wall
                        print(f"Collision detected at {point}")
                        return True
            return False

        # Check for collisions before moving
        if check_collision(new_rect) or \
            new_rect.left < 0 or \
            new_rect.right > win_width or \
            new_rect.top < 0 or \
            new_rect.bottom > win_height:
            # Change direction randomly
            if self.direction in ['up', 'down']: #if enemy is moving up-down and touches the wall, it will choose left-right randommly and continues moving
                self.direction = random.choice(['left', 'right'])
            elif self.direction in ['left', 'right']:
                self.direction = random.choice(['up', 'down'])
        else:
            self.rect = new_rect  # Only move if no collision



# SPRITES:
packman = Player('pac-1.png', 250, 300, 2)
food1 = GameSprite('treasure.png', 615, 8, 0)
food2 = GameSprite('treasure.png', 400, 360, 0)
food3 = GameSprite('treasure.png', 240, 480, 0)
enemy1 = Enemy('cyborg.png', 400, 240, 5)
enemy2 = Enemy('hero.png', 400, 640, 5)

#Create groups for storing sprites:
foods = sprite.Group()
foods.add(food1)
foods.add(food2)
foods.add(food3)

enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)

# SOUND
mixer.init()
mixer.music.load('pacman music.mp3')
mixer.music.set_volume(0.5) #from 0.0 - 1.0
mixer.music.play()


scoring_sound = mixer.Sound('scoring sound.mp3')
kick = mixer.Sound('touching sound.mp3')

# GAME LOOP:
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        packman.reset()
        packman.update()
        foods.draw(window)
        enemies.draw(window)
        enemies.update()

        if sprite.spritecollide(packman,foods,True):
            scoring_sound.play()
            packman.speed += 2
            print('speed:', packman.speed)
            print(len(foods))
            

        if sprite.spritecollide(packman,enemies, True):
            kick.play()
            finish = True
            window.blit(losing_background, (0, 0))

        if len(foods) <= 0: #if player eats all food, he wins
            finish = True
            window.blit(winning_background, (0, 0))


    display.update()
    clock.tick(FPS)


