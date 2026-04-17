import re
import requests
import time
from bs4 import BeautifulSoup


session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
})


def find_label_td(soup, label):
    # Normalize: collapse whitespace and replace NBSPs
    for td in soup.find_all("td", class_="indented"):
        text = td.get_text(" ", strip=True).replace("\xa0", " ")
        if label.lower() in text.lower():  # contains match
            return td
    return None

def analyze_word(word, delay=1):
    url = f"https://datayze.com/word-analyzer?word={word}"
    response = session.get(url, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    time.sleep(delay)

#Getting word rank
    rank_span = soup.find(id="word_rank")  # span with id="word_rank"
    rank = rank_span.get_text(strip=True)
    rank_no = re.sub('[^0-9]','',rank)
    label_td = find_label_td(soup, "Grade Level")

# Get the value from the next <td>
    value_td = label_td.find_next_sibling("td") if label_td else None
    grade_text = value_td.get_text(" ", strip=True) if value_td else None


    return {
        "word": word,
        "word_rank": rank_no,
        "reading_grade": grade_text
    }
