from flask import Flask, render_template, Markup, Response,request
from utils1 import generate_response
from flask import jsonify


takashi_profile = "Takashi Yamamoto is a shopkeeper who loves interacting with customers. He manages operations at Shino Grocery Store and is interested in the upcoming local mayor election."

yumi_profile = "Yumi Yamamoto is a caring housewife who seeks to make life enjoyable for her family. She follows a regular schedule and goes to bed around 10pm."

kazuki_profile = "Kazuki Sato is a physics student at Kogaku Institute of Physics. She leads a healthy lifestyle, exercises in Hanazawa Park, and enjoys connecting with people."

satoshi_profile = "Satoshi Takahashi is a retired navy officer with interesting stories. He lives healthily, tends the park, reads avidly, and plans to run for local mayor in the upcoming election. He follows a strict schedule."

yusuke_profile = "Yusuke Mori is a skilled carpenter known for woodworking. He repairs furniture, supplies Kogaku Institute of Physics, and maintains Hanazawa fences. He is also a religious person."

ayumi_profile = "Ayumi Kimura is a supportive college professor, teaching physics and doing research at Kogaku Institute of Physics. She is nature-loving, interacts with people, and is interested in the upcoming local mayor election. She follows a set schedule."

# Takashi Yamamoto's Relations
takashi_relations = "Yumi Yamamoto is wife of Takashi Yamamoto. They discuss daily happenings at the Shino Grocery Store and neighborhood, as well as local politics. Kazuki Sato occasionally visits Yamamoto Residence for dinner. Takashi does not think Satoshi Takahashi is an ideal candidate for the local mayor elections. Yusuke Mori is called by Takashi for repairing furniture. Ayumi Kimura lives in the same neighborhood as Takashi Yamamoto."

# Yumi Yamamoto's Relations
yumi_relations = "Takashi Yamamoto is the husband of Yumi Yamamoto. They have a strong bond and discuss daily happenings at the Shino Grocery Store, the neighborhood, and local politics. Kazuki Sato knows Yumi well and sometimes visits Yamamoto Residence for dinner. Yumi has reservations about Satoshi Takahashi as a mayoral candidate. Yusuke Mori is called by Takashi for repairing furniture. Yumi and Ayumi Kimura live in the same neighborhood."

# Kazuki Sato's Relations
kazuki_relations = "Yumi Yamamoto knows Kazuki Sato well and they enjoy each other's company. They have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner. Kazuki and Takashi Yamamoto also know each other and have meals together. Kazuki respects Satoshi Takahashi and seeks his advice. Kazuki occasionally interacts with Yusuke Mori for wooden work. Ayumi Kimura and Kazuki have a close relationship at Kogaku Institute of Physics."

# Satoshi Takahashi's Relations
satoshi_relations = "Takashi Yamamoto and Satoshi Takahashi have different political ideologies and do not get along well. Yumi Yamamoto and Satoshi have differences in their local political thinking. Kazuki Sato considers Satoshi as a mentor and seeks his advice. Yusuke Mori and Satoshi are good friends and interact at Mizukami Shrine. Ayumi Kimura and Satoshi have deep conversations in Hanazawa Park or Mizukami Shrine."

# Yusuke Mori's Relations
yusuke_relations = "Yumi Yamamoto and Yusuke Mori have good relations but differ in their political thinking. Kazuki Sato occasionally interacts with Yusuke for wooden work. Yusuke respects Satoshi Takahashi and considers him an ideal mayoral candidate. Takashi Yamamoto calls Yusuke for repairing furniture and they occasionally meet at Mizukami Shrine. Yusuke and Ayumi Kimura have strained relations due to a contract dispute at Kogaku Institute of Physics."

# Ayumi Kimura's Relations
ayumi_relations = "Yumi Yamamoto and Ayumi Kimura live in the same neighborhood. They both think highly of each other. Kazuki Sato and Ayumi have a close relationship and interact regularly at Kogaku Institute of Physics. Satoshi Takahashi and Ayumi have deep conversations in Hanazawa Park or Mizukami Shrine. Yusuke Mori and Ayumi have strained relations due to a contract dispute at Kogaku Institute of Physics. Takashi Yamamoto lives in the same neighborhood as Ayumi Kimura."

