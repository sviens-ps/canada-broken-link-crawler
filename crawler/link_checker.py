import requests
from bs4 import BeautifulSoup

def check_links(url, timeout):
    broken_links = []

    try:
        res = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(res.text, "html.parser")

        links = [a.get("href") for a in soup.find_all("a", href=True)]

        for link in links:
            if link.startswith("#") or link.startswith("mailto") or link.startswith("javascript"):
                continue
            if not link.startswith("http"):
                continue

            try:
                r = requests.head(link, allow_redirects=True, timeout=timeout)
                if r.status_code >= 400:
                    broken_links.append(f"{link} ({r.status_code})")

            except Exception:
                broken_links.append(f"{link} (error)")

    except Exception:
        return {
            "Title": "",
            "URL": url,
            "Broken Links": "Error",
            "Broken Link Count": 0,
            "Broken Link Details": "Page failed"
        }

    return {
        "Title": soup.title.string if soup.title else "",
        "URL": url,
        "Broken Links": "Yes" if broken_links else "No",
        "Broken Link Count": len(broken_links),
        "Broken Link Details": "; ".join(broken_links[:10])
    }
