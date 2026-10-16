from selectolax.lexbor import LexborHTMLParser
import json
import httpx
from urllib.parse import quote

def fetch_html():

    search = input("Enter search query: ").strip()
    if not search:
        raise ValueError("Search query must not be empty")
    query = quote("-".join(search.split()), safe="")
    # For some reason if in url we will remove path /nedvizhimost/kvartiry/
    # it will not return list of adverts
    url = (
        "https://www.olx.ua/uk/nedvizhimost/kvartiry/"
        f"q-{query}/"
    )
    headers = {
        "Host": "www.olx.ua",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Connection": "keep-alive",
        "Priority": "u=0, i",
        "TE": "trailers"
    }

    with httpx.Client(
        http2=True, follow_redirects=True,
        timeout=httpx.Timeout(30.0, connect=10.0),
    ) as session:
        session.headers.update(headers)

        homepage = session.get("https://www.olx.ua/uk/")
        homepage.raise_for_status()
        response = session.get(url)
        response.raise_for_status()
        if "text/html" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("OLX returned an unexpected non-HTML response")
        print(f"HTTP {response.status_code}: {response.url}")
        return response.text

def parse_results(html: str) -> list[dict]:
    parser = LexborHTMLParser(html)
    scripts = parser.css(
        'script[data-rh="true"][type="application/ld+json"]'
    )

    if not scripts:
        raise ValueError("No script tag found")

    data = json.loads(scripts[1].text())
    return data

main_results = fetch_html()
parsed_results = parse_results(main_results)
print(json.dumps(parsed_results, indent=4, ensure_ascii=False))


# with open("raw/single_result_example.html", "r", encoding="utf-8") as f:
#     single_result = f.read()
#
# tree_single = LexborHTMLParser(single_result)
#
# categories = tree_single.css(".css-odhutu")
#
# for category in categories:
#     print(category.text())
