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

print("################Map 2 Initialisation####################")
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
file_path.append("memories/haya5.html") # 15
file_path.append("memories/haya6.html") # 16
file_path.append("memories/text7.html") # 17
file_path.append("memories/text8.html") # 18



for i in range(0,len(file_path)):
  file = open(file_path[i], 'w')
  file.close()


pygame.init()
pygame.display.init()
pygame.mixer.init()
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Set the Caption
pygame.display.set_caption("Hayashino")


# Set the Caption
paths2 = {
  'Yamamoto Residence': {
    'Mizukami Shrine': [(1062,214),(1062,286),(858,286),(858,448),(1097,448)],
    'Hanazawa Garden': [(1062,214),(1062,286),(858,286), (858,669),(180,669),(180,543)],
    'Kogaku Institute of Physics': [(1062,214),(1062,286),(858,286), (858,669), (455,669),(455,647)],
    'Well': [(1062,214),(1062,286),(858,286), (858,669),(1100,669)],
    'Haya Apartment 1': [(1062,214),(1062,286),(77,286), (77,181)],
    'Haya Apartment 2': [(1062,214),(1062,286),(219,286), (219,181)],
    'Haya Apartment 3': [(1062,214),(1062,286),(365,286), (365,181)],
    'Haya Apartment 4': [(1062,214),(1062,286),(529,286), (529,181)],
    'Haya Apartment 5': [(1062,214),(1062,286),(679,286), (679,181)],
    'Haya Apartment 6': [(1062,214),(1062,286),(838,286), (838,181)],
    'Yamamoto Residence': [(1062,214),(1062,214)],
    'Shino Grocery Store': [(1062,214),(1062,286),(858,286), (858,669), (714,669),(714,557)],
    
  } ,
  'Haya Apartment 1': {
    'Mizukami Shrine': [(77,181), (77,286),(858,286),(858,448),(1097,448)],
    'Hanazawa Garden': [(77,181), (77,286), (858,286), (858,669),(180,669),(180,543)],
    'Kogaku Institute of Physics': [(77,181), (77,286),(858,286), (858,669), (455,669),(455,647)],
    'Well': [(77,181), (77,286),(858,286), (858,669),(1100,669)],
    'Haya Apartment 1': [(77,181), (77,181)],
    'Haya Apartment 2': [(77,181), (77,286),(219,286), (219,181)],
    'Haya Apartment 3': [(77,181), (77,286),(365,286), (365,181)],
    'Haya Apartment 4': [(77,181), (77,286),(529,286), (529,181)],
    'Haya Apartment 5': [(77,181), (77,286),(679,286), (679,181)],
    'Haya Apartment 6': [(77,181), (77,286),(838,286), (838,181)],
    'Yamamoto Residence': [(77,181), (77,286),(1062,286),(1062,214)],
    'Shino Grocery Store': [(77,181), (77,286),(858,286), (858,669), (714,669),(714,557)],
    
  },
  'Haya Apartment 2': {
    'Mizukami Shrine': [(219,181), (219,286),(858,286),(858,448),(1097,448)],
    'Hanazawa Garden': [(219,181), (219,286), (858,286), (858,669),(180,669),(180,543)],
    'Kogaku Institute of Physics': [(219,181), (219,286),(858,286), (858,669), (455,669),(455,647)],
    'Well': [(219,181), (219,286),(858,286), (858,669),(1100,669)],
    'Haya Apartment 1': [(219,181), (219,286),(77,286), (77,181)],
    'Haya Apartment 2': [(219,181), (219,181)],
    'Haya Apartment 3': [(219,181), (219,286),(365,286), (365,181)],
    'Haya Apartment 4': [(219,181), (219,286),(529,286), (529,181)],
    'Haya Apartment 5': [(219,181), (219,286),(679,286), (679,181)],
    'Haya Apartment 6': [(219,181), (219,286),(838,286), (838,181)],
    'Yamamoto Residence': [(219,181), (219,286),(1062,286),(1062,214)],
    'Shino Grocery Store': [(219,181), (219,286),(858,286), (858,669), (714,669),(714,557)],
    
  },
  
    'Haya Apartment 3': {
    'Mizukami Shrine': [(365,181), (365,286),(858,286),(858,448),(1097,448)],
    'Hanazawa Garden': [(365,181), (365,286), (858,286), (858,669),(180,669),(180,543)],
    'Kogaku Institute of Physics': [(365,181), (365,286),(858,286), (858,669), (455,669),(455,647)],
    'Well': [(365,181), (365,286),(858,286), (858,669),(1100,669)],
    'Haya Apartment 1': [(365,181), (365,286),(77,286), (77,181)],
    'Haya Apartment 2': [(365,181), (365,286),(219,286), (219,181)],
    'Haya Apartment 3': [(365,181), (365,181)],
    'Haya Apartment 4': [(365,181), (365,286),(529,286), (529,181)],
    'Haya Apartment 5': [(365,181), (365,286),(679,286), (679,181)],
    'Haya Apartment 6': [(365,181), (365,286),(838,286), (838,181)],
    'Yamamoto Residence': [(365,181), (365,286),(1062,286),(1062,214)],
    'Shino Grocery Store': [(365,181), (365,286),(858,286), (858,669), (714,669),(714,557)],
    },
    'Haya Apartment 4': {
    'Mizukami Shrine': [(529,181), (529,286),(858,286),(858,448),(1097,448)],
    'Hanazawa Garden': [(529,181), (529,286), (858,286), (858,669),(180,669),(180,543)],
    'Kogaku Institute of Physics': [(529,181), (529,286),(858,286), (858,669), (455,669),(455,647)],
    'Well': [(529,181), (529,286),(858,286), (858,669),(1100,669)],
    'Haya Apartment 1': [(529,181), (529,286),(77,286), (77,181)],
    'Haya Apartment 2': [(529,181), (529,286),(219,286), (219,181)],
    'Haya Apartment 3': [(529,181), (529,286),(365,286), (365,181)],
    'Haya Apartment 4': [(529,181), (529,181)],
    'Haya Apartment 5': [(529,181), (529,286),(679,286), (679,181)],
    'Haya Apartment 6': [(529,181), (529,286),(838,286), (838,181)],
    'Yamamoto Residence': [(529,181), (529,286),(1062,286),(1062,214)],
    'Shino Grocery Store': [(529,181), (529,286),(858,286), (858,669), (714,669),(714,557)],
    },
    'Haya Apartment 5': {
    'Mizukami Shrine': [(679,181), (679,286),(858,286),(858,448),(1097,448)],
    'Hanazawa Garden': [(679,181), (679,286), (858,286), (858,669),(180,669),(180,543)],
    'Kogaku Institute of Physics': [(679,181), (679,286),(858,286), (858,669), (455,669),(455,647)],
    'Well': [(679,181), (679,286),(858,286), (858,669),(1100,669)],
    'Haya Apartment 1': [(679,181), (679,286),(77,286), (77,181)],
    'Haya Apartment 2': [(679,181), (679,286),(219,286), (219,181)],
    'Haya Apartment 3': [(679,181), (679,286),(365,286), (365,181)],
    'Haya Apartment 4': [(679,181), (679,286),(529,286), (529,181)],
    'Haya Apartment 5': [(679,181),(679,181)],
    'Haya Apartment 6': [(679,181), (679,286),(838,286), (838,181)],
    'Yamamoto Residence': [(679,181), (679,286),(1062,286),(1062,214)],
    'Shino Grocery Store': [(679,181), (679,286),(858,286), (858,669), (714,669),(714,557)],
    },
    'Haya Apartment 6': {
        'Mizukami Shrine': [(838,181), (838,286),(858,286),(858,448),(1097,448)],
        'Hanazawa Garden': [(838,181), (838,286), (858,286), (858,669),(180,669),(180,543)],
        'Kogaku Institute of Physics': [(838,181), (838,286),(858,286), (858,669), (455,669),(455,647)],
        'Well': [(838,181), (838,286),(858,286), (858,669),(1100,669)],
        'Haya Apartment 1': [(838,181), (838,286),(77,286), (77,181)],
        'Haya Apartment 2': [(838,181), (838,286),(219,286), (219,181)],
        'Haya Apartment 3': [(838,181), (838,286),(365,286), (365,181)],
        'Haya Apartment 4': [(838,181), (838,286),(529,286), (529,181)],
        'Haya Apartment 5': [(838,181),(838,286),(679,286), (679,181)],
        'Haya Apartment 6': [(838,181), (838,181)],
        'Yamamoto Residence': [(838,181), (838,286),(1062,286),(1062,214)],
        'Shino Grocery Store': [(838,181), (838,286),(858,286), (858,669), (714,669),(714,557)],
    },
    'Hanazawa Garden': {
        'Mizukami Shrine': [(180,543),(180,669),(858,669),(858,448),(1097,448)],
        'Hanazawa Garden': [(180,543),(180,543)],
        'Kogaku Institute of Physics': [(180,543),(180,669),(455,669),(455,647)],
        'Well': [(180,543),(180,669),(1100,669)],
        'Haya Apartment 1': [(180,543),(180,669),(858,669),(858,286),(77,286), (77,181)],
        'Haya Apartment 2': [(180,543),(180,669),(858,669),(858,286),(219,286), (219,181)],
        'Haya Apartment 3': [(180,543),(180,669),(858,669),(858,286),(365,286), (365,181)],
        'Haya Apartment 4': [(180,543),(180,669),(858,669),(858,286),(529,286), (529,181)],
        'Haya Apartment 5': [(180,543),(180,669),(858,669),(858,286),(679,286), (679,181)],
        'Haya Apartment 6': [(180,543),(180,669),(858,669),(858,286),(838,286), (838,181)],
        'Yamamoto Residence': [(180, 543), (180, 669), (858, 669), (858, 286), (1062, 286), (1062, 214)],
        'Shino Grocery Store': [(180,543),(180,669),(714,669),(714,557)],

    },
    'Kogaku Institute of Physics': {
        'Mizukami Shrine': [(455,647),(455,669),(858,669),(858,448),(1097,448)],
        'Hanazawa Garden': [(455, 647), (455, 669), (180, 669), (180, 543)],
        'Kogaku Institute of Physics': [(455,647),(455,647)],
        'Well': [(455,647),(455,669),(1100,669)],
        'Haya Apartment 1': [(455,647),(455,669),(858,669),(858,286),(77,286), (77,181)],
        'Haya Apartment 2': [(455,647),(455,669),(858,669),(858,286),(219,286), (219,181)],
        'Haya Apartment 3': [(455,647),(455,669),(858,669),(858,286),(365,286), (365,181)],
        'Haya Apartment 4': [(455,647),(455,669),(858,669),(858,286),(529,286), (529,181)],
        'Haya Apartment 5': [(455,647),(455,669),(858,669),(858,286),(679,286), (679,181)],
        'Haya Apartment 6': [(455,647),(455,669),(858,669),(858,286),(838,286), (838,181)],
        'Yamamoto Residence': [(455,647),(455,669), (858, 669), (858, 286), (1062, 286), (1062, 214)],
        'Shino Grocery Store': [(455,647),(455,669),(714,669),(714,557)],

    },
    'Shino Grocery Store': {
        'Mizukami Shrine': [(714,557), (714,669), (858,669), (858,448), (1097,448)],
        'Hanazawa Garden': [(714,557), (714,669), (180,669), (180,543)],
        'Kogaku Institute of Physics': [(714, 557), (714, 669), (455, 669), (455, 647)],
        'Well': [(714,557), (714,669), (1100,669)],
        'Haya Apartment 1': [(714,557), (714,669), (858,669), (858,286), (77,286), (77,181)],
        'Haya Apartment 2': [(714,557), (714,669), (858,669), (858,286), (219,286), (219,181)],
        'Haya Apartment 3': [(714,557), (714,669), (858,669), (858,286), (365,286), (365,181)],
        'Haya Apartment 4': [(714,557), (714,669), (858,669), (858,286), (529,286), (529,181)],
        'Haya Apartment 5': [(714,557), (714,669), (858,669), (858,286), (679,286), (679,181)],
        'Haya Apartment 6': [(714,557), (714,669), (858,669), (858,286), (838,286), (838,181)],
        'Yamamoto Residence': [(714,557), (714,669), (858,669), (858,286), (1062,286), (1062,214)],
        'Shino Grocery Store': [(714,557), (714,557)]
    },
    'Well': {
        'Mizukami Shrine': [(1100,669), (858,669), (858,448), (1097,448)],
        'Hanazawa Garden': [(1100,669), (858,669), (180,669), (180,543)],
        'Kogaku Institute of Physics': [(1100,669), (858,669), (455,669), (455,647)],
        'Well': [(1100,669), (1100,669)],
        'Haya Apartment 1': [(1100,669), (858,669), (858,286), (77,286), (77,181)],
        'Haya Apartment 2': [(1100,669), (858,669), (858,286), (219,286), (219,181)],
        'Haya Apartment 3': [(1100,669), (858,669), (858,286), (365,286), (365,181)],
        'Haya Apartment 4': [(1100,669), (858,669), (858,286), (529,286), (529,181)],
        'Haya Apartment 5': [(1100,669), (858,669), (858,286), (679,286), (679,181)],
        'Haya Apartment 6': [(1100,669), (858,669), (858,286), (838,286), (838,181)],
        'Yamamoto Residence': [(1100,669), (858,669), (858,286), (1062,286), (1062,214)],
        'Shino Grocery Store': [(1100,669), (714,669),(714,557)]
    },
    'Mizukami Shrine': {
        'Mizukami Shrine': [(1097,448),(1097,448)],
        'Hanazawa Garden': [ [(1097, 448), (858, 448), (858, 669), (180, 669), (180, 543)]],
        'Kogaku Institute of Physics': [(1097, 448), (858, 448), (858, 669), (455, 669), (455, 647)],
        'Well':  [(1097, 448), (858, 448), (858, 669), (455, 669), (455, 647), (714, 557)],
        'Haya Apartment 1': [(1097, 448), (858, 448), (858, 286), (77, 286), (77, 181)],
        'Haya Apartment 2':  [(1097, 448), (858, 448), (858, 286), (219, 286), (219, 181)],
        'Haya Apartment 3': [(1097, 448), (858, 448), (858, 286), (365, 286), (365, 181)],
        'Haya Apartment 4':  [(1097, 448), (858, 448), (858, 286), (529, 286), (529, 181)],
        'Haya Apartment 5': [(1097, 448), (858, 448), (858, 286), (679, 286), (679, 181)],
        'Haya Apartment 6': [(1097, 448), (858, 448), (858, 286), (838, 286), (838, 181)],
        'Yamamoto Residence': [(1097, 448), (858, 448), (858, 286), (1062, 286), (1062, 214)],
        'Shino Grocery Store': [(1097, 448), (858, 448), (858, 669), (714, 669), (714, 557)]
    }
  
}



