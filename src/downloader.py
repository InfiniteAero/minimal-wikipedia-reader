"""
Downloading functions for Minimal Wikipedia Reader
"""

from urllib.request import urlopen
import sys
import re
from bs4 import BeautifulSoup


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
            for bad_link in bad_links:
                if bad_link in article_link:
                    link_good = False
            if link_good: linked_articles.append(article_link)
    return linked_articles
