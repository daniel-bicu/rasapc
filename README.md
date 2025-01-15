# Learning RASA while developing the project
RASA is a tool to help you build task oriented dialogue systems. 
The core of building a Rasa assistant is providing examples that your system learns from. That way, Rasa can attempt to generalise patterns in your data.

RASA  = 2 systems:
    * NLU  = natural language understanding - accepts raw text that goes in and machine-readable information goes out. 
    parts that accepts text and can turn it into INTENTS and ENTITIES.
    Rasa - neural net. architecture(DIET) that sorts texts into intents and entities based on examples it's been provided.
    
    * Dialogue Policies = the part of system that predicts the next action to take. To allow for generalization, Rasa also provides a neural net called TED that picks the next best turn based on the conversation so far and all the conversations that it trained on.

How to make conversation work?
    - manually review and annotate conversations
    - spend enough time to correct any errors your assistant makes in a conversation such that your assistant can learn it's mistakes.
    
-> "Conversation-Driven Development"

# Components

domain.yml  = the heart of the bot
    intents = users intention
    entities = extracted data points form user input
        ex: city, date, etc.
    slots = store information extracted from entities or set programatically; used to maintain context across a conversation (they have types)
    responses = what the bot says in response to the user - can include dynamic content (like slot values)

nlu.yml = training data for the bots NLU
    intents + examples
    entity annotations

stories.yml = conversation flows for training RASA Core
    user-bot interaction flow where you use intents, entities, bot responses


config.yml = pipelines for NLU and dialog policies
    NLU pipeline + policies

endpoints.yml = define external services the bot connects to, such as the action server or trackers (custom action server for handling custom python-based actions)

used extra: spacy download en_core_web_md


rasa data validate 
rasa train

keep other terminal for: rasa run actions 



rasa run (just server starting) or rasa shell (bot interaction) or rasa interactive (interactive training)
# rasapc
