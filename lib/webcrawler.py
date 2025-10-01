import requests
from bs4 import BeautifulSoup

def crawler(instructions):
    # initiate variables
    target_url = instructions["start_url"]
    urls_to_visit = [target_url]
    depth = instructions["depth"]
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


    # this code has an array called titles
    # titles holds one array for each link
    # each link array holds an array for each tag
    # each tag array holds the text for the respective tag
    titles=[]
    linkNum=0
    for link in visited:
        titles.append([])
        response=requests.get(link)
        response.raise_for_status()
        i=0 # setup for tag indexing

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in instructions["tags"]:
            titles[linkNum].append([])
            #Grab titles
            title_elements = soup.select("h1")
            for title_element in title_elements:
                title = title_element.get_text(strip=True)
                titles[linkNum][i].append(title)
            i+=1
        linkNum+=1
    print(titles)

    # Outputs all links into a file
    with open(instructions["url_output"], "w") as f:
        for link in visited:
            f.write(link + "\n")
    
    # Output a csv file with headers as tag,link,text
    with open(instructions["tag_output"], "w") as f: # Opens the file
        f.write("tag,link,text")
        linkNum=0
        for link in visited:
            tagNum=0
            for tag in instructions["tags"]:
                print(tagNum)
                for text in titles[linkNum][tagNum]:
                    f.write(tag+","+link+","+text+"\n")
                tagNum+=1
            linkNum+=1