from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from config_loader import load_config
from sitemap_parser import parse_sitemap
from url_filter import filter_urls
from link_checker import check_links
from excel_writer import write_excel

def main():
    config = load_config()

    settings = config["settings"]
    output_file = config["output"]["file"]

    # Step 1: Collect URLs
    all_urls = []

    for sm in config["sitemaps"]:
        urls = parse_sitemap(sm["url"], settings["timeout_seconds"])
        urls = filter_urls(
            urls,
            sm["include_prefixes"],
            sm["exclude_prefixes"]
        )
        all_urls.extend(urls)

    urls = list(set(all_urls))
    print(f"Total URLs after filtering: {len(urls)}")

    # Step 2: Parallel crawl
    results = []

    with ThreadPoolExecutor(max_workers=settings["max_workers"]) as executor:
        futures = {executor.submit(check_links, url, settings["timeout_seconds"]): url for url in urls}

        for i, future in enumerate(tqdm(as_completed(futures), total=len(futures)), 1):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error processing {futures[future]}: {e}")

    # Step 3: Sort results
    results.sort(
        key=lambda r: (
            r.get("Broken Links") != "Yes",
            -(r.get("Broken Link Count") or 0)
        )
    )

    # Step 4: Export to Excel
    write_excel(results, output_file)

    print(f"✅ Done. Output saved to {output_file}")


if __name__ == "__main__":
    main()
