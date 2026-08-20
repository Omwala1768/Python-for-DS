import requests
from bs4 import BeautifulSoup

url = "https://www.python.org/"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("Om Wala S119")
print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\n--- First 3 Paragraphs ---")
paragraphs = soup.find_all("p")
if paragraphs:
    for p in paragraphs[:3]:
        print(p.get_text(strip=True))
else:
    print("No paragraphs found.")

print("\n--- Image Source URLs ---")
images = soup.find_all("img")
if images:
    for img in images:
        print(img.get("src"))
else:
    print("No images found.")

print("\n--- Total Number of Links ---")
links = soup.find_all("a")
print("Total links:", len(links))

print("\n--- Headings ---")
headings = soup.find_all(["h1", "h2", "h3"])
if headings:
    for heading in headings:
        print(heading.get_text(strip=True))
else:
    print("No headings found.")

print("\n--- Language Names ---")
languages = soup.select(".central-featured-lang strong")
if languages:
    for lang in languages:
        print(lang.get_text(strip=True))
else:
    print("No language names found.")
