from app.tools.web_search import search_web


print("===== TAVILY TEST =====")

query = "Indian AI startup funding"

response = search_web(query)

print("Response type:", type(response))

print(
    "Number of results:",
    len(response.get("results", []))
)

print("\n===== FIRST RESULT =====")

if response.get("results"):

    first_result = response["results"][0]

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

else:

    print("No results returned.")