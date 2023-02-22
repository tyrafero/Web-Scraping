from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy import Nominatim


html_text= requests.get("https://basobaas.com/category/house?category=2&status=Sale").text
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
        is_seller_valid= getattr(house.find("span",class_="negotiable"),"text","Unverified")
        writer.writerow([property_title,property_location,property_size,property_price,is_seller_valid])

from unidecode import unidecode

# Read the CSV file
df = pd.read_csv('houses.csv', encoding="utf-8")

# Replace "None" string with empty string
df.replace("None","")



# Replace "NPR." string
df["Price"] = df["Price"].str.replace("NPR.", "")

# Replace "Onwards" and "Total Price" strings
df["Price"] = df["Price"].str.replace(" Onwards", "")
df["Price"] = df["Price"].str.replace(" Total Price", "")
df["Price"] = df["Price"].str.replace(",","")
df.dropna(inplace=True)

df["Location"]= df["Location"].apply(lambda x: x.split(",")[0])
# Convert Devanagari numerals to regular numbers

def convert_devanagari_to_number(text):
    return unidecode(text)

df['Price'] = df['Price'].apply(convert_devanagari_to_number)
# remove the three digit numbers




# geolocator = Nominatim(user_agent="http")

# from functools import partial
# geocode= partial(geolocator.geocode, language="en")

# def get_lat_long(location):
#     try:
#         location = geolocator.geocode(location)
#         return (location.latitude, location.longitude)
#     except:
#         return (None, None)

# # apply the function to a DataFrame column
# df['Location'] = df['Location'].map(get_lat_long)


df.to_csv("houses.csv", index= False)
print(df)

add= df["Location"].to_list()
cost= df["Price"].to_list()

import plotly.graph_objects as go
# This dataframe has 244 lines, but 4 distinct values for `day`
fig = go.Figure(data=[go.Pie(labels=add, values=cost, textinfo='label+value',
                             insidetextorientation='radial'
                            )])
fig.show()