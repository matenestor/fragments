import copy, os, sys
from random import randint as rng
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

# adjust these constants for different simulation result
AMOUNT_BALLS = 4
RADIUS_BALLS = 60
# WARNING values above 10 might
# cause seizures, ajdust at your own risk!
COLOUR_SPEED = 3
RADIUS_SHRINK = RADIUS_BALLS * 0.2
THRESHOLD = RADIUS_BALLS * 0.2

# program constants
WIDTH, HEIGHT = 700, 700
RESOLUTION = (WIDTH, HEIGHT)
FPS = 50
DELTA = 3
BLACK = (0, 0, 0)
COLOUR_TOP = 255 - COLOUR_SPEED
SCREEN = pygame.display.set_mode(RESOLUTION)
CLOCK = pygame.time.Clock()


def print_help():
    print("CONTROLS:\n"
          "  space            -- pause visualization\n"
          "  left mouse click -- new ball\n"
          "  q                -- quit\n")

class Ball:
    def __init__(self, ball=None, pos_x=None, pos_y=None, dir_x=None, dir_y=None):
        # ball is very first one to appear
        if ball is None:
            radius = RADIUS_BALLS
            pos_x = rng(RADIUS_BALLS, WIDTH - RADIUS_BALLS) if pos_x is None else pos_x
            pos_y = rng(RADIUS_BALLS, WIDTH - RADIUS_BALLS) if pos_y is None else pos_y
            dir_x = rng(3, 7) if rng(0, 1) == 0 else -rng(3, 7)
            dir_y = rng(3, 7) if rng(0, 1) == 0 else -rng(3, 7)
        # ball is a result of bounce and split of another ball
        else:
            radius = ball.radius
            pos_x = ball.pos_x
            pos_y = ball.pos_y

        self.radius = radius
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.colour = [
                rng(COLOUR_SPEED, COLOUR_TOP),
                rng(COLOUR_SPEED, COLOUR_TOP),
                rng(COLOUR_SPEED, COLOUR_TOP)]
        self.col_change = [COLOUR_SPEED, COLOUR_SPEED, COLOUR_SPEED]
        self.colour_hist = []


def render_frame(balls):
    is_bounced = 0
    new_balls = []

    SCREEN.fill(BLACK)

    for ball in balls:
        # compute motion
        # vertical collision
        if ball.pos_x < ball.radius - DELTA \
                or ball.pos_x > WIDTH - ball.radius + DELTA:
            ball.dir_x *= -1
            is_bounced = 1

        # horizontal collision
        if ball.pos_y < ball.radius - DELTA \
                or ball.pos_y > HEIGHT - ball.radius + DELTA:
            ball.dir_y *= -1
            is_bounced = 2

        # move ball
        ball.pos_x += ball.dir_x
        ball.pos_y += ball.dir_y

        if is_bounced > 0:
            # make ball smaller after collision
            ball.radius -= RADIUS_SHRINK

            # split ball after collision with opposite direction
            if ball.radius > THRESHOLD:
                new_balls.append(Ball(
                    ball,
                    dir_x =  ball.dir_x if is_bounced == 1 else -ball.dir_x,
                    dir_y = -ball.dir_y if is_bounced == 1 else  ball.dir_y,
                ))

            is_bounced = 0

        # compute colours
        for i in range(3):
            # boundary check
            if ball.colour[i] <= COLOUR_SPEED \
                    or ball.colour[i] >= COLOUR_TOP:
                ball.col_change[i] *= -1

            # animate colours
            ball.colour[i] += ball.col_change[i]

        # draw
        try:
            pygame.draw.circle(
                SCREEN, ball.colour, (ball.pos_x, ball.pos_y), ball.radius)
        except:
            print(ball.colour)

    # remove ball completely when it is too small
    # can't remove from a list which is just being iterated,
    # otherwise there bugs occur
    for ball in copy.copy(balls):
        if ball.radius < THRESHOLD:
            balls.remove(ball)

    # append newly created balls by splitting
    # can't append to a list which is just being iterated,
    # otherwise there bugs occur
    for ball in new_balls:
        balls.append(ball)

    pygame.display.update()
    CLOCK.tick(FPS)


def main():
    is_pause = False
    is_alive = True
    balls = [Ball() for _ in range(AMOUNT_BALLS)]

    while is_alive:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    is_alive = False
                elif event.key == pygame.K_SPACE:
                    is_pause = not is_pause
            # create new ball with mouseclick
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                balls.append(Ball(pos_x=pos_mouse[0], pos_y=pos_mouse[1]))

        # return when all balls disappeared
        if len(balls) == 0:
            is_alive = False

        if not is_pause:
            render_frame(balls)
        else:
            pygame.time.wait(100)

    pygame.quit()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('help', '--help', '-h'):
        print_help()
    else:
        pygame.init()
        main()
