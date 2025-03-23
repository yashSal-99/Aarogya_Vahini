import requests
from bs4 import BeautifulSoup

# Medicine Name
medicine_name = "dolo"


#1mg...................................................
# URL for 1mg
url = f"https://www.1mg.com/search/all?name={medicine_name}"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Request the page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract product details
products = soup.find_all("div", class_="style__price-tag___B2csA")  # Adjust class based on actual structure

prices = soup.find("div",{"class":"style__price-tag___B2csA"})
# len(prices)
# #print(all[0])
# price= prices[0].find("span").text
print(prices.text)
names = soup.find("span",{"class":"style__pro-title___3zxNC"})
print(names.text)