# OtsukaAGI: The Werewolves of Millers Hollow

Welcome to "The Werewolves of Millers Hollow," an extraordinary autosimulative game that takes inspiration from the popular concept of AmongUs, but with a captivating twist! In this enthralling game, the participants are not ordinary players; they are autonomous agents, brought to life using the groundbreaking OtsukaAGI framework.

Within the quaint village of Hayashino, both the gentle Townfolks and the cunning Werewolves coexist. The Townfolks have two objectives: either complete their assigned tasks or unite their forces to identify and eliminate the sly Werewolves through a democratic voting process. On the other hand, the mischievous Werewolves endeavor to eliminate one unsuspecting Townfolk each night until their numbers match.

As the game unfolds, the OtsukaAGI-created agents take center stage, demonstrating their unique traits, interactions, and strategic decision-making abilities. The Townfolks collaborate to protect their community, while the Werewolves employ their wit to create chaos and remain hidden amidst the shadows.

Embrace the thrilling experience of witnessing autonomous agents engage in an autosimulative adventure like never before! Explore the intricate dynamics, unravel the mysteries, and immerse yourself in the world of "The Werewolves of Millers Hollow," where artificial intelligence meets suspenseful gameplay.

<img src = "/static/env.png">

## Game Video On Youtube
[![AGI Game Video](https://img.youtube.com/vi/q1weLwLNo3o/0.jpg)](https://www.youtube.com/watch?v=q1weLwLNo3o)

<iframe width="560" height="315" src="https://www.youtube.com/embed/q1weLwLNo3o?si=nR9cdekX0if1-ENm" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## OtsukaAGI - Agent Attributes:

1. **Memory**: This component is based on the modified GameGenerativeMemory class inherited from Langchain.
   - `llm`: The engine used by the agent to generate responses.
   - `memory_retriever`: The retriever responsible for extracting information from the agent's memory.
   - `verbose`: Provides additional details regarding the LLM's response.
   - `reflection_threshold`: Determines the threshold for generating reflections based on the agent's memory.
   - `file_path`: Specifies the file path containing the agent's memory, serving various purposes.

2. **Person**: This component is based on the modified GameGenerativeAgent class inherited from Langchain.
   - `name`: The name of the agent.
   - `age`: The agent's age as an integer.
   - `traits`: Describes the unique traits of the agent.
   - `status`: Reflects the agent's current situation or status.
   - `memory_retriever`: The retriever responsible for extracting information from the agent's memory.
   - `llm`: The engine used by the agent to generate responses.
   - `file_path`: Specifies the file path containing the agent's memory, serving various purposes.
   - `memory`: A reference to the agent's memory.

3. **Agent_Type**: This component categorizes agents based on their distinct characteristics, such as TownFolks and WereWolfs.

4. **Profile**: A string describing the character of the agent.

5. **Relations**: A dictionary of strings describing the agent's interactions with other agents in the environment.

6. **Plans**: Specifies the basic plans of the agent, including its daily routine.

7. **State**: Determines whether the agent is in an "alive" or "dead" state.

8. **Location**: Represents the current location of the agent as an object of the Place class.

9. **View**: Specifies the radius of the agent's field of view in the environment.

10. **Score**: Represents the number of tasks completed by the agent.

## OtsukaAGI - Agent Methods:

1. **get_memory()**: Returns the complete memory as a string.

2. **get_mem_summary()**: Provides a concise summary from the memory that is most relevant, important, and recent in relation to the input prompt.
   - `recency`: A value indicating the age of the memory point.
   - `relevance`: A value indicating the extent to which the prompt is relevant to the memory point.
   - `importance`: A value indicating the significance of the prompt with respect to the memory point.

3. **make_interaction_conversation_tree()**: Executes an interaction between our agents within a well-defined context.

4. **make_interaction()**: Performs a general, less-contextualized interaction between the agents.

5. **draw()**: Renders the agents on the pygame display.

6. **update_location()**: Updates the agent's location object.

7. **move_agent()**: Facilitates the movement of agents from one location to another.

8. **killing_action()**: Executes the process of the WereWolf killing Townfolks.


## OtsukaAGI - Place Attributes:

1. **History**: The "History" attribute is an essential component based on the modified GameGenerativeMemory class inherited from Langchain, forming a crucial part of OtsukaAGI's functionality.
   - `llm`: The engine utilized by the agent to generate responses.
   - `memory_retriever`: The retriever responsible for extracting information from the agent's memory.
   - `verbose`: Provides additional details regarding the LLM's response.
   - `reflection_threshold`: Determines the threshold for generating reflections based on the agent's memory.

2. **Information about the Locations**:
   - `name`: Represents the name of the location.
   - `description`: Provides a detailed description of the location.
   - `objects`: Lists the objects present within the internal view of the location.
   - `file_path`: Specifies the file path containing the location's history, serving various purposes.
   - `sabotage_memory`: Utilized to store information about tasks that have been sabotaged.

## OtsukaAGI - Place Methods:

1. **add_history()**: The "add_history()" method enables the addition of historical or informational data about the location. This method plays a vital role in enriching the agents' knowledge base, contributing to more informed interactions and decision-making.

All the aforementioned methods and attributes are inherited from OtsukaAGI, the powerful framework that serves as the backbone of this simulation. Additionally, some methods have been custom-defined to suit the specific requirements of the simulation, including "draw()", "killing_action()", and "sabotage_memory," among others.

By integrating these attributes and methods, the OtsukaAGI framework facilitates a dynamic and engaging simulation, where agents navigate the intricate complexities of locations, history, and interactions with remarkable intelligence and autonomy.

Get ready to be amazed as OtsukaAGI brings to life a captivating world of simulated agents, intelligent decision-making, and immersive storytelling. Embrace the boundless possibilities of this exceptional simulation, where the fusion of artificial intelligence and strategic gameplay creates an experience that is both unique and enthralling.

## Evaluation and Results

### End to End Evaluation

In the end-to-end evaluation of the OtsukaAGI framework, we investigated the impact of varying key parameters on the performance and outcomes of the simulation. The parameters that were varied included:

1. Number of Townfolks: The count of peaceful Townfolks in the game.
2. Number of Werewolves: The count of cunning and mischievous Werewolves in the game.
3. Number of Tasks: The total number of tasks that need to be completed during the gameplay.

The following properties were analyzed by varying the above parameters:

1. Townfolks Win Percentage: The percentage of games where the Townfolks emerged victorious over the Werewolves.
2. Werewolves Win Percentage: The percentage of games where the Werewolves successfully defeated the Townfolks.
3. Average Real Time: The average time taken for the simulation to run in real-time.
4. Average Game Time: The average duration of the game within the simulation.

### Observations and Conclusions:

1. Equal Chance of Townfolks and Werewolves to Win:
   - Number of Townfolks: 5
   - Number of Werewolves: 3
   - Number of Tasks: 28
   
2. Maximum Game Time:
   - Number of Townfolks: 6
   - Number of Werewolves: 2
   - Number of Tasks: 28
   
From the analysis of the charts, we draw the following conclusions:

- For an equal chance of Townfolks and Werewolves to win, a configuration of 5 Townfolks and 3 Werewolves, with 28 tasks, provided balanced gameplay with neither faction having a significant advantage.

- To maximize the game's duration, a setup with 6 Townfolks and 2 Werewolves, with 28 tasks, proved effective in creating a more extended and engaging gameplay experience.

It is essential to note that on average, there is a synchronization between real-time and game time, where approximately 30 seconds of real-time corresponds to 1 hour of game time. However, the precise synchronization depends on the latency of the LLM (Chat GPT LLM) engine used for the simulation.

In conclusion, the end-to-end evaluation of the OtsukaAGI framework has provided valuable insights into the influence of various parameters on the simulation's dynamics. The flexibility of the framework allows developers to customize the gameplay and tailor it to different scenarios, achieving optimal balance and creating captivating experiences for players. The synergy between artificial intelligence and strategic gameplay in "The Werewolves of Millers Hollow" showcases the power and potential of the OtsukaAGI framework, promising a new era of autonomous agents and immersive storytelling.


