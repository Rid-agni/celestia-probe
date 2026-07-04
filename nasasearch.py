from ddgs import DDGS


def find_nasa_page(entity):

    query = f"site:science.nasa.gov {entity} facts"

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=10))

    best_url = None
    best_score = -1

    for r in results:

        url = r["href"].lower()
        score = 0

        # Must be NASA Science
        if "science.nasa.gov" not in url:
            continue

        # Prefer fact pages
        if "facts" in url:
            score += 100

        # Prefer the entity name in the URL
        if entity.lower() in url:
            score += 40

        # Avoid blogs
        if "blog" in url:
            score -= 30

        # Avoid mission pages unless necessary
        if "mission" in url:
            score -= 15

        # Avoid images/resources
        if "image" in url or "resource" in url:
            score -= 20

        if score > best_score:
            best_score = score
            best_url = r["href"]

    return best_url