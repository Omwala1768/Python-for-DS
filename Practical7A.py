import requests
from bs4 import BeautifulSoup

print("Om Wala S119")
url = "https://www.facebook.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print("Page Title:", soup.title.string)

for heading in soup.find_all("h1"):
    print("Heading:", heading.get_text())

for link in soup.find_all("a", href=True)[:5]:
    print("Link Text:", link.get_text(), "| URL:", link["href"])
