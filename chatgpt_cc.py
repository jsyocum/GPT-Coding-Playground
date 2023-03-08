import pygame
from collections import deque

# initialize Pygame
pygame.init()

# create window
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH = window.get_width()
WINDOW_HEIGHT = window.get_height()

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
scale = 10
for sprite_path in player_sprite_paths:
    sprite = pygame.image.load(sprite_path).convert_alpha()
    original_width, original_height = sprite.get_size()
    aspect_ratio = original_width / original_height
    new_width = int(WINDOW_HEIGHT / scale * aspect_ratio)
    new_height = int(WINDOW_HEIGHT / scale)
    sprite = pygame.transform.scale(sprite, (new_width, new_height))
    player_sprites.append(sprite)

# variable dictionary easily passed to any function
vd = {
    "TIME_TOTAL": 0,
    "TIME_DELTA": 0,
    "GAME_RUNNING": True,
    "WINDOW_WIDTH": WINDOW_WIDTH,
    "WINDOW_HEIGHT": WINDOW_HEIGHT,
    "WINDOW_SCALE_X": WINDOW_WIDTH / 640,
    "WINDOW_SCALE_Y": WINDOW_HEIGHT / 480,
    "GAME_SCALE": scale,
    "PLAYER_WIDTH": 32,
    "PLAYER_HEIGHT": 32,
    "GRAVITY": 2.8,
    "WALK_SPEED": 35,
    "JUMP_VELOCITY": 70,
    "DASH_SPEED": 77,
    "DASH_DURATION": 0.2,
    "DASH_COOLDOWN": 0.1,
    "CLIMB_SPEED": 21,
    "CLIMB_DURATION": 30,
    "player_rect": player_sprites[0].get_rect(),
    "player_spawn": (0, 0),
    "player_x_velocity": 0,
    "player_y_velocity": 0,
    "player_on_ground": False,
    "player_jumping": False,
    "player_wall_climbing": False,
    "player_wall_climbing_direction": 0,
    "player_wall_climb_timer": 0,
    "player_dash_timer": 0,
    "player_dash_available": True,
    "player_double_jump_available": True,
    "player_jump_after_dash": False,
    "player_x_direction": 1,
    "player_y_direction": 0,
}


def handle_timers(vd):
    for timer_name in ["player_dash_timer", "player_wall_climb_timer"]:
        if vd[timer_name] > 0:
            vd[timer_name] -= vd["TIME_DELTA"]
        else:
            vd[timer_name] = 0


def move_rect(rect: pygame.Rect, location: tuple):
    rect.center = location


# function for updating player position
def update_player_position(vd):
    # update player position based on velocities
    if vd["player_dash_timer"] > vd["DASH_COOLDOWN"]:
        vd["player_rect"].x += vd["player_x_direction"] * vd["DASH_SPEED"] * vd["WINDOW_SCALE_X"] / vd["GAME_SCALE"]
        vd["player_y_velocity"] = 0
    else:
        vd["player_rect"].x += vd["player_x_velocity"] * vd["WINDOW_SCALE_X"] / vd["GAME_SCALE"]
        vd["player_rect"].y += vd["player_y_velocity"] * vd["WINDOW_SCALE_Y"] / vd["GAME_SCALE"]

    # apply gravity to player velocity
    vd["player_y_velocity"] += vd["GRAVITY"]

    # check if player is on ground
    if vd["player_rect"].bottom >= vd["WINDOW_HEIGHT"]:
        vd["player_rect"].bottom = vd["WINDOW_HEIGHT"]
        vd["player_on_ground"] = True
        vd["player_y_velocity"] = 0

    # check if player is wall climbing
    if vd["player_wall_climbing"]:
        if vd["player_wall_climb_timer"] > 0:
            vd["player_wall_climb_timer"] -= 1
        else:
            vd["player_wall_climbing"] = False
            vd["player_x_velocity"] = vd["player_wall_climbing_direction"] * vd["WALK_SPEED"]

    # check for collision with walls
    wall_rects = [pygame.Rect(0, 0, 20, vd["WINDOW_HEIGHT"]), pygame.Rect(
        vd["WINDOW_WIDTH"] - 20, 0, 20, vd["WINDOW_HEIGHT"])]
    for wall_rect in wall_rects:
        if vd["player_rect"].colliderect(wall_rect):
            # check if player is climbing wall
            if vd["player_wall_climbing"]:
                vd["player_y_velocity"] = 0
                if vd["player_rect"].left < wall_rect.left:
                    vd["player_rect"].left = wall_rect.left - vd["PLAYER_WIDTH"]
                else:
                    vd["player_rect"].right = wall_rect.right + vd["PLAYER_WIDTH"]
            else:
                # stop player's horizontal movement
                if vd["player_x_velocity"] > 0:
                    vd["player_rect"].right = wall_rect.left
                else:
                    vd["player_rect"].left = wall_rect.right
                vd["player_x_velocity"] = 0


