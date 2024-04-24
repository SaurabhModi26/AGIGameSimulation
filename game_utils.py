import pygame
# from initialize import win,WINDOW_HEIGHT,WINDOW_WIDTH
from pygame import *

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Backgrounds
env = pygame.image.load("assets/env.png").convert_alpha()
env = pygame.transform.scale(env, (1300, 800))
env_night = pygame.image.load("assets/env_night.jpeg").convert_alpha()
env_night = pygame.transform.scale(env_night, (1300, 800))
env2 = pygame.image.load("assets/env2.png").convert_alpha()
env2= pygame.transform.scale(env2, (1300, 800))
env2_night = pygame.image.load("assets/env2_night.jpeg").convert_alpha()
env2_night = pygame.transform.scale(env2_night, (1300, 800))
killing_img = pygame.image.load("assets/killing_image.jpeg").convert_alpha()
killing_img = pygame.transform.scale(killing_img, (800, 400))
voting_img = pygame.image.load("assets/voting_image.jpeg").convert_alpha()
voting_img = pygame.transform.scale(voting_img, (800, 400))


####Emojis 

T_0 =  pygame.image.load("assets/emoji/T_0.png")
T_0 = pygame.transform.scale(T_0, (100, 80))

T_1 =  pygame.image.load("assets/emoji/T_1.png")
T_1 = pygame.transform.scale(T_1, (100, 80))


T_2 =  pygame.image.load("assets/emoji/T_2.png")
T_2 = pygame.transform.scale(T_2, (100, 80))

T_3 =  pygame.image.load("assets/emoji/T_3.png")
T_3 = pygame.transform.scale(T_3, (100, 80))

T_4 =  pygame.image.load("assets/emoji/T_4.png")
T_4 = pygame.transform.scale(T_4, (100, 80))

T_5 =  pygame.image.load("assets/emoji/T_5.png")
T_5 = pygame.transform.scale(T_5, (100, 80))

T_6 =  pygame.image.load("assets/emoji/T_6.png")
T_6 = pygame.transform.scale(T_6, (100, 80))

T_7 =  pygame.image.load("assets/emoji/T_7.png")
T_7 = pygame.transform.scale(T_7, (100, 80))

T_8 =  pygame.image.load("assets/emoji/T_8.png")
T_8 = pygame.transform.scale(T_8, (100, 80))

T_9 =  pygame.image.load("assets/emoji/T_9.png")
T_9 = pygame.transform.scale(T_9, (100, 80))

T_10 =  pygame.image.load("assets/emoji/T_10.png")
T_10 = pygame.transform.scale(T_10, (100, 80))

T_11 =  pygame.image.load("assets/emoji/T_11.png")
T_11 = pygame.transform.scale(T_11, (100, 80))

T_12 =  pygame.image.load("assets/emoji/T_12.png")
T_12 = pygame.transform.scale(T_12,  (100, 80))

T_13 =  pygame.image.load("assets/emoji/T_13.png")
T_13 = pygame.transform.scale(T_13, (100, 80))

T_14 =  pygame.image.load("assets/emoji/T_14.png")
T_14 = pygame.transform.scale(T_14, (100, 80))


##### Werewolf images
left_images_werewolf = [pygame.image.load("assets/werewolf_L1.png").convert_alpha(),pygame.image.load("assets/werewolf_L2.png").convert_alpha(),pygame.image.load("assets/werewolf_L3.png").convert_alpha()]
right_images_werewolf = [pygame.image.load("assets/werewolf_R1.png").convert_alpha(),pygame.image.load("assets/werewolf_R2.png").convert_alpha(),pygame.image.load("assets/werewolf_R3.png").convert_alpha()]
up_images_werewolf = [pygame.image.load("assets/werewolf_U1.png").convert_alpha(),pygame.image.load("assets/werewolf_U2.png").convert_alpha(),pygame.image.load("assets/werewolf_U3.png").convert_alpha()]
down_images_werewolf = [pygame.image.load("assets/werewolf_D1.png").convert_alpha(),pygame.image.load("assets/werewolf_D2.png").convert_alpha(),pygame.image.load("assets/werewolf_D3.png").convert_alpha()]

char_werewolf = pygame.image.load("assets/char_werewolf.png").convert_alpha()
char_townfolk = pygame.image.load("assets/char.gif").convert_alpha()


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)

# end game image
background_image = pygame.image.load("assets/bg_end.png")  
# Resize the background image to fit the screen
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))



# Create a font object
font = pygame.font.Font(None, 22)
font_japanese = pygame.font.Font("assets/japanese.otf", 80)

def change_background():
    global current_background, current_background_timer

    if (current_background == env):
        current_background = env_night
    else:
        current_background = env

    current_background_timer = pygame.time.get_ticks()




#################### Showing Story Screen ##################



# Set up fonts
title_font = pygame.font.Font("assets/japanese.otf", 50)
text_font = pygame.font.Font("assets/japanese.otf", 24)

