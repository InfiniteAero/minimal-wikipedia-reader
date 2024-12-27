"""
Main file for Minimal Wikipedia Reader
ONLY RUN THE PROGRAM FROM THIS FILE
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import sys
from rich.console import Console

from utils import find_article, pretty_print_article
from downloader import find_linked_articles

if __name__ == "__main__":
    global console
    console = Console(highlight=False)

    console.print("Minimal Wikipedia Reader")
    article_name = input("Enter the name of a topic: ")

    # make articles directory
    articles_folder = "wikipedia_saved_articles"
    if not os.path.exists(articles_folder):
        os.makedirs(articles_folder)

    # load article, if not found print generic error message and quit
    try:
        page, url = find_article(article_name)
    except ValueError:
        console.print("Article not found")
        sys.exit()
    html_bytes = page.read()
    html_content = html_bytes.decode("utf-8")
    selected_article = BeautifulSoup(html_content, "html.parser")
    # remove language select from article
    language_button = selected_article.find("div", {"id": "p-lang-btn"})
    language_button.clear()
    # TODO: remove navbox at end of article

    content = pretty_print_article(selected_article)

    console.print(content)

    # test output for downloader
    console.print("\n\nDownloader test output\n**********************")
    downloader_output = find_linked_articles(selected_article)
    console.print(downloader_output)
    console.print("Downloader Output Length: " + str(len(downloader_output)) + " elements")

    # write to file
    txt_name = url.replace("https://en.wikipedia.org/wiki/", "") + ".txt"
    with open(os.path.join(articles_folder, txt_name), "w", encoding="utf-8") as txt_f:
        txt_f.write(content)
