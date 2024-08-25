from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import os

print('Minimal Wikipedia Reader')
article_name = input('Enter the name of a topic: ')

# make articles directory
articles_folder = 'wikipedia_saved_articles'
if not os.path.exists(articles_folder):
    os.makedirs(articles_folder)

def find_article(article_name):
    article_name = article_name.strip().replace(' ', '_')

    # url = 'https://en.wikipedia.org/wiki/Human_body'
    url = 'https://en.wikipedia.org/wiki/' + article_name

    try:
        page = urlopen(url)
    except:
        print('Article not found, damn')
        sys.exit()
    return page, url

# html parser needs some work to cleanly produce an article with no werid characters
page, url = find_article(article_name)

html_bytes = page.read()
html_content = html_bytes.decode('utf-8')
soup = BeautifulSoup(html_content, 'html.parser')
content = soup.get_text().replace('[edit]', '')
print(content)

txt_name = url.replace('https://en.wikipedia.org/wiki/', '') + '.txt'

# write to file
with open(os.path.join(articles_folder, txt_name), "a", encoding="utf-8") as txt_f:
    txt_f.write(content)