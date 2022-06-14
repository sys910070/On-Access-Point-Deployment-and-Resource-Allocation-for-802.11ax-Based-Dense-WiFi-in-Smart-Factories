import pygame
pygame.init()
from parameter import*

win = pygame.display.set_mode((200, 180))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()
class Device_animate():
    def __init__(self, device):
        self.x = device.x
        self.y = device.y
        self.vx = device.vx
        self.vy = device.vy
        self.power = device.power
        self.channel = device.channel
        self.id = device.id
        self.type = device.type
        self.state = device.state
        self.ap = device.ap
        self.throughput = device.throughput
        self.timer = device.timer
    
    def move(self):
        self.x += self.vx
        self.y += self.vy

#main loop
run = True
while run :
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False
    win.fill(WHITE)
    pygame.draw.circle(win, RED, (50, 50), 2)    
    pygame.display.update()
    keys = pygame.key.get_pressed()
    
    # if keys[pygame.K_ESCAPE]:
    #     run = False
    # if not(man.isJump):
    #     if keys[pygame.K_LEFT]:
    #         man.x -= man.vel
    #     if keys[pygame.K_RIGHT]:
    #         man.x += man.vel
    #     if keys[pygame.K_UP]:
    #         man.isJump = True
    # else :
    #     if man.jumpCount < -10:
    #         neg = 1
    #         if man.jumpCount < 0:
    #             neg = -1
    #         y -= (man.jumpCount ** 2) * 0.5 * neg
    #         man.jumpCount -= 1
    #     else:
    #         man.isJump = False
    #         man.jumpCount = 10

    # redraw()
pygame.quit()