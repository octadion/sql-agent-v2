from fastapi import FastAPI
from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field
import os
import warnings
import sys
sys.path.append("C:/Master/langchain_sql")
from sql_agent.agent import create_agent
from typing import List, Union, Any
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage
from typing import AsyncIterator
from langchain_core.runnables import RunnableLambda

# import langchain
# langchain.debug = True

warnings.filterwarnings("ignore")

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.join(current_dir, "..")

sys.path.insert(0, parent_dir)

class Input(BaseModel):
    input: str
    tool_llm_name: str
    agent_llm_name: str

async def custom_stream(input: Input) -> AsyncIterator[str]:
    agent_executor = create_agent(input["tool_llm_name"], input["agent_llm_name"])
    async for event in agent_executor.astream_events(
        {
            "input": input["input"],
        },
    ):  
        print(f"Received event data: {event['data']}")
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "agent"
            ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
                yield "\n"
                yield (
                    f"Starting agent: {event['name']} "
                    f"with input: {event['data'].get('input')}"
                )
                yield "\n"
        elif kind == "on_chain_end":
            if (
                event["name"] == "agent"
            ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
                yield "\n"
                yield (
                    f"Done agent: {event['name']} "
                    f"with output: {event['data'].get('output')['output']}"
                )
                yield "\n"
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                yield content
        elif kind == "on_tool_start":
            yield "\n"
            yield (
                f"Starting tool: {event['name']} "
                f"with inputs: {event['data'].get('input')}"
            )
            yield "\n"
        elif kind == "on_tool_end":
            yield "\n"
            yield (
                f"Done tool: {event['name']} "
                f"with output: {event['data'].get('output')}"
            )
            yield {"output": event["data"].get("output")}

class Output(BaseModel):
    output: Any

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using LangChain's Runnable interfaces",
)

agent = create_agent()

add_routes(
    app,
    # RunnableLambda(custom_stream).with_types(input_type=Input, output_type=Output).with_config(
    #     {"run_name": "agent"}
    # ),
    agent.with_types(input_type=Input, output_type=Output).with_config(
        {"run_name": "agent"}
    ),
)

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
# from flask import Flask, request, jsonify
# import os
# import warnings
# import unidecode
# import sys
# sys.path.append("C:/Master/langchain_sql")
# from sql_agent.agent import create_agent

# # import langchain
# # langchain.debug = True

# warnings.filterwarnings("ignore")

# current_dir = os.path.dirname(os.path.abspath(__file__))

# parent_dir = os.path.join(current_dir, "..")

# sys.path.insert(0, parent_dir)

# app = Flask(__name__)

# # Initialize agent
# # agent = create_agent()

# @app.route('/generate_response', methods=['POST'])
# def generate_response():
#     """
#     Generates a response based on the given input text using the agent.

#     Args:
#         input_text (str): The input text to generate a response for.

#     Returns:
#         str: The generated response.
#     """
#     input_text = request.json['input_text']
#     prompt = unidecode.unidecode(input_text)
#     tool_llm_name = request.json.get('tool_llm_name', "gpt-3.5-turbo")
#     agent_llm_name = request.json.get('agent_llm_name', "gpt-3.5-turbo")
#     agent = create_agent(tool_llm_name, agent_llm_name)
#     response = agent.run(prompt)
#     return jsonify(response=response)

# if __name__ == '__main__':
#     app.run(debug=True)