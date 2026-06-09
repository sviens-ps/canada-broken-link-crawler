from urllib.parse import urlparse, urlunparse


def transform_url(url, transform_config):
    if not transform_config:
        return url

    parsed = urlparse(url)

    scheme = parsed.scheme
    netloc = parsed.netloc

    # Force HTTPS
    if transform_config.get("force_https"):
        scheme = "https"

    # Force www
    if transform_config.get("force_www") and not netloc.startswith("www."):
        netloc = "www." + netloc

    return urlunparse((scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))


def matches_language(url, language_config):
    if not language_config:
        return True

    if language_config["type"] == "path":
        return language_config["value"] in url

    if language_config["type"] == "suffix":
        return url.endswith(language_config["value"])

    return True


def filter_urls(urls, include_prefixes, exclude_prefixes, language_config=None, transform_config=None):
    result = []

    for url in urls:
        # Step 1: Normalize URL FIRST
        url = transform_url(url, transform_config)

        # Step 2: Apply language rule
        if not matches_language(url, language_config):
            continue

        # Step 3: Apply include filter
        if include_prefixes and not any(url.startswith(p) for p in include_prefixes):
            continue

        # Step 4: Apply exclude filter
        if any(url.startswith(p) for p in exclude_prefixes):
            continue

        result.append(url)

    # Deduplicate
    return list(set(result))
