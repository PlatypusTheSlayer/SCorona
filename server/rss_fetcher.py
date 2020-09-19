import typing
import urllib
from bs4 import BeautifulSoup
import itertools
import feedparser
import numpy as np

class RssFetcher:

    def fetch_news_data(self):
        RssSources = ["http://feeds.bbci.co.uk/news/uk/rss.xml", "https://www.dailymail.co.uk/news/coronavirus/index.rss", "http://feeds.skynews.com/feeds/rss/uk.xml"]
        article_arr = []
        for rss in RssSources:
            feed = feedparser.parse(rss)
            for entry in feed.entries:
                article_text = self.get_article_data(entry.link)
                if article_text != "":
                    article_arr = np.append(article_arr, article_text.replace('\n', ' '))
        
        return article_arr

    def get_content(self, url, soup):
        try:
            if "bbc" in url:
                return "\n".join([x.text
                            for x in soup.body.find("div", property="articleBody").find_all("p")])
            if "dailymail" in url:
                return "\n".join([x.text
                            for x in soup.body.find("div", itemprop="articleBody").find_all("p")])
            if "sky" in url:
                return "\n".join([x.text
                            for x in soup.body.find("div", class_="sdc-article-body").find_all("p")])
            return ""
        except:
            return ""


    def get_article_data(self, url):
        try:
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            headline = soup.head.find("meta", property="og:title")
            if headline:
                headline = headline["content"]
            else:
                headline = ""

            corona_words = ['corona', 'coronavirus', 'covid-19', 'virus', 'covid', 'symptoms', 'test', 'lockdown', 'vaccine', 'death', 'infections', 'Wuhan', 'social', 'pandemic', 'epidemic', 'mask', 'restrictions', 'hospital', 'anti-lockdown', 'case']
            if any(word in headline.lower() for word in corona_words):
                content = self.get_content(url, soup)

                article_text = headline + ' ' + content
                return article_text
            else:
                return ""

        except:
            return ""

    def get_news_from_file(self):
        news_array = []
        f = open('resources/news-feed.txt')
        files_as_list = f.readlines()
        for line in files_as_list:
            news_array.append(line)
        return news_array

# Testing
if __name__ == "__main__":
    rss_fetcher = RssFetcher()
    print(rss_fetcher.fetch_news_data())