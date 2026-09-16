from app.models.state import ResearchState
from app.agents.researcher import web_research_node


print("===== WEB RESEARCH AGENT TEST =====")


state = ResearchState(
    question="Analyze the Indian AI startup market.",
    search_queries=[
        "Indian AI startup funding"
    ]
)


result = web_research_node(state)


print(
    "\nNumber of sources:",
    len(result["sources"])
)


if result["sources"]:

    first_source = result["sources"][0]

    print("\n===== FIRST NORMALIZED SOURCE =====")

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

    print(
        "Content preview:",
        first_source["content"][:300]
    )

else:

    print("No sources returned.")