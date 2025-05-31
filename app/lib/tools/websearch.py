import requests
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs, unquote

# Common headers to mimic a real browser
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}


class DuckDuckGoLinkParser(HTMLParser):
    def __init__(self, max_results: int):
        super().__init__()
        self.max_results = max_results
        self.results = []

        # State for capturing a result link
        self.capturing_title = False
        self.current_title = ""
        self.current_url = ""

        # Counter to stop after max_results
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if self.count >= self.max_results:
            return

        attrs_dict = dict(attrs)
        # DuckDuckGo marks result links with rel="nofollow"
        if tag == "a" and attrs_dict.get("rel") == "nofollow":
            href = attrs_dict.get("href", "").strip()
            if href:
                # Begin capturing the <a> text as the title
                self.capturing_title = True
                self.current_url = href
                self.current_title = ""

    def handle_data(self, data):
        if self.capturing_title:
            # Accumulate text inside the <a> tag
            self.current_title += data.strip()

    def handle_endtag(self, tag):
        if tag == "a" and self.capturing_title:
            # Finalize this result
            title = self.current_title.strip()
            url = self.current_url
            if title and url:
                self.results.append({
                    "title": title,
                    "url": url,
                    "snippet": "",
                    # Placeholder for full page content, will be filled later
                    "content": ""
                })
                self.count += 1
            # Reset capturing state
            self.capturing_title = False
            self.current_title = ""
            self.current_url = ""


def _normalize_ddg_url(href: str) -> str:
    """
    Given a DuckDuckGo redirect link (e.g., "//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com"),
    return the actual destination URL by extracting and decoding the 'uddg' parameter.
    If href is already a normal URL, return it unchanged.
    """
    # If it's a protocol-relative URL, prepend "https:"
    if href.startswith("//"):
        href = "https:" + href

    parsed = urlparse(href)
    # Check if it's a DuckDuckGo redirect path, like "duckduckgo.com/l/"
    if parsed.netloc.endswith("duckduckgo.com") and parsed.path.startswith("/l/"):
        qs = parse_qs(parsed.query)
        uddg_list = qs.get("uddg")
        if uddg_list:
            real_url = uddg_list[0]
            return unquote(real_url)

    return href


def web_search(query: str, num_results: int = 5, fetch_content: bool = True) -> list[dict]:
    """
    Perform a web search by scraping DuckDuckGo’s HTML interface,
    capturing top <num_results> links (title + URL), and optionally fetching
    the full HTML content of each result page (using a browser-like User-Agent).

    Args:
      query: The search query string.
      num_results: Number of top results to return (default is 5).
      fetch_content: If True, perform an HTTP GET on each result URL with headers
                     and store the raw HTML under "content". If False, leave "content" empty.

    Returns:
      List[dict]: A list of dictionaries, each containing:
        - "title": The title text of the result.
        - "url": The actual destination URL (decoded from DuckDuckGo’s redirect).
        - "snippet": An empty string (DuckDuckGo HTML interface does not expose a reliable snippet for all results when parsing manually).
        - "content": The full HTML text of the result page (if fetched), or "".
    """
    # Use DuckDuckGo’s HTML endpoint via GET
    search_url = "https://html.duckduckgo.com/html/"

    try:
        resp = requests.get(search_url, params={"q": query}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[web_search] HTTP error while searching: {e}")
        return []

    # Parse search results
    parser = DuckDuckGoLinkParser(max_results=num_results)
    parser.feed(resp.text)
    results = parser.results

    # Normalize each URL and optionally fetch full page content
    for item in results:
        raw_href = item["url"]
        actual_url = _normalize_ddg_url(raw_href)
        item["url"] = actual_url

        if fetch_content:
            try:
                page_resp = requests.get(actual_url, headers=HEADERS, timeout=10)
                page_resp.raise_for_status()
                item["content"] = page_resp.text
            except Exception as e:
                print(f"[web_search] Could not fetch content from {actual_url}: {e}")
                item["content"] = ""

    return results


# Example usage
if __name__ == "__main__":
    query = "Weather at budapest?"
    top_results = web_search(query, num_results=3, fetch_content=True)
    if not top_results:
        print("No results found or an error occurred.")
    else:
        for idx, item in enumerate(top_results, start=1):
            print(f"\nResult #{idx}")
            print("Title  :", item["title"])
            print("URL    :", item["url"])
            # Print first 200 characters of content (if fetched)
            snippet = item["content"][:200].replace("\n", " ")
            print("Content snippet (first 200 chars):")
            print(snippet + ("..." if len(item["content"]) > 200 else ""))
            print()