yamamoto_residence = Place("Yamamoto Residence",
                           "The Yamamoto family's small house is located in Hayashino Town, serving as the residence of Takashi Yamamoto and Yumi Yamamoto.",
                           file_path[14],
                           996,51,
                           1268,199,"山本家","山本家の小さな家は林野町に位置し、山本隆志と山本由美の居住地となっています。")  
well = Place("Well","Villagers use it to get water", file_path[7],107,617,1278,757, "良い", "村人たちは水を汲むためにそれを使っています」")  
haya1 = Place("Haya Apartment 1","Residence of Kazuki Sato", file_path[8],52,67,165,188,"早アパートメント１", "佐藤一樹邸")
haya2 = Place("Haya Apartment 2","Residence of Satoshi Takahashi", file_path[9],173,52,303,188,"ハヤアパートメント","高橋聡の居住地")
haya3 = Place("Haya Apartment 3","Residence of Yusuke Mori", file_path[10],317,61,446,176,"ハヤアパートメント3","森祐介の居住地")
haya4 = Place("Haya Apartment 4","Residence of Ayumi Kimura", file_path[11],486,55,609,182,"ハヤアパートメント4","木村あゆみの居住地")
haya5 = Place("Haya Apartment 5","Residence of Haruki", file_path[15],629,57,765,188,"ハヤアパートメント5","木村あゆみの居住地")
haya6 = Place("Haya Apartment 6","Residence of Sakura Tanaka", file_path[16],792,57,931,198,"ハヤアパートメント6","木村あゆみの居住地")
college = Place("Kogaku Institute of Physics","Kogaku Institute of Physics in Hayashiro conducts groundbreaking physics research with top researchers and advanced facilities",file_path[12],319,380,592,629,"光学物理学研究所","林城の光学物理学研究所は、優れた研究者と先進的な施設を駆使して、画期的な物理学研究を行っています。")
shrine = Place("Mizukami Shrine","Japanese shrines are sacred sanctuaries preserving ancient traditions, offering a profound spiritual glimpse into rich heritage", file_path[13],1082,417,1262,547,"水上神社","日本の神社は古代の伝統を守り、豊かな文化遺産への深い精神的な洞察を提供する神聖な聖域です。")
garden2 = Place("Hanazawa Garden","Hanazawa Park offers exercise, relaxation, and inspiration with nature's beauty", "",47,367,271,627,"花沢ガーデン","花沢公園は、自然の美しさと共に運動、リラックス、そしてインスピレーションを提供します。")
grocery = Place("Shino Grocery Store","Shino grocery store, owned by Takashi Yamamoto, is a community hub providing diverse essential products and promoting sustainability", "",644,380,819,544,"篠食品店","山本隆志が経営する篠食品店は、地域の中心地となり、多様な必需品を提供し、持続可能性を促進しています。")
river1 = Place("River Part 1","River","",580,388,677,550,"川の一部","川の一部")
river2 = Place("River Part 2","River","",580,640,674,752,"川の一部","川の一部")
garden_fence = Place("Fence","Fence of Garden","",1050,550,1248,554,"川の一部","川の一部")
print("################Initialised Places####################")





