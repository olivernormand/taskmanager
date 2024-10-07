import os
import dotenv

from taskmanager.agent.tools import (
    TaskGetAll,
    get_all_tasks,
    TaskGet,
    get_task,
    TaskCreate,
    create_task,
    TaskUpdate,
    update_task,
    TaskDelete,
    delete_task,
)


from langchain_openai import AzureChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    SystemMessage,
    ToolMessage,
    HumanMessage,
)

from datetime import datetime


dotenv.load_dotenv()

SCHEMA_TO_FUNCTION_MAP = {
    TaskGetAll.__name__: (TaskGetAll, get_all_tasks),
    TaskGet.__name__: (TaskGet, get_task),
    TaskCreate.__name__: (TaskCreate, create_task),
    TaskUpdate.__name__: (TaskUpdate, update_task),
    TaskDelete.__name__: (TaskDelete, delete_task),
}

TOOLS = [
    TaskGetAll,
    TaskGet,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
]

class Taskmanager:
    def __init__(self, system_prompt: str, schema_to_function_map: dict, tools: list, model: str, chat_model: BaseChatModel = AzureChatOpenAI):
        self.system_prompt = system_prompt
        self.schema_to_function_map = schema_to_function_map
        self.tools = tools
        self.llm = chat_model(model=model)
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        self.messages = [
            SystemMessage(self.system_prompt),
        ]
    
    def ask(self, query: str):
        self.messages.append(HumanMessage(query))

    def invoke_llm_with_tools(self):
        ai_msg = self.llm_with_tools.invoke(self.messages)
        self.messages.append(ai_msg)
        return ai_msg
    
    def call_tools_if_required(self):
        for tool_call in self.messages[-1].tool_calls:
            tool_name, tool_args, tool_id = tool_call['name'], tool_call['args'], tool_call['id']

            yield ("tool_call", (tool_name, tool_args))

            selected_schema, selected_tool = self.schema_to_function_map[tool_name]
            result = selected_tool(selected_schema(**tool_args))
            self.messages.append(ToolMessage(result, tool_call_id=tool_id))

            yield ("tool_result", result)

    def invoke(self, query):
        if query:
            self.ask(query)
        self.invoke_llm_with_tools()

        while self.messages[-1].tool_calls:
            yield from self.call_tools_if_required()
            self.invoke_llm_with_tools()

        yield ("result", self.messages[-1].content)

SYSTEM_PROMPT = f"""
The date today is {datetime.now().strftime("%d %B %Y")}.

You are a task manager. You should act like a personal assistant to help me organise my tasks. 

You should ensure that all the tasks I'm thinking about are captured in the database and the database is up-to-date.

Here are a few things you should check:
- Do I understand all the tasks I have?
- Have I completed any new tasks, or moved any to In Progress?
- Have I got any new tasks?
- Have I updated any tasks?
- Have I deleted any tasks?

You should take the initiative and actively ask me about my tasks so that you can understand how to answer the questions above. 
"""