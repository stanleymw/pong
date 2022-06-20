import pygame
import math
import random
import numpy
clip = numpy.clip
pygame.init()



AUTO_PLAY = True
VISUALIZE_DIRECTION = False



WIDTH = 1000
HEIGHT = 1000



FRAMERATE = 60

def normalize_vel(at, relrate = 60, realrate = FRAMERATE):
    return (at * relrate)/realrate


# colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pygame.display.set_caption("Pong")

display = pygame.display.set_mode((WIDTH,HEIGHT))




paddle_height = 125
paddle_left = pygame.Rect((10, 10), (10,paddle_height))
paddle_right = pygame.Rect((WIDTH - 20, 10), (10,paddle_height))

paddle_speed = normalize_vel(10)


ball_pos = [WIDTH/2, HEIGHT/2]
ball_radius = 40
ball_max_bounce_angle = 35
ball_angle = random.randint(0,45)
ball_speed = normalize_vel(10)

origspeed = ball_speed
ball = pygame.Rect((0,0), (ball_radius, ball_radius))
clock = pygame.time.Clock()
monofont = pygame.font.SysFont("123", 45)



score = [0, 0]

def spawnball():
    global ball_angle
    global ball_pos
    global ball_speed
    global ball
    possible = [random.randint(30,60), random.randint(180-60, 180-30)]
    ball_angle = random.choice(possible)
    #
    ball.center = [WIDTH/2, HEIGHT/2]
    ball_speed = normalize_vel(3) # slow down ball when it just spawned (more time to react)



spawnball()

while True:
    display.fill(BLACK)
    clock.tick(FRAMERATE)

    pressed = pygame.key.get_pressed()
    
    #ball_speed = normalize_vel(random.randint(5,10))

    #paddle movement
    if pressed[pygame.K_DOWN]:
        paddle_right.y += paddle_speed
    if pressed[pygame.K_UP]:
        paddle_right.y -= paddle_speed

    if pressed[pygame.K_w]:
        paddle_left.y -= paddle_speed
    if pressed[pygame.K_s]:
        paddle_left.y += paddle_speed

    # auto play
    if AUTO_PLAY:
        paddle_right.centery += clip(-paddle_speed, paddle_speed, ball.centery - paddle_right.centery)
        # paddle_left.centery = ball.centery

    # clamp paddles
    if paddle_left.bottom >= HEIGHT:
        paddle_left.bottom = HEIGHT
    if paddle_left.top <= 0:
        paddle_left.top = 0

    if paddle_right.bottom >= HEIGHT:
        paddle_right.bottom = HEIGHT
    if paddle_right.top <= 0:
        paddle_right.top = 0




    #ball_angle += 1
    # ball_angle %= 360

    # draw paddles
    pygame.draw.rect(display, WHITE, paddle_left)
    pygame.draw.rect(display, WHITE, paddle_right)

    # handle ball + paddle collisions
    if paddle_left.colliderect(ball):
        #original calculation:
        # ball_angle = 180 - ball_angle
        distnormal = (paddle_left.centery - ball.centery) / (paddle_height/2)
        print(distnormal)
        ball_angle = distnormal * ball_max_bounce_angle

        ball_speed = origspeed
    if paddle_right.colliderect(ball):
        #original calculation:
        #ball_angle = 180 - ball_angle
        distnormal = (paddle_right.centery - ball.centery) / (paddle_height / 2)
        print(distnormal)
        ball_angle = 180 + distnormal * ball_max_bounce_angle

        ball_speed = origspeed

    # bounce off top
    if ball.top < 0:
        ball_angle = -ball_angle
        ball.top = 1
    if ball.bottom > HEIGHT:
        ball_angle = -ball_angle
        ball.bottom = HEIGHT - 1

    #print(ball_angle)

    if ball.right < 0:
        score[1] += 1
        spawnball()
    if ball.left > WIDTH:
        score[0] += 1
        spawnball()




    # calculate ball movement

    angrad = math.radians(ball_angle + 90)

    movy = math.cos(angrad) * ball_speed
    movx = math.sin(angrad) * ball_speed
    ball.centerx += movx
    ball.centery += movy


    pygame.draw.rect(display, WHITE, ball)

    if VISUALIZE_DIRECTION:
        pygame.draw.line(display, WHITE, ball.center, [ball.centerx + movx * 30, ball.centery + movy * 30])




    score1 = monofont.render(str(score[0]), True, WHITE)
    score2 = monofont.render(str(score[1]), True, WHITE)
    s1r = score1.get_rect()
    s2r = score2.get_rect()
    s1r.right = WIDTH//2 - 30
    s2r.left = WIDTH//2 + 30

    display.blit(score1, s1r)
    display.blit(score2, s2r)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            break
    pygame.display.flip()

pygame.quit()