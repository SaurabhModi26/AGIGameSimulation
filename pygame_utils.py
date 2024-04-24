import pygame




#Popups  Variables
popup_width = 0
popup_height = 0
popup_title = ""
popup_text = ""

show_popup = False

# font = pygame.font.Font("assets/japanese.otf", 20)

def create_popup(p_title, p_text, p_x, p_y, win, WINDOW_HEIGHT, WINDOW_WIDTH):
    # Define colors
    background_color = (255, 255, 200)
    border_color = (0, 0, 0)
    title_color = (0, 0, 0)
    text_color = (0, 0, 0)

    # Define padding and spacing
    padding = 20
    title_spacing = 20
    line_spacing = 10
    text_font_size = 14
    title_font_size = 14
    border_width = 2

    max_line_width = max(len(line) for line in p_text.split("\n"))
    # Calculate the required width for the popup content
    content_width = (max_line_width * text_font_size) + (2 * padding)
    # Calculate the width of the popup based on the content width and desired padding
    popup_width = min(content_width, WINDOW_WIDTH - (2 * padding))
    # Calculate the dimensions of the popup based on text length
    popup_height = (len(p_text.split("\n")) + 3) * line_spacing + title_spacing

    if p_x + popup_width > WINDOW_WIDTH:
        p_x = WINDOW_WIDTH - popup_width
    if p_y + popup_height > WINDOW_HEIGHT:
        p_y = WINDOW_HEIGHT - popup_height
    # Create the popup rectangle
    popup_rect = pygame.Rect(p_x, p_y, popup_width, popup_height)

    # Draw the rectangle popup background
    pygame.draw.rect(win, border_color, popup_rect, border_width)
    pygame.draw.rect(win, background_color, popup_rect)

    # Render the popup title
    title_font = pygame.font.Font("assets/japanese.otf", title_font_size)  # Use a bold font
    title_surface = title_font.render(p_title, True, title_color)
    title_rect = title_surface.get_rect(center=(popup_rect.centerx, popup_rect.top + padding))
    win.blit(title_surface, title_rect)

    # Render the popup text
    text_font = pygame.font.Font("assets/japanese.otf", text_font_size)
    lines = p_text.split("\n")

    # Calculate the position of the first line of text
    text_start_y = popup_rect.top + padding + title_spacing

    # Render each line of text
    for i, line in enumerate(lines):
        text_surface = text_font.render(line, True, text_color)
        text_rect = text_surface.get_rect(center=(popup_rect.centerx, text_start_y + i * line_spacing))
        win.blit(text_surface, text_rect)

# # Making a function to check collission between agents and objects
# def check_point_inside(object,x,y):
#     if(x>object.x and x<object.x_bottom and y>object.y and y<object.y_bottom):
#         return True
#     return False


def check_collision(agent,object):
    keys = pygame.key.get_pressed()

    if(agent.x < object.x + object.width and agent.x + agent.width > object.x and agent.y < object.y + object.height and agent.y + agent.height > object.y):
            if keys[pygame.K_UP]:
                agent.y = object.y + object.height
            if keys[pygame.K_DOWN]:
                agent.y = object.y - agent.height
            if keys[pygame.K_LEFT]:
                agent.x = object.x + object.width
            if keys[pygame.K_RIGHT]:
                agent.x = object.x - agent.height    