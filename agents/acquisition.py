from search.search import find_best_source
from search.search import search_wikipedia

from scrapers.nasa import scrape_nasa_page
from scrapers.wikipedia import scrape_wikipedia_page

from rag.ingest import ingest_text


SCRAPERS = {
    "NASA": scrape_nasa_page,
    "Wikipedia": scrape_wikipedia_page
}


def acquisition_node(state):
    
    print("=" * 60)
    print("ENTERED acquisition NODE")
    print("=" * 60)
    # Already exists? Nothing to do.
    if state["archive_exists"]:
        return state

    entity = state["entity"]

    result = find_best_source(
        entity,
        state["preferred_sources"],
        state["object_type"]
    )

    if result is None:
        raise Exception("No trusted source found.")

    source = result["source"]
    url = result["url"]

    print("Source:", source)
    print("URL:", url)

    raw_text = SCRAPERS[source](url)

    if (
        source == "NASA"
        and (raw_text is None or len(raw_text.split()) < 600)
    ):

        print("NASA page too small. Switching to Wikipedia...")

        wiki = search_wikipedia(entity)

        if wiki:
            source = wiki["source"]
            url = wiki["url"]

            raw_text = scrape_wikipedia_page(url)

            print("Wikipedia URL:", url)

    if raw_text:

        ingest_text(
            raw_text,
            url,
            entity,
            source
        )

        print("Added", entity, "to archive")

    state["source"] = source
    state["url"] = url

    return state