# function for handling player input
def handle_player_input(vd):
    # get keyboard input
    keys = pygame.key.get_pressed()

    # quit game
    if keys[pygame.K_ESCAPE]:
        vd["GAME_RUNNING"] = False

    # handle stage reset
    if keys[pygame.K_r]:
        move_rect(vd["player_rect"], (0, 30))
        vd["player_x_velocity"] = vd["player_y_velocity"] = vd["player_dash_timer"] = 0
        vd["player_dash_available"] = True

    # handle left and right movement
    if vd["player_dash_timer"] < vd["DASH_COOLDOWN"]:
        if keys[pygame.K_LEFT]:
            vd["player_x_velocity"] = -vd["WALK_SPEED"]
            vd["player_x_direction"] = -1
        elif keys[pygame.K_RIGHT]:
            vd["player_x_velocity"] = vd["WALK_SPEED"]
            vd["player_x_direction"] = 1
        else:
            vd["player_x_velocity"] = 0

    # handle jumping and dashing detections
    if vd["player_y_velocity"] >= -3:
        vd["player_jumping"] = False

    if vd["player_on_ground"]:
        vd["player_dash_available"] = True
        vd["player_double_jump_available"] = True

    # handle jumping
    if keys[pygame.K_SPACE] and vd["player_on_ground"] and vd["player_dash_timer"] == 0:
        vd["player_y_velocity"] = -vd["JUMP_VELOCITY"]
        vd["player_on_ground"] = False
        vd["player_jumping"] = True

    # handle jumping if player jumped during dash
    if keys[pygame.K_SPACE] and vd["player_dash_timer"] == 0 and vd["player_jump_after_dash"]:
        if not vd["player_on_ground"]:
            vd["player_double_jump_available"] = False

        vd["player_y_velocity"] = -vd["JUMP_VELOCITY"]
        vd["player_on_ground"] = False
        vd["player_jumping"] = True
        vd["player_jump_after_dash"] = False

    # letting go of space ends jump early
    if not keys[pygame.K_SPACE] and vd["player_jumping"]:
        vd["player_y_velocity"] = -2
        vd["player_jumping"] = False

    # handle dashing
    if keys[pygame.K_LSHIFT] and vd["player_dash_available"]:
        if vd["player_dash_timer"] == 0:
            vd["player_dash_timer"] = vd["DASH_DURATION"] + vd["DASH_COOLDOWN"]
            vd["player_dash_available"] = False

    # handle wall climbing
    if not vd["player_on_ground"] and not vd["player_wall_climbing"]:
        wall_rects = [pygame.Rect(0, 0, 20, vd["WINDOW_HEIGHT"]), pygame.Rect(
            vd["WINDOW_WIDTH"] - 20, 0, 20, vd["WINDOW_HEIGHT"])]
        for wall_rect in wall_rects:
            if vd["player_rect"].colliderect(wall_rect):
                if keys[pygame.K_UP]:
                    vd["player_wall_climbing"] = True
                    vd["player_wall_climbing_direction"] = 1 if wall_rect.left == 0 else -1
                    vd["player_x_velocity"] = 0
                    vd["player_y_velocity"] = 0
                    vd["player_wall_climb_timer"] = vd["CLIMB_DURATION"]
                    vd["player_rect"].left = wall_rect.left - \
                        (vd["PLAYER_WIDTH"] / 2) * vd["player_wall_climbing_direction"]
                    vd["player_rect"].bottom = wall_rect.bottom

    # handle wall jump
    if vd["player_wall_climbing"] and keys[pygame.K_SPACE]:
        vd["player_y_velocity"] = -vd["JUMP_VELOCITY"]
        vd["player_x_velocity"] = vd["player_wall_climbing_direction"] * vd["WALK_SPEED"]
        vd["player_wall_climbing"] = False
        vd["player_wall_climb_timer"] = 0


def draw_player(vd):
    if vd["player_on_ground"]:
        if vd["player_x_velocity"] == 0:
            player_sprite_index = 0
        else:
            player_sprite_index = (pygame.time.get_ticks() // 100) % 2 + 1
    elif vd["player_wall_climbing"]:
        player_sprite_index = 5
    elif abs(vd["player_x_velocity"]) > 5:
        player_sprite_index = 4
    else:
        player_sprite_index = 3
    player_sprite = player_sprites[player_sprite_index]
    if vd["player_x_direction"] == -1:
        player_sprite = pygame.transform.flip(player_sprite, True, False)
    window.blit(player_sprite, vd["player_rect"])


while vd["GAME_RUNNING"]:
    # handle game timing
    vd["TIME_DELTA"] = pygame.time.get_ticks() / 1000 - vd["TIME_TOTAL"]
    vd["TIME_TOTAL"] += vd["TIME_DELTA"]

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vd["GAME_RUNNING"] = False

        # handle double jumping
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if vd["player_dash_timer"] > 0:
                if vd["player_double_jump_available"] and not vd["player_on_ground"]:
                    vd["player_jump_after_dash"] = True

                elif vd["player_on_ground"]:
                    vd["player_jump_after_dash"] = True

            if vd["player_double_jump_available"] and not vd["player_on_ground"] and vd["player_dash_timer"] == 0:
                vd["player_y_velocity"] = -vd["JUMP_VELOCITY"]
                vd["player_jumping"] = True
                vd["player_double_jump_available"] = False
                vd["player_jump_after_dash"] = False

    # handle timers
    handle_timers(vd)

    # handle player input
    handle_player_input(vd)

    # update player position
    update_player_position(vd)

    # clear screen
    window.fill((0, 0, 0))

    # draw player
    draw_player(vd)

    # update screen
    pygame.display.update()

    # set frame rate
    clock.tick(60)
