import requests
from bs4 import BeautifulSoup

def parse_sitemap(url, timeout):
    urls = []

    try:
        res = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(res.content, "xml")

        if soup.find("sitemapindex"):
            for sm in soup.find_all("sitemap"):
                loc = sm.find("loc").text
                urls.extend(parse_sitemap(loc, timeout))
        else:
            for u in soup.find_all("url"):
                loc = u.find("loc").text
                urls.append(loc)

    except Exception as e:
        print(f"Error parsing sitemap {url}: {e}")

    return urls
