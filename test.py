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
# TODO finish method
def scrapeIntroduction(soup):
    # Gets everything in the introduction
    soup = scrapeContentText(soup)
    p_h2_tags = soup.find_all(['p', 'h2'])
    printemptyspace()
    for tag in p_h2_tags:
        print(tag)

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

wiki_soup = createSoup(url)
# print(scrapeTOC(wiki_soup))

# scrapeIntroduction(createSoup(url))

print(scrapeTitle(wiki_soup))
