"""
Downloading functions for Minimal Wikipedia Reader
"""


import random
from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup

from utils import save_article, pretty_print_article, articles_folder

def find_linked_articles(selected_article: object) -> list:
    """Given an article name, find all wikipedia articles it links to"""
    # prepare link filter
    with open("src/filters/filter.txt", "r") as txt_bad:
        bad_links = txt_bad.read().splitlines()
    # find links to article
    linked_articles = []
    links = selected_article.find_all("a")
    for link in links:
        link_good = True
        article_link = link.get("href")
        if article_link is not None and "/wiki/" in article_link and article_link not in linked_articles:
            # filter out non article links
            article_link = article_link.split("#")[0]
            for bad_link in bad_links:
                if bad_link in article_link:
                    link_good = False
            if link_good: linked_articles.append(article_link)
    return linked_articles


def article_downloader(start_article: object, limit: int, chance: int) -> None:
    """Main function to handle downloading many articles at once"""
    links = find_linked_articles(start_article)
    internal_count = 0
    for link in links:
        if internal_count <= limit and random.randint(1,100) <= chance:
            # turn page into soup
            url = "https://en.wikipedia.org" + str(link)
            page = urlopen(url)
            html_bytes = page.read()
            html_content = html_bytes.decode("utf-8")
            link_soup = BeautifulSoup(html_content, "html.parser")
            # pull all links from soup and add to queue
            link_soup_links = find_linked_articles(link_soup)
            for soup_link in link_soup_links:
                links.append(soup_link)
            save_article(url, articles_folder, pretty_print_article(link_soup))
            internal_count += 1
            print("Downloaded: " + str(link) + " (#" + str(internal_count) + ")")
            sleep(0.5)
        else: break
    print("Download task complete!")
