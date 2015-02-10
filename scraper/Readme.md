## Dependancies
Requires BeautifulSoup4

## Instructions
Run with following parameters

    ./scraper.py [first-char]
    
Where `[first-char]` is the first character for the words to be scraped

There is a 5 second backoff every 10 requests so we are relatively nice to the
server.