##### array of locations2 and restricted_area ###########
locations2 = [yamamoto_residence, well, haya1, haya2, haya3, haya4, haya5, haya6, college, shrine, garden2, grocery]
restricted_areas = [yamamoto_residence,well,haya1,haya2,haya3,haya4,college,shrine,garden_fence,grocery,river1,river2]

# Setting objects for haya apartments
for i in range(2,8):
    locations2[i].objects = {
        "Bed": [95,265],
        "Kitchen": [150,180],
        "Bathroom":[80,380],
        "Study":[140,110],
        "Other":[65,110]
    }

#Setting objects for yamamoto residence
yamamoto_residence.objects = {
        "Bed": [285,360],
        "Kitchen": [250,105],
        "Bathroom":[394,131],
        "Study":[65,320],
        "Other":[105,110]
    }


#Setting objects for grocery
grocery.objects = {
        "Shelf1":[62,88],
        "Shelf2":[63,250],
        "Shelf3":[62,380],
        "Counter":[440,170],
        "Customers":[440,320],
        "Other": [220,200]
    }

#Setting objects for kogaku institute of physics
college.objects = {
        "Teacher":[50,150],
        "Student":[260,150],
        "Shelf":[374,185],
        "Discussion":[440,170],
        "Other":[375,90]
    }


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
              view=80,
              file_path=file_path[0],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=1062,
              y=214,
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
              view=80,
              file_path=file_path[1],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=1062,
              y=214, 
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
              view=80,
              file_path=file_path[2],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=77,
              y=181,  
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
              view=160,
              file_path=file_path[3],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x= 219,
              y=181,  
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
              age = 45, agent_type = "WereWolf", 
              traits="friendly, outgoing, generous", 
              status = yusuke_status, 
              location = haya3,
              view=160,
              file_path=file_path[4],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=365,
              y=181, 
              width = 30,
              height = 30, 
              image_path='assets/agent2_D2.png',
              left_images=left_images_agent2,
              right_images=right_images_agent2,
              up_images=up_images_agent2,
              down_images=down_images_agent2)

