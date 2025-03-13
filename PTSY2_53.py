from pygame import *

# CREATING WINDOW
win_width = 700
win_height = 700
display.set_caption("The pacman")
display.set_icon(image.load('game.png'))
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("pacmandbackground.png"), (win_width, win_height)).convert()

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
        self.image = transform.scale(image.load(player_image), (45, 45))
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
                        print(f"Collision detected at {point}")
                        return True
            return False
        
        # Check for collisions before moving
        if not check_collision(new_rect):
            self.rect = new_rect  # Only move if no collision
            




# SPRITES:
packman = Player('pac-1.png', 220, 300, 2)
food1 = GameSprite('treasure.png', 100, 100, 0)
food2 = GameSprite('treasure.png', 400, 300, 0)

foods = sprite.Group()
foods.add(food1)
foods.add(food2)

# SOUND

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

        if sprite.spritecollide(packman,foods,True):
            packman.speed += 2
            print('speed:', packman.speed)

    display.update()
    clock.tick(FPS)


