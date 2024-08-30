# app11.py

## Overview

`app11.py` is a Python script designed to perform various tasks including:

- Loading credentials and handling configuration.
- Interacting with APIs to fetch and parse data.
- Processing and parsing RSS feeds.
- Utilizing natural language processing via the Anthropic library.
- Generating colored output for terminal readability using Colorama.

## Features

- **Credential Management**: Securely loads and manages credentials for API access.
- **RSS Feed Parsing**: Fetches and parses RSS feeds to extract relevant information.
- **Web Scraping**: Uses BeautifulSoup to scrape data from web pages.
- **Natural Language Processing**: Integrates with the Anthropic API for AI-generated responses.
- **Terminal Output Formatting**: Enhances readability with color-coded terminal output using Colorama.

## Requirements

To run `app11.py`, you'll need the following Python libraries:

- `json`
- `feedparser`
- `requests`
- `bs4` (BeautifulSoup)
- `anthropic`
- `colorama`

You can install these dependencies using pip:

```
pip install feedparser requests beautifulsoup4 anthropic colorama
```

## SUNO API (unofficial)

git clone https://github.com/gcui-art/suno-api.git
cd suno-api
npm install

VISIT http://localhost:3000/api/get_limit to see limitations by Suno

{"credits_left":485,"period":"month","monthly_limit":2500,"monthly_usage":2015}

# we use custom_generate to upload bigger prompt 

- `/api/generate`: Generate music
- `/v1/chat/completions`: Generate music - Call the generate API in a format 
  that works with OpenAI’s API.
- `/api/custom_generate`: Generate music (Custom Mode, support setting lyrics, 
  music style, title, etc.)
- `/api/generate_lyrics`: Generate lyrics based on prompt
- `/api/get`: Get music list
- `/api/get?ids=`: Get music Info by id, separate multiple id with ",".
- `/api/get_limit`: Get quota Info
- `/api/extend_audio`: Extend audio length
- `/api/concat`: Generate the whole song from extensions


# EXAMPLE
```
Welcome to RADIO.AI MVP!
Loading credentials...
Credentials loaded successfully.
Fetching 5 articles from music RSS feeds...
Successfully fetched 5 articles from music RSS feeds.
Displaying fetched articles:

1. Title: Big Sean Releases ‘Better Me Than You’ Album Featuring Gunna, Kodak Black & More: Stream It Now
   Abstract: Dwayne "The Rock" Johnson even stops by to make a cameo.
   Source: Billboard

2. Title: Foster the People Land Third Top 10 on Billboard’s Album Sales Chart With ‘Paradise State of Mind’
   Abstract: Plus: Post Malone, Falling In Reverse, KATSEYE and Mori Calliope debut in the top 10.
   Source: Billboard

3. Title: Warner Music Brazil Announces New Structure to Boost Local Expansion
   Abstract: The company brings on executives Tatiana Cantinho and Mariana Frensel to fortify its genre-focused strategies and strengthen its market presence.
   Source: Billboard

4. Title: Chappell Roan Shares Her Favorite Songs Off Sabrina Carpenter’s ‘Short n’ Sweet’
   Abstract: Carpenter released her latest project on Aug. 23.
   Source: Billboard

5. Title: 10 Best Labor Day Men’s Clothing Deals — Starting At $7
   Abstract: Celebrate the long weekend with new clothes and major savings.
   Source: Billboard

Choose an article (1-5): 

Billboard is a part of Penske Media Corporation. © 2024 Billboard Media, LLC. All Rights Reserved.

Source: Billboard

URL: https://www.billboard.com/music/pop/chappell-roan-favorite-songs-sabrina-carpenter-short-n-sweet-1235764386/

IMPORTANT read this! ---------------------

Create a lyric for a funny song about this music news.
Create choruses with 2-3 words per line, end with wowels, use band, artist,
magazin, label names from the article in the first chorus line


Create last line in chorus 1 word line, repeat 1 word line for 6 times
Create prechorus with 2 lines and tag [pre chorus]
After first chorus put [instrumental] tag






--------------------------------------------------
Would you like to edit the prompt again? (y/n): 


```