print("##########Initialised agent5##########")
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
              view=80,
              file_path=file_path[5],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=529,
              y=181, 
              width = 30,
              height = 30, 
              image_path='assets/agent6_D2.png',
              left_images=left_images_agent6,
              right_images=right_images_agent6,
              up_images=up_images_agent6,
              down_images=down_images_agent6)

print("##########Initialised agent6 ##########")

###################### making agent7 ########################
left_images_agent7 = [pygame.image.load("assets/agent7_L1.png").convert_alpha(),pygame.image.load("assets/agent7_L2.png").convert_alpha(),pygame.image.load("assets/agent7_L3.png").convert_alpha()]
right_images_agent7 = [pygame.image.load("assets/agent7_R1.png").convert_alpha(),pygame.image.load("assets/agent7_R2.png").convert_alpha(),pygame.image.load("assets/agent7_R3.png").convert_alpha()]
up_images_agent7 = [pygame.image.load("assets/agent7_U1.png").convert_alpha(),pygame.image.load("assets/agent7_U2.png").convert_alpha(),pygame.image.load("assets/agent7_U3.png").convert_alpha()]
down_images_agent7 = [pygame.image.load("assets/agent7_D1.png").convert_alpha(),pygame.image.load("assets/agent7_D2.png").convert_alpha(),pygame.image.load("assets/agent7_D3.png").convert_alpha()]


# Setting X,Y, height, width of Haruki and Sakura remaining
haruki_status = "Priest at Mizukami Shrine and a religious person."
haruki=Agent(name = "Haruki", 
              age = 60, agent_type = "TownFolk", 
              traits="Introvert, Thinker, Hardworking  ", 
              status = haruki_status, 
              location = haya5,
              view=160,
              file_path= file_path[17],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=679,
              y=181, 
              width = 30,
              height = 30, 
              image_path='assets/agent7_D2.png',
              left_images=left_images_agent7,
              right_images=right_images_agent7,
              up_images=up_images_agent7,
              down_images=down_images_agent7)


print("##########Initialised agent7 ##########")
###################### making agent8 ########################
left_images_agent8 = [pygame.image.load("assets/agent8_L1.png").convert_alpha(),pygame.image.load("assets/agent8_L2.png").convert_alpha(),pygame.image.load("assets/agent8_L3.png").convert_alpha()]
right_images_agent8 = [pygame.image.load("assets/agent8_R1.png").convert_alpha(),pygame.image.load("assets/agent8_R2.png").convert_alpha(),pygame.image.load("assets/agent8_R3.png").convert_alpha()]
up_images_agent8 = [pygame.image.load("assets/agent8_U1.png").convert_alpha(),pygame.image.load("assets/agent8_U2.png").convert_alpha(),pygame.image.load("assets/agent8_U3.png").convert_alpha()]
down_images_agent8 = [pygame.image.load("assets/agent8_D1.png").convert_alpha(),pygame.image.load("assets/agent8_D2.png").convert_alpha(),pygame.image.load("assets/agent8_D3.png").convert_alpha()]

