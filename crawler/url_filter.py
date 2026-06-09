def filter_urls(urls, include_prefixes, exclude_prefixes):
    result = []

    for url in urls:
        if "/en/" not in url:
            continue

        if include_prefixes and not any(url.startswith(p) for p in include_prefixes):
            continue

        if any(url.startswith(p) for p in exclude_prefixes):
            continue

        result.append(url)

    return list(set(result))
