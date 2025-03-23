import requests
from bs4 import BeautifulSoup

# Medicine Name (Example: Paracetamol)
medicine_name = "Crocin"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# ---------------- PharmEasy ----------------
print("Fetching data from PharmEasy...\n")
pharmeasy_url = f"https://pharmeasy.in/search/all?name={medicine_name}"
r = requests.get(pharmeasy_url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

try:
    price = soup.find("div", {"class": "ProductCard_gcdDiscountContainer__ADM_t"}).find("span").text
except AttributeError:
    price = "Price Not Found"

try:
    name = soup.find("h1", {"class": "ProductCard_medicineName__Uzjm7"}).text
except AttributeError:
    name = "Medicine Name Not Found"

print(f"PharmEasy Medicine: {name}")
print(f"PharmEasy Price: {price}")
print("-" * 40)


# ---------------- 1mg ----------------
print("Fetching data from 1mg...\n")
one_mg_url = f"https://www.1mg.com/search/all?name={medicine_name}"
response = requests.get(one_mg_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

try:
    price = soup.find("div", {"class": "style__price-tag___B2csA"}).text.strip()
except AttributeError:
    price = "Price Not Found"

try:
    name = soup.find("span", {"class": "style__pro-title___3zxNC"}).text.strip()
except AttributeError:
    name = "Medicine Name Not Found"

print(f"1mg Medicine: {name}")
print(f"1mg Price: {price}")
print("-" * 40)
