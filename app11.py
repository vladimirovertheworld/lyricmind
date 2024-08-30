import json
import feedparser
import requests
from bs4 import BeautifulSoup
import tempfile
import os
import subprocess
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)
MAX_PROMPT_LENGTH = 200

# Replace with your actual Vercel domain or localhost if running locally
BASE_URL = 'http://localhost:3000/'

def load_credentials():
    print(Fore.CYAN + "Loading credentials...")
    try:
        with open('creds.json', 'r') as f:
            creds = json.load(f)
        print(Fore.GREEN + "Credentials loaded successfully.")
        return creds
    except FileNotFoundError:
        print(Fore.RED + "Error: creds.json file not found.")
        return None
    except json.JSONDecodeError:
        print(Fore.RED + "Error: creds.json file is not valid JSON.")
        return None

def fetch_rss_feeds(num_articles=5):
    print(Fore.CYAN + f"Fetching {num_articles} articles from music RSS feeds...")
    rss_feeds = [
        "https://www.billboard.com/feed/",
        "https://www.clashmusic.com/feed/"
    ]
    
    articles = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'abstract': entry.summary if 'summary' in entry else entry.description,
                'url': entry.link,
                'source': feed.feed.title
            })
            if len(articles) >= num_articles:
                break
        if len(articles) >= num_articles:
            break
    
    print(Fore.GREEN + f"Successfully fetched {len(articles)} articles from music RSS feeds.")
    return articles

def display_articles(articles):
    print(Fore.CYAN + "Displaying fetched articles:")
    for i, article in enumerate(articles, 1):
        print(Fore.YELLOW + f"\n{i}. Title: {article['title']}")
        print(Fore.WHITE + f"   Abstract: {article['abstract']}")
        print(Fore.BLUE + f"   Source: {article['source']}")

def get_user_choice(max_choice):
    while True:
        try:
            choice = int(input(Fore.CYAN + f"\nChoose an article (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(Fore.RED + f"Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

def fetch_full_article(article):
    print(Fore.CYAN + "Fetching full article text...")
    try:
        response = requests.get(article['url'])
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the article content (this may need adjustment based on the website's HTML structure)
        content_div = soup.find('div', class_='content-body')
        if content_div:
            paragraphs = content_div.find_all('p')
        else:
            paragraphs = soup.find_all('p')
        full_text = '\n\n'.join([p.get_text() for p in paragraphs])
        
        if full_text:
            print(Fore.GREEN + "Full article text fetched successfully.")
            return full_text
        else:
            print(Fore.YELLOW + "Couldn't find article body. Falling back to abstract.")
            return article['abstract']
    except Exception as e:
        print(Fore.RED + f"Failed to fetch full article text: {str(e)}")
        print(Fore.YELLOW + "Using article abstract as fallback.")
        return article['abstract']


def create_request_template(article, full_text):
    print(Fore.CYAN + "Creating request template...")
    with open('request.txt', 'r') as f:
        template = f.read()
    
    article_content = f"Title: {article['title']}\n\nContent: {full_text}\n\nSource: {article['source']}\n\nURL: {article['url']}"
    request = f"Selected Article:\n\n{article_content}\n\n{template}"
    print(Fore.GREEN + "Request template created successfully.")
    return request

def edit_request(request):
    editor = os.environ.get('EDITOR', 'nano')  # default to nano if no EDITOR is set
    print(Fore.CYAN + f"Opening request in {editor} for editing...")
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".tmp") as tf:
        tf.write(request)
        tf.flush()
        subprocess.call([editor, tf.name])
        
        tf.seek(0)
        edited_request = tf.read()
    
    print(Fore.GREEN + "Request editing completed.")
    return edited_request

def display_full_prompt(request):
    print(Fore.CYAN + "Full prompt to be sent to Anthropic API:")
    print(Fore.WHITE + "-" * 50)
    print(Fore.YELLOW + request)
    print(Fore.WHITE + "-" * 50)

def generate_lyrics(client, request):
    print(Fore.CYAN + "Generating lyrics using Anthropic API...")
    prompt = f"{HUMAN_PROMPT}{request}{AI_PROMPT}"
    
    response = client.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=prompt,
    )
    print(Fore.GREEN + "Lyrics generated successfully.")
    return response.completion

def shorten_prompt(prompt, max_length=500):
    """Shorten the prompt to a maximum length while trying to keep it coherent."""
    if len(prompt) <= max_length:
        return prompt
    
    # Split the prompt into lines
    lines = prompt.split('\n')
    
    # Keep the first line (which should be the instruction) and as many lyrics as possible
    shortened = [lines[0]]
    current_length = len(lines[0])
    
    for line in lines[1:]:
        if current_length + len(line) + 1 > max_length:
            break
        shortened.append(line)
        current_length += len(line) + 1
    
    return '\n'.join(shortened)


def generate_audio(prompt):
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise ValueError(f"Prompt too long: {len(prompt)} characters. Max allowed is {MAX_PROMPT_LENGTH}.")
        print(Fore.CYAN + "Generating audio using Suno API...")
    url = f"{BASE_URL}/api/custom_generate"
    
    original_prompt = f"An song with the following lyrics: {lyrics}. The music should have a retro video game feel, with characteristic electronic bleeps and bloops."
    prompt = original_prompt
    
    for attempt in range(max_retries):
        payload = {
            "prompt": prompt,
            "make_instrumental": False,
            "wait_audio": False
        }
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            
            if response.status_code == 200:
                data = response.json()
                if data is None:
                    print(Fore.RED + "Received empty response from Suno API.")
                    return None
                if not isinstance(data, list) or len(data) < 2:
                    print(Fore.RED + f"Unexpected response format. Received: {data}")
                    return None
                print(Fore.GREEN + "Audio generation initiated successfully.")
                return data
            else:
                print(Fore.RED + f"Unexpected response. Status code: {response.status_code}")
                print(Fore.RED + f"Response content: {response.text}")
                
                # Check if the error is due to topic length
                error_detail = json.loads(response.text).get('detail', '')
                if 'Topic too long' in error_detail:
                    if attempt < max_retries - 1:
                        print(Fore.YELLOW + "Shortening prompt and retrying...")
                        prompt = shorten_prompt(prompt)
                    else:
                        print(Fore.RED + "Failed to generate audio after shortening prompt.")
                        return None
                else:
                    return None
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"An error occurred while making the request: {str(e)}")
            return None
        except json.JSONDecodeError:
            print(Fore.RED + "Failed to parse JSON response from Suno API.")
            print(Fore.RED + f"Raw response: {response.text}")
            return None
    
    print(Fore.RED + "Failed to generate audio after all retries.")
    return None