#Sales agent complete profile 
name = "Aiko Tanaka"
age = 28
traits = ["charismatic", "persistent", "analytical"]
status = "Active"
description = "Aiko Tanaka is a dynamic sales agent working for Otsuka Shokai in Tokyo, Japan. With her magnetic personality and unwavering persistence, she has become a trusted representative of the company. Aiko's analytical mindset allows her to understand market trends and adapt her strategies accordingly, ensuring maximum sales outcomes. Her dedication to customer satisfaction and professionalism have earned her a stellar reputation in the industry. Aiko's proactive approach and strong work ethic make her an invaluable asset to Otsuka Shokai."
sales_agent_profile = "Aiko Tanaka, a 28-year-old sales agent, is a charismatic and persistent professional representing Otsuka Shokai in Tokyo. With her analytical mindset, she stays updated on market trends and devises effective strategies for optimal sales results. Aiko's commitment to customer satisfaction drives her to go the extra mile, fostering long-term relationships with clients. She is known for her proactive approach, strong work ethic, and unwavering professionalism, making her a valuable contributor to Otsuka Shokai's success."

plans = "Aiko's plans as a sales agent are centered around building strong relationships with clients and expanding the company's market share. She aims to deepen her understanding of customer needs by conducting thorough research and analysis. Aiko plans to identify potential growth areas and capitalize on emerging trends to drive sales. Additionally, she intends to enhance her knowledge and skills through ongoing training and professional development programs to stay ahead of the competition."

agent_tactics = "Aiko employs a variety of tactics to convince customers to buy Otsuka Shokai's products. She begins by actively listening to their needs and concerns, ensuring a personalized approach. Aiko then highlights the unique features and benefits of the company's offerings, using persuasive language and real-life examples to create a compelling case for the product's value. She leverages her analytical skills to provide data-driven insights and comparisons, demonstrating how Otsuka Shokai's products outperform competitors. Aiko also offers flexible pricing options, tailored solutions, and excellent after-sales support, building trust and customer loyalty."

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', text='')

@app.route('/check_window')
def index_testing_movement():
    return render_template('testing_movement.html', text='')

@app.route('/index_japanese')
def index0s():
    return render_template('index_japanese.html', text='')


@app.route('/sales_agent/chatbot')
def index1cs():
    return render_template('sales_agent_chatbot.html')


