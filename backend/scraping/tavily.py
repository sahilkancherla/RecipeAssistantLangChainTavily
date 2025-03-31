import requests
import os
import json
from bs4 import BeautifulSoup
import re

tavily_key = os.getenv("TAVILY_API_KEY")
tavily_extract_url = "https://api.tavily.com/extract"

def extract_raw_html_from_url(url: str):
    
    payload = {
        "urls": url,
        "include_images": False,
        "extract_depth": "advanced"
    }
    headers = {
        "Authorization": tavily_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", tavily_extract_url, json=payload, headers=headers)
    
    byte_data = response._content
    decoded_data = byte_data.decode('utf-8')

    json_data = json.loads(decoded_data)

    if len(json_data["results"]) > 0:
        results = json_data["results"][0]
        raw_scraped_text = results['raw_content']
    else:
        raw_scraped_text = ""
        
    scraped_text =  clean_html(raw_scraped_text)

    return scraped_text    

def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    
    for script in soup(["script", "style"]):
        script.extract()
    
    # Get text and clean up whitespace
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

    