# 一个GraphAgent类，用于初始化代理并运行相关工具，包括在交通知识图谱中搜索信息的Cypher工具
from langchain.agents.agent import AgentExecutor
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType


from env import getEnv
from cypher_tool import LLMCypherGraphChain

class GraphAgent(AgentExecutor):
    """Graph agent"""

    @staticmethod
    def function_name():
        return "GraphAgent"

    @classmethod
    def initialize(cls, graph, model_name, *args, **kwargs):
        if model_name in ['gpt-3.5-turbo', 'gpt-4']:
            llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=getEnv('OPENAI_KEY'))

        
        else:
            raise Exception(f"Model {model_name} is currently not supported")
        

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True)
        readonlymemory = ReadOnlySharedMemory(memory=memory)

        cypher_tool = LLMCypherGraphChain(
            llm=llm, graph=graph, verbose=True, memory=readonlymemory)

        # Load the tool configs that are needed.
        tools = [
            Tool(
                name="Cypher search",
                func=cypher_tool.run,
                description="""
                利用此工具在交通知识图谱中搜索信息，该数据库专门用于回答与交通相关的问题。
                输入应该是一个完整的问题。
                """,
            )
        ]

        agent_chain = initialize_agent(
            tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

        return agent_chain

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)
