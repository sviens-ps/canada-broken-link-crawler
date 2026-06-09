import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_valid_link(link):
    if not link:
        return False
    if link.startswith("#"):
        return False
    if link.startswith("mailto") or link.startswith("javascript"):
        return False
    if not link.startswith("http"):
        return False
    return True


def check_url(link, timeout):
    try:
        # Try HEAD first
        r = requests.head(link, allow_redirects=True, timeout=timeout)

        # Fallback to GET if blocked or invalid
        if r.status_code >= 400 or r.status_code in [403, 405]:
            r = requests.get(link, allow_redirects=True, timeout=timeout)

        return r.status_code

    except Exception:
        return "error"


def check_links(url, timeout):
    broken_links = []
    warnings = []

    try:
        res = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else ""

        # Deduplicate links
        links = list(set(
            a.get("href") for a in soup.find_all("a", href=True)
        ))

        for link in links:
            if not is_valid_link(link):
                continue

            status = check_url(link, timeout)

            # TRUE broken links only
            if status in [404, 410]:
                broken_links.append(f"{link} ({status})")

            # warnings (not counted as broken)
            elif status in [403, 401, 500, 502, 503, 504, "error"]:
                warnings.append(f"{link} ({status})")

    except Exception:
        return {
            "Title": "",
            "URL": url,
            "Broken Links": "Error",
            "Broken Link Count": 0,
            "Broken Link Details": "",
            "Warnings": "Page failed"
        }

    return {
        "Title": title,
        "URL": url,
        "Broken Links": "Yes" if broken_links else "No",
        "Broken Link Count": len(broken_links),
        "Broken Link Details": "; ".join(broken_links),
        "Warnings": "; ".join(warnings[:10])  # limit noise
    }
