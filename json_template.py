'''

"WIKI-NAME":
    {
        "info": {
                "scraped_from": "complete wikipedia link",
                "scraped_at": "timestamp of scrape",
                "scraper_version": "api_version"
        },
        "TOC": {
                "index": "topic_title1",
                "index": "topic_title2",
                "index": "topic_title3"
        },
        "TOC_CONTENTS": {
                "index": "topic_title1",
                "index": "topic_title2"
        },
        "contents": [
            {
                "topic_title": "string with title",
                "topic_index": "index",
                "topic_text": "string with all the text",
                "topic_wiki_link": ["/wiki/link1", "/wiki/link2"]
            },
            {
                "topic_title": "string with title",
                "topic_index": int,
                "topic_text": "string with all the text",
                "topic_wiki_link": ["/wiki/link1", "/wiki/link2"]
            },
        ],
    },

'''