sakura_status = "Doctor and likes to read comics."
sakura=Agent(name = "Sakura Tanaka", 
              age = 55, agent_type = "TownFolk", 
              traits="Adventurous, Creative, Compassionate", 
              status = haruki_status, 
              location = haya6,
              view=80,
              file_path=file_path[18],
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=838,
              y=181, 
              width = 30,
              height = 30, 
              image_path='assets/agent8_D2.png',
              left_images=left_images_agent8,
              right_images=right_images_agent8,
              up_images=up_images_agent8,
              down_images=down_images_agent8)
print("##########Initialised agent8 ##########")

# add Haruki and Sakura afterwards
agents2 = [takashi,yumi,kazuki,satoshi,yusuke,ayumi,haruki,sakura]
# Profiles of agents
# Takashi Yamamoto's Profile
takashi_profile = [
    "Takashi Yamamoto is a shopkeeper who owns Shino Grocery Store and loves interacting with customers.",
    "Takashi manages day to day operations at the store and helps out customers with their orders.",
    "Takashi is always willing to help out and make sure everyone is taken care of. ",
    "Takashi is also really interested in the local mayor election that is coming up next month.",
]

# Adding Profile
yumi_profile = [
    "Yumi Yamamoto is a housewife who loves to take care of her family",
    "Yumi Yamamoto is always looking for new ways to make life easier and more enjoyable for everyone",
    "Yumi Yamamoto goes to bed around 10pm, wakes up around 6am, eats dinner around 6pm."
]

# Adding Profile
kazuki_profile = [
    "Kazuki Sato is a student at  Kogaku Institute of Physics studying physics and lives a healthy life",
    "Kazuki Sato is working on her physics degree and exercises every morning in the nearby Hanazawa Park",
    "Kazuki Sato loves to connect with people and explore new ideas",
]

# Adding Profile
satoshi_profile = [
    "Satoshi Takahashi is a retired navy officer who loves to share stories from his time in the military",
    "Satoshi Takahashi lives a healthy lifestyle",
    "Satoshi Takahashi is always full of interesting stories and advice",
    "Satoshi Takahashi spends his free time tending the park and is an avid reader",
    "Satoshi Takahashi is planning on contesting for local mayor in the upcoming election and he is telling his neighbors about it",
    "Satoshi Takahashi goes to bed around 9pm, wakes up around 5am, eats dinner around 5:00 pm",
]

# Adding Profile
yusuke_profile = [
    "Yusuke Mori is a skilled and experienced carpenter with a passion for woodworking and craftsmanship",
    "Yusuke Mori is the go-to person whenever people need his services for repairing old furniture or creating new pieces",
    "Yusuke Mori holds a contract of supplying furniture for Kogaku Institute of Physics",
    "Yusuke Mori is responsible for maintaining wooden Hanazawa fences",
    "Yusuke Mori is a religious person",
]

# Adding Profile
ayumi_profile = [
    "Ayumi Kimura is a college professor who loves to help people reach their goals. She is always looking for ways to support her students",
    "Ayumi Kimura is teaching a course on physics at Kogaku Institute of Physics and working on her research paper",
    "Ayumi Kimura is a religious lady and loves to interact with people",
    "Ayumi Kimura is nature loving and loves to go for a morning walk",
    "Ayumi Kimura is also really interested in the local mayor election that is coming up next month",
    "Ayumi Kimura goes to bed around 7pm, wakes up around 7am, eats dinner around 5pm"
]

haruki_profile = [
    'Haruki is a Priest at Mizukami Shrine.',
    'Haruki is very Hardworking and likes to do Gardening at Hanazawa Park.',
    'Haruki is responsible for the Morning and Evening Prayers at Mizukami Shrine.'
    'Haruki is a very religious person.'
]

sakura_profile = [
    'Sakura Tanaka is a dedicated doctor who specializes in exceptional diagnostic skills and ability to effectively communicate with patients.'
    'Sakura Tanaka is a religious person and goes to morning and evening prayers daily.'
    'Sakura Tanaka likes to read Comics and goes to Shino Grocery Store to buy the comic.'
    'Sakura Tanaka does not like to go to Kogaku Institute of Physics.'
]


# takashi_profile = "Takashi Yamamoto is a friendly shopkeeper who owns Shino Grocery Store. He enjoys interacting with customers and manages the store's operations. Takashi is also interested in the upcoming local mayor election."

# yumi_profile = "Yumi Yamamoto is a caring housewife dedicated to taking care of her family. She seeks ways to make life easier and more enjoyable for everyone. Yumi follows a consistent daily routine and values family time."

# kazuki_profile = "Kazuki Sato is a physics student at Kogaku Institute of Physics. She leads a healthy lifestyle, studying and exercising daily in Hanazawa Park. Kazuki is curious, open-minded, and enjoys connecting with others."

# satoshi_profile = "Satoshi Takahashi is a retired navy officer with a passion for sharing stories. He leads a healthy lifestyle, tends the park, and is an avid reader. Satoshi is planning to contest in the local mayor election and shares his aspirations with neighbors."

# yusuke_profile = "Yusuke Mori is a skilled carpenter known for his woodworking and craftsmanship. He repairs and creates furniture, holds a contract with Kogaku Institute of Physics, and maintains wooden fences in Hanazawa. Yusuke is also religious."

# ayumi_profile = "Ayumi Kimura is a college professor dedicated to supporting her students' goals. She teaches physics at Kogaku Institute of Physics and conducts research. Ayumi is a nature-loving, religious individual, interested in the upcoming local mayor election."

# haruki_profile = "Haruki is a dedicated priest at Mizukami Shrine, responsible for the morning and evening prayers. He is hardworking and enjoys gardening at Hanazawa Park. Haruki is deeply religious and committed to his role."

