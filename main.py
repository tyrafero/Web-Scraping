import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
import plotly.graph_objects as go
import collections

html_text = requests.get("https://broadwayinfosys.com/offers").text
soup = BeautifulSoup(html_text, "lxml")

offers = soup.find_all("div", class_="col-inner d-flex offer-card")

with open("offers.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["offer_name", "offer_start_date", "offer_end_date", "offer_validity"])

    for offer in offers:
        offer_name = offer.find("strong", class_="content-title").text
        offer_start_date = offer.find("span", class_="inn").text
        offer_end_date = offer.find("span", class_="off").text
        offer_validity = offer.find("span", class_="badge badge-expired").text

        writer.writerow([offer_name, offer_start_date, offer_end_date, offer_validity])

df = pd.read_csv('offers.csv', encoding="latin1")
name = df["offer_name"].tolist()
start = df["offer_start_date"].tolist()
end = df["offer_end_date"].tolist()
validity = df["offer_validity"].tolist()

# Count the number of occurrences of each unique value in the `validity` list
start_counts = collections.Counter(start)
name_counts = collections.Counter(name)

# Create a list of labels and values for the pie chart
start_labels = list(start_counts.keys())
start_values = list(start_counts.values())
name_labels = list(name_counts.keys())
name_values = list(name_counts.values())

# Create the pie chart
fig = go.Figure(data=[go.Pie(labels=name_labels, values=start_values)])

# Set the chart title
fig.update_layout(title_text='Offer Starting')

# Show the chart
fig.show()