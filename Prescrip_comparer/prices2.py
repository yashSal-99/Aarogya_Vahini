import requests
from bs4 import BeautifulSoup

# Medicine Name (Example: Paracetamol)
medicine_name = "crocin"

# URL for PharmEasy ..............................................................................................................
url = f"https://pharmeasy.in/search/all?name={medicine_name}"
r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c,"html.parser")
 
prices = soup.find_all("div",{"class":"ProductCard_gcdDiscountContainer__ADM_t"})
len(prices)
#print(all[0])
price= prices[0].find("span").text
print(price)

names = soup.find("h1",{"class":"ProductCard_medicineName__Uzjm7"})
print(names.text)