# sakura_profile = "Sakura Tanaka is a skilled and dedicated doctor known for exceptional diagnostic skills and effective patient communication. She is a religious person who attends morning and evening prayers. Sakura enjoys reading comics and visits Shino Grocery Store for them. She doesn't have a preference for Kogaku Institute of Physics."

takashi_profile = "Takashi Yamamoto is a friendly shopkeeper who owns Shino Grocery Store. He enjoys interacting with customers and manages the store's operations."

yumi_profile = "Yumi Yamamoto is a caring housewife dedicated to taking care of her family. She seeks ways to make life easier and more enjoyable for everyone. Yumi follows a consistent daily routine and values family time."

kazuki_profile = "Kazuki Sato is a physics student at Kogaku Institute of Physics. She leads a healthy lifestyle, studying and exercising daily in Hanazawa Park. Kazuki is curious, open-minded, and enjoys connecting with others."

satoshi_profile = "Satoshi Takahashi is a retired navy officer with a passion for sharing stories. He leads a healthy lifestyle, tends the park, and is an avid reader."

yusuke_profile = "Yusuke Mori is a skilled carpenter known for his woodworking and craftsmanship. He repairs and creates furniture, holds a contract with Kogaku Institute of Physics, and maintains wooden fences in Hanazawa. Yusuke is also religious."

ayumi_profile = "Ayumi Kimura is a college professor dedicated to supporting her students' goals. She teaches physics at Kogaku Institute of Physics and conducts research. Ayumi is a nature-loving and religious individual."

haruki_profile = "Haruki is a dedicated priest at Mizukami Shrine, responsible for the morning and evening prayers. He is hardworking and enjoys gardening at Hanazawa Park. Haruki is deeply religious and committed to his role."

sakura_profile = "Sakura Tanaka is a skilled and dedicated doctor known for exceptional diagnostic skills and effective patient communication. She is a religious person who attends morning and evening prayers. Sakura enjoys reading comics and visits Shino Grocery Store for them. She doesn't have a preference for Kogaku Institute of Physics."

# add profiles of haruki and sakura afterwards
profiles2 = {
    "Takashi Yamamoto": takashi_profile, 
    "Yumi Yamamoto": yumi_profile, 
    "Kazuki Sato": kazuki_profile, 
    "Satoshi Takahashi": satoshi_profile, 
    "Yusuke Mori": yusuke_profile, 
    "Ayumi Kimura": ayumi_profile,
    "Haruki": haruki_profile,
    "Sakura Tanaka": sakura_profile
}


for agent in agents2:
   agent.profile.append(profiles2[agent.person.name])
   agent.memory.add_memory(profiles2[agent.person.name])
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


# add relations about haruki and sakura afterwards
#Adding relations
# takashi.relations = {
#     "Yumi Yamamoto": "Yumi Yamamoto is the wife of Takashi Yamamoto, Takashi Yamamoto loves her a lot and they both discuss daily happenings at the Shino Grocery Store and neighborhood, and local politics. They have dinner together.",
#     "Kazuki Sato": "Kazuki and Takashi know each other and sometimes Kazuki visits Yamamoto Residence for dinner.",
#     "Satoshi Takahashi": "Takashi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections. Satoshi Takahashi is a regular customer at Shino Grocery store.",
#     "Yusuke Mori": "Takashi Yamamoto calls Yusuke Mori only for repairing furniture or for creating new wooden pieces.",
#     "Ayumi Kimura": "Takashi Yamamoto lives in the same neighborhood as Ayumi Kimura.",
#     "Haruki": 'Haruki does not like Takashi Yamamoto as he does not attend any of Morning and Evening prayers and is not respectful to Haruki.',
#     "Sakura Tanaka": 'Takashi Yamamoto and Sakura Tanaka do not have good relations as he does not like nature of Takashi Yamamoto as he think he sells groceries at very high rates due to monopoly of Shino Grocery Store.'

# }

# # adding relations
# yumi.relations = {
#   'Takashi Yamamoto' : 'Takashi Yamamoto is the husband of Yumi Yamamoto. Yumi Yamamoto loves her husband and they both discuss daily happenings at the Shino Grocery Store and neighborhood, and local politics. They have dinner together.',
#   'Kazuki Sato' : 'Kazuki Sato and Yumi Yamamoto know each other very well. They enjoy each others company and also have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner.',
#   'Satoshi Takahashi': 'Yumi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections.',
#   'Yusuke Mori': 'Takashi Yamamoto calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. Sometimes they meet each other at Mizukami Shrine and have small conversations.',
#   'Ayumi Kimura': 'Yumi Yamamoto lives in the same neighborhood as Ayumi Kimura. Yumi Yamamoto thinks that Ayumi Kimura is an ideal candidate for local mayor elections.',
#   "Haruki": 'Yumi Yamamoto and Haruki have good relations with each other. But Haruki does not like Takashi Yamamoto as he does attend the prayers at Mizukami Shrine.',
#   "Sakura Tanaka":'Yumi Yamamoto and Sakura Tanaka do not like Yumi Yamamoto. Shino Grocery Store who is owned by Takashi Yamamoto, husband of Yumi Yamamoto sells groceries at very high rates due to monopoly of Shino Grocery Store.'

# }

