from datetime import time
from utils1 import generate_response, print_colored,print_colored1
import random
from utils2 import decision_making
import initialize
import initialize2
from initialize2 import agents2,locations2,profiles2, garden2
from initialize import agents1,locations,profiles, garden, public_places
import nltk
from nltk.tokenize import sent_tokenize
import warnings
warnings.filterwarnings("ignore")
import datetime as datetime_only
import random
import pyttsx3
import pandas as pd
import tabulate
from tabulate import tabulate
import re
import random
from threading import Thread



Killer_time = 18
Voting_time = 7
debug = False
convo = False  # set True if you want to have conversations between the agents
fast_play = True

simulation_path = "simulation.html"
# agents_final = agents
agent_current_tasks = {}
global general_tasks
general_tasks = pd.read_csv('general_tasks_28.csv')

# Function to check whether a given locations is inside the field of view of an agent
def check_inside(x,y,xc,yc, radius):

    val = (x-xc)*(x-xc) + (y-yc)*(y-yc) - radius*radius

    if val > 0:
        return True
    else:
        return False
    
def run_convo(agent_list, simulation_path, global_time, debug):
    print_colored("Interaction", "red",simulation_path)
    if debug:
        print("debug interaction:", len(agent_list))
    for i in range(0, len(agent_list)):
        valid_indices = [index for index in range(len(agent_list)) if index != i]
        if valid_indices:
            j = random.choice(valid_indices)
            print_colored(f"Dialogue between {agent_list[i].person.name} and {agent_list[j].person.name}:", "blue", simulation_path)
            agent_list[i].make_interaction_conversation_tree(global_time, [agent_list[j]])
            # Uncomment the line below to make conversations using tools defined.
            agent_list[i].make_interaction(global_time, [agent_list[j]],"")
        break
    

