"""
Doanloading functions for Minimal Wikipedia Reader
"""

from urllib.request import urlopen
import sys
import re

from wiki_reader_main import console

def find_linked_articles(article: str) -> list:
    """"""
    linked_articles = []
    