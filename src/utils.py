"""
Utility functions for Minimal Wikipedia Reader
"""

from urllib.request import urlopen
import sys
import re
import datetime


def pretty_print_article(selected_article: str) -> str:
    """Takes selected article's contents and prettifies it"""
    content = ""
    tag_list = [tag for tag in selected_article.find_all()]
    for tag in tag_list:
        if tag.name == "h1":
            # prints a fancy title for the article
            content += (
                "\n"
                + "".join(["*"] * len(tag.get_text()))
                + "****\n"
                + "* "
                + tag.get_text()
                + " *\n"
                + "".join(["*"] * len(tag.get_text()))
                + "****\n"
            )
        if tag.name == "h2":
            # end web scrape if we reach "See also"
            if tag.get_text() == "See also":
                break
            # ignore heading that reads "Contents"
            if tag.get_text() == "Contents":
                continue
            content += (
                "\n" + tag.get_text() + "\n" + "".join(["*"] * len(tag.get_text())) + "\n"
            )
        if tag.name == "h3":
            content += "~" + tag.get_text() + "~\n"
        if tag.name == "p":
            # avoid printing random blank lines
            if tag.get_text():
                content += tag.get_text() + "\n"
    # remove citations from article
    content = re.sub(r"\[(.*?)\]", "", content)
    # add timestamp to indicate how old the article copy is
    content += "\nThis article was scraped and saved at: " + str(
        datetime.datetime.now().replace(microsecond=0)
    )
    return content


def find_article(article_name: str):
    """Opens a wikipedia article link based on the name provided by the user, if it exists"""
    article_name = article_name.strip().replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/" + article_name
    try:
        page = urlopen(url)
    except:
        print("Article not found, damn")
        sys.exit()
    return page, url