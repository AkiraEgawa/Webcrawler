import requests
from bs4 import BeautifulSoup

def crawler(start, depth):
    # initiate variables
    target_url = start
    urls_to_visit = [target_url]
    visited = []
    crawl_count = 0
    
    # the crawler
    while urls_to_visit and crawl_count < depth:
        # grab the top url
        current_url = urls_to_visit.pop(0)
        # never visit this link again
        visited.append(current_url)

        response = requests.get(current_url)
        response.raise_for_status()
        
        # Parse this HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Grab links
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element["href"]

            # convert to absolute URL
            if url.startswith("#"):
                continue
            elif (not url.startswith("http")):
                absolute_url = requests.compat.urljoin(target_url, url)
            else:
                absolute_url = url

            if (
                # ensure same domain
                absolute_url.startswith(target_url) and absolute_url not in visited
            ):
                urls_to_visit.append(url)
            
        crawl_count+=1
    print(visited)

crawler("https://www.scrapingcourse.com/ecommerce/", 20)