# Set up the storyline text
title_text = "林野村"
story_text = "ミラーホロウの狼人たちは、戦略と推理が交差する、高度な心理戦と対立が織り成す、壮大なサスペンスゲームです。"

# Set up buttons
button_width, button_height = 120, 40
button_pos = (WINDOW_WIDTH // 2 - button_width // 2, WINDOW_HEIGHT - 100)



# num_players = None
def show_story_screen():
    alpha = 0
    fade_speed = 1
    fade_out = False
      # Variable to store the selected number of players
    num_players = None
    button_width, button_height = 120, 40
    button_padding = 20
    button_x = WINDOW_WIDTH // 2 - ((button_width + button_padding) * 2) // 2
    button_y = 450
    button_rect_6 = pygame.Rect(button_x, button_y, button_width, button_height)
    button_rect_8 = pygame.Rect(button_x + button_width + button_padding, button_y, button_width, button_height)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                fade_out = True
            if event.type == KEYDOWN and event.key == K_RETURN:
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect_6.collidepoint(mouse_pos):
                    num_players = 6
                elif button_rect_8.collidepoint(mouse_pos):
                    num_players = 8

        if fade_out:
            if alpha >= 255:
                pygame.quit()
                return
            alpha += fade_speed

        win.blit(background_image, (0, 0))
        pygame.time.delay(10)  # Delay after blitting the background

        # Draw the title text with transparency
        title_surface = title_font.render(title_text, True, (255, 255, 255, alpha))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 150))
        win.blit(title_surface, title_rect)
        pygame.time.delay(10)  # Delay after blitting the title text

        # Draw a dividing line with transparency
        line_rect = pygame.Rect(200, 200, WINDOW_WIDTH - 400, 2)
        pygame.draw.rect(win, (255, 255, 255, alpha), line_rect)
        pygame.time.delay(10)  # Delay after blitting the dividing line

        # Draw the story text with transparency
        story_surface = text_font.render(story_text, True, (255, 255, 255, alpha))
        story_rect = story_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))
        win.blit(story_surface, story_rect)
        pygame.time.delay(10)  # Delay after blitting the story text

        # Draw the question text with transparency
        question_text = "プレーヤーの数を選択します (6 または 8):"
        question_surface = text_font.render(question_text, True, (255, 255, 255, alpha))
        question_rect = question_surface.get_rect(center=(WINDOW_WIDTH // 2, 400))
        win.blit(question_surface, question_rect)
        pygame.time.delay(10)  # Delay after blitting the question text

        # Draw the option buttons with transparency
       

        pygame.draw.rect(win, (0, 0, 0, alpha), button_rect_6)
        pygame.draw.rect(win, (255, 255, 255, alpha), button_rect_6.inflate(-4, -4))
        button_text_6 = text_font.render("6", True, (0, 0, 0, alpha))
        button_text_rect_6 = button_text_6.get_rect(center=button_rect_6.center)
        win.blit(button_text_6, button_text_rect_6)

        pygame.draw.rect(win, (0, 0, 0, alpha), button_rect_8)
        pygame.draw.rect(win, (255, 255, 255, alpha), button_rect_8.inflate(-4, -4))
        button_text_8 = text_font.render("8", True, (0, 0, 0, alpha))
        button_text_rect_8 = button_text_8.get_rect(center=button_rect_8.center)
        win.blit(button_text_8, button_text_rect_8)

        pygame.time.delay(10)  # Delay after blitting the option buttons
        # print("######################### Number of Players in the game = ",num_players)
        if num_players is not None:
            # If a valid option is selected, proceed to the end
            # pygame.quit()
            print("######### Number of Players in the game: ",num_players,"##########")
            return num_players

        pygame.display.flip()
        pygame.time.delay(100)  # Delay before rendering the next frame


########### Blitting image for n seconds ##############

def blit_image(image, duration):
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        current_time = pygame.time.get_ticks()

        # Clear the screen
        win.fill(WHITE)

        # Check if the image should be displayed
        if current_time - start_time < duration:
            # Blit the image onto the screen
            image_rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            win.blit(image, image_rect)
        else:
            return

        pygame.display.flip()

######### END #############




######### Generating pop up for n seconds #############

def generate_popup(text,duration):
    popup_start_time = pygame.time.get_ticks()
    popup_duration = duration  # 5 seconds in milliseconds

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        current_time = pygame.time.get_ticks()

        # Clear the screen
        # win.fill(WHITE)

        # Check if the pop-up duration has passed
        if current_time - popup_start_time >= popup_duration:
            return

        # Create the pop-up window
        popup_surface = pygame.Surface((200, 100))
        popup_surface.fill((255, 0, 0))  # Red background color
        popup_text_surface = text_font.render(text, True, (255, 255, 255))
        popup_text_rect = popup_text_surface.get_rect(center=(100, 50))
        popup_surface.blit(popup_text_surface, popup_text_rect)

        # Blit the pop-up window onto the screen
        popup_rect = popup_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        win.blit(popup_surface, popup_rect)

        pygame.display.flip()

############## END ###################
