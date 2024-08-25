from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import os

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
soup = BeautifulSoup(html_content, "html.parser")

# format the page correctly
content = ""
tag_list = [tag for tag in soup.find_all()]
for tag in tag_list:
    if tag.name == "h1":
        # prints a fancy title with an underline
        content += tag.get_text() + "\n" + "".join(["-"] * len(tag.get_text())) + "\n"
    if tag.name == "h2":
        # end web scrape if we reacht he end of the main article's contents
        if tag.get_text() == "See also":
            break
        content += "\n" + tag.get_text() + "\n\n"
    if tag.name == "p":
        content += tag.get_text() + "\n"

# text_list = soup.find_all(['h1', 'h2', 'p'])
# content = ''
# for i in range(len(text_list)):
#     content += text_list[i].get_text()
#     content == '\n'
print(content)

txt_name = url.replace("https://en.wikipedia.org/wiki/", "") + ".txt"

# write to file
with open(os.path.join(articles_folder, txt_name), "a", encoding="utf-8") as txt_f:
    txt_f.write(content)
