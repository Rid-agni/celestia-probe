from ddgs import DDGS

def find_best_source(entity):

    searchers = [

        search_nasa,

        search_wikipedia
    ]

    for search in searchers:

        result = search(entity)

        if result:

            return result

    return None
def search_nasa(entity):

    query = f"site:science.nasa.gov {entity} facts"

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=10))

    best_result = None
    best_score = -1

    for r in results:

        url = r["href"].lower()
        score = 0

        if "science.nasa.gov" not in url:
            continue

        if "facts" in url:
            score += 100

        if entity.lower() in url:
            score += 40

        if "blog" in url:
            score -= 30

        if "mission" in url:
            score -= 15

        if "image" in url or "resource" in url:
            score -= 20

        if score > best_score:
            best_score = score
            best_result = {
            "url": r["href"],
            "source": "NASA"
        }
    return best_result
from ddgs import DDGS

def search_wikipedia(entity):

    query = entity

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    for r in results:

        url = r["href"]

        if "wikipedia.org/wiki/" in url:

            return {
                "url": url,
                "source": "Wikipedia"
            }

    return None