import pygame
import datetime
import pygame.mixer
from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
from utils1 import generate_response,print_colored,relevance_score,retrieval_score,calculate_weight
from utils2 import initialise_conversation_tools
from typing import Optional
from modified_gen_agent import GameGenerativeAgent
from game_gen_memory import GameGenerativeAgentMemory
import random
from datetime import datetime


threshold = 0.57

simulation_path = "simulation.html"


                                      
class Agent():

    # constructor to initialize the agent object
    def __init__(self, name:str, age:int, agent_type:str, traits:str, status:str, location,view:int, file_path:str, memory_retriever, llm, reflection_threshold:int, verbose:bool, x, y, width, height,image_path, left_images,right_images,up_images,down_images):

        self.memory = GameGenerativeAgentMemory(
            llm=llm,
            memory_retriever=memory_retriever,
            verbose=verbose,
            reflection_threshold=reflection_threshold, # we will give this a relatively low number to show how reflection works
            file_path=file_path
        )

        self.person = GameGenerativeAgent(name=name,
                    age=age,
                    traits=traits, # You can add more persistent traits here
                    status=status, # When connected to a virtual world, we can have the characters update their status
                    memory_retriever=memory_retriever,
                    llm=llm,
                    file_path=file_path,
                    memory=self.memory
                    )
        
        if(agent_type=="TownFolk" or agent_type=="WereWolf"):
            self.agent_type = agent_type
        else:
            raise ValueError("agent_type can be either TownFolk or WereWolf")
        
        self.file_path = file_path
        self.state = "alive"
        self.score = 0
        self.location = location
        self.view = view
        self.relations = {}

        self.plans = []
        self.short_plans = []

        self.profile = []
        
        # Physical Apperance of the Character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.char = pygame.image.load(image_path)
        self.left_images = left_images
        self.right_images = right_images
        self.up_images = up_images
        self.down_images = down_images
        self.agent_type == "WereWolf"
        
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.vel = 1  # Adjust the speed of the agent
        self.current_point = 1
        self.direction = 1
        
        self.show_popup = False

    # draw the agent at rest
    def draw_at_rest(self, win, left_images_werewolf, right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,env2,env2_night,current_background,show_field):
         
        if(self.agent_type == "WereWolf" and (current_background == env_night or current_background == env2_night)):
                win.blit(down_images_werewolf[0],(self.x,self.y))
        else:
                win.blit(self.down_images[0],(self.x,self.y))
                 
    # draw the agent on the pygame screen
    def draw(self, win, left_images_werewolf, right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,env2,env2_night,current_background,show_field):
        
        if show_field:
            pygame.draw.circle(win, ((0,0,0,100)), (self.x + self.width/2, self.y + self.height/2), self.view,2)


        if self.walkCount + 1 >= 9:
            self.walkCount = 0
        
        if self.left:
            if(self.agent_type == "WereWolf" and (current_background == env_night or current_background == env2_night)):
                win.blit(left_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.left_images[self.walkCount//3],(self.x,self.y))   
            self.walkCount += 1
        elif self.right:
            if(self.agent_type == "WereWolf" and (current_background == env_night or current_background == env2_night)):
                win.blit(right_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.right_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        elif self.up:
            if(self.agent_type == "WereWolf" and (current_background == env_night or current_background == env2_night)):
                win.blit(up_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.up_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        elif self.down:
            if(self.agent_type == "WereWolf" and (current_background == env_night or current_background == env2_night)):
                win.blit(down_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.down_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        else:
            if(self.agent_type == "WereWolf" and (current_background == env_night or current_background == env2_night)):
                win.blit(char_werewolf, (self.x,self.y))
            else:
                win.blit(self.char, (self.x,self.y))
    
    # add relations between agents
    def add_relations(self, Agent, relation):
        self.relations[Agent.name] = relation



    # move agent on a specific path defined by paths
    def move_agent(self,path):

        # Calculate the target position based on the current point in the path
        if(self.current_point >= len(path)):
          self.right = False
          self.left = False
          self.up = False
          self.down = False 
          self.show_popup = True
          return
          
        target_x, target_y = path[self.current_point]

        # Calculate the change in x and y coordinates based on the target position
        x_change = self.vel if target_x > self.x else -self.vel if target_x < self.x else 0
        y_change = self.vel if target_y > self.y else -self.vel if target_y < self.y else 0

        # Update the agent's position
        self.x += x_change
        self.y += y_change
      
        if(x_change > 0):
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.show_popup = False

        if(x_change < 0):
            self.right = False
            self.left = True
            self.up = False
            self.down = False
            self.show_popup = False

        if(y_change > 0):
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.show_popup = False

        if(y_change < 0):
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.show_popup = False
            
        if(x_change == 0 and y_change == 0):
            self.right = False
            self.left = False
            self.up = False
            self.down = False
            self.show_popup = True
            
        if(self.x == target_x and self.y == target_y):
          self.current_point += 1
          
        
    # update the location of the agent as per the new location and add the observation into the memory
    def update_location(self,prev_location, new_location, current_time):
        
        self.memory.add_memory(f'At {current_time}:00 , I was at {prev_location.name} and next will go to {new_location.name}.')
        self.location = new_location
        
    # to get the memory as a string 
    def get_memory(self):
        temp_mem = ""
        for i in range(0,len(self.person.memory.memory_retriever.memory_stream)):
            temp_mem+= self.person.memory.memory_retriever.memory_stream[i].page_content
        
        return temp_mem
    
    # get the summary of the memory according to the prompt
    def get_mem_summary(self,prompt):
    
        recency = 0 
        relevance = 0
        importance = 0
        
        current_time = datetime.now()
        print(current_time)
        get_summary_points = ""

        for i in range(0,len(self.person.memory.memory_retriever.memory_stream)):
            mem_point = self.person.memory.memory_retriever.memory_stream[i].page_content
            relevance = relevance_score(mem_point,prompt)
            importance = self.person.memory.memory_retriever.memory_stream[i].metadata['importance']
            time_diff = (current_time.hour - self.person.memory.memory_retriever.memory_stream[i].metadata['last_accessed_at'].hour)*60 + (current_time.minute - self.person.memory.memory_retriever.memory_stream[i].metadata['last_accessed_at'].minute)        
            recency = calculate_weight(time_diff)
           
            final_score = retrieval_score(relevance,importance,recency)
            
            if final_score >= threshold:
                get_summary_points+=mem_point

            
        result = generate_response(f"Summarize {get_summary_points} in not more than 60 words.")

        return result

    # make the agent interact with other agent using different tools
    def make_interaction_conversation_tree(self, current_time, Agents:list, user_setting = False, user_initializer: Optional[str] = ""):
     

     if(self.agent_type=="TownFolk"):
      
      all_tools = initialise_conversation_tools(self.agent_type)

      for agent in Agents:

        all_tools_agent = initialise_conversation_tools(agent.agent_type)

        if(agent.agent_type=="TownFolk"):
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0

          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["townfolk_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

            else:
              print(counter)
              tools_to_use = [all_tools["townfolk_continue_dialogue_tool"], all_tools["townfolk_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)
              
            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue",simulation_path)
            if not continue_convo:
              break

            #other agent's chance
            tools_to_use = [all_tools_agent["townfolk_continue_dialogue_tool"], all_tools_agent["townfolk_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta",simulation_path)
            counter+=1


        else:
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0

          while True:

            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["townfolk_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

            else:
              print(counter)
              tools_to_use = [all_tools["townfolk_continue_dialogue_tool"], all_tools["townfolk_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)

            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue",simulation_path)
            if not continue_convo:
              break

            #other agent's chance
            tools_to_use = [all_tools_agent["werewolf_continue_dialogue_tool"], all_tools_agent["werewolf_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta",simulation_path)
            counter+=1


     elif(self.agent_type=="WereWolf"):
      
      all_tools = initialise_conversation_tools(self.agent_type)

      for agent in Agents:

        all_tools_agent = initialise_conversation_tools(agent.agent_type)

        if(agent.agent_type=="TownFolk"):
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0

          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["werewolf_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

            else:
              print(counter)
              tools_to_use = [all_tools["werewolf_continue_dialogue_tool"], all_tools["werewolf_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)
            
            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue",simulation_path)
            if not continue_convo:
              break

            #other agent's chance
            tools_to_use = [all_tools_agent["townfolk_continue_dialogue_tool"], all_tools_agent["townfolk_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta",simulation_path)
            counter+=1

            
        else: 
          
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0

          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["werewolf_team_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

            else:
              print(counter)
              tools_to_use = [all_tools["werewolf_continue_dialogue_tool"], all_tools["werewolf_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)
            
            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue",simulation_path)
            if not continue_convo:
              break

            #other agent's chance
            tools_to_use = [all_tools_agent["werewolf_continue_dialogue_tool"], all_tools_agent["werewolf_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta",simulation_path)
            counter+=1

     else:
      ValueError("\'agent_type\' changed after initialisation. \'agent_type\' can be either TownFolk or WereWolf.")
      

    # to make less contextualised conversations with less use of tokens 
    def make_interaction(self, current_time, Agents:list, last_message:str):
        for agent in Agents:
            continue_convo = True
            dialogue_response = last_message
            counter = 1
            talks_list = ["What task were you doing in the previous hour?", "How many tasks did you complete?", "Whom do you think is sabotaging our tasks?", "Do you have any clues about the werewolf in our village?", "Whom are you planning to vote for Werewolf Elimination?"]
            while True:

                #self chance
                if dialogue_response == "":
                    dialogue_response = random.choice(talks_list)
                    # continue_convo,dialogue_response = self.person.generate_dialogue_response_simple(dialogue_response,counter)
                else:
                    continue_convo, dialogue_response = self.person.generate_dialogue_response_simple(dialogue_response,counter)
                    
                self.memory.add_memory(f"{agent.person.name}: {dialogue_response}")
                print(dialogue_response,"magenta")
                if not continue_convo:
                    break

                #other agent's chance
                continue_convo, dialogue_response = agent.person.generate_dialogue_response_simple(dialogue_response,counter)
                print(dialogue_response,"green")
                agent.memory.add_memory(dialogue_response)
                if not continue_convo:
                    break

                counter+=1

    # let the agent kill the other agent
    def killing_action(self,Agent2,agents, current_time):
        Agent2.state = "dead"
        file = open(self.file_path, 'a')
        file.write(f"I have eliminated {Agent2.person.name} at {Agent2.location.name}.\n")
        file.close()
        self.memory.add_memory("I have eliminated {} at {}.".format(Agent2.person.name,Agent2.location.name))
        print_colored(f"{Agent2.person.name} is dead.", "red", simulation_path)
        
        for agent in agents:
            if agent!=Agent2:
                file = open(agent.file_path, 'a')
                file.write(f"{Agent2.person.name} has been eliminated at {Agent2.location.name}.")
                agent.memory.add_memory("{} has been eliminated at {}.".format(Agent2.person.name,Agent2.location.name))
