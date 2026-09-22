from app.tools.web_search import search_web


def test_tavily_search():

    print("===== TAVILY TEST =====")

    query = "Indian AI startup funding"

    response = search_web(query)

    print("Response type:", type(response))

    print(
        "Number of results:",
        len(response)
    )

    assert isinstance(response, list)

    print("\n===== FIRST RESULT =====")

    assert len(response) > 0

    first_result = response[0]

    print(
        "Title:",
        first_result.get("title", "")
    )

    print(
        "URL:",
        first_result.get("url", "")
    )

    print(
        "Content:",
        first_result.get("content", "")[:500]
    )

    print(
        "Score:",
        first_result.get("score", 0.0)
    )

    assert "title" in first_result
    assert "url" in first_result