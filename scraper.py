html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


from bs4 import BeautifulSoup
import requests
import re

url = 'https://en.wikipedia.org/wiki/Winterswijk'
html = requests.get(url)


soup = BeautifulSoup(html.text, 'html.parser')

def printemptyspace():
    for x in range(0,10):
        print("")

# Creates the Soup-object out of a Wikipedia URL
def createSoup(wikipedia_url):
    # Checks if the hyperlink is truely a wikipedia link
    pattern = '(https://en.wikipedia.org/wiki/).+'
    check = re.search(pattern, wikipedia_url)
    # If it's NOT a correct link:
    if check == None:
        print("not the right stuff man")
        return None
    else:
        #TODO add more detailed check later
        html = requests.get(url)
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
    # Gets everything in the introduction
    p_h2_tags = soup.find_all(['p', 'h2'])
    pattern = '(<h2>)'
    p_introduction_list = list()
    for tag in p_h2_tags:
        if re.search(pattern, str(tag)):
            break
        else:
            p_introduction_list.append(tag)
    return p_introduction_list

def scrapeTopic(soup, topic_title):
    p_h2_tags = soup.find_all(['p', 'h2'])
    p_topic_list = list()
    topic_title_found = False

    for tag in p_h2_tags:
        if topic_title_found:
            if re.search('(<h2>)', str(tag.get_text)):
                return p_topic_list
            else:
                p_topic_list.append(tag)
        if re.search('(<h2>)', str(tag)):
            if re.search(topic_title, str(tag.get_text)):
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

def getTagText(tag):
    return tag.get_text()

wiki_soup = createSoup(url)
# print(scrapeTOC(wiki_soup))

# scrapeIntroduction(createSoup(url))

print(scrapeTitle(wiki_soup))
print("")
print("")
# print(scrapeIntroduction(wiki_soup))
print(scrapeTopic(wiki_soup, 'Geography'))
