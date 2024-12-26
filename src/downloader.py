"""
Downloading functions for Minimal Wikipedia Reader
"""

from urllib.request import urlopen
import sys
import re
from bs4 import BeautifulSoup

from utils import find_article, pretty_print_article

def find_linked_articles(article: str) -> list:
    """Given an article name, find all wikipedia articles it links to"""
    # load article
    page, url = find_article(article)
    html_bytes = page.read()
    html_content = html_bytes.decode("utf-8")
    selected_article = BeautifulSoup(html_content, "html.parser")
    # find links to article
    linked_articles = []
    links = selected_article.find_all('a')
    for link in links:
        if link.get("href") is not None:
            if "/wiki/" in link.get("href"):
                linked_articles.append(link.get("href"))
    return linked_articles

    