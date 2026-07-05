import requests
from bs4 import BeautifulSoup


def scrape_wikipedia_page(url):

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    content = soup.find("div", id="mw-content-text")

    if not content:
        return None

    IGNORE = {
        "See also",
        "References",
        "External links",
        "Notes",
        "Further reading",
        "Bibliography",
        "Sources",
        "Citations"
    }

    text = ""

    for element in content.find_all(["h2", "h3", "p"]):

        if element.name in ["h2", "h3"]:

            heading = element.get_text(" ", strip=True)
            heading = heading.replace("[edit]", "")

            if heading in IGNORE:
                break

            text += "\n" + heading + "\n"
            text += "-" * 30 + "\n"

        elif element.name == "p":

            paragraph = element.get_text(" ", strip=True)

            if paragraph:
                text += paragraph + "\n\n"

    return text


if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Horsehead_Nebula"

    article = scrape_wikipedia_page(url)

    print(article)