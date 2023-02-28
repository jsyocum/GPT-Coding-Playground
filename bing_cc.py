# Import pygame module
import pygame

# Initialize pygame
pygame.init()

# Create a screen with width 800 and height 600
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption("Character Controller")

# Load the character image from a file
character_sprite = pygame.image.load("character.png")

# Get the width and height of the screen
screen_width = screen.get_width()
screen_height = screen.get_height()

# Get the width and height of the character image
character_width = character_sprite.get_width()
character_height = character_sprite.get_height()

# If the character image is too large for the screen, scale it down proportionally
if character_width > screen_width or character_height > screen_height:

    # Calculate the scaling factor based on the smaller dimension ratio
    scale_factor = 1 / 15

    # Scale down the character image by multiplying its width and height by the scaling factor
    scaled_character_sprite = pygame.transform.scale(character_sprite, (int(
        character_width * scale_factor), int(character_height * scale_factor)))

    # Use the scaled image instead of the original one
    character_sprite = scaled_character_sprite

# Get a rect object with the size and position of the character image
character_rect = character_sprite.get_rect()

# Set the initial position of the character at the center of the screen
character_rect.center = (400, 300)

# Define some constants for movement speed and gravity
WALK_SPEED = 5  # Pixels per frame
JUMP_SPEED = 15  # Pixels per frame
DASH_SPEED = 20  # Pixels per frame
GRAVITY = 1  # Pixels per frame squared

# Define some flags for movement state
is_walking_left = False  # True if holding left arrow key
is_walking_right = False  # True if holding right arrow key
is_jumping = False  # True if jumping up
is_falling = False  # True if falling down
is_dashing_left = False  # True if dashing left once per jump/fall cycle
is_dashing_right = False  # True if dashing right once per jump/fall cycle

# Define some variables for movement logic
vertical_speed = 0  # The current vertical speed of the character
dash_timer = 0  # The timer for dash cooldown

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create a loop for the main game logic
running = True
while running:

    # Fill the screen with black color
    screen.fill((0, 0, 0))

    # Draw the character on the screen
    screen.blit(character_sprite, character_rect)

    # Update the display
    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():

        # If the user clicks on the close button, exit the loop
        if event.type == pygame.QUIT:
            running = False

        # If a key is pressed down
        elif event.type == pygame.KEYDOWN:

            # If it is left arrow key, set is_walking_left flag to True
            if event.key == pygame.K_LEFT:
                is_walking_left = True

            # If it is right arrow key, set is_walking_right flag to True
            elif event.key == pygame.K_RIGHT:
                is_walking_right = True

            # If it is space key and not jumping or falling already,
            elif event.key == pygame.K_SPACE and not (is_jumping or is_falling):

                # Set is_jumping flag to True and vertical_speed to JUMP_SPEED
                is_jumping = True
                vertical_speed = JUMP_SPEED

            # If it is z key and not dashing already,
            elif event.key == pygame.K_z and not (is_dashing_left or is_dashing_right):

                # If walking left or holding left arrow key,
                if is_walking_left or (event.mod & pygame.KMOD_LSHIFT):

                    # Set is_dashing_left flag to True and dash_timer to DASH_SPEED
                    is_dashing_left = True
                    dash_timer = DASH_SPEED

                else:

                    ## Set is_dashing_right flag to True and dash_timer to DASH_SPEED
                    ## This will be executed when walking right or holding right arrow key,
                    ## Or when neither walking nor holding any arrow keys.
                    ## You can change this logic according to your preference.
                    ## For example, you can make dash direction depend on mouse position instead of keyboard input.
                    ## Or you can disable dashing when neither walking nor holding any arrow keys.
                    ## Or you can make dashing require both z key and shift key.

                    is_dashing_right = True
                    dash_timer = DASH_SPEED

        elif event.type == pygame.KEYUP:

            ## If it's left arrow key release then set `is_walking_left` flag as `False`
            if event.key == pygame.K_LEFT:
                is_walking_left = False

            ## Else-if it's right arrow key release then set `is_walking_right` flag as `False`
            elif event.key == pygame.K_RIGHT:
                is_walking_right = False

