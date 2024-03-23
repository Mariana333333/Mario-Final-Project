from pygame import *

mixer.init()
FPS = 60
WIDTH, HEIGHT = 700, 525
window = display.set_mode((WIDTH, HEIGHT))
count = 0


display.set_caption('Маріо')
sprites = sprite.Group()


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, sprite_img, x, y, width, height):
        super().__init__(sprite_img, x, y, width, height)
        self.ground = False
        self.speed_y = 0
        self.speed_x = 3
        self.speed = 3
        self.jump_speed = 8
        self.gravity = 0.85

    def update(self):
        self.speed_x = 0

        pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if pressed[K_w] and self.ground:
            self.speed_y -= self.jump_speed

            self.ground = False

        # if pressed[K_s] and self.rect.y < HEIGHT - 70:
        #     self.rect.y = -self.jump_speed
        #     self.ground = False

        if pressed[K_a] and self.rect.x > 0:
            self.speed_x = -self.speed

        if pressed[K_d]:
            self.speed_x = self.speed

        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        for w in walls:
            if sprite.collide_rect(player, w):
                if self.speed_y > 0:
                    self.rect.bottom = w.rect.top
                    self.speed_y = 0
                    self.ground = True
                    break
        else:
            self.ground = False


class Enemy(GameSprite):
    def __init__(self, x, y, sprite_img='assets/snailShell.png', speed=2):
        super().__init__(sprite_img, x, y, 30, 30)
        self.speed = speed

    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, w):
                self.speed = self.speed * -1

        self.rect.x += self.speed


class Wall(GameSprite):
    def __init__(self, x, y, ):
        super().__init__('assets/grass.png', x, y, 35, 35)


class Coin(GameSprite):
    def __init__(self, x, y, ):
        super().__init__('assets/coinGold.png', x, y, 20, 20)


bg = transform.scale(image.load("assets/sky.png"), (WIDTH, HEIGHT))
player = Player('assets/p1_stand.png', 40, 350, 30, 30)

walls = []
enemys = []
coins = []
SIZE = 35
level = 1


def load_level(level=1):
    walls.clear()
    enemys.clear()
    coins.clear()
    sprites.empty()
    with open(f'Level_{level}.txt', 'r') as file:
        x, y = 0, 0
        map = file.readlines()
        for line in map:
            for symbol in line:
                if symbol == 'G':
                    walls.append(GameSprite('assets/grass.png', x, y, SIZE, SIZE))

                if symbol == 'L':
                    GameSprite('assets/liquidlavaTop.png', x, y, SIZE, SIZE)

                if symbol == 'S':
                    GameSprite('assets/spikes.png', x, y, SIZE, SIZE)

                if symbol == 'C':
                    coins.append(GameSprite('assets/coinGold.png', x, y, SIZE, SIZE))


                if symbol == 'O':
                    GameSprite('assets/boxCoin.png', x, y, SIZE, SIZE)

                if symbol == 'E':
                    enemys.append(GameSprite('assets/snailShell.png', x, y, SIZE, SIZE))

                if symbol == 'W':
                    GameSprite('assets/exit.png', x, y, SIZE, SIZE)

                if symbol == 'Z':
                    GameSprite('assets/star.png', x, y, SIZE, SIZE)

                if symbol == 'M':
                    GameSprite('assets/mushroomRed.png', x, y, SIZE, SIZE)
                if symbol == 'P':
                    player.rect.x = x
                    player.rect.y = y
                x += SIZE
            y += SIZE
            x = 0


run = True
finish = False
clock = time.Clock()

font.init()
font1 = font.SysFont('Impact', 70)
result = font1.render('YOU LOSE', True, (140, 100, 30))

load_level(level)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        player.update()
        if player.rect.x >= WIDTH:
            level += 1
            load_level(level)

        window.blit(bg, (0, 0))
        player.draw()
        sprites.draw(window)

        for c in coins:
            c.draw()
            if sprite.collide_rect(player, c):
                count += 1
                coins.remove(c)
                c.kill()


    else:
        window.blit(result, (250, 200))
    display.update()
    clock.tick(FPS)
