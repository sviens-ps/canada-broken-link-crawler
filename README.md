# Canada.ca Broken Link Crawler

Manual Python crawler that:

- reads these sitemap sources:
  - https://www.canada.ca/en/public-safety-canada.sitemap.xml
  - https://www.canada.ca/en/services.sitemap.xml
- keeps English pages only
- limits Services pages to:
  - /en/services/defence/nationalsecurity
  - /en/services/defence/securingborder
  - /en/services/policing
- excludes Public Safety news pages
- checks each page for broken links (internal and external)
- exports results to XLSX with a formatted Excel table

## Output columns
- Title  
- URL  
- Broken Links (Yes/No)  
- Broken Link Count  
- Broken Link Details  
