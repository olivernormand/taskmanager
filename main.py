import os

import dotenv

from taskmanager.agent.taskmanager import (
    SCHEMA_TO_FUNCTION_MAP,
    SYSTEM_PROMPT,
    TOOLS,
    Taskmanager,
)

dotenv.load_dotenv()

tm = Taskmanager(
    system_prompt=SYSTEM_PROMPT,
    schema_to_function_map=SCHEMA_TO_FUNCTION_MAP,
    tools=TOOLS,
    model=os.getenv("AZURE_OPENAI_MODEL")
)

# Define the main event loop
while True:
    user_input = input("> ")
    if user_input == "/bye":
        exit()
    
    chain = tm.invoke(user_input)

    for event, data in chain:
        if event == "tool_call":
            tool_name, tool_args = data
            print(f"Calling tool: {tool_name} with args: {tool_args}")
        if event == "result":
            print(data)

    
