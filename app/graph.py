import time

from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.planner import planner_node
from app.agents.researcher import web_research_node
from app.agents.market_researcher import market_research_node
from app.agents.company_discovery import company_discovery_node
from app.agents.company_researcher import company_research_node
from app.agents.verifier import source_verifier_node
from app.agents.rag_indexer import rag_indexer_node
from app.agents.retriever import retriever_node
from app.agents.company_qualifier import company_qualification_node
from app.agents.scorer import scoring_node
from app.agents.confidence import confidence_node
from app.agents.synthesizer import synthesizer_node
from app.agents.hallucination_validator import validate_report

from app.services.observability import measure_latency


def timed_node(node_name, node_function):
    """Measure and display execution time for each graph node."""

    def wrapper(state):
        start_time = time.perf_counter()

        result = node_function(state)

        elapsed = measure_latency(start_time)

        print(
            f"[TIMING] {node_name}: "
            f"{elapsed:.2f} seconds"
        )

        return result

    return wrapper


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node(
        "planner",
        timed_node(
            "planner",
            planner_node,
        ),
    )

    graph.add_node(
        "web_researcher",
        timed_node(
            "web_researcher",
            web_research_node,
        ),
    )

    graph.add_node(
        "market_researcher",
        timed_node(
            "market_researcher",
            market_research_node,
        ),
    )

    graph.add_node(
        "company_discovery",
        timed_node(
            "company_discovery",
            company_discovery_node,
        ),
    )

    graph.add_node(
        "company_researcher",
        timed_node(
            "company_researcher",
            company_research_node,
        ),
    )

    graph.add_node(
        "source_verifier",
        timed_node(
            "source_verifier",
            source_verifier_node,
        ),
    )

    graph.add_node(
        "rag_indexer",
        timed_node(
            "rag_indexer",
            rag_indexer_node,
        ),
    )

    graph.add_node(
        "retriever",
        timed_node(
            "retriever",
            retriever_node,
        ),
    )

    graph.add_node(
        "company_qualifier",
        timed_node(
            "company_qualifier",
            company_qualification_node,
        ),
    )

    graph.add_node(
        "scorer",
        timed_node(
            "scorer",
            scoring_node,
        ),
    )

    graph.add_node(
        "confidence",
        timed_node(
            "confidence",
            confidence_node,
        ),
    )

    graph.add_node(
        "synthesizer",
        timed_node(
            "synthesizer",
            synthesizer_node,
        ),
    )

    graph.add_node(
        "hallucination_validator",
        timed_node(
            "hallucination_validator",
            validate_report,
        ),
    )

    graph.add_edge(
        START,
        "planner",
    )

    graph.add_edge(
        "planner",
        "web_researcher",
    )

    graph.add_edge(
        "planner",
        "market_researcher",
    )

    graph.add_edge(
        "web_researcher",
        "company_discovery",
    )

    graph.add_edge(
        "company_discovery",
        "company_researcher",
    )

    graph.add_edge(
        [
            "market_researcher",
            "company_researcher",
        ],
        "source_verifier",
    )

    graph.add_edge(
        "source_verifier",
        "rag_indexer",
    )

    graph.add_edge(
        "rag_indexer",
        "retriever",
    )

    graph.add_edge(
        "retriever",
        "company_qualifier",
    )

    graph.add_edge(
        "company_qualifier",
        "scorer",
    )

    graph.add_edge(
        "scorer",
        "confidence",
    )

    graph.add_edge(
        "confidence",
        "synthesizer",
    )

    graph.add_edge(
        "synthesizer",
        "hallucination_validator",
    )

    graph.add_edge(
        "hallucination_validator",
        END,
    )

    return graph.compile()