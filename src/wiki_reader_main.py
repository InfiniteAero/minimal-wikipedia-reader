from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import os
import re

print("Minimal Wikipedia Reader")
article_name = input("Enter the name of a topic: ")

# make articles directory
articles_folder = "wikipedia_saved_articles"
if not os.path.exists(articles_folder):
    os.makedirs(articles_folder)


def find_article(article_name):
    article_name = article_name.strip().replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/" + article_name
    try:
        page = urlopen(url)
    except:
        print("Article not found, damn")
        sys.exit()
    return page, url


page, url = find_article(article_name)

# TODO: document code and split into multiple functions

html_bytes = page.read()
html_content = html_bytes.decode("utf-8")
selected_article = BeautifulSoup(html_content, "html.parser")

# format the page correctly
# TODO: add timestamp for each article generation
content = ""
tag_list = [tag for tag in selected_article.find_all()]
for tag in tag_list:
    if tag.name == "h1":
        # prints a fancy title for the article
        content += (
            "\n" + "".join(["*"] * len(tag.get_text()))+ "****\n"
            + "* " + tag.get_text() + " *\n" 
            + "".join(["*"] * len(tag.get_text())) + "****\n"
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

print(content)

txt_name = url.replace("https://en.wikipedia.org/wiki/", "") + ".txt"

# write to file
with open(os.path.join(articles_folder, txt_name), "w", encoding="utf-8") as txt_f:
    txt_f.write(content)
