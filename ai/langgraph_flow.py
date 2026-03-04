# app/ai/langgraph_flow.py

from langgraph.graph import StateGraph
from typing import TypedDict
from ai.gemini_client import generate_text


class CareerState(TypedDict):
    qualification: str
    skills: str
    aim: str
    roadmap: str


async def generate_roadmap(state: CareerState):

    prompt = f"""
    You are a professional career consultant.

    Qualification: {state['qualification']}
    Skills: {state['skills']}
    Aim: {state['aim']}

    Generate a structured 6-month career roadmap.
    Include:
    - Skills to learn
    - Projects to build
    - Learning resources
    - Links to relevant courses, tutorials, and communities
    """

    result = await generate_text(prompt)

    state["roadmap"] = result

    return state


builder = StateGraph(CareerState)

builder.add_node("generate", generate_roadmap)

builder.set_entry_point("generate")

builder.set_finish_point("generate")

career_graph = builder.compile()