def get_audio_information(audio_ids):
    url = f"{BASE_URL}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

def check_audio_status(audio_ids):
    print(Fore.CYAN + "Checking audio generation status...")
    for _ in range(60):  # Check for up to 5 minutes
        data = get_audio_information(audio_ids)
        if data[0]["status"] == 'streaming':
            print(Fore.GREEN + "Audio generation completed.")
            return data
        print(Fore.YELLOW + "Audio generation in progress. Waiting...")
        time.sleep(5)  # Wait for 5 seconds before checking again
    print(Fore.RED + "Audio generation timed out.")
    return None

def main():
    print(Fore.MAGENTA + Style.BRIGHT + "Welcome to RADIO.AI MVP!")
    creds = load_credentials()
    
    if not creds:
        print(Fore.RED + "Failed to load credentials. Exiting.")
        return

    articles = fetch_rss_feeds()

    if articles:
        display_articles(articles)
        choice = get_user_choice(len(articles))
        selected_article = articles[choice - 1]
        
        print(Fore.CYAN + "\nSelected Article:")
        print(Fore.YELLOW + f"Title: {selected_article['title']}")
        print(Fore.WHITE + f"Abstract: {selected_article['abstract']}")
        print(Fore.BLUE + f"Source: {selected_article['source']}")
        print(Fore.BLUE + f"URL: {selected_article['url']}")
        
        full_text = fetch_full_article(selected_article)
        request = create_request_template(selected_article, full_text)
        edited_request = edit_request(request)
        
        while True:
            display_full_prompt(edited_request)
            edit_again = input(Fore.CYAN + "Would you like to edit the prompt again? (y/n): ").lower()
            if edit_again != 'y':
                break
            edited_request = edit_request(edited_request)
        
        print(Fore.CYAN + "\nGenerating lyrics based on the edited request...")
        
        # Anthropic API integration
        anthropic_key = creds['anthropic']['api_key']
        anthropic_client = Anthropic(api_key=anthropic_key)
        lyrics = generate_lyrics(anthropic_client, edited_request)
        
        print(Fore.GREEN + "\nGenerated Lyrics:")
        print(Fore.YELLOW + lyrics)
        
        print(Fore.CYAN + "\nGenerating 8bit chiptune style music...")
        
        # Suno API integration
        audio_data = generate_audio_by_prompt(lyrics)
        if audio_data:
            ids = f"{audio_data[0]['id']},{audio_data[1]['id']}"
            print(Fore.CYAN + f"Audio generation IDs: {ids}")
            
            final_audio_data = check_audio_status(ids)
            if final_audio_data:
                print(Fore.GREEN + "Audio URLs (8bit chiptune style):")
                print(Fore.YELLOW + f"1. {final_audio_data[0]['id']} ==> {final_audio_data[0]['audio_url']}")
                print(Fore.YELLOW + f"2. {final_audio_data[1]['id']} ==> {final_audio_data[1]['audio_url']}")
            else:
                print(Fore.RED + "Failed to generate audio.")
        else:
            print(Fore.RED + "Failed to initiate audio generation.")
            print(Fore.YELLOW + "Please check the Suno API server status and your network connection.")
    else:
        print(Fore.RED + "Failed to fetch articles. Exiting.")

if __name__ == "__main__":
    main()