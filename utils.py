from langchain.chat_models import ChatOpenAI

from langchain_community.llms import Ollama

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.llms import SagemakerEndpoint
from langchain_community.llms.sagemaker_endpoint import LLMContentHandler

from constants import chat_openai_model_kwargs, langchain_chat_kwargs

import json

# Optional, set the API key for OpenAI if it's not set in the environment.
# os.environ["OPENAI_API_KEY"] = "xxxxxx"


def get_chat_openai(model_name):
    """
    Returns an instance of the ChatOpenAI class initialized with the specified model name.

    Args:
        model_name (str): The name of the model to use.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI class.

    """
    llm = ChatOpenAI(
        openai_api_key="",
        model_name=model_name,
        model_kwargs=chat_openai_model_kwargs,
        **langchain_chat_kwargs
    )
    return llm

def get_ollama_llms(model_name):
    llm = Ollama(
        model=model_name,
        temperature=0,
        base_url=''
    )
    return llm

def get_chat_gemini(model_name):
    llm = ChatGoogleGenerativeAI(
        google_api_key="",
        model=model_name,
    )
    return llm
class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_str = json.dumps({"inputs": prompt, "parameters": model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]

content_handler = ContentHandler()

def get_sagemaker_endpoint(endpoint):
    llm=SagemakerEndpoint(
        endpoint_name=endpoint,
        region_name='ap-southeast-1',
        model_kwargs={"temperature": 0.1, "max_new_tokens": 1024},
        # endpoint_kwargs={"CustomAttributes": "accept_eula=true"},
        content_handler=content_handler,
    )
    return llm