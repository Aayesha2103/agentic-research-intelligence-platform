from langchain_ollama import ChatOllama

from app.models.planning import ResearchPlan


def get_llm():
    return ChatOllama(
        model="qwen3:8b",
        temperature=0,
    )


def get_planner_llm():
    llm = get_llm()

    return llm.with_structured_output(
        ResearchPlan,
        include_raw=True,
    )