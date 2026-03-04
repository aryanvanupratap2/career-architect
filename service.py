# app/career/service.py

from ai.langgraph_flow import career_graph


async def generate_career_path(data: dict):

    result = await career_graph.ainvoke(data)

    return result["roadmap"]