@app.route('/sales_agent/chatbot/process', methods=['POST'])
def process1s():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('sales_agent_memory.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('sales_agent_memory.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are {name}. You are {age} years old. You are charismatic, persistent, and analytical. You have the following description {description}. You have the following profile: {sales_agent_profile}. You have the following plans: {plans}. You generally follow the given tactics to attract the customers to buy your product: {agent_tactics}. Therefore, follow the above given tactics and the experience in your memory: {memory}, and without explicitly mentioning that you are {name}, answer the following prompt to attract the customer accordingly in not more than 40 words: {user_message}.")

    file = open('sales_agent_memory.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/takashi', methods=['GET', 'POST'])
def index1():

    return render_template('takashi.html')


@app.route('/takashi/chatbot')
def index1c():
    return render_template('takashi_chatbot.html')


@app.route('/takashi/chatbot/process', methods=['POST'])
def process1():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('memories/text1.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('memories/text1.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are Takashi Yamamoto. You have the following profile: {takashi_profile}. You have the following relations with other agents in the Hayashino village: {takashi_relations}. This is your past memory: {memory}. Considering your past memory, without explicitly mentioning that you are Takashi, answer the following prompt accordingly in not more than 20 words: {user_message}.")
    

    file = open('memories/text1.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/yumi', methods=['GET', 'POST'])
def index2():

    return render_template('yumi.html')


@app.route('/yumi/chatbot')
def index2c():
    return render_template('yumi_chatbot.html')


@app.route('/yumi/chatbot/process', methods=['POST'])
def process2():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('memories/text2.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('memories/text2.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are Yumi Yamamoto. You have the following profile: {yumi_profile}. You have the following relations with other agents in the Hayashino village: {yumi_relations}. This is your past memory: {memory}. Considering your past memory, without explicitly mentioning that you are Yumi, answer the following prompt accordingly in not more than 20 words: {user_message}.")

    file = open('memories/text2.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/satoshi', methods=['GET', 'POST'])
def index3():

    return render_template('satoshi.html')


@app.route('/satoshi/chatbot')
def index3c():
    return render_template('satoshi_chatbot.html')


@app.route('/satoshi/chatbot/process', methods=['POST'])
def process3():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('memories/text3.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('memories/text3.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are Satoshi Takahashi. You have the following profile: {satoshi_profile}. You have the following relations with other agents in the Hayashino village: {satoshi_relations}. This is your past memory: {memory}. Considering your past memory, without explicitly mentioning that you are satoshi, answer the following prompt accordingly in not more than 20 words: {user_message}.")

    file = open('memories/text3.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/ayumi', methods=['GET', 'POST'])
def index4():

    return render_template('ayumi.html')


@app.route('/ayumi/chatbot')
def index4c():
    return render_template('ayumi_chatbot.html')


@app.route('/ayumi/chatbot/process', methods=['POST'])
def process4():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('memories/text4.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('memories/text4.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are Ayumi Kimura. You have the following profile: {ayumi_profile}. You have the following relations with other agents in the Hayashino village: {ayumi_relations}. This is your past memory: {memory}. Considering your past memory, without explicitly mentioning that you are ayumi, answer the following prompt accordingly in not more than 20 words: {user_message}.")

    file = open('memories/text4.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/yusuke', methods=['GET', 'POST'])
def index5():

    return render_template('yusuke.html')


@app.route('/yusuke/chatbot')
def index5c():
    return render_template('yusuke_chatbot.html')


@app.route('/yusuke/chatbot/process', methods=['POST'])
def process5():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('memories/text5.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('memories/text5.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are Yusuke Mori. You have the following profile: {yusuke_profile}. You have the following relations with other agents in the Hayashino village: {yusuke_relations}.  This is your past memory: {memory}. Considering your past memory, without explicitly mentioning that you are yusuke, answer the following prompt accordingly in not more than 20 words: {user_message}.")

    file = open('memories/text5.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/kazuki', methods=['GET', 'POST'])
def index6():

    return render_template('kazuki.html')


@app.route('/kazuki/chatbot')
def index6c():
    return render_template('kazuki_chatbot.html')


@app.route('/kazuki/chatbot/process', methods=['POST'])
def process6():
    # Retrieve the data from the request
    data = request.json  # assuming the request content type is JSON

    user_message = data.get('message')

    file = open('memories/text6.html','a')
    file.write(f"User: {user_message} \n")
    file.close()

    with open('memories/text6.html', 'r') as file:
        memory =  file.read()
    
    bot_response = generate_response(f"You are Kazuki Sato. You have the following profile: {kazuki_profile}. You have the following relations with other agents in the Hayashino village: {kazuki_relations}. This is your past memory: {memory}. Considering your past memory, without explicitly mentioning that you are kazuki, answer the following prompt accordingly in not more than 20 words: {user_message}.")

    file = open('memories/text6.html','a')
    file.write(f"Me: {bot_response} \n")
    file.close()

    return jsonify(response=bot_response)

@app.route('/simulation')
def index7():
    return render_template('simulation_logs.html', text='')

@app.route('/well')
def index8():
    return render_template('well.html', text='')

@app.route('/haya1')
def index9():
    return render_template('haya1.html', text='')

@app.route('/haya2')
def index10():
    return render_template('haya2.html', text='')

@app.route('/haya3')
def index11():
    return render_template('haya3.html', text='')

@app.route('/haya4')
def index12():
    return render_template('haya4.html', text='')

@app.route('/college')
def index13():
    return render_template('college.html', text='')

@app.route('/shrine')
def index14():
    return render_template('shrine.html', text='')

@app.route('/yamamoto_residence')
def index15():
    return render_template('yamamoto_residence.html', text='')

@app.route('/get-text')

def get_text():
    # Replace this logic with your own code to fetch and return the updated text
    # Read the text from the file
    file_path = []

    file_path.append("memories/text1.html")
    file_path.append("memories/text2.html")
    file_path.append("memories/text3.html")
    file_path.append("memories/text4.html")
    file_path.append("memories/text5.html")
    file_path.append("memories/text6.html")
    file_path.append("memories/simulation.html")
    file_path.append("memories/well.html")
    file_path.append("memories/haya1.html")
    file_path.append("memories/haya2.html")
    file_path.append("memories/haya3.html")
    file_path.append("memories/haya4.html")
    file_path.append("memories/college.html")
    file_path.append("memories/shrine.html")
    file_path.append("memories/yamamoto_residence.html")

    
    texts = []

    for i in range(0,len(file_path)):
        with open(file_path[i], 'r') as file:
            texts.append(file.read())
    
    safe_html_contents = []
    for i in range(0,len(texts)):
        texts[i] = texts[i].replace('\n', '<br>')
        # Apply color to the text
        safe_html_contents.append(Markup(texts[i]))

    return safe_html_contents

@app.route('/updates')
def updates():
    def generate_updates():
        # Replace this logic with your own code to generate and yield the updated logs
        yield 'Updated Logs 1\n'
        yield 'Updated Logs 2\n'
        yield 'Updated Logs 3\n'

    return Response(generate_updates(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
