import requests
from bs4 import BeautifulSoup

def scrape_nasa_page(url):

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    headings = soup.find_all(
        "h2",
        attrs={"class": "wp-block-heading"}
    )

    text = ""

    for h in headings:

        text += "\n" + h.get_text(strip=True) + "\n"
        text += "-" * 30 + "\n"

        current = h.find_next_sibling()

        while current and current.name != "h2":

            if current.name == "p":
                text += current.get_text(strip=True) + "\n\n"

            current = current.find_next_sibling()

    return text