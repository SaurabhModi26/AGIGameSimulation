import pygame
import datetime
import pygame.mixer
from agent_game import Agent
from place_game import Place
from pygame_utils import create_popup,check_collision, show_popup
from pipeline import pipeline,pipeline2
from initialize import agents1,locations, paths,df
from initialize2 import agents2,locations2, paths2
import threading
from threading import Thread
import time
import warnings
from pygame import *
import moviepy
from moviepy.editor import VideoFileClip
from game_utils import T_0,T_1,T_2,T_3,T_10,T_11,T_12,T_13,T_14,T_4,T_5,T_6,T_7,T_8,T_9,env,env_night,env2,env2_night, blit_image,BLACK,WHITE,LIGHT_BLUE,background_image,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_townfolk,char_werewolf,show_story_screen,title_font,text_font,font,font_japanese,generate_popup,killing_img,voting_img
import pandas as pd
from pipeline import general_tasks
import random

# Some default settings to ignore warnings in the terminal
warnings.filterwarnings("ignore")

# Font settings
font = pygame.font.Font(None, 36)

#Initialise the pygame display and the mixer
pygame.init()
pygame.display.init()
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hayashino")
pygame.mixer.init()
pygame.mixer.music.load("assets/background_song.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Set up clock
clock = pygame.time.Clock()
time = datetime.datetime(2023, 6, 26, 7, 0)  # Starting time is 7:00 AM

# Set up the background 
current_background = env
current_background_timer = pygame.time.get_ticks()

# Start time
initial_start_time = time.now()


counter = 0    # counter for hour
data_modified = threading.Event() #event 

# location dictionaries
i_location = {}
target_location = {}
buffer_location = {}
current_actions = {}

#Showing the initial window for asking number of players in the game
num_players = show_story_screen()  

townfolkN = 0
werewolfN = 0

if(num_players==6):
    townfolkN = 5
    werewolfN = 1
    response = [agents1,{},True]
    for agent in agents1:
        i_location[agent.person.name] = agent.location
        buffer_location[agent.person.name] = agent.location
        target_location[agent.person.name] = agent.location
        current_actions[agent.person.name] = "Resting"
if(num_players==8):
    townfolkN = 6
    werewolfN = 2
    response = [agents2,{},True]
    for agent in agents2:
        i_location[agent.person.name] = agent.location
        buffer_location[agent.person.name] = agent.location
        target_location[agent.person.name] = agent.location
        current_actions[agent.person.name] = "Resting"


winning_status = "Playing"  # status of the gameplay
day = 0  # day of the simulation
global_time = [time for time in df['Time']] #global time array to extract current time for the game


is_running = True

blit_agents_location = {agent.person.name:agent.location for agent in response[0]}      # locations of agents inside the house

def fetch_data():
    global i_location, counter, day, response, winning_status,num_players,is_running,agent_current_tasks,townfolkN,werewwolfN, blit_agents_location
    while True:
        print("Day: ", day)
        
        # call the backend code as per the number of agents in the code
        if(num_players==6):
            if counter == 0:
                day+=1
            response = pipeline(counter + 7, day,num_players)
        if(num_players==8):
            if counter == 0:
                day+=1
            response = pipeline2(counter + 7, day,num_players)
        
        
        for agent in response[0]:
            buffer_location[agent.person.name] = agent.location
            if len(response[1]) != 0:
                current_actions[agent.person.name] = response[1][agent.person.name]
            else:
                current_actions[agent.person.name] = "0"
        

        blit_agents_location = {agent.person.name:agent.location for agent in response[0]}
        
        # count the number of each type of agent after every hour
        townfolkN=0
        werewolfN=0
        for agent in response[0]:
            if agent.state == "alive":
                if agent.agent_type == "WereWolf":
                    werewolfN+=1
                else:
                    townfolkN+=1
        

        # Checking for the number of werewolves and townfolks to decide the flow of the game
        status = True 
        is_running = response[2]
        if werewolfN==0:
            print("The Game has been finished. TownFolks Won.")
            print("Game Time: ", time.now()-initial_start_time)
            winning_status = "TownFolks Won"
            status = False
        elif (townfolkN<=werewolfN):
            print("The Game has been finished. WereWolfs Won.")
            print("Game Time: ", time.now()-initial_start_time)
            winning_status = "Werewolf Won"
            status = False

        if not is_running:
            print("The Game has been finished. TownFolks Won. (All Tasks Completed).")
            print("Game Time: ", time.now()-initial_start_time)
            winning_status = "TownFolks Won"
            status= False
        if not status:
            break
    
        counter += 1
        counter %= 15 
        data_modified.set()

        data_modified.wait()
        data_modified.clear()

# Initialise the thread for the backend
thread1 = Thread(target = fetch_data, args = ())
thread1.start()


# Load the images for the inside view of the locations 
haya1_image = pygame.image.load("assets\haya.jpg")
haya1_image = pygame.transform.scale(haya1_image, (220, 460))
haya1_image_rect = haya1_image.get_rect()
haya1_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2) 