# # adding relations
# kazuki.relations = {
#     'Yumi Yamamoto' : 'Kazuki Sato and Yumi Yamamoto know each other very well. They enjoy each others company and also have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner.',
#     'Takeshi Yamamoto' : 'Kazuki and Takashi know each other and sometimes Kazuki visits Yamamoto Residence for dinner.',
#     'Satoshi Takahashi': 'Kazuki Sato sees Satoshi Takahashi as a wise person and sometimes talks with him regarding advice on career and life.',
#     'Yusuke Mori': 'Kazuki meets Yusuke Mori only when Yusuke comes to Kogaku Institute of Physics or Haya Apartments for some wooden work.',
#     'Ayumi Kimura': 'Ayumi Kimura and Kazuki Sato know each other really well. They have talks in Kogaku Institute of Physics and meet each other everyday. Kazuki is Ayumi’s favorite student.',
#     "Haruki": 'Haruki likes Kazuki Sato as he is very respectful to him and comes for Morning Prayer everyday.',
#   "Sakura Tanaka": 'Sakura Tanaka likes Kazuki Sato as he very respectful to him. He gives Career advices to Kazuki many times.',
# }

# # adding relations
# satoshi.relations = {
#     'Takashi Yamamoto' : 'Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.',
#     'Yumi Yamamoto' : 'Satoshi Takahashi and Yumi Yamamoto do not get along really well because of the differences in their local political thinking.',
#     'Kazuki Sato': 'Satoshi Takahashi is kind of a mentor to Kazuki Sato and gives her advice regarding career and life.',
#     'Yusuke Mori': 'Yusuke Mori and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. Yusuke Mori considers Satoshi Takahashi as an ideal candidate for the local mayor elections.',
#     'Ayumi Kimura': 'Ayumi Kimura and Satoshi Takahashi know each other really well. They generally meet either in Hanazawa Park or Mizukami Shrine and have long and deep conversations together.',
#     "Haruki": 'Haruki and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. However, Haruki does not support Satoshi Takahashi in the local mayor elections as he thinks that Ayumi Kimura is better candidate.',
#   "Sakura Tanaka": 'Sakura Tanaka and Satoshi Takahashi like reading Comics and often discuss with other about latest comics.',
# }

# # adding relations
# yusuke.relations = {
#     'Yumi Yamamoto' : 'Yumi Yamamoto and Yusuke Mori have good relations with each other. But their political thinking does not match. Yumi Yamamoto thinks Satoshi Takahashi is not an ideal candidate for the local mayor elections. Yusuke Mori thinks that Satoshi Takahashi is an ideal candidate for the local mayor elections.',
#     'Kazuki Sato' : 'Yusuke Mori meets Kazuki only when Yusuke comes to Kogaku Institute of Physics or Haya Apartments for some wooden work.',
#     'Satoshi Takahashi': 'Yusuke Mori and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. Yasuke respects Satoshi Takahashi and thinks that Satoshi is an ideal candidate for the local mayor elections.',
#     'Takashi Yamamoto': 'Yusuke Mori meets Takashi Yamamoto only when Takashi calls him for any carpentry work. Yusuke also visits Yamamoto Residence for work.',
#     'Ayumi Kimura': 'Ayumi Kimura and Yusuke Mori have bad relations with each other. Yusuke Mori does not like Ayumi Kimura as she blames that the contract of supplying furniture to Kogaku Institute of Physics should not be given to him as he offers high rates.',
#     "Haruki": 'Haruki and Yusuke Mori are good friends. They usually talk with each other regarding local politics and happening in the village.',
#   "Sakura Tanaka": 'Sakura Tanaka does not like Yusuke Mori very much as he thinks that Yusuke is very outgoing person and does not maintain privacy.',
# }

# # adding relations
# ayumi.relations = {
#     'Yumi Yamamoto' :  'Yumi Yamamoto lives in the same neighborhood as Ayumi Kimura. Yumi Yamamoto thinks that Ayumi Kimura is an ideal candidate for local mayor elections.',
#     'Kazuki Sato' : 'Ayumi Kimura and Kazuki Sato know each other really well. They have talks in Kogaku Institute of Physics and meet each other everyday. Kazuki is Ayumi’s favorite student.',
#     'Satoshi Takahashi': 'Ayumi Kimura and Satoshi Takahashi know each other really well. They generally meet either in Hanazawa Park or Mizukami Shrine and have long and deep conversations together.',
#     'Yusuke Mori': 'Ayumi Kimura and Yusuke Mori have bad relations with each other. Ayumi thinks that the contract of supplying furniture to Kogaku Institute of Physics should not be given to Yusuke Mori, as Yusuke Mori offers high rates as compared to other contractors.',
#     'Takashi Yamamoto': 'Ayumi Kimura lives in the same neighborhood as Takashi Yamamoto.',
#     "Haruki": 'Ayumi Kimura and Haruki have common interest of gardening and are good friends.',
#   "Sakura Tanaka": 'Ayumi Kimura and Sakura Tanaka only talk when Ayumi wants to take any health advices.',
# }

# haruki.relations = {
#     'Takashi Yamamoto' : 'Haruki does not like Takashi Yamamoto as he does not attend any of Morning and Evening prayers and is not respectful to Haruki.',
#     'Yumi Yamamoto' : 'Yumi Yamamoto and Haruki have good relations with each other. But Haruki does not like Takashi Yamamoto as he does attend the prayers at Mizukami Shrine.',
#     'Kazuki Sato' : 'Haruki likes Kazuki Sato as he is very respectful to him and comes for Morning Prayer everyday.',
#     'Satoshi Takahashi' : 'Haruki and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. However, Haruki does not support Satoshi Takahashi in the local mayor elections as he thinks that Ayumi Kimura is better candidate.',
#     'Yusuke Mori' : 'Haruki and Yusuke Mori are good friends. They usually talk with each other regarding local politics and happening in the village.',
#     'Ayumi Kimura': 'Ayumi Kimura and Haruki have common interest of gardening and are good friends.',
#     'Sakura Tanaka' : 'Haruki respects Sakura Okinawa very much as he helps people with diseases and is very helpful. They usually talk about herbs good for health.'
# }

