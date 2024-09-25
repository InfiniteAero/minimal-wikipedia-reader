"""
Main file for Minimal Wikipedia Reader
ONLY RUN THE PROGRAM FROM THIS FILE
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from rich.console import Console

from utils import find_article, pretty_print_article


if __name__ == "__main__":
    global console
    console = Console(highlight=False)

    console.print("Minimal Wikipedia Reader")
    article_name = input("Enter the name of a topic: ")

    # make articles directory
    articles_folder = "wikipedia_saved_articles"
    if not os.path.exists(articles_folder):
        os.makedirs(articles_folder)

    # load article
    page, url = find_article(article_name, console)
    html_bytes = page.read()
    html_content = html_bytes.decode("utf-8")
    selected_article = BeautifulSoup(html_content, "html.parser")

    content = pretty_print_article(selected_article)

    console.print(content)

    # write to file
    txt_name = url.replace("https://en.wikipedia.org/wiki/", "") + ".txt"
    with open(os.path.join(articles_folder, txt_name), "w", encoding="utf-8") as txt_f:
        txt_f.write(content)
