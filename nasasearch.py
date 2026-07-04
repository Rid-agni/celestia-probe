from ddgs import DDGS

def find_nasa_page(entity):

    query = f"{entity} NASA"
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        print(results)
        for r in results:
            url = r["href"]
            if "science.nasa.gov" in url and "facts" in url:
                return url
        for r in results:
            url = r["href"]
            if "science.nasa.gov" in url:
                return url
    #print("Query:", query)
    #print(results)
    return None