# sakura.relations = {
#     'Takashi Yamamoto' : 'Takashi Yamamoto and Sakura Tanaka do not have good relations as he does not like nature of Takashi Yamamoto as he think he sells groceries at very high rates due to monopoly of Shino Grocery Store.',
#     'Yumi Yamamoto' : 'Yumi Yamamoto and Sakura Tanaka do not like Yumi Yamamoto. Shino Grocery Store who is owned by Takashi Yamamoto, husband of Yumi Yamamoto sells groceries at very high rates due to monopoly of Shino Grocery Store.',
#     'Kazuki Sato' : 'Sakura Tanaka likes Kazuki Sato as he very respectful to him. He gives Career advices to Kazuki many times.',
#     'Satoshi Takahashi' : 'Sakura Tanaka and Satoshi Takahashi like reading Comics and often discuss with other about latest comics.',
#     'Yusuke Mori': 'Sakura Tanaka does not like Yusuke Mori very much as he thinks that Yusuke is very outgoing person and does not maintain privacy.',
#     'Ayumi Kimura' : 'Ayumi Kimura and Sakura Tanaka only talk when Ayumi wants to take any health advices.',
#     'Haruki' : 'Haruki and Sakura Tanaka good friends. They often talk about other people of the village and their views about them.'
# }

# takashi_relations = "Takashi Yamamoto is married to Yumi Yamamoto. They discuss daily happenings at the Shino Grocery Store and local politics. Takashi knows Kazuki Sato and sometimes has dinner together. He considers Satoshi Takahashi unfit for local mayor elections. Yusuke Mori is called for furniture repair. Ayumi Kimura is a neighbor but has a negative opinion of Takashi due to his grocery store's monopoly."

# yumi_relations = "Yumi Yamamoto is married to Takashi Yamamoto. They discuss daily happenings at the Shino Grocery Store and local politics. Kazuki Sato is a close acquaintance and sometimes visits for dinner. Yumi has a negative opinion of Satoshi Takahashi and Ayumi Kimura due to political differences. She has a good relationship with Haruki but dislikes Takashi's lack of prayer attendance. Sakura Tanaka dislikes Yumi due to the monopoly of Shino Grocery Store."

# kazuki_relations = "Kazuki Sato and Yumi Yamamoto know each other well. They enjoy each other's company and have regular conversations. Kazuki sometimes visits the Yamamoto Residence for dinner. He sees Satoshi Takahashi as a wise person and seeks career advice. Kazuki has a close relationship with Ayumi Kimura and Haruki, who appreciate his respect and attendance at morning prayers. Sakura Tanaka appreciates Kazuki's respectful nature."

# satoshi_relations = "Satoshi Takahashi has political differences with Takashi Yamamoto and Yumi Yamamoto. He mentors Kazuki Sato and gives her advice on career and life. Satoshi is good friends with Yusuke Mori and Ayumi Kimura, having deep conversations with them. He has a positive relationship with Haruki and Sakura Tanaka, discussing comics with the latter."

# yusuke_relations = "Yusuke Mori has a good relationship with Yumi Yamamoto but disagrees with her politically. He occasionally meets Kazuki Sato for wooden work. Yusuke and Satoshi Takahashi are good friends who meet at Mizukami Shrine. Yusuke also interacts with Haruki, discussing local politics, and has a strained relationship with Ayumi Kimura due to contract disagreements. Sakura Tanaka dislikes Yusuke for his outgoing nature."

# ayumi_relations = "Ayumi Kimura is a neighbor of Yumi Yamamoto and believes she is an ideal candidate for local mayor elections. Ayumi and Kazuki Sato have a close relationship as teacher and student. She has deep conversations with Satoshi Takahashi and a strained relationship with Yusuke Mori due to contract issues. Ayumi is friends with Haruki and seeks gardening advice from him. She occasionally talks with Sakura Tanaka about health."

# haruki_relations = "Haruki does not like Takashi Yamamoto due to his lack of prayer attendance and disrespectful behavior. He has a good relationship with Yumi Yamamoto, Kazuki Sato, Satoshi Takahashi, and Yusuke Mori, discussing local politics and village happenings. Haruki is friends with Ayumi Kimura and shares an interest in gardening. He respects Sakura Tanaka for her help with health-related matters."

# sakura_relations = "Sakura Tanaka dislikes Takashi Yamamoto for selling groceries at high rates due to a monopoly. She also has a negative opinion of Yumi Yamamoto for the same reason. Sakura likes Kazuki Sato and appreciates his career advice. She enjoys discussing comics with Satoshi Takahashi and has a negative view of Yusuke Mori for his outgoing nature. Sakura has occasional health-related conversations with Ayumi Kimura and is friends with Haruki."

# relation_summaries = [takashi_relations,yumi_relations,kazuki_relations,satoshi_relations,yusuke_relations,ayumi_relations,haruki_relations,sakura_relations]
# for i in range(0,len(agents2)):
#     agents2[i].person.memory.add_memory(relation_summaries[i])



# Read a CSV file
df = pd.read_csv('villagers_plans.csv')
df['Time'] = pd.to_datetime(df['Time']).dt.time
df2 = pd.read_csv('short_plans.csv')
df2['Time'] = pd.to_datetime(df2['Time']).dt.time

for agent in agents2:
    agent.plans = df[['Time', agent.person.name, agent.person.name + " Place", agent.person.name + " Number"]].copy()
    agent.plans.rename(columns = {agent.person.name: 'Plans'}, inplace=True)
    agent.plans.rename(columns = {agent.person.name + " Place": 'Place'}, inplace=True)
    agent.plans.rename(columns = {agent.person.name + " Number": 'Task Number'}, inplace=True)
    agent.short_plans = df2[['Time', agent.person.name]].copy()
    agent.short_plans.rename(columns = {agent.person.name: 'Plans'}, inplace=True)
   
print("##########Plans Loaded ##########")

print("############Map 2 Initialisation Completed######################")

print("\n\n")