haya2_image = pygame.image.load("assets\haya2.jpg")
haya2_image = pygame.transform.scale(haya2_image, (220, 460))
haya2_image_rect = haya2_image.get_rect()
haya2_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)  

haya3_image = pygame.transform.scale(haya1_image, (220, 460))
haya3_image_rect = haya3_image.get_rect()
haya3_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)  

haya4_image = pygame.transform.scale(haya2_image, (220, 460))
haya4_image_rect = haya4_image.get_rect()
haya4_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)  

haya5_image = pygame.transform.scale(haya1_image, (220, 460))
haya5_image_rect = haya5_image.get_rect()
haya5_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)  

haya6_image = pygame.transform.scale(haya2_image, (220, 460))
haya6_image_rect = haya6_image.get_rect()
haya6_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)  

yamamoto_image = pygame.image.load("assets\yamamoto.jpg")
yamamoto_image = pygame.transform.scale(yamamoto_image, (440, 420))
yamamoto_image_rect = yamamoto_image.get_rect()
yamamoto_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)   

store_image = pygame.image.load("assets\storeroom.jpg")
# store_image = pygame.transform.scale(store_image, (440, 420))
store_image_rect = store_image.get_rect()
store_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)   

college_image = pygame.image.load("assets\college.jpg")
# college_image = pygame.transform.scale(college_image, (440, 420))
college_image_rect = college_image.get_rect()
college_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)   

# Flag to indicate if the image screen is visible
haya1_image_screen_visible = False
haya2_image_screen_visible = False
haya3_image_screen_visible = False
haya4_image_screen_visible = False
haya5_image_screen_visible = False
haya6_image_screen_visible = False
yamamoto_image_screen_visible = False
store_image_screen_visible = False
college_image_screen_visible = False



# include the objects in the task data frame so that each task is associated with a particular object only

def blit_agents(location,rectangle):

   
    for agent in response[0]: 
        if blit_agents_location[agent.person.name] == location:
            if agent.state == 'alive':
                prev_x = agent.x
                prev_y = agent.y
                # object_name = general_tasks[int(current_actions[agent.person.name])] 
                if current_actions[agent.person.name] == "Resting" :
                    object_name = "Other"
                elif int(current_actions[agent.person.name]) == 0: 
                    object_name = "Other"
                else:
                    # filtered = general_tasks[general_tasks['Task Number'].isin([int(current_actions[agent.person.name])])][['Objects']].
                    object_name = general_tasks[general_tasks['Task Number'] == int(current_actions[agent.person.name])]['Objects'].values[0]
                    if object_name == "-":
                        object_name = "Other"
                try:
                    agent.x = WINDOW_WIDTH//2 - rectangle.width//2 + location.objects[object_name][0]       
                    agent.y = WINDOW_HEIGHT//2 - rectangle.height//2 + location.objects[object_name][1]  
                except Exception:
                    agent.x = WINDOW_WIDTH//2 - rectangle.width//2 + location.objects["Other"][0]       
                    agent.y = WINDOW_HEIGHT//2 - rectangle.height//2 + location.objects["Other"][1] 
                    
                if agent.show_popup == True:
                    action_emoji_number = 0
                    if current_actions[agent.person.name] != "Resting":
                        action_emoji_number = int(current_actions[agent.person.name])

                    if  action_emoji_number >= 1 and action_emoji_number<= 14 :
                        win.blit(emojis_list[action_emoji_number], (agent.x+20, agent.y - 40))
                    else:
                        win.blit(T_0, (agent.x+20, agent.y - 40))

                agent.draw_at_rest(win,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,env2,env2_night,current_background,False)
                agent.x = prev_x
                agent.y = prev_y


