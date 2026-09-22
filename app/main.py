import time

from app.graph import build_research_graph
from app.models.state import ResearchState
from app.services.memory import (
    save_research_result,
    get_previous_research,
    is_memory_available,
)
from app.services.observability import flush_langfuse


def run_research(question: str) -> ResearchState:
    if is_memory_available():
        print("Redis memory: available")
    else:
        print(
            "Redis memory: unavailable "
            "— continuing without cache"
        )

    previous_result = get_previous_research(question)

    if previous_result:
        print()
        print("===== PREVIOUS RESEARCH FOUND =====")
        print("Using cached research from Redis.")
        print("===================================")
        print()

        return ResearchState(
            question=question,
            final_report=previous_result["report"],
        )

    graph = build_research_graph()

    initial_state = ResearchState(
        question=question
    )

    start_time = time.perf_counter()

    result = graph.invoke(
        initial_state
    )

    end_time = time.perf_counter()

    latency = end_time - start_time

    result["total_latency_seconds"] = round(
        latency,
        2,
    )

    final_state = ResearchState(
        **result
    )

    saved = save_research_result(
        question=question,
        report=final_state.final_report,
    )

    if saved:
        print(
            "Research result saved to Redis."
        )

    # Send pending Langfuse traces.
    flush_langfuse()

    print()
    print(
        "===== RESEARCH COMPLETED ====="
    )
    print()

    print(
        "Total latency: "
        f"{final_state.total_latency_seconds} "
        "seconds"
    )

    print(
        "Confidence score: "
        f"{final_state.confidence_score}"
    )

    print()
    print(
        "===== FINAL REPORT ====="
    )
    print()

    print(
        final_state.final_report
    )

    print()
    print(
        "===== END FINAL REPORT ====="
    )

    return final_state


if __name__ == "__main__":
    question = (
        "Analyze the Indian AI startup market "
        "and identify promising companies."
    )

    run_research(question)