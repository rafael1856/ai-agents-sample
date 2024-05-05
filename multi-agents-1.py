"""
Original code
https://colab.research.google.com/drive/1WgWKLH3sdXvzY7bd-ZZqCfZ8lI-pol05

This script demonstrates the usage of multiple agents in a group chat scenario. It defines several agents with different roles, such as Admin, Engineer, Planner, Executor, and Critic. These agents interact with each other to discuss and execute plans.

The code uses the litellm library for language model completion and autogen library for agent management. It also sets up environment variables for the OLLAMA host and LD_LIBRARY_PATH.

The script initializes the agents with their respective configurations and system messages. It then creates a GroupChat object and a GroupChatManager to manage the chat interactions.

The Admin agent initiates the chat by sending a message to the manager, requesting the creation of a Python app to get the weather forecast for today based on a given city name.

Note: This code is a simplified example and may require additional implementation for a complete working solution.
"""

import os
from litellm import completion
from autogen import AssistantAgent, GroupChatManager, UserProxyAgent
from autogen.agentchat import GroupChat

os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
os.environ["LD_LIBRARY_PATH"] = "/usr/lib64-nvidia"
MODEL = os.environ["MODEL"]
API_PORT="4000"

# print("MODEL:",MODEL)
# print("API_PORT:",API_PORT)

response = completion(
    model="ollama/" + MODEL,
    messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],
    api_base="http://127.0.0.1:11434",
    stream=True
)

for chunk in response:
    print("chunk",chunk['choices'][0]['delta'])

config_list = [
    {
        "model": "ollama/" + MODEL,
        "base_url": "http://localhost:" + API_PORT,  # litellm compatible endpoint ----> depends on the run!
        "api_key": "NULL",  # just a placeholder
    }
]
llm_config = {"config_list": config_list,}
code_config = {"config_list": config_list,}

# Define the agents and roles
admin = UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    llm_config=llm_config,
    code_execution_config=False,
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=code_config,
    system_message="""Engineer. You follow an approved plan. You write python code to solve tasks. Wrap the code in a code block that specifies the script type. Use good mdularization. The user can't modify your code. So do not suggest incomplete code which requires others to modify. If you use code using API key, please ask for the api_key so executor can test the code. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
""",
)

planner = AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=llm_config,
)


executor = UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    llm_config=llm_config,
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
)


critic = AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=llm_config,
)


groupchat = GroupChat(
    agents=[admin, engineer, planner, executor, critic],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

admin.initiate_chat(
    manager,
    message=""" Create a simple python pacman game. Where the player have to escape from the ghost and eat fruits" 
""",
)
