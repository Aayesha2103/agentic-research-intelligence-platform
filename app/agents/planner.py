from app.models.state import ResearchState
from app.services.llm import get_planner_llm


def planner_node(state: ResearchState) -> ResearchState:
    """
    Planner node.

    Uses the local Qwen3 LLM to convert the user's question
    into a structured research plan.
    """

    planner = get_planner_llm()

    plan = planner.invoke(
        f"""
        Create a research plan for the following question:

        {state.question}

        Your job is to decide what information must be researched.

        IMPORTANT RULES:

        1. Follow the user's question exactly.

        2. The user did NOT specify a year.
           Therefore, DO NOT put a specific year such as 2023,
           2024, 2025, or 2026 in research topics or search queries.

        3. Use wording such as:
           - current
           - latest
           - recent
           - present
           when time-sensitive information is required.

        4. Identify companies that are genuinely relevant
           to the user's research question.

        5. For this project, a company should be included in
           companies_to_research only when there is strong reason
           to believe that:

           - it is an Indian company or Indian startup,
           - AI is a core part of its primary product or business,
           - and it is relevant to the Indian AI startup ecosystem.

        6. DO NOT include large established corporations,
           IT-service companies, consulting companies, banks,
           traditional retailers, or other companies merely
           because they use AI internally.

        7. DO NOT include companies merely because:

           - they operate in India,
           - they have an Indian office,
           - they use AI internally,
           - they have an AI division,
           - they provide general technology services,
           - or they are a large multinational corporation.

        8. DO NOT include companies primarily headquartered
           outside India merely because they have Indian operations.

        9. Examples of companies that should NOT be included
           merely because they have Indian operations or
           AI-related activities include:

           - Bosch
           - Cognizant
           - Infosys
           - TCS
           - Wipro

        10. Be conservative when identifying companies.

            If you are uncertain whether a company is genuinely
            an Indian AI-focused startup, DO NOT include it as
            a confirmed company.

            Instead, use search queries to discover and verify
            suitable companies through web research.

        11. Do not include unnamed companies.

            Every company in companies_to_research must have
            a specific company name.

        12. Do not invent facts about companies.

            The plan should identify what needs to be researched.
            It should not claim that a company is successful,
            highly valued, or promising without evidence.

        13. Search queries should focus on collecting evidence about:

            - current funding
            - investors
            - products
            - customers
            - market position
            - growth
            - competitive differentiation
            - recent developments
            - Indian AI startup ecosystem trends
            - government support
            - market opportunities and challenges

        14. Generate approximately 6 to 8 high-value,
            non-duplicate search queries.

        15. Prefer broad ecosystem queries that can discover
            suitable Indian AI startups rather than guessing
            many company names.

        16. Do not create separate search queries for every
            possible company.

            Company-specific research should happen after
            suitable candidates have been identified.

        17. Search queries must NOT contain a specific year
            unless the user explicitly provided that year.

        18. Prefer queries that can return reliable evidence from:

            - company websites
            - reputable financial publications
            - established technology publications
            - government sources
            - research organizations
            - credible startup databases

        19. Avoid duplicate or nearly identical search queries.

        20. Return:

            - major research topics
            - only high-confidence AI-focused Indian companies
              when there is strong reason to include them
            - approximately 6 to 8 high-value search queries
              needed to gather reliable evidence

        Remember:

        The planner should NOT try to answer the user's question.

        The planner should create a research plan that allows
        downstream web research, qualification, verification,
        scoring, and report-generation agents to answer it
        using evidence.
        """
    )

    state.research_topics = plan.research_topics
    state.companies_to_research = plan.companies_to_research
    state.search_queries = plan.search_queries

    return state