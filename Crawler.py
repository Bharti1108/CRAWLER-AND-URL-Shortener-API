import re
import time
from collections import deque
from urllib.parse import urljoin , urlparse

import requests
from bs4 import BeautifulSoup

#indian numbers
PHONE_REGEX = re.compile(
    r"""(?<!\d)
    (?:\+91[\s\-]?|0)?
    [6-9]\d{4}[\s\-]?\d{5}
    (?!\d)
""",
re.VERBOSE,
)

def normalize_phone(raw):
    digits = re.sub(r"\D","",raw)
    if len(digits) ==10 and digits[0] in "6789":
        return f"$${digits}$$"
    if len(digits)==11 and digits.startswith("0")and digits[1] in "6789":
        return f"$${digits[1:]}$$"
    if len(digits) == 12 and digits.startswith("91") and digits[2] in "6789":
        return f"$${digits}$$"
    return None

print(normalize_phone('919354782076'))

def extract_phones_from_text(text):
    phones = set()
    for match in PHONE_REGEX.finditer(text):
        normalized = normalize_phone(match.group())
        if normalized:
            phones.add(normalized)
    return phones
    
text = """Please contact the support team if you face any issues. You can reach us at +91 98765 43210 or call our backup number 09876543210.

For urgent queries, dial 919876543210 directly. Our office landline is (080) 4567 8901, available during working hours."""
 


def get_links(url,html):
    domain=urlparse(url).netloc
    soup = BeautifulSoup(html,"html.parser")
    links = []
    for tag in soup.find_all("a",href=True):
        absolute_url = urljoin(url,tag["href"])
        if urlparse(absolute_url).netloc == domain:
            links.append(absolute_url)
    return links


def crawl(start_url , max_pages=30,delay=0.5):
    visited = set()
    queue = deque([start_url])
    all_phones = set()
    while queue and len(visited)<max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        try:
            response = requests.get(url,timeout=10,headers = {"User-Agent":"PhoneCrawler/1.0"})
            if "text/html" not in response.headers.get("Content-Type",""):
                continue
            response.raise_for_status()
        except  requests.RequestException as e:
            print(f"warning:{e}")
            continue
        html = response.text

        soup = BeautifulSoup(html,"html.parser")
        page_text = soup.get_text(separator=" ")
        phones_found = extract_phones_from_text(page_text)
        if phones_found:
            print(f"found phones:{phones_found}")
        all_phones.update(phones_found)
        for link in get_links(url,html):
            if link not in visited:
                queue.append(link)
        time.sleep(delay)
    return sorted(all_phones)



#url = "https://nammadirectory.com/"

#print(crawl(url))



