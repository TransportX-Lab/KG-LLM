# 处理FastAPI路由的代码，其中包括了对Neo4j数据库的连接和一个用于预测的LLM智能体
import logging
from agent import GraphAgent
from env import getEnv
from database import Neo4jDatabase
from fastapi import APIRouter, HTTPException, Query
from run import get_result_and_thought_using_graph

neo4j_host = getEnv("NEO4J_URL")
neo4j_user = getEnv("NEO4J_USER")
neo4j_password = getEnv("NEO4J_PASS")
model_name = getEnv("MODEL_NAME")
# build router
router = APIRouter()
logger = logging.getLogger(__name__)
graph = Neo4jDatabase(
    host=neo4j_host, user=neo4j_user, password=neo4j_password)
print(neo4j_host)
# 不使用记忆组件功能，每次接口初始化
# agent_graph = GraphAgent.initialize(
#     graph=graph, model_name=model_name)


@router.get("/predict")
def get_load(message: str = Query(...)):
    try:
        agent_graph = GraphAgent.initialize(
            graph=graph, model_name=model_name)   
        # print('-------------------',message)
        # message = '兰亭序的演唱者是谁'
        return get_result_and_thought_using_graph(agent_graph, message)
        # return example_output
    except Exception as e:
        # Log stack trace
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e)) from e
