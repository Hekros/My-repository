from pygame import*
from random import randint

font.init()
font2 = font.SysFont('Arial', 36)
win = font2.render('YOU WIN!', True, (255,255,255))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 695:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0
speed = 1
window = display.set_mode((700, 500))
display.set_caption('Вы не пройдете дальше, пока не получите бумаги 2')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

monsters = sprite.Group()
for i in range(1,13):
    monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50,randint(1,3))
    monsters.add(monster)

rocket = player('rocket.png', 350, 400,10,10,5)
win_width = 700
win_height = 500

bullets = sprite.Group()

mixer.init()
mixer.music.load('reign.mp3')
mixer.music.play(-1)



font.init()
font2 = font.SysFont('Arial', 36)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if not finish:
        window.blit(background,(0,0))
        rocket.reset()
        rocket.update()
        bullets.update()
        monsters.update()

        bullets.draw(window)
        monsters.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50,randint(1,3))

        if score >= 10:
            finish = True
            window.blit(win,(200,200))
            mixer.music.stop()
            mixer.music.load('win.mp3')
            mixer.music.play()

        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 50))
        display.update()
time.delay(50)    