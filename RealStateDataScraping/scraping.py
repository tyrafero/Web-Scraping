from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd


html_text= requests.get("https://basobaas.com/category/house").text
soup= BeautifulSoup(html_text,"lxml")

houses= soup.find_all("div",class_="padding-right-remove col-lg-6 col-md-6 col-xl-3")

with open("houses.csv","w",encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Location", "Area", "Price", "Seller Validity"])
    for house in houses:
        property_title= getattr(house.find("h5",class_="title"),"text",None)
        property_location= getattr(house.find("small",class_=""),"text",None)
        property_size= getattr(house.find("div",class_="area"),"text",None)
        property_price= getattr(house.find("span",class_="price"),"text",None)
        is_seller_valid= getattr(house.find("span",class_="negotiable"),"text",None)
        writer.writerow([property_title,property_location,property_size,property_price,is_seller_valid])
df = pd.read_csv('houses.csv', encoding="utf-8")
print(df)