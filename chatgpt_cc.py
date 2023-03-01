import pygame

# initialize Pygame
pygame.init()

# set window dimensions
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# set player dimensions
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32

# set movement constants
WALK_SPEED = 5
JUMP_VELOCITY = 10
DASH_SPEED = 10

# set gravity constant
GRAVITY = 0.5

# set wall climbing constants
CLIMB_SPEED = 3
CLIMB_DURATION = 30

# create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# set up clock
clock = pygame.time.Clock()

# load player sprites
player_sprite_paths = [
    # "player_idle.png",
    # "player_walk1.png",
    # "player_walk2.png",
    # "player_jump.png",
    # "player_dash.png",
    # "player_wall_climb.png"
    "character.png",
    "character.png",
    "character.png",
    "character.png",
    "character.png",
    "character.png"
]
player_sprites = []
for sprite_path in player_sprite_paths:
    sprite = pygame.image.load(sprite_path).convert_alpha()
    original_width, original_height = sprite.get_size()
    aspect_ratio = original_width / original_height
    scale = 10
    new_width = int(WINDOW_HEIGHT / scale * aspect_ratio)
    new_height = int(WINDOW_HEIGHT / scale)
    sprite = pygame.transform.scale(sprite, (new_width, new_height))
    player_sprites.append(sprite)

# set up player
# player_rect = pygame.Rect(
#     WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
player_rect = player_sprites[0].get_rect()
player_x_velocity = 0
player_y_velocity = 0
player_on_ground = False
player_wall_climbing = False
player_wall_climbing_direction = 0
player_wall_climb_timer = 0

# create function for updating player position


def update_player_position():
    global player_rect
    global player_x_velocity
    global player_y_velocity
    global player_on_ground
    global player_wall_climbing
    global player_wall_climbing_direction
    global player_wall_climb_timer

    # update player position based on velocities
    player_rect.x += player_x_velocity
    player_rect.y += player_y_velocity

    # apply gravity to player velocity
    player_y_velocity += GRAVITY

    # check if player is on ground
    if player_rect.bottom >= WINDOW_HEIGHT:
        player_rect.bottom = WINDOW_HEIGHT
        player_on_ground = True
        player_y_velocity = 0

    # check if player is wall climbing
    if player_wall_climbing:
        if player_wall_climb_timer > 0:
            player_wall_climb_timer -= 1
        else:
            player_wall_climbing = False
            player_x_velocity = player_wall_climbing_direction * WALK_SPEED

    # check for collision with walls
    wall_rects = [pygame.Rect(0, 0, 20, WINDOW_HEIGHT), pygame.Rect(
        WINDOW_WIDTH - 20, 0, 20, WINDOW_HEIGHT)]
    for wall_rect in wall_rects:
        if player_rect.colliderect(wall_rect):
            # check if player is climbing wall
            if player_wall_climbing:
                player_y_velocity = 0
                if player_rect.left < wall_rect.left:
                    player_rect.left = wall_rect.left - PLAYER_WIDTH
                else:
                    player_rect.right = wall_rect.right + PLAYER_WIDTH
            else:
                # stop player's horizontal movement
                if player_x_velocity > 0:
                    player_rect.right = wall_rect.left
                else:
                    player_rect.left = wall_rect.right
                player_x_velocity = 0

# create function for handling player input


def handle_player_input():
    global player_x_velocity
    global player_y_velocity
    global player_on_ground
    global player_wall_climbing
    global player_wall_climbing_direction
    global player_wall_climb_timer

    # get keyboard input
    keys = pygame.key.get_pressed()

    # handle left and right movement
    if keys[pygame.K_LEFT]:
        player_x_velocity = -WALK_SPEED
    elif keys[pygame.K_RIGHT]:
        player_x_velocity = WALK_SPEED
    else:
        player_x_velocity = 0

    # handle jumping
    if keys[pygame.K_SPACE] and player_on_ground:
        player_y_velocity = -JUMP_VELOCITY
        player_on_ground = False

    # handle dashing
    if keys[pygame.K_LSHIFT] and not player_wall_climbing:
        if player_x_velocity != 0:
            player_x_velocity = player_x_velocity / \
                abs(player_x_velocity) * DASH_SPEED
        elif player_y_velocity != 0:
            player_y_velocity = player_y_velocity / \
                abs(player_y_velocity) * DASH_SPEED
        player_rect.inflate_ip(-PLAYER_WIDTH / 2, -PLAYER_HEIGHT / 2)

    # handle wall climbing
    if not player_on_ground and not player_wall_climbing:
        wall_rects = [pygame.Rect(0, 0, 20, WINDOW_HEIGHT), pygame.Rect(
            WINDOW_WIDTH - 20, 0, 20, WINDOW_HEIGHT)]
        for wall_rect in wall_rects:
            if player_rect.colliderect(wall_rect):
                if keys[pygame.K_UP]:
                    player_wall_climbing = True
                    player_wall_climbing_direction = 1 if wall_rect.left == 0 else -1
                    player_x_velocity = 0
                    player_y_velocity = 0
                    player_wall_climb_timer = CLIMB_DURATION
                    player_rect.left = wall_rect.left - \
                        (PLAYER_WIDTH / 2) * player_wall_climbing_direction
                    player_rect.bottom = wall_rect.bottom

    # handle wall jump
    if player_wall_climbing and keys[pygame.K_SPACE]:
        player_y_velocity = -JUMP_VELOCITY
        player_x_velocity = player_wall_climbing_direction * WALK_SPEED
        player_wall_climbing = False
        player_wall_climb_timer = 0


while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # handle player input
    handle_player_input()

    # update player position
    update_player_position()

    # # apply gravity to player velocity
    # player_y_velocity += GRAVITY
    #
    # # check for collisions with ground
    # if player_rect.bottom >= WINDOW_HEIGHT:
    #     player_rect.bottom = WINDOW_HEIGHT
    #     player_y_velocity = 0
    #     player_on_ground = True
    #
    # # check for collisions with walls
    # if player_wall_climbing:
    #     player_rect.move_ip(0, -CLIMB_SPEED * player_wall_climbing_direction)
    #     player_wall_climb_timer -= 1
    #     if player_wall_climb_timer <= 0:
    #         player_wall_climbing = False
    # else:
    #     wall_rects = [pygame.Rect(0, 0, 20, WINDOW_HEIGHT), pygame.Rect(WINDOW_WIDTH - 20, 0, 20, WINDOW_HEIGHT)]
    #     for wall_rect in wall_rects:
    #         if player_rect.colliderect(wall_rect):
    #             player_rect.clamp_ip(wall_rect)
    #             if player_rect.right == wall_rect.left or player_rect.left == wall_rect.right:
    #                 player_x_velocity = 0
    #             player_on_ground = False

    # clear screen
    window.fill((0, 0, 0))

    # draw player
    if player_on_ground:
        if player_x_velocity == 0:
            player_sprite_index = 0
        else:
            player_sprite_index = (pygame.time.get_ticks() // 100) % 2 + 1
    elif player_wall_climbing:
        player_sprite_index = 5
    elif abs(player_x_velocity) > 5:
        player_sprite_index = 4
    else:
        player_sprite_index = 3
    player_sprite = player_sprites[player_sprite_index]
    if player_x_velocity < 0:
        player_sprite = pygame.transform.flip(player_sprite, True, False)
    window.blit(player_sprite, player_rect)

    # update screen
    pygame.display.update()

    # set frame rate
    clock.tick(60)