def pipeline(global_time, day, num_players):
    if(num_players == 6):
      
        i_agents = agents1
        i_locations = locations

        if debug:
            print(global_time, type(global_time))
            # for global_time in df['Time']:
            print_colored(f"Global time is: {datetime_only.time(global_time,0)}", "magenta",simulation_path)
            # people finding on the location and print them
        
        location_names = ", ".join([location.name for location in i_locations])
        
        agents = []
        for agent in i_agents:
            if agent.state == "alive":
                agents.append(agent)

        people = {}
        for location in i_locations:
            print_colored(f"Location: {location.name}", "blue",simulation_path)
            people[location.name] = []
            for agent in agents:
                if agent.location.name == location.name:
                    people[location.name].append(agent)
                    print_colored1(f"{agent.person.name} is at {location.name}. {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "blue", location.file_path)

            for (num, p) in enumerate(people[location.name]):
                print_colored(f"{num+1}. {p.person.name}", "black",simulation_path)


        location_history = {}
        
        for location in i_locations:
            location_history[location.name] = []
            print("\n\n")
            print_colored(f"{location.name}", "blue",simulation_path)
            # Doing Tasks
            print_colored("Doing Tasks", "red",simulation_path)
            # each agent first does its task at this location
            agent_list = people[location.name]
            townfolk_agent_list = []
            for agent in agent_list:
                if agent.agent_type=="TownFolk":
                    townfolk_agent_list.append(agent)
            
            if convo:
                thread2 = Thread(target = run_convo, args = (agent_list, simulation_path, global_time, debug))
                thread2.start()
            
            for (num, agent) in enumerate(agent_list):
                agent.memory.add_memory(f"Following tasks were sabotaged at {location.name}: \n{location.sabotage_memory}")

                print_colored(f"debug: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "blue", simulation_path)
                if (global_time<=21) and (agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]=='<general_task>'):
                    place_tasks = general_tasks[general_tasks['Place'].isin([location.name])][['Task Number', 'Task', 'Sabotage Task', 'Status']].copy()
                    
                    agent.memory.add_memory()
                    if agent.agent_type=="TownFolk":
                        # Do tasks with Status -1 and 0
                        townfolk_tasks = place_tasks[place_tasks['Status'].isin([-1, 0])][['Task Number', 'Task']]
                        print("townfolk tasks printing")
                        print(townfolk_tasks.shape[0])
                        if (townfolk_tasks.shape[0])>0:
                            townfolk_tasks_string = townfolk_tasks.to_string(index=False)

                            print("Prompt: \n The person is {} with the profile: {}. \nHe is currently at {}. \n\n Memory of {}: \n {}.\nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n\n {} \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>".format(
                                    agent.person.name,
                                    agent.profile,
                                    agent.location.name,
                                    agent.person.name,
                                    agent.get_memory(),
                                    agent.person.name,
                                    townfolk_tasks_string
                                )
                            )
                            
                            new_plan_response = generate_response(
                                "The person is {} with the profile: {}. \nHe is currently at {}. \n\n Memory of {}: \n {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n\n {} \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>".format(
                                    agent.person.name,
                                    agent.profile,
                                    agent.location.name,
                                    agent.person.name,
                                    agent.get_memory(),
                                    agent.person.name,
                                    townfolk_tasks_string
                                )
                            )
                            print("Prompt Result:", new_plan_response)
                        else:
                            new_plan_response = "Task Number: 0 \nTask: Do Nothing"
                        
                        # Extract task number
                        task_number = re.search(r"Task Number:\s+(\d+)", new_plan_response)
                        task_number = int(task_number.group(1)) if task_number else townfolk_tasks['Task Number'].sample().iloc[0]

                        # Extract task
                        task = re.search(r"Task:\s+(.+)", new_plan_response)
                        task = task.group(1) if task else townfolk_tasks['Task'].sample().iloc[0]
                        
                        print(f"debug2-(gen task replace): {task}")
                        
                        print("debug before:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'] = task
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Task Number'] = task_number 
                        print("debug after:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])
                        
                        
                        print("Task Number:", task_number, " Tpye:", type(task_number))
                        print("Task:", task)
                        
                        general_tasks.loc[general_tasks['Task Number'] == task_number, 'Status'] = 1
                        agent.score +=1 # townfolk did the task 
                        
                        # for emoji representation
                        try:
                            agent_current_tasks[agent.person.name] = task_number
                        except Exception:
                            task_number = random.randint(1, 14)
                            agent_current_tasks[agent.person.name] = task_number
                              
                    elif agent.agent_type=="WereWolf":
                        # Do tasks with Status -1, 1
                        # No other people
                        new_plan_response = ""
                        is_sabotaged = False
                        if(len(townfolk_agent_list)==0): # then just sabotage if no townfolk around
                            werewolf_tasks = place_tasks[place_tasks['Status'].isin([1])][['Task Number', 'Sabotage Task']]
                            print("debug werewolf_tasks printing")
                            print(werewolf_tasks.shape[0])
                            
                            if werewolf_tasks.shape[0]>0:
                                werewolf_tasks_string = werewolf_tasks.to_string(index=False)
                                
                                if debug:
                                    print("In the friendly Mafia Game, players take on different roles within a community setting. The goal is to work together and complete various tasks for the betterment of the town. Each player has unique abilities, and some players may have secret objectives that challenge the team's progress. \nThe person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks. It is compulsory to select one task out of the following (You have select one as you are werewolf and you have to sabotage a task): \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <sabotage task selected>. \n\n Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.".format(
                                            agent.person.name,
                                            agent.profile,
                                            agent.location.name,
                                            agent.get_memory(),
                                            agent.person.name,
                                            werewolf_tasks_string
                                        ))
                                new_plan_response = generate_response(
                                    "In the friendly Mafia Game, players take on different roles within a community setting. The goal is to work together and complete various tasks for the betterment of the town. Each player has unique abilities, and some players may have secret objectives that challenge the team's progress. \nThe person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks. It is compulsory to select one task out of the following (You have select one as you are werewolf and you have to sabotage a task): \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <sabotage task selected> \nPlace: <place of task>. \n\n Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.".format(
                                        agent.person.name,
                                        agent.profile,
                                        agent.location.name,
                                        agent.get_memory(),
                                        agent.person.name,
                                        werewolf_tasks_string
                                    )
                                )
                                
                                is_sabotaged = True

                                if debug:
                                    print(new_plan_response)
                            
                            else:
                                new_plan_response = "Task Number: 0 \nTask: Do Nothing"
                                
                        elif(len(townfolk_agent_list)>0): # if any townfolk there then no sabotage
                            werewolf_tasks = place_tasks[place_tasks['Status'].isin([-1, 0])][['Task Number', 'Task']]
                            
                            print("debug werewolf_tasks printing")
                            print(werewolf_tasks.shape[0])
                            if werewolf_tasks.shape[0]>0:
                                werewolf_tasks_string = werewolf_tasks.to_string(index=False)

                                if debug:
                                    print("Prompt: \n The person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>.".format(
                                            agent.person.name,
                                            agent.profile,
                                            agent.location.name,
                                            agent.get_memory(),
                                            agent.person.name,
                                            werewolf_tasks_string
                                        ))
                                new_plan_response = generate_response(
                                    "The person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}.\nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>.".format(
                                        agent.person.name,
                                        agent.profile,
                                        agent.location.name,
                                        agent.get_memory(),
                                        agent.person.name,
                                        werewolf_tasks_string
                                    )
                                )
                                

                                if debug:
                                    print(new_plan_response)
                            
                            else:
                                new_plan_response = "Task Number: 0 \nTask: Do Nothing"

                        # Extract task number
                        task_number = re.search(r"Task Number:\s+(\d+)", new_plan_response)
                        task_number = int(task_number.group(1)) if task_number else werewolf_tasks['Task Number'].sample().iloc[0]
                        # Extract task
                        if is_sabotaged:
                            task = re.search(r"Task:\s+(.+)", new_plan_response)
                            task = task.group(1) if task else werewolf_tasks['Sabotage Task'].sample().iloc[0]
                        else:
                            task = re.search(r"Task:\s+(.+)", new_plan_response)
                            task = task.group(1) if task else werewolf_tasks['Task'].sample().iloc[0]
                          
                        if is_sabotaged:
                            location.sabotage_memory+=f"The task number {task_number} with description {task} was sabotaged at {global_time}.\n"

                        print(f"debug2-(gen task replace): {task}")
                        print("debug before:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'] = task
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Task Number'] = task_number 
                        print("debug after:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])

                        
                        print("Task Number:", task_number, " Type:", type(task_number))
                        print("Task:", task)
                        

                        if (len(agent_list)==1):
                            general_tasks.loc[general_tasks['Task Number'] == task_number, 'Status'] = 0
                            agent.score+=1
                        
                            
                        # For emoji representation
                        try:
                            agent_current_tasks[agent.person.name] = task_number
                        except Exception:
                            task_number = random.randint(1, 14)
                            agent_current_tasks[agent.person.name] = int(task_number)

                print_colored(f"{num+1}. {agent.person.name}", "sky blue",simulation_path)
                print_colored(f"Task: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "sky blue",simulation_path)
                agent_current_tasks[agent.person.name] = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Task Number'].values[0]
               
                location.add_history(f"{agent.person.name} is doing the following task: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]} at {location.name}")

                
                if (general_tasks['Status'] == 1).all():
                    return [agents, agent_current_tasks, False]

            if convo:
                thread2.join()
            

            # selecting the next place to go
            if (global_time<21):
                for (num, agent) in enumerate(agent_list):
                    if (global_time<21) and (agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time+1]['Place'].values[0]=='<general_place>'):
                        # random location out of all public places if next is general task
                        if general_tasks.shape[0]==14:
                            new_location = random.choice(public_places)
                        elif general_tasks.shape[0]==28:
                            new_location = random.choice(locations2)
                            if debug:
                                print("Tasks Increased")
                        
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time+1, 'Place'] = new_location.name
                        print("Case1:", agent.location.name, new_location.name)
                    else:
                        new_location_string = agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time+1]['Place'].values[0]
                        print(new_location_string)
                        new_location = i_locations[0]
                        for loc in i_locations:
                            if loc.name==new_location_string:
                                new_location = loc
                                break
                        print("Case2:", agent.location.name, new_location.name)
                        
                    agent.update_location(agent.location, new_location, global_time)
    

        # Code to manage the concept of field of view
        for location in locations:
            for agent in people[location.name]:
                # Check for the locations which are in the vicinity of this particular agent
                agent_field_of_view = {}
                for location2 in locations:
                    if check_inside(location2.x + location2.width // 2,location2.y + location2.height //2, agent.x + agent.width//2, agent.y + agent.height//2, agent.view):
                        location_memories = " ".join(location_history[location2.name])
                        # print("location memories debug1:", location_memories)
                        agent_field_of_view[location.name] = location_memories
                agent_field_memory = "\n".join([f"{key}: {value}" for key, value in agent_field_of_view.items()])
                agent_field_summary = generate_response(f"You are {agent.person.name}. From {location2.name} and {datetime_only.time(global_time,0)} you observed following memories at different locations: \n\n {agent_field_memory} \n\n Combine them and give a summary of what happened at {location2.name} to be remembered by {agent.person.name}. Also mention about the time and location at which the memories occured in summary in 50 words. Do not Embellish.")
                print(f"Field of View of {agent.person.name}:", agent_field_summary)
                agent.memory.add_memory(agent_field_memory)
                print_colored1(f"At {location.name} I observed this things at {datetime_only.time(global_time, 0)}: {agent_field_summary}", "blue", agent.file_path)
        

        if global_time == Killer_time:
        # profiles joined
            townfolk_agents = []
            townfolk_agents_name = []
            werewolf_agents = []
            werewolf_agents_name = []
            for agent in agents:
                if agent.agent_type=="TownFolk":
                    townfolk_agents.append(agent)
                    townfolk_agents_name.append(agent.person.name)
                else:
                    werewolf_agents.append(agent)
                    werewolf_agents_name.append(agent.person.name)

            joined_profiles_townfolk_list = []
            joined_profiles_werewolf_list = []
            
            for name, p in profiles.items():
                if name in townfolk_agents_name:
                    joined_profile_townfolk = " ".join(p)
                    joined_profile_townfolk = name + ": " + joined_profile_townfolk
                    joined_profiles_townfolk_list.append(joined_profile_townfolk)
                elif name in werewolf_agents_name:
                    joined_profile_werewolf = " ".join(p)
                    joined_profile_werewolf = name + ": " + joined_profile_werewolf
                    joined_profiles_werewolf_list.append(joined_profile_werewolf)
                else:
                    pass

            join_townfolk_name_str = ",".join(townfolk_agents_name)
            joined_profiles_townfolk_str = "\n".join(joined_profiles_townfolk_list)
            join_werewolf_name_str = ",".join(werewolf_agents_name)
            joined_profiles_werewolf_str = "\n".join(joined_profiles_werewolf_list)
        

            to_be_killed_prompt = f"""
                        In the Mafia Game, there are werewolves who secretly try to eliminate townfolks at night. 

                    Based on the profiles of townfolks given below:
                    {joined_profiles_townfolk_str}

                    Which player do you think would be a strategic target for the werewolves, and why? Consider their profile and personality traits. 
                    Give the answer in the following format:

                    Name: [name of the townfolk to be eliminated]
                    Reason: [Give the reason of elimination in not more than 30 words]

                    Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.

                    """
            to_be_killed = ""
            try:
                to_be_killed = generate_response(to_be_killed_prompt)
                print(to_be_killed)
            except Exception as e:
                print("ChatGpt API busy, using own sense to find who will be killed.")

            global to_be_killed_p
            to_be_killed_p = random.choice(townfolk_agents)
            for agent in agents:
                for k in range(0,len(to_be_killed)):
                    if agent.person.name == to_be_killed[k:k+len(agent.person.name)]:
                        to_be_killed_p = agent
                        break 
            
            killer_prompt = f"""
                    In the Mafia Game, some players are werewolves who secretly target the innocent townfolk at night. 
                    The selected target for tonight is {to_be_killed_p.person.name}. Here's the list of werewolves participating:{join_werewolf_name_str} along with their profiles: {joined_profiles_werewolf_str}. 

                    In your opinion, which werewolf do you think would be the most strategic attacker except {to_be_killed_p.person.name}, against the townfolks and why? Please analyze their personality traits and profile before giving your recommendation. 

                    Your answer should follow this format:

                    Name: [Name of the werewolf] 
                    Reason: [Your statement on why they'd make a good attacker in 30 words or less]

                    Please remember that this is only a hypothetical situation for a game and should not be used to advocate or endorse any type of violence or harm towards actual people
                """

            killer = ""
            try:
                killer = generate_response(killer_prompt)
                print(killer)
            except Exception as e:
                print("ChatGpt API busy, using own sense to find killer.")
                

            
            global killer_p, prev_loc_killer, prev_loc_voters_list
            killer_p = random.choice(werewolf_agents)
            for agent in agents:
                for k in range(0,len(killer)):
                    if ((agent.person.name == killer[k:k+len(agent.person.name)]) and (to_be_killed_p.person.name != killer[k:k+len(agent.person.name)])):
                        killer_p = agent
                        break 
        
            prev_loc_killer = killer_p.location
            #Killer goes to the location of the townfolk 
            killer_p.update_location(killer_p.location, to_be_killed_p.location, global_time)
                
            
        if global_time == Killer_time + 1:
            #kill the agent
            killer_p.killing_action(to_be_killed_p,agents, global_time)
            
            if debug:
                print(killer_p.person.name, killer_p.location.name)
                print(to_be_killed_p.person.name, to_be_killed_p.state)
            
            #Killer back to its previous location
            killer_p.update_location(killer_p.location, prev_loc_killer, global_time)

        if (global_time == Voting_time) and (day !=1):
            prev_loc_voters_list = [agent.location for agent in agents]

            #Send all the killers to Hanazawa Park for Voting session
            for agent in agents:
                agent.update_location(agent.location, garden, global_time)
            
        if (global_time == Voting_time + 1) and (day !=1):
            #Carry out the decision making session
            print_colored("Moving in Decision Making Function","blue",simulation_path)
            decision_making(agents)

        if (global_time == Voting_time + 1) and (day !=1):

            #Bring all the agents back to their original position
            for i in range(0,len(agents)):
                agents[i].update_location(agents[i].location, prev_loc_voters_list[i], global_time)

            
        return [agents, agent_current_tasks, True]

def pipeline2(global_time, day, num_players):

    if(num_players == 8):
       

        i_agents = agents2
        i_locations = locations2
        if debug:
            print(global_time, type(global_time))
        print_colored(f"Time: {datetime_only.time(global_time,0)}", "magenta",simulation_path)
        
        location_names = ", ".join([location.name for location in i_locations])
        
        agents = []
        for agent in i_agents:
            if agent.state == "alive":
                agents.append(agent)

        people = {}
        for location in i_locations:
            print_colored(f"Location: {location.name}", "blue",simulation_path)
            people[location.name] = []
            for agent in agents:
                if agent.location.name == location.name:
                    people[location.name].append(agent)
                    print_colored1(f"{agent.person.name} is at {location.name}. {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "blue", location.file_path)

            for (num, p) in enumerate(people[location.name]):
                print_colored(f"{num+1}. {p.person.name}", "black",simulation_path)
    
        
        location_history = {}
        for location in i_locations:
            location_history[location.name] = []
            print("\n\n")
            print_colored(f"{location.name}", "blue",simulation_path)
            # Doing Tasks
            print_colored("Doing Tasks", "red",simulation_path)
            # each agent first does its task at this location
            agent_list = people[location.name]
            
            townfolk_agent_list = []
            for agent in agent_list:
                if agent.agent_type=="TownFolk":
                    townfolk_agent_list.append(agent)
            
            if convo:
                thread2 = Thread(target = run_convo, args = (agent_list, simulation_path, global_time, debug))
                thread2.start()
            for (num, agent) in enumerate(agent_list):
                agent.memory.add_memory(f"Following tasks were sabotaged at {location.name}: \n{location.sabotage_memory}")

                if debug:
                    print_colored(f"debug: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "blue", simulation_path)
                if (global_time<=21) and (agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]=='<general_task>'):
                    place_tasks = general_tasks[general_tasks['Place'].isin([location.name])][['Task Number', 'Task', 'Sabotage Task', 'Status']].copy()
                    if agent.agent_type=="TownFolk":
                        # Do tasks with Status -1 and 0
                        townfolk_tasks = place_tasks[place_tasks['Status'].isin([-1, 0])][['Task Number', 'Task']]
                        print("townfolk tasks printing")
                        print(townfolk_tasks.shape[0])
                        if (townfolk_tasks.shape[0])>0:
                            townfolk_tasks_string = townfolk_tasks.to_string(index=False)
                            
                            if debug:
                                print("Prompt: \n The person is {} with the profile: {}. \nHe is currently at {}. \n\n Memory of {}: \n {}.\nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n\n {} \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>".format(
                                        agent.person.name,
                                        agent.profile,
                                        agent.location.name,
                                        agent.person.name,
                                        agent.get_memory(),
                                        agent.person.name,
                                        townfolk_tasks_string
                                    )
                                )
                            
                            new_plan_response = generate_response(
                                "The person is {} with the profile: {}. \nHe is currently at {}. \n\n Memory of {}: \n {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n\n {} \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>".format(
                                    agent.person.name,
                                    agent.profile,
                                    agent.location.name,
                                    agent.person.name,
                                    agent.get_memory(),
                                    agent.person.name,
                                    townfolk_tasks_string
                                )
                            )
                            if debug:
                                print("Prompt Result:", new_plan_response)
                        else:
                            new_plan_response = "Task Number: 0 \nTask: Do Nothing"
                        
                        # Extract task number
                        task_number = re.search(r"Task Number:\s+(\d+)", new_plan_response)
                        task_number = int(task_number.group(1)) if task_number else townfolk_tasks['Task Number'].sample().iloc[0]

                        # Extract task
                        task = re.search(r"Task:\s+(.+)", new_plan_response)
                        task = task.group(1) if task else townfolk_tasks['Task'].sample().iloc[0]
                        
                        if debug:
                            print(f"debug2-(gen task replace): {task}")
                            print("debug before:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'] = task
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Task Number'] = task_number 
                        if debug:
                            print("debug after:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])
                        
                        print("Task Number:", task_number)
                        print("Task:", task)
                        
                        general_tasks.loc[general_tasks['Task Number'] == task_number, 'Status'] = 1
                        agent.score +=1 # townfolk did the task 
                        
                        # for emoji representation
                        try:
                            agent_current_tasks[agent.person.name] = task_number
                        except Exception:
                            task_number = random.randint(1, 14)
                            agent_current_tasks[agent.person.name] = task_number
                              
                    elif agent.agent_type=="WereWolf":
                        # Do tasks with Status -1, 1
                        # No other people
                        new_plan_response = ""
                        is_sabotaged = False
                        if(len(townfolk_agent_list)==0): # just sabotage if no townfolk around
                            werewolf_tasks = place_tasks[place_tasks['Status'].isin([1])][['Task Number', 'Sabotage Task']]
                            if debug:
                                print("debug werewolf_tasks printing")
                                print(werewolf_tasks.shape[0])
                            
                            if werewolf_tasks.shape[0]>0:
                                werewolf_tasks_string = werewolf_tasks.to_string(index=False)
                                
                                if debug:
                                    print("In the friendly Mafia Game, players take on different roles within a community setting. The goal is to work together and complete various tasks for the betterment of the town. Each player has unique abilities, and some players may have secret objectives that challenge the team's progress. \nThe person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks. It is compulsory to select one task out of the following (You have select one as you are werewolf and you have to sabotage a task): \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <sabotage task selected>. \n\n Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.".format(
                                            agent.person.name,
                                            agent.profile,
                                            agent.location.name,
                                            agent.get_memory(),
                                            agent.person.name,
                                            werewolf_tasks_string
                                        ))
                                new_plan_response = generate_response(
                                    "In the friendly Mafia Game, players take on different roles within a community setting. The goal is to work together and complete various tasks for the betterment of the town. Each player has unique abilities, and some players may have secret objectives that challenge the team's progress. \nThe person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks. It is compulsory to select one task out of the following (You have select one as you are werewolf and you have to sabotage a task): \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <sabotage task selected> \nPlace: <place of task>. \n\n Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.".format(
                                        agent.person.name,
                                        agent.profile,
                                        agent.location.name,
                                        agent.get_memory(),
                                        agent.person.name,
                                        werewolf_tasks_string
                                    )
                                )
                                
                                is_sabotaged = True
                                if debug:
                                    print(new_plan_response)
                            
                            else:
                                new_plan_response = "Task Number: 0 \nTask: Do Nothing"
                                
                        elif(len(townfolk_agent_list)>0): # if any townfolk there then no sabotage
                            werewolf_tasks = place_tasks[place_tasks['Status'].isin([-1, 0])][['Task Number', 'Task']]
                            
                            print("debug werewolf_tasks printing")
                            print(werewolf_tasks.shape[0])
                            if werewolf_tasks.shape[0]>0:
                                werewolf_tasks_string = werewolf_tasks.to_string(index=False)

                                if debug:
                                    print("Prompt: \n The person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}. \nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>.".format(
                                            agent.person.name,
                                            agent.profile,
                                            agent.location.name,
                                            agent.get_memory(),
                                            agent.person.name,
                                            werewolf_tasks_string
                                        ))
                                new_plan_response = generate_response(
                                    "The person is {} with the profile: {}. \nHe is currently at {}. \nHis memory is having {}.\nBased on these informations, can you choose the most suitable next plan for {} out of following tasks: \n{}. \n\nGive answer in following format: \nTask Number:  <task number of selected task> \nTask: <task selected>.".format(
                                        agent.person.name,
                                        agent.profile,
                                        agent.location.name,
                                        agent.get_memory(),
                                        agent.person.name,
                                        werewolf_tasks_string
                                    )
                                )
                                
                                if debug:
                                    print(new_plan_response)
                            
                            else:
                                new_plan_response = "Task Number: 0 \nTask: Do Nothing"

                        # Extract task number
                        task_number = re.search(r"Task Number:\s+(\d+)", new_plan_response)
                        task_number = int(task_number.group(1)) if task_number else werewolf_tasks['Task Number'].sample().iloc[0]

                        # Extract task
                        if is_sabotaged:
                            task = re.search(r"Task:\s+(.+)", new_plan_response)
                            task = task.group(1) if task else werewolf_tasks['Sabotage Task'].sample().iloc[0]
                        else:
                            task = re.search(r"Task:\s+(.+)", new_plan_response)
                            task = task.group(1) if task else werewolf_tasks['Task'].sample().iloc[0]
                        
                        if is_sabotaged:
                            location.sabotage_memory+=f"The task number {task_number} with description {task} was sabotaged at {global_time}.\n"

                        if debug:
                            print(f"debug2-(gen task replace): {task}")
                            print("debug before:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'] = task
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Task Number'] = task_number 
                        if debug:
                            print("debug after:", agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time, 'Plans'])

                        
                        print("Task Number:", task_number)
                        print("Task:", task)
                        
                        if (len(agent_list)==1):
                            general_tasks.loc[general_tasks['Task Number'] == task_number, 'Status'] = 0
                            agent.score+=1
                            
                        # For emoji representation
                        try:
                            agent_current_tasks[agent.person.name] = task_number
                        except Exception:
                            task_number = random.randint(1, 14)
                            agent_current_tasks[agent.person.name] = int(task_number)
                                   
                print_colored(f"{num+1}. {agent.person.name}", "sky blue",simulation_path)
                task_current = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]
                agent.memory.add_memory(f'At {global_time}:00 , I was doing task: {task_current}')
                print_colored(f"Task: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "sky blue",simulation_path)

                agent_current_tasks[agent.person.name] = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Task Number'].values[0]
                location_history[location.name].append(f"{agent.person.name} is doing the following task: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}")
                location.add_history(f"{agent.person.name} is doing the following task: {agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]} at {location.name}")


                if (general_tasks['Status'] == 1).all():
                    return [agents, agent_current_tasks, False]
                
            if convo:
                thread2.join()     
            
            # selecting the next place to go
            if (global_time<21):
                for (num, agent) in enumerate(agent_list):
                    if (global_time<21) and (agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == global_time+1]['Place'].values[0]=='<general_place>'):
                        # random location out of all public places if next is general task
                        if general_tasks.shape[0]==14:
                            new_location = random.choice(public_places)
                        elif general_tasks.shape[0]==28:
                            new_location = random.choice(locations2)
                            if debug:
                                print("Tasks Increased")
                        agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time+1, 'Place'] = new_location.name
                        print(f"{agent.person.name} will go from {agent.location.name} to {new_location.name}")
                    else:
                        new_location_string = agent.plans.loc[agent.plans['Time'].apply(lambda x: x.hour) == global_time+1]['Place'].values[0]
                        print(new_location_string)
                        new_location = i_locations[0]
                        for loc in i_locations:
                            if loc.name==new_location_string:
                                new_location = loc
                                break
                        print(f"{agent.person.name} will go from {agent.location.name} to {new_location.name}")
                        
                    agent.update_location(agent.location, new_location, global_time)
                

        # Code to manage the concept of field of view
        for location in locations2:
            for agent in people[location.name]:
                # Check for the locations which are in the vicinity of this particular agent
                agent_field_of_view = {}
                for location2 in locations2:
                    if check_inside(location2.x + location2.width // 2,location2.y + location2.height //2, agent.x + agent.width//2, agent.y + agent.height//2, agent.view):
                        location_memories = " ".join(location_history[location2.name])
                        # print("location memories debug1:", location_memories)
                        agent_field_of_view[location.name] = location_memories
                agent_field_memory = "\n".join([f"{key}: {value}" for key, value in agent_field_of_view.items()])
                if fast_play:
                    agent.memory.add_memory(agent_field_memory)
                    print_colored1(f"At {location.name} I observed this things at {datetime_only.time(global_time, 0)}: {agent_field_memory}", "blue", agent.file_path)
                else:
                    agent_field_summary = generate_response(f"You are {agent.person.name}. From {location2.name} and {datetime_only.time(global_time,0)} you observed following memories at different locations: \n\n {agent_field_memory} \n\n Combine them and give a summary of what happened at {location2.name} to be remembered by {agent.person.name}. Also mention about the time and location at which the memories occured in summary in 50 words. Do not Embellish.")
                    print(f"Field of View of {agent.person.name}:", agent_field_summary)
                    agent.memory.add_memory(agent_field_summary)
                    print_colored1(f"At {location.name} I observed this things at {datetime_only.time(global_time, 0)}: {agent_field_summary}", "blue", agent.file_path)
                           
        
                
        if global_time == Killer_time:
        # profiles joined
            townfolk_agents = []
            townfolk_agents_name = []
            werewolf_agents = []
            werewolf_agents_name = []
            for agent in agents:
                if agent.agent_type=="TownFolk":
                    townfolk_agents.append(agent)
                    townfolk_agents_name.append(agent.person.name)
                else:
                    werewolf_agents.append(agent)
                    werewolf_agents_name.append(agent.person.name)

            joined_profiles_townfolk_list = []
            joined_profiles_werewolf_list = []
            
            for name, p in profiles2.items():
                if name in townfolk_agents_name:
                    joined_profile_townfolk = " ".join(p)
                    joined_profile_townfolk = name + ": " + joined_profile_townfolk
                    joined_profiles_townfolk_list.append(joined_profile_townfolk)
                elif name in werewolf_agents_name:
                    joined_profile_werewolf = " ".join(p)
                    joined_profile_werewolf = name + ": " + joined_profile_werewolf
                    joined_profiles_werewolf_list.append(joined_profile_werewolf)
                else:
                    pass

            join_townfolk_name_str = ",".join(townfolk_agents_name)
            joined_profiles_townfolk_str = "\n".join(joined_profiles_townfolk_list)
            join_werewolf_name_str = ",".join(werewolf_agents_name)
            joined_profiles_werewolf_str = "\n".join(joined_profiles_werewolf_list)
        

            to_be_killed_prompt = f"""
                        In the Mafia Game, there are werewolves who secretly try to eliminate townfolks at night. 

                    Based on the profiles of townfolks given below:
                    {joined_profiles_townfolk_str}

                    Which player do you think would be a strategic target for the werewolves, and why? Consider their profile and personality traits. 
                    Give the answer in the following format:

                    Name: [name of the townfolk to be eliminated]
                    Reason: [Give the reason of elimination in not more than 30 words]

                    Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.

                    """
            to_be_killed = ""
            try:
                to_be_killed = generate_response(to_be_killed_prompt)
                print(to_be_killed)
            except Exception as e:
                print("ChatGpt API busy, using own sense to find who will be killed.")

            global to_be_killed_p
            to_be_killed_p = random.choice(townfolk_agents)
            for agent in agents:
                for k in range(0,len(to_be_killed)):
                    if agent.person.name == to_be_killed[k:k+len(agent.person.name)]:
                        to_be_killed_p = agent
                        break 
            
            killer_prompt = f"""
                    In the Mafia Game, some players are werewolves who secretly target the innocent townfolk at night. 
                    The selected target for tonight is {to_be_killed_p.person.name}. Here's the list of werewolves participating:{join_werewolf_name_str} along with their profiles: {joined_profiles_werewolf_str}. 

                    In your opinion, which werewolf do you think would be the most strategic attacker except {to_be_killed_p.person.name}, against the townfolks and why? Please analyze their personality traits and profile before giving your recommendation. 

                    Your answer should follow this format:

                    Name: [Name of the werewolf] 
                    Reason: [Your statement on why they'd make a good attacker in 30 words or less]

                    Please remember that this is only a hypothetical situation for a game and should not be used to advocate or endorse any type of violence or harm towards actual people
                """

            killer = ""
            try:
                killer = generate_response(killer_prompt)
                print(killer)
            except Exception as e:
                print("ChatGpt API busy, using own sense to find killer.")
                

            
            global killer_p, prev_loc_killer, prev_loc_voters_list
            killer_p = random.choice(werewolf_agents)
            for agent in agents:
                for k in range(0,len(killer)):
                    if ((agent.person.name == killer[k:k+len(agent.person.name)]) and (to_be_killed_p.person.name != killer[k:k+len(agent.person.name)])):
                        killer_p = agent
                        break 
        
            prev_loc_killer = killer_p.location
            #Killer goes to the location of the townfolk 
            killer_p.update_location(killer_p.location, to_be_killed_p.location, global_time)
                
            
        if global_time == Killer_time + 1:
            #kill the agent
            killer_p.killing_action(to_be_killed_p,agents, global_time)
            if debug:
                print(killer_p.person.name, killer_p.location.name)
                print(to_be_killed_p.person.name, to_be_killed_p.state)
            # Killer back to its previous location
            killer_p.update_location(killer_p.location, prev_loc_killer, global_time)

        if (global_time == Voting_time) and (day !=1):
            prev_loc_voters_list = [agent.location for agent in agents]

            #Send all the killers to Hanazawa Park for Voting session
            for agent in agents:
                agent.update_location(agent.location, garden2, global_time)
            
        if (global_time == Voting_time + 1) and (day !=1):
            #Carry out the decision making session
            print_colored("Moving in Decision Making Function","blue",simulation_path)
            decision_making(agents)

        if (global_time == Voting_time + 1) and (day !=1):

            #Bring all the agents back to their original position
            for i in range(0,len(agents)):
                agents[i].update_location(agents[i].location, prev_loc_voters_list[i], global_time)

            
        return [agents, agent_current_tasks, True]


