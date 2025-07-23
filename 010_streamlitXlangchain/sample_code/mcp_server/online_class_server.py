from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Kmong Class Search")

@mcp.tool()
def class_search(keyword: str) -> List[Dict[str, str]]:
    """
    Crawl Kmong Website for the given keyword and return structured list(title & url).
    """
    response = requests.get(f"https://kmong.com/search?type=gigs&keyword={keyword}")
    if response.status_code != 200:
        return [{"error": f"HTTP 요청 실패: 상태 코드 {response.status_code}"}]

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("a", class_=lambda c: c and "gig-card" in c)
    results = []
    for a in cards:
        href = a.get("href", "")
        link = href if href.startswith("http") else "https://kmong.com" + href
        spans = a.select("div.pt-2 div.flex.flex-col.gap-1 > span")
        if not spans: continue
        full_title = spans[0].get_text(strip=True)
        badge = spans[1].get_text(strip=True) if len(spans) > 1 else ""
        title = full_title[len(badge):] if full_title.startswith(badge) else full_title
        results.append({"title": title, "url": link})

    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")
