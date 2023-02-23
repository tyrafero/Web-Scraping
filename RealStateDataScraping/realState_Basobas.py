from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import csv
import pandas as pd
from unidecode import unidecode
import plotly.graph_objects as go
# from geopy.extra.rate_limiter import RateLimiter


# Set up the Selenium driver
service = Service('C:/path/to/chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://basobaas.com/properties/premium-properties/all/house"
driver.get(url)


# Wait for the page to load
time.sleep(5)

# Click the "Load More" button
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Wait for the element to become visible
wait = WebDriverWait(driver, 10)
load_more_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'btn btn-primary loading-btn')]")))
# Wait for the new data to load


# Get the HTML content of the page after all the dynamic content is loaded
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


houses= soup.find_all("div",class_="padding-right-remove col-lg-6 col-md-6 col-xl-3")

file= "D:\OneDrive\Desktop\Projects\Web Scrapping\RealStateDataScraping\csvFiles\houses.csv"

with open(file,"w",encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Location", "Area", "Price", "Seller Validity"])
    for house in houses:
        property_title= getattr(house.find("h5",class_="title"),"text",None)
        property_location= getattr(house.find("small",class_=""),"text",None)
        property_size= getattr(house.find("div",class_="area"),"text",None)
        property_price= getattr(house.find("span",class_="price"),"text",None)
        is_seller_valid= getattr(house.find("span",class_="negotiable"),"text","Unverified")
        writer.writerow([property_title,property_location,property_size,property_price,is_seller_valid])





# Read the CSV file
df = pd.read_csv(file, encoding="utf-8")
# Replace "None" string with empty string
df.replace("None","")



# Replace "NPR." string
df["Price"] = df["Price"].str.replace("NPR.", "")

# Replace "Onwards" and "Total Price" strings
df["Price"] = df["Price"].str.replace(" Onwards", "")
df["Price"] = df["Price"].str.replace(" Total Price", "")
df["Price"] = df["Price"].str.replace(",","")
df["Price"] = df["Price"].str.replace("onwards","")
df["Price"] = df["Price"].str.replace("Starting From","")
# Drop rows where the "Title" column contains the word "Office"
df = df.loc[~df['Title'].astype(str).str.contains('Office')]

# Drop rows where the "Title" column contains the word "Rent"
df = df.loc[~df['Title'].astype(str).str.contains('Rent')]

df = df.loc[~df['Title'].astype(str).str.contains('Apartment')]


df.dropna(inplace=True)

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
df.to_csv(file, index= False)
print(df)

add= df["Location"].to_list()
cost= df["Price"].to_list()



# Convert cost to a list of integers
cost_int = [int(c.replace(",", "")) for c in cost]

# Create the figure with the updated y-axis range
fig = go.Figure(data=[go.Bar(x=add, y=cost_int)])

# Customize the layout
fig.update_layout(
    title="Cost of houses in different locations",
    xaxis_title="Location",
    yaxis_title="Cost",
    font=dict(size=12),
    margin=dict(l=50, r=50, b=50, t=80, pad=4),
    plot_bgcolor="white",
)

# Customize the traces
fig.update_traces(
    marker_color="steelblue",
    textposition="outside",
    texttemplate="%{y:,.0f}",
    hovertemplate="Location: %{x}<br>Cost: %{y:,.0f}",
)
fig.show()