from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
import os
import re
from collections import Counter
from selenium.common.exceptions import StaleElementReferenceException

# ======================================================
# RAPIDAPI TRANSLATION FUNCTION (ADD YOUR KEY HERE)
# ======================================================
def translate_to_english(text):
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

    # clean smart quotes & special chars
    clean_text = (
        text.replace("‘", "'")
            .replace("’", "'")
            .replace("¿", "")
            .replace("?", "")
    )

    payload = {
        "from": "es",
        "to": "en",
        "q": [clean_text]
    }

    headers = {
        "X-RapidAPI-Key": "f04ad1be29msh06314ffb6835911p144c9fjsn4be4515f0435",
        "X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()

    result = response.json()

    if isinstance(result, list) and len(result) > 0:
        return result[0]
    else:
        raise Exception("Invalid translation response")



# ======================================================
# SETUP
# ======================================================
os.makedirs("images", exist_ok=True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)

# ======================================================
# OPEN OPINION PAGE
# ======================================================
driver.get("https://elpais.com/opinion/")
time.sleep(3)

# ======================================================
# ACCEPT COOKIES (SAFE)
# ======================================================
try:
    accept_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
    )
    accept_btn.click()
    print("Cookies accepted\n")
    time.sleep(2)
except:
    print("No cookie popup found\n")

# ======================================================
# COLLECT CANDIDATE ARTICLE LINKS (DATE BASED)
# ======================================================
anchors = driver.find_elements(By.TAG_NAME, "a")

candidate_links = []
for a in anchors:
    href = a.get_attribute("href")
    if href and re.search(r"/opinion/\d{4}-\d{2}-\d{2}/", href):
        if href not in candidate_links:
            candidate_links.append(href)

print("--- COLLECTED ARTICLE LINKS ---")
for l in candidate_links[:10]:
    print(l)

# ======================================================
# SAFE CONTENT EXTRACTION
# ======================================================
def get_article_content():
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
    texts = []
    for p in paragraphs:
        try:
            txt = p.text.strip()
            if len(txt) > 40:
                texts.append(txt)
        except StaleElementReferenceException:
            continue
    return " ".join(texts)

print("\n--- ARTICLE DATA ---")

spanish_titles = []
translated_titles = []

# ======================================================
# SCRAPE UNTIL 5 VALID ARTICLES
# ======================================================
valid_count = 0

for link in candidate_links:
    if valid_count == 5:
        break

    driver.get(link)

    try:
        title = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except:
        continue

    if not title or title.lower() == "opinión":
        continue

    content = get_article_content()
    if not content:
        continue

    valid_count += 1
    spanish_titles.append(title)

    print(f"\nArticle {valid_count}")
    print("Title (Spanish):", title)
    print("Content (Spanish):", content[:400])

    # ==================================================
    # IMAGE DOWNLOAD (IF AVAILABLE)
    # ==================================================
    try:
        img = driver.find_element(By.CSS_SELECTOR, "figure img")
        img_url = img.get_attribute("src")

        if img_url and img_url.startswith("http"):
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                with open(f"images/article_{valid_count}.jpg", "wb") as f:
                    f.write(response.content)
                print(f"Article {valid_count}: Cover image downloaded")
            else:
                print(f"Article {valid_count}: Image download blocked")
        else:
            print(f"Article {valid_count}: Image URL not available")

    except:
        print(f"Article {valid_count}: No cover image found")

# ======================================================
# TRANSLATE TITLES USING RAPIDAPI
# ======================================================
print("\n--- TRANSLATED TITLES (ENGLISH) ---")

for title in spanish_titles:
    try:
        translated = translate_to_english(title)
        translated_titles.append(translated)
        print(translated)
    except Exception as e:
        print("Translation failed for:", title)

# ======================================================
# WORD FREQUENCY ANALYSIS (>2 TIMES)
# ======================================================
print("\n--- REPEATED WORDS (>2 times) ---")

all_text = " ".join(translated_titles).lower()
words = re.findall(r"\b\w+\b", all_text)
counts = Counter(words)

found = False
for word, count in counts.items():
    if count > 2:
        print(word, ":", count)
        found = True

if not found:
    print("No words repeated more than twice")

driver.quit()
