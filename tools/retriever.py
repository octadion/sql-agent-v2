# Few shots
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
# from langchain.agents.agent_toolkits import create_retriever_tool

from tools.tools_constants import few_shots_examples, retriever_tool_description

from dotenv import load_dotenv

load_dotenv()
def get_retriever_tool():
    embeddings = OpenAIEmbeddings()

    few_shot_docs = [
        Document(
            page_content=question, metadata={"sql_query": few_shots_examples[question]}
        )
        for question in few_shots_examples.keys()
    ]
    vector_db = FAISS.from_documents(few_shot_docs, embeddings)
    retriever = vector_db.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever, name="sql_get_few_shot", description=retriever_tool_description
    )
    return retriever_tool