from bs4 import BeautifulSoup
import requests
import re

class Scraper:
    def __init__(self, wiki_url):
        self.wiki_url = wiki_url
        self.wiki_soup = self.createSoup(wiki_url)
        self.wiki_title = self.getTagText(self.scrapeTitle())
        self.wiki_toc = self.scrapeTOC()

    #TODO CHECK FOR URL VALIDITIE

    #TODO CREATE SOUP
    def createSoup(self, wiki_url):
        # Checks if the hyperlink is truely a wikipedia link
        pattern = '(https://en.wikipedia.org/wiki/).+'
        # TODO: add a check for a wiki/wiki_name#TOPIC link
        check = re.search(pattern, wiki_url)
        # If it's NOT a correct link:
        if check == None:
            print("not the right stuff man")
            return None
        else:
            #TODO add more detailed check later
            html = requests.get(wiki_url)
            print("Created the wiki-soup")
            return BeautifulSoup(html.text, 'html.parser')

    #TODO SCRAP UNNECCESSARY STUFF FROM SOUP
    def scrapeContent(self, wiki_soup):
        wiki_title = wiki_soup.find("h1", id="firstHeading")
        wiki_content = wiki_soup.find("div", id="mw-content-text")
        content_list = list()
        content_list.append(wiki_title)
        for tag in wiki_content:
            content_list.append(tag)
        return content_list

    #TODO SCRAPE TITLE
    def scrapeTitle(self):
        return self.wiki_soup.find("h1", id="firstHeading")

    #TODO SCRAPE TOC
    def scrapeTOC(self):
        # Gets the content table (toc)
        soup_content_table = self.wiki_soup.find("div", id="toc")
        # Gets all the <a> taggs from the toc
        content_list = list(soup_content_table.find_all('a'))
        # Loop over all the hyperlink-tags in the toc and create dictionary
        toc = {}
        for a in content_list:
            # Get content number and text and add them to the dictionary
            toc_number = a.find('span', {'class': 'tocnumber'}).text
            toc_text = a.find('span', {'class': 'toctext'}).text
            toc[toc_number] = toc_text
        return toc

    #TODO SCRAPE INTRODUCTION
    #TODO SCRAPE CONTENT

    #TODO GET TITLE
    #TODO GET TEXT
    def getTagText(self, tag):
        return tag.get_text()

    #TODO GET HYPERLINKS

    #TODO BUILD JSON
    #TODO GET JSON

url = 'https://en.wikipedia.org/wiki/Winterswijk'
scrapy = Scraper(url)
print(scrapy.wiki_title)
print(scrapy.wiki_toc)
