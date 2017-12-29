from bs4 import BeautifulSoup
import requests
import re

class Scraper:
    def __init__(self, wiki_url):
        self.wiki_url = wiki_url
        self.wiki_soup = self.createSoup(wiki_url)
        self.wiki_title = self.getTagText(self.scrapeTitle())
        self.wiki_toc = self.scrapeTOC()
        self.wiki_toc_contents = self.trimTOC()
        self.version = "1.0"
        self.wiki_json = self.buildJSON()

    #TODO CHECK FOR URL VALIDITIE
        # Check if true URL
        # Check if topic URL #

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
            #TODO Add check if it's actually a WIKI
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

    #TODO TRUE TOC
    def trimTOC(self):
        wiki_toc_contents = {}
        non_considered_topics = ['References', 'External links', 'See also']
        for index in self.wiki_toc:
            topic = self.wiki_toc[index]
            if topic in non_considered_topics:
                continue
            else:
                wiki_toc_contents[index] = topic
        return wiki_toc_contents

    #TODO SCRAPE INTRODUCTION
    #TODO SCRAPE CONTENT
    def scrapeTopic(self, topic_title):
        p_h2_tags = self.wiki_soup.find_all(['p', 'h2', 'h3'])
        p_topic_list = list()
        topic_title_found = False
        # It will first identify from which h-tag onwards the scrape should start
        for tag in p_h2_tags:
            if topic_title_found:
                # Will continue to append until a new h-tag is found
                if (re.search('(<h2>)', str(tag.get_text))) or (re.search('(<h3>)', str(tag.get_text))):
                    return p_topic_list
                else:
                    p_topic_list.append(tag)
            # After a h-tag was found with the title, it will start appending
            if (re.search('(<h2>)', str(tag))) or (re.search('(<h3>)', str(tag))):
                if re.search(topic_title, str(tag.get_text)):
                    p_topic_list.append(tag)
                    topic_title_found = True
            else:
                continue
        return 0

    #TODO GET TITLE
    #TODO GET TEXT
    def getTagText(self, tag):
        return tag.get_text()

    #TODO GET HYPERLINKS FROM CONTENT
    def getTopicWikilinks(self, topic_title):
        tags = self.scrapeTopic(topic_title)
        if tags:
            wiki_href_list = list()
            for tag in tags:
                wiki_links = self.getTagWikilinks(tag)
                if wiki_links:
                    for wiki_link in wiki_links:
                        wiki_href_list.append(wiki_link)
            return wiki_href_list
        # return 0 if no tags were obtained (topic title was not found)
        else:
            return 0

    #TODO GET HYPERLINKS FROM TAG
    def getTagWikilinks(self, tag):
        wiki_href_list = list()
        for link in tag.find_all('a'):
            href = link.get('href')
            if re.search('/wiki/', href):
                wiki_href_list.append(href)
        if wiki_href_list:
            return wiki_href_list
        else:
            return 0

    #TODO GET all
    def topicsToJSON(self):
        topic_dict_collection = list()
        for index in self.wiki_toc_contents:
            topic_dict = {}
            topic = self.wiki_toc_contents[index]
            topic_scrape_text = self.scrapeTopic(str(topic))
            topic_scrape_links = self.getTopicWikilinks(str(topic))
            #Only do things with topics that contain text, not list #TODO ADD LIST SUPPORT
            if len(topic_scrape_text) > 1:
                topic_text_list = list()
                for tag in topic_scrape_text:
                    tag_text = self.getTagText(tag)
                    topic_text_list.append(tag_text)
            else:
                continue
            topic_dict = {
                "topic_title": str(topic),
                "topic_index": str(index),
                "topic_text": str(' '.join(topic_text_list[1:])),
                "topic_wiki_link": topic_scrape_links,
            }
            print('The topic dict:')
            print(topic_dict)
            topic_dict_collection.append(topic_dict.copy())
            # TODO append them to the main dictionary
        return topic_dict_collection

    #TODO BUILD JSON
    def buildJSON(self):
        info = {
            "scraped_from": self.wiki_url,
            "scraped_at": 1, #insert timestamp
            "version": str(self.version),
        }
        TOC = self.wiki_toc
        TOC_contents = self.wiki_toc_contents
        contents = self.topicsToJSON()

        # Build the JSON-collection for this Wiki
        json_collection = {
            "info": info,
            "toc": TOC,
            "toc_contents": TOC_contents,
            "contents": contents,
        }
        return json_collection

url = 'https://en.wikipedia.org/wiki/Winterswijk'
scrapy = Scraper(url)

# print(scrapy.topicsToJSON())
print(scrapy.buildJSON())

# for topic in scrapy.wiki_toc_contents.values():
#     print(scrapy.scrapeTopic(topic))
#     print("")
#     print("")
#
#     print("")