# Update the character position based on movement state and speed

    # If dashing left,
    if is_dashing_left:

        # Move the character rect left by DASH_SPEED pixels
        character_rect.x -= DASH_SPEED

        # Decrease dash_timer by 1
        dash_timer -= 1

        # If dash_timer reaches 0, set is_dashing_left flag to False
        if dash_timer == 0:
            is_dashing_left = False

    # Else-if dashing right,
    elif is_dashing_right:

        # Move the character rect right by DASH_SPEED pixels
        character_rect.x += DASH_SPEED

        # Decrease dash_timer by 1
        dash_timer -= 1

        # If dash_timer reaches 0, set is_dashing_right flag to False
        if dash_timer == 0:
            is_dashing_right = False

    # Else-if walking left,
    elif is_walking_left:

        # Move the character rect left by WALK_SPEED pixels
        character_rect.x -= WALK_SPEED

    # Else-if walking right,
    elif is_walking_right:

        # Move the character rect right by WALK_SPEED pixels
        character_rect.x += WALK_SPEED

    # If jumping,
    if is_jumping:

        # Move the character rect up by vertical_speed pixels
        character_rect.y -= vertical_speed

        ## Decrease `vertical_speed` by `GRAVITY` pixels
        ## This will make the jump arc more realistic
        vertical_speed -= GRAVITY

        ## If `vertical_speed` becomes negative or zero then
        ## Set `is_jumping` flag as `False`
        ## Set `is_falling` flag as `True`
        if vertical_speed <= 0:
         is_jumping = False
         is_falling = True

    ## Else-if falling,
    elif is_falling:

        ## Increase `vertical_speed` by `GRAVITY` pixels
        ## This will make the fall faster over time
        vertical_speed += GRAVITY

        ## Move the character rect down by `vertical_speed` pixels
        character_rect.y += vertical_speed

     ## Check for collision with screen boundaries and adjust position accordingly

    ## If `character_rect.left` < 0 then set it to 0
    if character_rect.left < 0:
        character_rect.left = 0

    ## Else-if `character_rect.right` > screen width then set it to screen width
    elif character_rect.right > screen.get_width():
        character_rect.right = screen.get_width()

    ## If `character_rect.top` < 0 then set it to 0
    if character_rect.top < 0:
        character_rect.top = 0

    ## Else-if `character_rect.bottom` > screen height then set it to screen height
    elif character_rect.bottom > screen.get_height():

        ### Set it to screen height
        ### This will make the ground level for wall climbing logic later on.
        ### You can change this according to your game design.
        ### For example, you can make a platformer game with different ground levels and platforms.
        ### Or you can make a side scroller game with scrolling background and obstacles.

        ### Set it to screen height - (screen height /10)
        ### This will leave some space below for wall climbing logic later on.
        ### You can change this according to your game design.

        #### Uncomment one of these lines according to your preference.

        #### Option A: No space below (ground level)
        #### Option B: Some space below (wall climbing level)

        #### Option A: No space below (ground level)
        #### Uncomment this line for option A.

        #### Option B: Some space below (wall climbing level)
        #### Uncomment this line for option B.

        # Option A: No space below (ground level)
        # Uncomment this line for option A.

        # character_rect.bottom = screen.get_height()

        # Option B: Some space below (wall climbing level)
        # Uncomment this line for option B.

        character_rect.bottom = screen.get_height() - (screen.get_height() / 10)

        ## Set `is_falling` flag as `False`
        ## This will stop the falling motion when the character reaches the ground
        is_falling = False

    ## Draw the character sprite on the screen at its current position
    screen.blit(character_sprite, character_rect)

    ## Update the display
    pygame.display.update()

    ## Wait for 1/60 seconds
    clock.tick(60)

## Quit pygame and exit the program when the loop ends
pygame.quit()
