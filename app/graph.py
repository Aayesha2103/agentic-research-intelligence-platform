from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.planner import planner_node
from app.agents.researcher import web_research_node
from app.agents.market_researcher import market_research_node
from app.agents.company_discovery import company_discovery_node
from app.agents.company_qualifier import company_qualification_node
from app.agents.company_researcher import company_research_node
from app.agents.verifier import source_verifier_node
from app.agents.scorer import scoring_node
from app.agents.synthesizer import synthesizer_node


def build_research_graph():

    graph = StateGraph(ResearchState)

    # Register all agent nodes

    graph.add_node(
        "planner",
        planner_node
    )

    graph.add_node(
        "web_researcher",
        web_research_node
    )

    graph.add_node(
        "market_researcher",
        market_research_node
    )

    graph.add_node(
        "company_discovery",
        company_discovery_node
    )

    graph.add_node(
        "company_researcher",
        company_research_node
    )

    graph.add_node(
        "company_qualifier",
        company_qualification_node
    )

    graph.add_node(
        "source_verifier",
        source_verifier_node
    )

    graph.add_node(
        "scorer",
        scoring_node
    )

    graph.add_node(
        "synthesizer",
        synthesizer_node
    )

    # Start with the Planner

    graph.add_edge(
        START,
        "planner"
    )

    # Planner starts two parallel research branches

    graph.add_edge(
        "planner",
        "web_researcher"
    )

    graph.add_edge(
        "planner",
        "market_researcher"
    )

    # General web research discovers candidate companies

    graph.add_edge(
        "web_researcher",
        "company_discovery"
    )

    # Discovered companies are researched before qualification

    graph.add_edge(
        "company_discovery",
        "company_researcher"
    )

    # Qualification now has company-specific evidence available

    graph.add_edge(
        "company_researcher",
        "company_qualifier"
    )

    # Both research branches eventually reach source verification

    graph.add_edge(
        "market_researcher",
        "source_verifier"
    )

    graph.add_edge(
        "company_qualifier",
        "source_verifier"
    )

    # Final node

    graph.add_edge(
        "source_verifier",
        "scorer"
    )

    graph.add_edge(
        "scorer",
        "synthesizer"
    )

    graph.add_edge(
        "synthesizer",
        END
    )

    return graph.compile()