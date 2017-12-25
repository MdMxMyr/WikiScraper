from bs4 import BeautifulSoup
import requests
import re

# URLS for testing purposes
url = 'https://en.wikipedia.org/wiki/Winterswijk'
url_2 = 'https://en.wikipedia.org/wiki/Artificial_intelligence'

def printemptyspace():
    for x in range(0,10):
        print("")

# Creates the Soup-object out of a Wikipedia URL
def createSoup(wikipedia_url):
    # Checks if the hyperlink is truely a wikipedia link
    pattern = '(https://en.wikipedia.org/wiki/).+'
    # TODO: add a check for a wiki/wiki_name#TOPIC link
    check = re.search(pattern, wikipedia_url)
    # If it's NOT a correct link:
    if check == None:
        print("not the right stuff man")
        return None
    else:
        #TODO add more detailed check later
        html = requests.get(wikipedia_url)
        print("got the html")
        return BeautifulSoup(html.text, 'html.parser')

# Scrapes all the content of the page (except for the "from Wikipedia.." tag)
def scrapeContent(soup):
    wiki_title = soup.find("h1", id="firstHeading")
    wiki_content = soup.find("div", id="mw-content-text")
    content_list = list()
    content_list.append(wiki_title)
    for tag in wiki_content:
        content_list.append(tag)
    return content_list

# Scrapes the title of the wikipage
def scrapeTitle(soup):
    return soup.find("h1", id="firstHeading")

# Scrapes the Introduction of the wikipage
def scrapeIntroduction(soup):
    # Gets all the p and h2 tags from the wiki
    p_h2_tags = soup.find_all(['p', 'h2'])
    pattern = '(<h2>)'
    p_introduction_list = list()
    for tag in p_h2_tags:
        if re.search(pattern, str(tag)):
            break
        else:
            p_introduction_list.append(tag)
    return p_introduction_list

# Scrapes all the tags after a specific title/header (h-tag)
def scrapeTopic(soup, topic_title):
    p_h2_tags = soup.find_all(['p', 'h2', 'h3'])
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

# Scrapes the Table of Contents of the wikipage
def scrapeTOC(soup):
    # Gets the content table (toc)
    soup_content_table = soup.find("div", id="toc")
    # Gets all the <a> taggs from the toc
    content_list = list(soup_content_table.find_all('a'))
    # Loop over all the hyperlink-tags in the toc and create dictionary
    content = {}
    for a in content_list:
        # Get content number and text and add them to the dictionary
        toc_number = a.find('span', {'class': 'tocnumber'}).text
        toc_text = a.find('span', {'class': 'toctext'}).text
        content[toc_number] = toc_text
    return content

# Returns all the wiki-links for any given topic of a wiki
def getTopicWikilinks(soup, topic_title):
    tags = scrapeTopic(soup, topic_title)
    if tags:
        wiki_href_list = list()
        for tag in tags:
            wiki_links = getTagWikilinks(tag)
            if wiki_links:
                for wiki_link in wiki_links:
                    wiki_href_list.append(wiki_link)
        return wiki_href_list
    # return 0 if no tags were obtained (topic title was not found)
    else:
        return 0

# Returns 'displayed' text inbetween the tags
def getTagText(tag):
    return tag.get_text()

# Returns a list with all the links reffering to other Wiki's
def getTagWikilinks(tag):
    wiki_href_list = list()
    for link in tag.find_all('a'):
        href = link.get('href')
        if re.search('/wiki/', href):
            wiki_href_list.append(href)
    if wiki_href_list:
        return wiki_href_list
    else:
        return 0

wiki_soup = createSoup(url)
wiki_soup_2 = createSoup(url_2)

# print(scrapeTitle(wiki_soup_2))
#
# printemptyspace()
# for x in scrapeTopic(wiki_soup_2, 'History'):
#     if x:
#         for y in x:
#             print(y)
#
# printemptyspace()
for y in getTopicWikilinks(wiki_soup_2, 'History'):
    print(y)
# print(scrapeTopic(wiki_soup, 'World War II Liberation'))
