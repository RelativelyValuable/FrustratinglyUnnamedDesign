from bs4 import BeautifulSoup

import requests

def find_links_in_page(url):
    resp = requests.get(url)
    page_title = None
    links_on_page = []

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'xml')

        for link in soup.find_all("a"):
            try:
                links_on_page.append(link.get("href"))
            except:
                pass
        
        if soup.title:
            page_title = soup.title.text

    return page_title, links_on_page
