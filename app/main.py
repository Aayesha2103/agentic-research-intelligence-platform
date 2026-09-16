from app.models.state import ResearchState
from app.graph import build_research_graph


graph = build_research_graph()


initial_state = ResearchState(
    question="Analyze the Indian AI startup market and tell me which companies are most promising."
)


final_state = graph.invoke(initial_state)


print("\n===== RESEARCH PLAN =====")

print("\nResearch topics:")
for topic in final_state["research_topics"]:
    print("-", topic)

print("\nCompanies identified by Planner:")
for company in final_state["companies_to_research"]:
    print("-", company)

print("\nSearch queries:")
for query in final_state["search_queries"]:
    print("-", query)


print("\n===== RESEARCH RESULTS =====")

print(
    "\nGeneral sources:",
    len(final_state["sources"])
)

print(
    "Market sources:",
    len(final_state["market_sources"])
)

print(
    "Company sources:",
    len(final_state["company_sources"])
)

print(
    "Verified sources:",
    len(final_state["verified_sources"])
)


print("\n===== COMPANY QUALIFICATION =====")

for qualification in final_state["company_qualifications"]:

    print("\nCompany:", qualification["company_name"])

    print(
        "AI focused:",
        qualification["is_ai_focused"]
    )

    print(
        "Indian:",
        qualification["is_indian"]
    )

    print(
        "Startup:",
        qualification["is_startup"]
    )

    print(
        "AI is core business:",
        qualification["ai_is_core_business"]
    )

    print(
        "Should research:",
        qualification["should_research"]
    )

    print(
        "Qualification confidence:",
        qualification["qualification_confidence"]
    )

    print(
        "Reason:",
        qualification["reason"]
    )

    print("Evidence:")

    for evidence in qualification["evidence"]:
        print("-", evidence)