# Function to blit the new screen
def show_new_screen():
    
    blur = pygame.image.load("assets\\env_blur.png")
    blur = pygame.transform.scale(blur, (1300, 800))
    blur_rect = blur.get_rect()
    # Blit the new screen onto the main screen
    if haya1_image_screen_visible:
        # win.blit(blur,blur_rect)
        win.blit(blur,blur_rect)
        win.blit(haya1_image, haya1_image_rect)
        blit_agents(locations2[2], haya1_image_rect)
    if haya2_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(haya2_image, haya2_image_rect)
        blit_agents(locations2[3], haya1_image_rect)
    if haya3_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(haya3_image, haya3_image_rect)
        blit_agents(locations2[4], haya1_image_rect)
    if haya4_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(haya4_image, haya4_image_rect)
        blit_agents(locations2[5], haya1_image_rect)
    if haya5_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(haya5_image, haya5_image_rect)
        blit_agents(locations2[6], haya1_image_rect)
    if haya6_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(haya6_image, haya6_image_rect)
        blit_agents(locations2[7], haya1_image_rect)
    if yamamoto_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(yamamoto_image, yamamoto_image_rect)
        blit_agents(locations2[0], yamamoto_image_rect)
    if store_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(store_image, store_image_rect)
        blit_agents(locations2[11], store_image_rect)
    if college_image_screen_visible:
        win.blit(blur,blur_rect)
        win.blit(college_image, college_image_rect)
        blit_agents(locations2[8], college_image_rect)
    



##################### Voting starts #######################
run = True
ctr_killing_time  = 0
ctr_voting_time  = 0

field1 = {}
field2 = {}
for agent in agents1:
    field1[agent.person.name] = False
for agent in agents2:
    field2[agent.person.name] = False

emojis_list = [T_0,T_1,T_2,T_3,T_4,T_5,T_6,T_7,T_8,T_9,T_10,T_11,T_12,T_13,T_14]

