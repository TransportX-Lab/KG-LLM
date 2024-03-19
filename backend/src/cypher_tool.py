# 用于生成Cypher查询语句的工具，通过示例Cypher查询生成对应的查询语句
from env import getEnv
from database import Neo4jDatabase
from pydantic import BaseModel, Extra
from langchain.prompts.base import BasePromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.base import Chain
from langchain.memory import ReadOnlySharedMemory, ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from typing import Dict, List, Any

from logger import logger

with open('examples.txt', 'rb') as file:
    examples = file.read().decode('utf-8', errors='ignore')


SYSTEM_TEMPLATE = """
您是一名助手，能够根据示例Cypher查询生成Cypher查询。
示例Cypher查询是：\n""" + examples + """\n
不要回复除Cypher查询以外的任何解释或任何其他信息。
请严格根据提供的Cypher示例生成Cypher语句。
请严格遵守提供的Cypher示例的格式
在Cypher语句中不要添加'''符号
不要提供任何无法从密码示例中推断出的Cypher语句。
"""
SYSTEM_CYPHER_PROMPT = SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE)

HUMAN_TEMPLATE = "{question}"
HUMAN_PROMPT = HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)


class LLMCypherGraphChain(Chain, BaseModel):
    """Chain that interprets a prompt and executes python code to do math.
    """

    llm: Any
    """LLM wrapper to use."""
    system_prompt: BasePromptTemplate = SYSTEM_CYPHER_PROMPT
    human_prompt: BasePromptTemplate = HUMAN_PROMPT
    input_key: str = "question"  #: :meta private:
    output_key: str = "answer"  #: :meta private:
    graph: Neo4jDatabase
    memory: ReadOnlySharedMemory

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Expect input key.
        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Expect output key.
        :meta private:
        """
        return [self.output_key]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        logger.debug(f"Cypher generator inputs: {inputs}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_prompt] + inputs['chat_history'] + [self.human_prompt]
        )
        # print(chat_prompt)
        cypher_executor = LLMChain(
            prompt=chat_prompt, llm=self.llm, callback_manager=self.callback_manager
        )
        # print(cypher_executor)
        cypher_statement = cypher_executor.predict(
            question=inputs[self.input_key], stop=["Output:"])
        print(cypher_statement)
        self.callback_manager.on_text(
            "Generated Cypher statement:", color="green", end="\n", verbose=self.verbose
        )

        self.callback_manager.on_text(
            cypher_statement, color="blue", end="\n", verbose=self.verbose
        )

        print(cypher_statement)
        print('------------------------')
        # If Cypher statement was not generated due to lack of context

        if not "MATCH" in cypher_statement:
            return {'answer': '无法创建查询语句'}
        
        try:
            context = self.graph.query(cypher_statement)
            print ('answer', context)
            return {'answer': context}

        except: 
            logger.debug('Cypher generator context:')
            return {'answer': '缺少符合问题的查询语句'}



if __name__ == "__main__":
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(
        openai_api_key=getEnv('OPENAI_KEY'),
        temperature=1,
        request_timeout=600)
    
    database = Neo4jDatabase(host="bolt://localhost:7687",
                             user="neo4j", password="404404404")

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    readonlymemory = ReadOnlySharedMemory(memory=memory)

    chain = LLMCypherGraphChain(llm=llm, verbose=True, graph=database, memory=readonlymemory)
    print('chain scuess')

    output = chain.run(
        "会议有哪些"
    )

    print(output)
