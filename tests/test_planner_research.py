from app.models.state import ResearchState
from app.agents.planner import planner_node
from app.agents.researcher import web_research_node


print("===== PLANNER → WEB RESEARCH TEST =====")


state = ResearchState(
    question=(
        "Analyze the Indian AI startup market "
        "and tell me which companies are most promising."
    )
)


print("\n===== RUNNING PLANNER =====")

state = planner_node(state)


print("\n===== PLANNER OUTPUT =====")

print(
    "Research topics:",
    state.research_topics
)

print(
    "Companies to research:",
    state.companies_to_research
)

print(
    "\nSearch queries:"
)

for query in state.search_queries:
    print("-", query)


print("\n===== RUNNING WEB RESEARCH =====")

research_result = web_research_node(state)


print("\n===== WEB RESEARCH OUTPUT =====")

print(
    "Number of sources:",
    len(research_result["sources"])
)


if research_result["sources"]:

    first_source = research_result["sources"][0]

    print("\n===== FIRST SOURCE =====")

    print(
        "Query:",
        first_source["query"]
    )

    print(
        "Title:",
        first_source["title"]
    )

    print(
        "URL:",
        first_source["url"]
    )

    print(
        "Relevance score:",
        first_source["relevance_score"]
    )