def redrawGameWindow():
    
    # win.blit(env, (0,0))
   if(run == True):

    win.blit(current_background, (0, 0))
    
    # Blitting the time, day, number of werwolves alive, number of townfolks alive
    day_render = font.render(f" DAY: {day}   TIME: {global_time[counter]}    TOWNFOLKS ALIVE: {townfolkN}    WEREWOLVES ALIVE: {werewolfN}   ", True, (0,0,0))

    day_render_surface = pygame.Surface(day_render.get_size())
    day_render_surface.fill((255,255,255))
    day_render_surface.blit(day_render,(1,0))

    win.blit(day_render_surface,(0,0))

    if(num_players==6):
        for agent in agents1:
            if agent.state == 'alive':
                if agent.show_popup == True:
                    action_emoji_number = 0
                    if current_actions[agent.person.name] != "Resting":
                        action_emoji_number = int(current_actions[agent.person.name])

                    if  action_emoji_number >= 1 and action_emoji_number<= 14 :
                        win.blit(emojis_list[action_emoji_number], (agent.x+20, agent.y - 40))
                    else:
                        win.blit(T_0, (agent.x+20, agent.y - 40))
                # Blit the agents in the game
                agent.draw(win,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,env2,env2_night,current_background,field1[agent.person.name])
    
    if(num_players==8):
        for agent in agents2:
            if agent.state == 'alive':
                if agent.show_popup == True:
                    # win.blit(font.render(current_actions[agent.person.name], True, BLACK, LIGHT_BLUE), (agent.x+20, agent.y))
                    action_emoji_number = 0
                    if current_actions[agent.person.name] != "Resting":
                        action_emoji_number = int(current_actions[agent.person.name])

                    if  action_emoji_number >= 1 and action_emoji_number<= 14 :
                        win.blit(emojis_list[action_emoji_number], (agent.x+20, agent.y - 40))
                    else:
                        win.blit(T_0, (agent.x+20, agent.y - 40))
                #blit the agents in the game
                agent.draw(win,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,env2,env2_night,current_background,field2[agent.person.name])


    if show_popup:
        create_popup(popup_title , popup_text,mouse_pos[0]-80, mouse_pos[1]-20, win, WINDOW_HEIGHT, WINDOW_WIDTH)

    show_new_screen()
    
    pygame.display.update()


