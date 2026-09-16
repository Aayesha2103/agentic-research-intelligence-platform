from langchain_ollama import ChatOllama

from app.models.planning import ResearchPlan


def get_llm():
    """
    Creates and returns the local LLM client used by the agents.
    """

    return ChatOllama(
        model="qwen3:8b",
        temperature=0
    )


def get_planner_llm():
    """
    Creates an LLM client that returns structured research plans.
    """

    llm = get_llm()

    return llm.with_structured_output(ResearchPlan)