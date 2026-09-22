DEMO_RESEARCH_SOURCES = [
    {
        "company": "Sarvam AI",
        "title": "Sarvam AI funding and investor interest",
        "url": "https://example.com/demo/sarvam-ai-funding",
        "content": (
            "Sarvam AI is an Indian AI company focused on "
            "developing AI models and applications for India. "
            "The source reports investor interest and funding "
            "activity around the company."
        ),
        "relevance_score": 0.95,
        "evidence_type": "funding",
        "query": "Indian AI startup funding",
    },
    {
        "company": "Sarvam AI",
        "title": "Sarvam AI products and technology",
        "url": "https://example.com/demo/sarvam-ai-product",
        "content": (
            "Sarvam AI develops artificial intelligence models "
            "and technology with a focus on Indian languages "
            "and applications."
        ),
        "relevance_score": 0.92,
        "evidence_type": "product",
        "query": "Indian AI startup products technology",
    },
    {
        "company": "Krutrim",
        "title": "Krutrim AI cloud growth",
        "url": "https://example.com/demo/krutrim-growth",
        "content": (
            "Krutrim is an Indian AI company developing AI "
            "technology and cloud services. The source reports "
            "strong revenue growth and a strategic move toward "
            "AI cloud services."
        ),
        "relevance_score": 0.94,
        "evidence_type": "growth",
        "query": "Indian AI startup growth",
    },
    {
        "company": "Krutrim",
        "title": "Krutrim AI products",
        "url": "https://example.com/demo/krutrim-product",
        "content": (
            "Krutrim develops AI products and infrastructure "
            "with a focus on artificial intelligence and cloud "
            "computing services."
        ),
        "relevance_score": 0.91,
        "evidence_type": "product",
        "query": "Indian AI startup products technology",
    },
    {
        "company": "CoRover",
        "title": "CoRover conversational AI platform",
        "url": "https://example.com/demo/corover-product",
        "content": (
            "CoRover is an Indian conversational AI company "
            "developing AI assistants and conversational "
            "applications for organizations."
        ),
        "relevance_score": 0.90,
        "evidence_type": "product",
        "query": "Indian AI startup products",
    },
    {
        "company": "E42",
        "title": "E42 conversational AI",
        "url": "https://example.com/demo/e42-product",
        "content": (
            "E42 develops conversational artificial intelligence "
            "solutions and virtual assistant technology for "
            "business use cases."
        ),
        "relevance_score": 0.89,
        "evidence_type": "product",
        "query": "Indian AI startup products",
    },
    {
        "company": "Yellow.ai",
        "title": "Yellow.ai conversational AI",
        "url": "https://example.com/demo/yellow-ai-product",
        "content": (
            "Yellow.ai develops conversational AI technology "
            "for automated customer and employee interactions."
        ),
        "relevance_score": 0.90,
        "evidence_type": "product",
        "query": "Indian AI startup products",
    },
    {
        "company": "Uniphore",
        "title": "Uniphore conversational AI",
        "url": "https://example.com/demo/uniphore-product",
        "content": (
            "Uniphore develops AI technology for enterprise "
            "conversations, customer service, and business "
            "automation."
        ),
        "relevance_score": 0.90,
        "evidence_type": "product",
        "query": "Indian AI startup products",
    },
]


def get_demo_research_sources() -> list[dict]:
    """
    Returns local research data used when live web
    search is unavailable.
    """

    return DEMO_RESEARCH_SOURCES.copy()