# main loop
while run:
    clock.tick(60)
    
    
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                 # Check if the click occurs within the image screen
                
                if haya1_image_screen_visible and not (mouse_x >= locations2[2].x and mouse_x <= locations2[2].x + locations2[2].width and mouse_y >= locations2[2].y and mouse_y <= locations2[2].y + locations2[2].height):
                    haya1_image_screen_visible = False
                elif not haya1_image_screen_visible and (mouse_x >= locations2[2].x and mouse_x <= locations2[2].x + locations2[2].width and mouse_y >= locations2[2].y and mouse_y <= locations2[2].y + locations2[2].height):
                    haya1_image_screen_visible = True
                
                if haya2_image_screen_visible and not (mouse_x >= locations2[3].x and mouse_x <= locations2[3].x + locations2[3].width and mouse_y >= locations2[3].y and mouse_y <= locations2[3].y + locations2[3].height):
                    haya2_image_screen_visible = False
                elif not haya2_image_screen_visible and (mouse_x >= locations2[3].x and mouse_x <= locations2[3].x + locations2[3].width and mouse_y >= locations2[3].y and mouse_y <= locations2[3].y + locations2[3].height):
                    haya2_image_screen_visible = True

                if haya3_image_screen_visible and not (mouse_x >= locations2[4].x and mouse_x <= locations2[4].x + locations2[4].width and mouse_y >= locations2[4].y and mouse_y <= locations2[4].y + locations2[4].height):
                    haya3_image_screen_visible = False
                elif not haya3_image_screen_visible and (mouse_x >= locations2[4].x and mouse_x <= locations2[4].x + locations2[4].width and mouse_y >= locations2[4].y and mouse_y <= locations2[4].y + locations2[4].height):
                    haya3_image_screen_visible = True

                if haya4_image_screen_visible and not (mouse_x >= locations2[5].x and mouse_x <= locations2[5].x + locations2[5].width and mouse_y >= locations2[5].y and mouse_y <= locations2[5].y + locations2[5].height):
                    haya4_image_screen_visible = False
                elif not haya4_image_screen_visible and (mouse_x >= locations2[5].x and mouse_x <= locations2[5].x + locations2[5].width and mouse_y >= locations2[5].y and mouse_y <= locations2[5].y + locations2[5].height):
                    haya4_image_screen_visible = True

                if haya5_image_screen_visible and not (mouse_x >= locations2[6].x and mouse_x <= locations2[6].x + locations2[2].width and mouse_y >= locations2[6].y and mouse_y <= locations2[6].y + locations2[6].height):
                    haya5_image_screen_visible = False
                elif not haya5_image_screen_visible and (mouse_x >= locations2[6].x and mouse_x <= locations2[6].x + locations2[2].width and mouse_y >= locations2[6].y and mouse_y <= locations2[6].y + locations2[6].height):
                    haya5_image_screen_visible = True

                if haya6_image_screen_visible and not (mouse_x >= locations2[7].x and mouse_x <= locations2[7].x + locations2[7].width and mouse_y >= locations2[7].y and mouse_y <= locations2[7].y + locations2[7].height):
                    haya6_image_screen_visible = False
                elif not haya6_image_screen_visible and (mouse_x >= locations2[7].x and mouse_x <= locations2[7].x + locations2[7].width and mouse_y >= locations2[7].y and mouse_y <= locations2[7].y + locations2[7].height):
                    haya6_image_screen_visible = True
                
                if yamamoto_image_screen_visible and not (mouse_x >= locations2[0].x and mouse_x <= locations2[0].x + locations2[0].width and mouse_y >= locations2[0].y and mouse_y <= locations2[0].y + locations2[0].height):
                    yamamoto_image_screen_visible = False
                elif not yamamoto_image_screen_visible and (mouse_x >= locations2[0].x and mouse_x <= locations2[0].x + locations2[0].width and mouse_y >= locations2[0].y and mouse_y <= locations2[0].y + locations2[0].height):
                    yamamoto_image_screen_visible = True

                if college_image_screen_visible and not (mouse_x >= locations2[8].x and mouse_x <= locations2[8].x + locations2[8].width and mouse_y >= locations2[8].y and mouse_y <= locations2[8].y + locations2[8].height):
                    college_image_screen_visible = False
                elif not college_image_screen_visible and (mouse_x >= locations2[8].x and mouse_x <= locations2[8].x + locations2[8].width and mouse_y >= locations2[8].y and mouse_y <= locations2[8].y + locations2[8].height):
                    college_image_screen_visible = True

                if store_image_screen_visible and not (mouse_x >= locations2[11].x and mouse_x <= locations2[11].x + locations2[11].width and mouse_y >= locations2[11].y and mouse_y <= locations2[11].y + locations2[11].height):
                    store_image_screen_visible = False
                elif not store_image_screen_visible and (mouse_x >= locations2[11].x and mouse_x <= locations2[11].x + locations2[11].width and mouse_y >= locations2[11].y and mouse_y <= locations2[11].y + locations2[11].height):
                    store_image_screen_visible = True
                
                # Field of view for 6 Players
                for agent in agents1:
                    if not field1[agent.person.name] and mouse_x >= agent.x and mouse_x <= agent.x + agent.width and mouse_y >= agent.y and mouse_y <= agent.y + agent.height:
                          field1[agent.person.name] = True
                    elif field1[agent.person.name] and not (mouse_x >= agent.x and mouse_x <= agent.x + agent.width and mouse_y >= agent.y and mouse_y <= agent.y + agent.height):
                          field1[agent.person.name] = False

                # Field of view for 8 Players
                for agent in agents2:
                    if not field2[agent.person.name] and mouse_x >= agent.x and mouse_x <= agent.x + agent.width and mouse_y >= agent.y and mouse_y <= agent.y + agent.height:
                          field2[agent.person.name] = True
                    elif field2[agent.person.name] and not (mouse_x >= agent.x and mouse_x <= agent.x + agent.width and mouse_y >= agent.y and mouse_y <= agent.y + agent.height):
                          field2[agent.person.name] = False


        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            if(num_players==6):
                for object in locations:
                    if object.rect.collidepoint(mouse_pos):
                        # print("Colliding")
                        popup_title = object.name_japan
                        popup_text = object.desc_japan
                        popup_width = 600
                        popup_height = 200
                        show_popup = True
                        break
                    else:
                        show_popup = False
            if(num_players==8):
                for object in locations2:
                    if object.rect.collidepoint(mouse_pos):
                        # print("Colliding")
                        popup_title = object.name_japan
                        popup_text = object.desc_japan
                        popup_width = 600
                        popup_height = 200
                        show_popup = True
                        break
                    else:
                        show_popup = False
    

    ######### Checking if the game ends ########################

    if (winning_status != "Playing"):
        # Clear the screen
        win.fill((0, 0, 0))

        win.blit(background_image, (0, 0))
        
        # Render the "Game End" message
        ans = "人狼の勝利"
        if(winning_status == "TownFolks Won"):
            ans = "タウンフォークスが勝ちました"
        else:
            ans = "人狼が勝ちました"

        text = font_japanese.render(ans, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        win.blit(text, text_rect)

        ########### Imges ###############
        image1_rect = char_werewolf.get_rect()
        image2_rect = char_townfolk.get_rect()
        image1_rect.bottomleft = (50, WINDOW_HEIGHT - 20)
        image2_rect.bottomright = (WINDOW_WIDTH - 50, WINDOW_HEIGHT - 20)
        win.blit(char_werewolf, image1_rect)
        win.blit(char_townfolk, image2_rect)



        pygame.display.flip()
        
        # Delay for a few seconds before closing the screen
        pygame.time.delay(10000)  # Adjust the delay duration as needed
        
        win.fill((0, 0, 0))
        win.blit(background_image, (0, 0))
        text = font_japanese.render("ゲームエンド", True, (255, 255, 255))
        # text = font.render("Game END", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # Draw the "Game End" message on the screen
        win.blit(text, text_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Delay for a few seconds before closing the screen
        pygame.time.delay(10000)  # Adjust the delay duration as needed
        
        # Exit the game loop
        # run = False
        pygame.mixer.music.stop()
        pygame.quit()
        break

    ####### Generating Pop Out ##########
    if (counter% 15)+7 == 19:
        if(ctr_killing_time == 0):
            # generate_popup("暇つぶし",5000)
            blit_image(killing_img, 8000)
            ctr_killing_time += 1
    else:
        ctr_killing_time = 0
    if (counter% 15)+7 == 8:
        if(ctr_voting_time == 0 and day!=1):
            # generate_popup("Voting Starts!",5000)
            blit_image(voting_img, 8000)
            ctr_voting_time += 1
    else:
        ctr_voting_time = 0
        
    if(num_players==6):
        for agent in agents1:
            if(buffer_location[agent.person.name] != target_location[agent.person.name]):
                i_location[agent.person.name] = target_location[agent.person.name]
                target_location[agent.person.name] = buffer_location[agent.person.name]
                agent.current_point = 1
                agent.move_agent(paths[i_location[agent.person.name].name][target_location[agent.person.name].name])
            else:
                agent.move_agent(paths[i_location[agent.person.name].name][target_location[agent.person.name].name])

            # if agent.x == target_location[agent.person.name].x and agent.y == target_location[agent.person.name].y:
            #     blit_agents_location = {agent.person.name:agent.location for agent in response[0]}
 
    if(num_players==8):
        for agent in agents2:
            if(buffer_location[agent.person.name] != target_location[agent.person.name]):
                i_location[agent.person.name] = target_location[agent.person.name]
                target_location[agent.person.name] = buffer_location[agent.person.name]
                agent.current_point = 1
                agent.move_agent(paths2[i_location[agent.person.name].name][target_location[agent.person.name].name])
            else:
                agent.move_agent(paths2[i_location[agent.person.name].name][target_location[agent.person.name].name]) 
            
            # if agent.x == target_location[agent.person.name].x and agent.y == target_location[agent.person.name].y:
            #     blit_agents_location = {agent.person.name:agent.location for agent in response[0]}
    
  
    # Time handling
    time += datetime.timedelta(minutes=1)  # Increment time by 1 minute
    

    if(num_players==8):
        if((counter% 15)+7 >=7 and (counter% 15)+7 < 18):
            current_background = env2
        else:
            current_background = env2_night


    redrawGameWindow()
    
thread1.join() 
    
pygame.quit()