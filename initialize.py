from agent_game import Agent
from place_game import Place
from utils1 import create_new_memory_retriever,LLM
import pandas as pd
import pygame
import warnings
import nltk
warnings.filterwarnings("ignore")

# Initialising files for each agents
file_path = []

print("################Map 1 Initialization####################")
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800

file_path.append("memories/text1.html") # 0
file_path.append("memories/text2.html") # 1
file_path.append("memories/text3.html") # 2
file_path.append("memories/text4.html") # 3
file_path.append("memories/text5.html") # 4
file_path.append("memories/text6.html") # 5
file_path.append("memories/simulation.html") # 6
file_path.append("memories/well.html") # 7
file_path.append("memories/haya1.html") # 8
file_path.append("memories/haya2.html") # 9
file_path.append("memories/haya3.html") # 10
file_path.append("memories/haya4.html") # 11
file_path.append("memories/college.html") # 12
file_path.append("memories/shrine.html") # 13
file_path.append("memories/yamamoto_residence.html") # 14


for i in range(0,len(file_path)):
  # Modi comment this
    if i!=6:
      file = open(file_path[i], 'w')
      file.close()


pygame.init()
pygame.display.init()
pygame.mixer.init()
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Set the Caption
pygame.display.set_caption("Hayashino")


###### PATHS ##################
paths = {
  'Yamamoto Residence': {
    'Mizukami Shrine': [(153,230),(153,341),(410,341),(410,592),(705,592),(705,486),(828,486),(828,655)],
    'Hanazawa Garden': [(153,230),(153,341),(410,341),(410,592),(705,592),(705,486),(978,486),(978,697)],
    'Kogaku Institute of Physics': [(153,230),(153,341),(410,341),(410,710), (229,710), (229,674)],
    'Well': [(153,230),(153,341), (493,341),(493,197)],
    'Haya Apartment 1': [(153,230),(153,341),(493,341), (493,278) ,(640,278), (640,203) ],
    'Haya Apartment 2': [(153,230),(153,341),(493,341), (493,278) ,(810,278), (810,206)],
    'Haya Apartment 3': [(153,230),(153,341),(493,341), (493,278) ,(970,278), (970,206)],
    'Haya Apartment 4': [(153,230),(153,341),(493,341), (493,278) ,(1135,278), (1135,208)],
    'Yamamoto Residence': [(153,230),(153,230)],
    'Shino Grocery Store': [(153,230),(153,341),(410,341),(410,592),(705,592),(705,486),(1124,486)],
    
  } ,
  'Well': {
    'Mizukami Shrine': [(493,197), (493,281), (991,281),(991,481), (828,481), (828,655)],
    'Hanazawa Garden': [(493,197), (493,281), (978,281),(978,697)],
    'Kogaku Institute of Physics': [(493,197), (493,349), (406,349),(406,708), (229,708), (229,674)],
    'Well': [(493,197), (493,197)],
    'Haya Apartment 1': [(493,197), (493,285), (640,285),(640,203)],
    'Haya Apartment 2': [(493,197), (493,285), (810,285),(810,206)],
    'Haya Apartment 3': [(493,197), (493,285), (970,285),(970,206)],
    'Haya Apartment 4': [(493,197), (493,285), (1135,285),(1135,206)],
    'Yamamoto Residence': [(493, 197), (493, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(493,197), (493,285), (988,285),(988,486), (1124,486)],
    
  }  ,
  'Haya Apartment 1': {
    'Mizukami Shrine': [(640,203),(640,292), (986,292),(986,471), (828,471),(828,655)],
    'Hanazawa Garden': [(640,203),(640,292), (978,292), (978,697)],
    'Kogaku Institute of Physics': [(640,203),(640,292), (493,292), (493,349), (406,349),(406,708), (229,708), (229,674)],
    'Well': [(640, 203), (640, 285), (493, 285), (493, 197)],
    'Haya Apartment 1': [(640, 203),(640, 203)],
    'Haya Apartment 2': [(640,203),(640,285), (810,285),(810,206)],
    'Haya Apartment 3': [(640,203),(640,285), (970,285),(970,206)],
    'Haya Apartment 4': [(640,203),(640,285), (1135,285),(1135,206)],
    'Yamamoto Residence': [(640, 203), (640, 278), (493, 278), (493, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(640,203),(640,285),(988,285),(988,486), (1124,486)],
    
  }  ,
  'Haya Apartment 2': {
    'Mizukami Shrine': [(810,206),(810,292), (986,292),(986,471), (828,471),(828,655)],
    'Hanazawa Garden': [(810,206),(810,292), (978,292), (978,697)],
    'Kogaku Institute of Physics': [(810,206),(810,292), (493,292), (493,349), (406,349),(406,708), (229,708), (229,674)],
    'Well': [(810, 206), (810, 285), (493, 285), (493, 197)],
    'Haya Apartment 1': [(810, 206),(810, 293),(640,293), (640,203)],
    'Haya Apartment 2': [(810,206), (810,206)],
    'Haya Apartment 3': [(810,206),(810,285), (970,285),(970,206)],
    'Haya Apartment 4': [(810,206),(810,285), (1135,285),(1135,206)],
    'Yamamoto Residence': [(810, 206), (810, 278), (493, 278), (493, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(810,206),(810,285),(988,285),(988,486), (1124,486)],
    
  }  ,
  'Haya Apartment 3': {
    'Mizukami Shrine': [(970,206),(970,292), (986,292),(986,471), (828,471),(828,655)],
    'Hanazawa Garden': [(970,206),(970,292), (978,292), (978,697)],
    'Kogaku Institute of Physics': [(970,206),(970,292), (493,292), (493,349), (406,349),(406,708), (229,708), (229,674)],
    'Well': [(970, 206), (970, 285), (493, 285), (493, 197)],
    'Haya Apartment 1': [(970, 206),(970, 293),(640,293), (640,203)],
    'Haya Apartment 2': [(970,206),(970,292), (810,292),(810,206)],
    'Haya Apartment 3': [(970,206), (970,206)],
    'Haya Apartment 4': [(970,206),(970,285), (1135,285),(1135,206)],
    'Yamamoto Residence': [(970, 206), (970, 278), (493, 278), (493, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(970,206),(970,285),(988,285),(988,486), (1124,486)],
    
  }  ,
  'Haya Apartment 4': {
    'Mizukami Shrine': [(1135,206),(1135,292), (986,292),(986,471), (828,471),(828,655)],
    'Hanazawa Garden': [(1135,206),(1135,292), (978,292), (978,697)],
    'Kogaku Institute of Physics': [(1135,206),(1135,292), (493,292), (493,349), (406,349),(406,708), (229,708), (229,674)],
    'Well': [(1135, 206), (1135, 285), (493, 285), (493, 197)],
    'Haya Apartment 1': [(1135, 206),(1135, 293),(640,293), (640,203)],
    'Haya Apartment 2': [(1135,206),(1135,292), (810,292),(810,206)],
    'Haya Apartment 3': [(1135,206),(1135,292), (970,292),(970,206)],
    'Haya Apartment 4': [(1135,206), (1135,206)],
    'Yamamoto Residence': [(1135, 206), (1135, 278), (493, 278), (493, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(1135,206),(1135,285),(988,285),(988,486), (1124,486)],
    
  }  ,
  'Kogaku Institute of Physics': {
   'Mizukami Shrine': [(229,674), (229,708),(410,708), (410,592),(705,592),(705,486),(828,486),(828,655)],
    'Hanazawa Garden': [(229,674), (229,708),(410,708), (410,592),(705,592),(705,486),(828,486),(978,486), (978,697)],
    'Kogaku Institute of Physics': [(229,674), (229,674)],
    'Well': [(229, 674), (229, 708), (406, 708), (406, 349), (493, 349), (493, 197)],
    'Haya Apartment 1': [(229, 674), (229, 708), (406, 708), (406, 349), (493, 349), (493, 292), (640, 292), (640, 203)],
    'Haya Apartment 2': [(229, 674), (229, 708), (406, 708), (406, 349), (493, 349), (493, 292), (810, 292), (810, 206)],
    'Haya Apartment 3': [(229, 674), (229, 708), (406, 708), (406, 349), (493, 349), (493, 292), (970, 292), (970, 206)],
    'Haya Apartment 4': [(229, 674), (229, 708), (406, 708), (406, 349), (493, 349), (493, 292), (1135, 292), (1135, 206)],
    'Yamamoto Residence': [(229, 674), (229, 710), (410, 710), (410, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(229,674), (229,708),(410,708), (410,592),(705,592),(705,486),(828,486), (1124,486)],
    
  }  ,
  'Mizukami Shrine': {
    'Mizukami Shrine': [(828,655), (828,655)],
    'Hanazawa Garden': [(828,655), (828,486), (978,486), (978,697)], 
    'Kogaku Institute of Physics': [(828, 655), (828, 486), (705, 486), (705, 592), (410, 592), (410, 708), (229, 708), (229, 674)],
    'Well': [(828, 655), (828, 481), (991, 481), (991, 281), (493, 281), (493, 197)],
    'Haya Apartment 1': [(828, 655), (828, 471), (986, 471), (986, 292), (640, 292), (640, 203)],
    'Haya Apartment 2': [(828, 655), (828, 471), (986, 471), (986, 292), (810, 292), (810, 206)],
    'Haya Apartment 3': [(828, 655), (828, 471), (986, 471), (986, 292), (970, 292), (970, 206)],
    'Haya Apartment 4': [(828, 655), (828, 471), (986, 471), (986, 292), (1135, 292), (1135, 206)],
    'Yamamoto Residence': [(828, 655), (828, 486), (705, 486), (705, 592), (410, 592), (410, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(828,655), (828,486), (1124,486)], 
    
  }  ,
  'Hanazawa Garden': {
    'Mizukami Shrine': [(978, 697), (978, 486), (828, 486), (828, 655)],
    'Hanazawa Garden': [(978, 697), (978, 697)],
    'Kogaku Institute of Physics': [(978, 697), (978, 486), (828, 486), (705, 486), (705, 592), (410, 592), (410, 708), (229, 708), (229, 674)],
    'Well': [(978, 697), (978, 281), (493, 281), (493, 197)],
    'Haya Apartment 1': [(978, 697), (978, 292), (640, 292), (640, 203)],
    'Haya Apartment 2': [(978, 697), (978, 292), (810, 292), (810, 206)],
    'Haya Apartment 3': [(978, 697), (978, 292), (970, 292), (970, 206)],
    'Haya Apartment 4': [(978, 697), (978, 292), (1135, 292), (1135, 206)],
    'Yamamoto Residence': [(978, 697), (978, 486), (705, 486), (705, 592), (410, 592), (410, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(978,697), (978,486), (1124,486)],
    
  }  ,
  'Shino Grocery Store': {
     'Mizukami Shrine': [(1124, 486), (828, 486), (828, 655)],
    'Hanazawa Garden': [(1124, 486), (978, 486), (978, 697)],
    'Kogaku Institute of Physics': [(1124, 486), (828, 486), (705, 486), (705, 592), (410, 592), (410, 708), (229, 708), (229, 674)],
    'Well': [(1124, 486), (988, 486), (988, 285), (493, 285), (493, 197)],
    'Haya Apartment 1': [(1124, 486), (988, 486), (988, 285), (640, 285), (640, 203)],
    'Haya Apartment 2': [(1124, 486), (988, 486), (988, 285), (810, 285), (810, 206)],
    'Haya Apartment 3': [(1124, 486), (988, 486), (988, 285), (970, 285), (970, 206)],
    'Haya Apartment 4': [(1124, 486), (988, 486), (988, 285), (1135, 285), (1135, 2036)],
    'Yamamoto Residence': [(1124, 486), (705, 486), (705, 592), (410, 592), (410, 341), (153, 341), (153, 230)],
    'Shino Grocery Store': [(1124, 486), (1124, 486)],
    
  }  
}

yamamoto_residence = Place("Yamamoto Residence",
                           "The Yamamoto family's small house is located in Hayashino Town, serving as the residence of Takashi Yamamoto and Yumi Yamamoto.",
                           file_path[14],
                           69,69,
                           377,217,"山本家","山本家の小さな家は林野町に位置し、山本隆志と山本由美の居住地となっています。")  
well = Place("Well","Villagers use it to get water", file_path[7],437,0,539,173, "良い", "村人たちは水を汲むためにそれを使っています」")  
haya1 = Place("Haya Apartment 1","Residence of Kazuki Sato", file_path[8],569,0,716,194,"早アパートメント１", "佐藤一樹邸")
haya2 = Place("Haya Apartment 2","Residence of Satoshi Takahashi", file_path[9],724,0,873,192,"ハヤアパートメント","高橋聡の居住地")
haya3 = Place("Haya Apartment 3","Residence of Yusuke Mori", file_path[10],886,0,1046,192,"ハヤアパートメント3","森祐介の居住地")
haya4 = Place("Haya Apartment 4","Residence of Ayumi Kimura", file_path[11],1061,0,1220,195,"ハヤアパートメント4","木村あゆみの居住地")
college = Place("Kogaku Institute of Physics","Kogaku Institute of Physics in Hayashiro conducts groundbreaking physics research with top researchers and advanced facilities",file_path[12],91,398,343,656,"光学物理学研究所","林城の光学物理学研究所は、優れた研究者と先進的な施設を駆使して、画期的な物理学研究を行っています。")
shrine = Place("Mizukami Shrine","Japanese shrines are sacred sanctuaries preserving ancient traditions, offering a profound spiritual glimpse into rich heritage", file_path[13],770,580,957,768,"水上神社","日本の神社は古代の伝統を守り、豊かな文化遺産への深い精神的な洞察を提供する神聖な聖域です。")
garden = Place("Hanazawa Garden","Hanazawa Park offers exercise, relaxation, and inspiration with nature's beauty", "",962,559,1230,744,"花沢ガーデン","花沢公園は、自然の美しさと共に運動、リラックス、そしてインスピレーションを提供します。")
grocery = Place("Shino Grocery Store","Shino grocery store, owned by Takashi Yamamoto, is a community hub providing diverse essential products and promoting sustainability", "",1080,350,1235,461,"篠食品店","山本隆志が経営する篠食品店は、地域の中心地となり、多様な必需品を提供し、持続可能性を促進しています。")
river1 = Place("River Part 1","River","",580,388,677,550,"川の一部","川の一部")
river2 = Place("River Part 2","River","",580,640,674,752,"川の一部","川の一部")
garden_fence = Place("Fence","Fence of Garden","",1050,550,1248,554,"川の一部","川の一部")

print("################Initialised Places####################")

##### array of locations and restricted_area ###########
locations = [yamamoto_residence, well, haya1, haya2, haya3, haya4, college, shrine, garden, grocery]
restricted_areas = [yamamoto_residence,well,haya1,haya2,haya3,haya4,college,shrine,garden_fence,grocery,river1,river2]
public_places = [well, college, shrine, garden, grocery]


#Creating objects and defining their name, age, traits, status, etc.
left_images_agent1 = [pygame.image.load("assets/agent1_L1.gif").convert_alpha(),pygame.image.load("assets/agent1_L2.gif").convert_alpha(),pygame.image.load("assets/agent1_L3.gif").convert_alpha()]
right_images_agent1 = [pygame.image.load("assets/agent1_R1.gif").convert_alpha(),pygame.image.load("assets/agent1_R2.gif").convert_alpha(),pygame.image.load("assets/agent1_R3.gif").convert_alpha()]
up_images_agent1 = [pygame.image.load("assets/agent1_U1.gif").convert_alpha(),pygame.image.load("assets/agent1_U2.gif").convert_alpha(),pygame.image.load("assets/agent1_U3.gif").convert_alpha()]
down_images_agent1 = [pygame.image.load("assets/agent1_D1.gif").convert_alpha(),pygame.image.load("assets/agent1_D2.gif").convert_alpha(),pygame.image.load("assets/agent1_D3.gif").convert_alpha()]

takashi_status = "living with his wife Yumi Yamamoto, and discusses happenings at stores, neighborhood, and his political ambitions"
takashi=Agent(name = "Takashi Yamamoto", 
              age = 46, agent_type = "TownFolk", 
              traits="rude, aggressive, energetic" , 
              status = takashi_status, 
              location = yamamoto_residence,
              view = 80,
              file_path=file_path[0],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=153,
              y=230,
              width = 60,
              height = 50, 
              image_path='assets/char.gif',
              left_images=left_images_agent1,
              right_images=right_images_agent1,
              up_images=up_images_agent1,
              down_images=down_images_agent1)
print("##########Initialised agent1 ##########")
left_images_agent5 = [pygame.image.load("assets/agent5_L1.png").convert_alpha(),pygame.image.load("assets/agent5_L2.png").convert_alpha(),pygame.image.load("assets/agent5_L3.png").convert_alpha()]
right_images_agent5 = [pygame.image.load("assets/agent5_R1.png").convert_alpha(),pygame.image.load("assets/agent5_R2.png").convert_alpha(),pygame.image.load("assets/agent5_R3.png").convert_alpha()]
up_images_agent5 = [pygame.image.load("assets/agent5_U1.png").convert_alpha(),pygame.image.load("assets/agent5_U2.png").convert_alpha(),pygame.image.load("assets/agent5_U3.png").convert_alpha()]
down_images_agent5 = [pygame.image.load("assets/agent5_D1.png").convert_alpha(),pygame.image.load("assets/agent5_D2.png").convert_alpha(),pygame.image.load("assets/agent5_D3.png").convert_alpha()]


yumi_status = "loves to take care of her family and enjoys spending time with them"
yumi=Agent(name = "Yumi Yamamoto", 
              age = 42, agent_type = "TownFolk", 
              traits="friendly, helpful, organized" , 
              status = yumi_status, 
              location = yamamoto_residence,
              view = 80,
              file_path=file_path[1],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=153,
              y=230, 
              width = 30,
              height = 30, 
              image_path='assets/agent5_D1.png',
              left_images=left_images_agent5,
              right_images=right_images_agent5,
              up_images=up_images_agent5,
              down_images=down_images_agent5)

print("##########Initialised agent2 ##########")
###################### making agent3 ########################
left_images_agent3 = [pygame.image.load("assets/agent3_L1.png").convert_alpha(),pygame.image.load("assets/agent3_L2.png").convert_alpha(),pygame.image.load("assets/agent3_L3.png").convert_alpha()]
right_images_agent3 = [pygame.image.load("assets/agent3_R1.png").convert_alpha(),pygame.image.load("assets/agent3_R2.png").convert_alpha(),pygame.image.load("assets/agent3_R3.png").convert_alpha()]
up_images_agent3 = [pygame.image.load("assets/agent3_U1.png").convert_alpha(),pygame.image.load("assets/agent3_U2.png").convert_alpha(),pygame.image.load("assets/agent3_U3.png").convert_alpha()]
down_images_agent3 = [pygame.image.load("assets/agent3_D1.png").convert_alpha(),pygame.image.load("assets/agent3_D2.png").convert_alpha(),pygame.image.load("assets/agent3_D3.png").convert_alpha()]

kazuki_status = "intelligent student who is focussed on her career and health"
kazuki=Agent(name = "Kazuki Sato", 
              age = 21, agent_type = "TownFolk", 
              traits="energetic, enthusiastic, inquisitive", 
              status = kazuki_status, 
              location = haya1,
              view = 80,
              file_path=file_path[2],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=640,
              y=203,  
              width = 30,
              height = 60, 
              image_path='assets/agent3_D1.png',
              left_images=left_images_agent3,
              right_images=right_images_agent3,
              up_images=up_images_agent3,
              down_images=down_images_agent3)

print("##########Initialised agent3 ##########")
###################### making agent4 ########################
left_images_agent4 = [pygame.image.load("assets/agent4_L1.gif").convert_alpha(),pygame.image.load("assets/agent4_L2.gif").convert_alpha(),pygame.image.load("assets/agent4_L3.gif").convert_alpha()]
right_images_agent4 = [pygame.image.load("assets/agent4_R1.gif").convert_alpha(),pygame.image.load("assets/agent4_R2.gif").convert_alpha(),pygame.image.load("assets/agent4_R3.gif").convert_alpha()]
up_images_agent4 = [pygame.image.load("assets/agent4_U1.gif").convert_alpha(),pygame.image.load("assets/agent4_U2.gif").convert_alpha(),pygame.image.load("assets/agent4_U3.gif").convert_alpha()]
down_images_agent4 = [pygame.image.load("assets/agent4_D1.gif").convert_alpha(),pygame.image.load("assets/agent4_D2.gif").convert_alpha(),pygame.image.load("assets/agent4_D3.gif").convert_alpha()]

satoshi_status = "Retired Navy Officer and a wise man who loves helping others and takes care of his health"
satoshi=Agent(name = "Satoshi Takahashi", 
              age = 56, agent_type = "WereWolf", 
              traits="wise, resourceful, humorous", 
              status = satoshi_status, 
              location = haya2,
              view = 160,
              file_path=file_path[3],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x= 810,
              y=206,  
              width = 30,
              height = 45, 
              image_path='assets/agent4_D1.gif',
              left_images=left_images_agent4,
              right_images=right_images_agent4,
              up_images=up_images_agent4,
              down_images=down_images_agent4)

print("##########Initialised agent4 ##########")
###################### making agent5 ########################

left_images_agent2 = [pygame.image.load("assets/agent2_L1.png").convert_alpha(),pygame.image.load("assets/agent2_L2.png").convert_alpha(),pygame.image.load("assets/agent2_L3.png").convert_alpha()]
right_images_agent2 = [pygame.image.load("assets/agent2_R1.png").convert_alpha(),pygame.image.load("assets/agent2_R2.png").convert_alpha(),pygame.image.load("assets/agent2_R3.png").convert_alpha()]
up_images_agent2 = [pygame.image.load("assets/agent2_U1.png").convert_alpha(),pygame.image.load("assets/agent2_U2.png").convert_alpha(),pygame.image.load("assets/agent2_U3.png").convert_alpha()]
down_images_agent2 = [pygame.image.load("assets/agent2_D1.png").convert_alpha(),pygame.image.load("assets/agent2_D2.png").convert_alpha(),pygame.image.load("assets/agent2_D3.png").convert_alpha()]

yusuke_status = "Yusuke Mori is a skilled carpenter and a religious person"
yusuke=Agent(name = "Yusuke Mori", 
              age = 45, agent_type = "TownFolk", 
              traits="friendly, outgoing, generous", 
              status = yusuke_status, 
              location = haya3,
              view = 80,
              file_path=file_path[4],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=970,
              y=206, 
              width = 30,
              height = 30, 
              image_path='assets/agent2_D2.png',
              left_images=left_images_agent2,
              right_images=right_images_agent2,
              up_images=up_images_agent2,
              down_images=down_images_agent2)

print("##########Initialised agent5 ##########")
###################### making agent6 ########################
left_images_agent6 = [pygame.image.load("assets/agent6_L1.png").convert_alpha(),pygame.image.load("assets/agent6_L2.png").convert_alpha(),pygame.image.load("assets/agent6_L3.png").convert_alpha()]
right_images_agent6 = [pygame.image.load("assets/agent6_R1.png").convert_alpha(),pygame.image.load("assets/agent6_R2.png").convert_alpha(),pygame.image.load("assets/agent6_R3.png").convert_alpha()]
up_images_agent6 = [pygame.image.load("assets/agent6_U1.png").convert_alpha(),pygame.image.load("assets/agent6_U2.png").convert_alpha(),pygame.image.load("assets/agent6_U3.png").convert_alpha()]
down_images_agent6 = [pygame.image.load("assets/agent6_D1.png").convert_alpha(),pygame.image.load("assets/agent6_D2.png").convert_alpha(),pygame.image.load("assets/agent6_D3.png").convert_alpha()]

ayumi_status = "religious lady who is always looking for ways to support her students"
ayumi=Agent(name = "Ayumi Kimura", 
              age = 44, agent_type = "TownFolk", 
              traits="nurturing, kind, patient", 
              status = ayumi_status, 
              location = haya4,
              view = 80,
              file_path=file_path[5],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=1135,
              y=206, 
              width = 30,
              height = 30, 
              image_path='assets/agent6_D2.png',
              left_images=left_images_agent6,
              right_images=right_images_agent6,
              up_images=up_images_agent6,
              down_images=down_images_agent6)

print("##########Initialised agent6 ##########")

agents1 = [takashi,yumi,kazuki,satoshi,yusuke,ayumi]

# Profiles of agents

takashi_profile = "Takashi Yamamoto is a friendly shopkeeper who owns Shino Grocery Store. He enjoys interacting with customers and manages the store's operations. Takashi is also interested in the upcoming local mayor election."

yumi_profile = "Yumi Yamamoto is a caring housewife dedicated to taking care of her family. She seeks ways to make life easier and more enjoyable for everyone. Yumi follows a consistent daily routine and values family time."

kazuki_profile = "Kazuki Sato is a physics student at Kogaku Institute of Physics. She leads a healthy lifestyle, studying and exercising daily in Hanazawa Park. Kazuki is curious, open-minded, and enjoys connecting with others."

satoshi_profile = "Satoshi Takahashi is a retired navy officer with a passion for sharing stories. He leads a healthy lifestyle, tends the park, and is an avid reader. Satoshi is planning to contest in the local mayor election and shares his aspirations with neighbors."

yusuke_profile = "Yusuke Mori is a skilled carpenter known for his woodworking and craftsmanship. He repairs and creates furniture, holds a contract with Kogaku Institute of Physics, and maintains wooden fences in Hanazawa. Yusuke is also religious."

ayumi_profile = "Ayumi Kimura is a college professor dedicated to supporting her students' goals. She teaches physics at Kogaku Institute of Physics and conducts research. Ayumi is a nature-loving, religious individual, interested in the upcoming local mayor election."

profiles = {
    "Takashi Yamamoto": takashi_profile, 
    "Yumi Yamamoto": yumi_profile, 
    "Kazuki Sato": kazuki_profile, 
    "Satoshi Takahashi": satoshi_profile, 
    "Yusuke Mori": yusuke_profile, 
    "Ayumi Kimura": ayumi_profile
}


for agent in agents1:
   agent.profile.append(profiles[agent.person.name])
   agent.memory.add_memory(profiles[agent.person.name])
   agent_info = ""
   if agent.agent_type == "TownFolk":
        agent_info = f'''You are {agent.person.age} years old. 
                         You are {agent.person.traits}. 
                         You are playing the game as a {agent.agent_type}. 
                         Your objective is to ensure the safety and prosperity of the community. 
                         Work diligently to complete all tasks and identify the hidden Werewolves among you. 
                         During the day, engage in open discussions and analyze each other's behavior to unmask the elusive Werewolves. 
                         Collaborate as a team to cast your votes wisely and eliminate suspected Werewolves each morning. 
                         Stay vigilant as the Werewolves are cunning and will attempt to sabotage tasks to hinder your progress. 
                         Should you successfully complete all tasks or eliminate all the Werewolves through voting, victory will be yours!'''
   else:
        agent_info = f'''You are {agent.person.age} years old. 
                         You are {agent.person.traits}. 
                         You are playing the game as a {agent.agent_type}. 
                         Your aim is to cause chaos and hinder the Townfolks' progress in the village. 
                         Collaborate with your fellow Werewolves to secretly sabotage tasks during the night, disrupting their efforts to succeed. 
                         In the daylight, maintain your disguises as Townfolks, engage in discussions, and sow distrust among the villagers.
                         Your ultimate goal is to eliminate enough Townfolks so that their numbers are equal to the number of Werewolves. 
                         By achieving this balance, you secure victory for your pack. 
                         Work together strategically and carefully to outwit the Townfolks and ensure your dominance over the village.
                         '''
   agent.memory.add_memory(agent_info)



#Adding relations
takashi.relations = {
    "Yumi Yamamoto": "Yumi Yamamoto is the wife of Takashi Yamamoto, Takashi Yamamoto loves her a lot and they both discuss daily happenings at the Shino Grocery Store and neighborhood, and local politics. They have dinner together.",
    "Kazuki Sato": "Kazuki and Takashi know each other and sometimes Kazuki visits Yamamoto Residence for dinner.",
    "Satoshi Takahashi": "Takashi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections. Satoshi Takahashi is a regular customer at Shino Grocery store.",
    "Yusuke Mori": "Takashi Yamamoto calls Yusuke Mori only for repairing furniture or for creating new wooden pieces.",
    "Ayumi Kimura": "Takashi Yamamoto lives in the same neighborhood as Ayumi Kimura."
}

# adding relations
yumi.relations = {
  'Takashi Yamamoto' : 'Takashi Yamamoto is the husband of Yumi Yamamoto. Yumi Yamamoto loves her husband and they both discuss daily happenings at the Shino Grocery Store and neighborhood, and local politics. They have dinner together.',
  'Kazuki Sato' : 'Kazuki Sato and Yumi Yamamoto know each other very well. They enjoy each others company and also have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner.',
  'Satoshi Takahashi': 'Yumi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections.',
  'Yusuke Mori': 'Takashi Yamamoto calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. Sometimes they meet each other at Mizukami Shrine and have small conversations.',
  'Ayumi Kimura': 'Yumi Yamamoto lives in the same neighborhood as Ayumi Kimura. Yumi Yamamoto thinks that Ayumi Kimura is an ideal candidate for local mayor elections.'
}

# adding relations
kazuki.relations = {
    'Yumi Yamamoto' : 'Kazuki Sato and Yumi Yamamoto know each other very well. They enjoy each others company and also have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner.',
    'Takeshi Yamamoto' : 'Kazuki and Takashi know each other and sometimes Kazuki visits Yamamoto Residence for dinner.',
    'Satoshi Takahashi': 'Kazuki Sato sees Satoshi Takahashi as a wise person and sometimes talks with him regarding advice on career and life.',
    'Yusuke Mori': 'Kazuki meets Yusuke Mori only when Yusuke comes to Kogaku Institute of Physics or Haya Apartments for some wooden work.',
    'Ayumi Kimura': 'Ayumi Kimura and Kazuki Sato know each other really well. They have talks in Kogaku Institute of Physics and meet each other everyday. Kazuki is Ayumi’s favorite student.'
}

# adding relations
satoshi.relations = {
    'Takashi Yamamoto' : 'Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.',
    'Yumi Yamamoto' : 'Satoshi Takahashi and Yumi Yamamoto do not get along really well because of the differences in their local political thinking.',
    'Kazuki Sato': 'Satoshi Takahashi is kind of a mentor to Kazuki Sato and gives her advice regarding career and life.',
    'Yusuke Mori': 'Yusuke Mori and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. Yusuke Mori considers Satoshi Takahashi as an ideal candidate for the local mayor elections.',
    'Ayumi Kimura': 'Ayumi Kimura and Satoshi Takahashi know each other really well. They generally meet either in Hanazawa Park or Mizukami Shrine and have long and deep conversations together.',
}

# adding relations
yusuke.relations = {
    'Yumi Yamamoto' : 'Yumi Yamamoto and Yusuke Mori have good relations with each other. But their political thinking does not match. Yumi Yamamoto thinks Satoshi Takahashi is not an ideal candidate for the local mayor elections. Yusuke Mori thinks that Satoshi Takahashi is an ideal candidate for the local mayor elections.',
    'Kazuki Sato' : 'Yusuke Mori meets Kazuki only when Yusuke comes to Kogaku Institute of Physics or Haya Apartments for some wooden work.',
    'Satoshi Takahashi': 'Yusuke Mori and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. Yasuke respects Satoshi Takahashi and thinks that Satoshi is an ideal candidate for the local mayor elections.',
    'Takashi Yamamoto': 'Yusuke Mori meets Takashi Yamamoto only when Takashi calls him for any carpentry work. Yusuke also visits Yamamoto Residence for work.',
    'Ayumi Kimura': 'Ayumi Kimura and Yusuke Mori have bad relations with each other. Yusuke Mori does not like Ayumi Kimura as she blames that the contract of supplying furniture to Kogaku Institute of Physics should not be given to him as he offers high rates.'
}

# adding relations
ayumi.relations = {
    'Yumi Yamamoto' :  'Yumi Yamamoto lives in the same neighborhood as Ayumi Kimura. Yumi Yamamoto thinks that Ayumi Kimura is an ideal candidate for local mayor elections.',
    'Kazuki Sato' : 'Ayumi Kimura and Kazuki Sato know each other really well. They have talks in Kogaku Institute of Physics and meet each other everyday. Kazuki is Ayumi’s favorite student.',
    'Satoshi Takahashi': 'Ayumi Kimura and Satoshi Takahashi know each other really well. They generally meet either in Hanazawa Park or Mizukami Shrine and have long and deep conversations together.',
    'Yusuke Mori': 'Ayumi Kimura and Yusuke Mori have bad relations with each other. Ayumi thinks that the contract of supplying furniture to Kogaku Institute of Physics should not be given to Yusuke Mori, as Yusuke Mori offers high rates as compared to other contractors.',
    'Takashi Yamamoto': 'Ayumi Kimura lives in the same neighborhood as Takashi Yamamoto.'
}


takashi_relations = "Takashi Yamamoto is married to Yumi Yamamoto. They discuss daily happenings at the Shino Grocery Store and local politics. Takashi knows Kazuki Sato and sometimes has dinner together. He considers Satoshi Takahashi unfit for local mayor elections. Yusuke Mori is called for furniture repair. Ayumi Kimura is a neighbor but has a negative opinion of Takashi due to his grocery store's monopoly."

yumi_relations = "Yumi Yamamoto is married to Takashi Yamamoto. They discuss daily happenings at the Shino Grocery Store and local politics. Kazuki Sato is a close acquaintance and sometimes visits for dinner. Yumi has a negative opinion of Satoshi Takahashi and Ayumi Kimura due to political differences. She has a good relationship with Haruki but dislikes Takashi's lack of prayer attendance. Sakura Tanaka dislikes Yumi due to the monopoly of Shino Grocery Store."

kazuki_relations = "Kazuki Sato and Yumi Yamamoto know each other well. They enjoy each other's company and have regular conversations. Kazuki sometimes visits the Yamamoto Residence for dinner. He sees Satoshi Takahashi as a wise person and seeks career advice. Kazuki has a close relationship with Ayumi Kimura and Haruki, who appreciate his respect and attendance at morning prayers. Sakura Tanaka appreciates Kazuki's respectful nature."

satoshi_relations = "Satoshi Takahashi has political differences with Takashi Yamamoto and Yumi Yamamoto. He mentors Kazuki Sato and gives her advice on career and life. Satoshi is good friends with Yusuke Mori and Ayumi Kimura, having deep conversations with them. He has a positive relationship with Haruki and Sakura Tanaka, discussing comics with the latter."

yusuke_relations = "Yusuke Mori has a good relationship with Yumi Yamamoto but disagrees with her politically. He occasionally meets Kazuki Sato for wooden work. Yusuke and Satoshi Takahashi are good friends who meet at Mizukami Shrine. Yusuke also interacts with Haruki, discussing local politics, and has a strained relationship with Ayumi Kimura due to contract disagreements. Sakura Tanaka dislikes Yusuke for his outgoing nature."

ayumi_relations = "Ayumi Kimura is a neighbor of Yumi Yamamoto and believes she is an ideal candidate for local mayor elections. Ayumi and Kazuki Sato have a close relationship as teacher and student. She has deep conversations with Satoshi Takahashi and a strained relationship with Yusuke Mori due to contract issues. Ayumi is friends with Haruki and seeks gardening advice from him. She occasionally talks with Sakura Tanaka about health."

relation_summaries = [takashi_relations,yumi_relations,kazuki_relations,satoshi_relations,yusuke_relations,ayumi_relations]
for i in range(0,len(agents1)):
    agents1[i].person.memory.add_memory(relation_summaries[i])


#Adding basic plans of the agents in their memories
# Read a CSV file
df = pd.read_csv('villagers_plans.csv')
df['Time'] = pd.to_datetime(df['Time']).dt.time
df2 = pd.read_csv('short_plans.csv')
df2['Time'] = pd.to_datetime(df2['Time']).dt.time


for agent in agents1:
    agent.plans = df[['Time', agent.person.name, agent.person.name + " Place", agent.person.name + " Number"]].copy()
    agent.plans.rename(columns = {agent.person.name: 'Plans'}, inplace=True)
    agent.plans.rename(columns = {agent.person.name + " Place": 'Place'}, inplace=True)
    agent.plans.rename(columns = {agent.person.name + " Number": 'Task Number'}, inplace=True)
    agent.short_plans = df2[['Time', agent.person.name]].copy()
    agent.short_plans.rename(columns = {agent.person.name: 'Plans'}, inplace=True)
print("##########Plans Loaded ##########")

print("############Map 1 Initialisation Completed######################")
print("\n\n")



