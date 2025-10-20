from datetime import date

import matplotlib.pyplot as plt
import requests
import json


def get_data():
   # """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    data = response.json()
    return data

def get_year(earthquake):
    # """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    # """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


    # This is function you may want to create to break down the computations,
    # although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    #"""Retrieve the magnitudes of all the earthquakes in a given year.
    #Returns a dictionary with years as keys, and lists of magnitudes as values.
    magnitudes_per_year = {}
    for quake in earthquakes:
        year = get_year(quake)
        magnitude = get_magnitude(quake)
        if magnitude is None:
            continue
        magnitudes_per_year.setdefault(year, []).append(magnitude)

    return magnitudes_per_year
    



def plot_average_magnitude_per_year(earthquakes):
    """Plot number of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    counts = [len(magnitudes_per_year[y]) for y in years]

    plt.figure(figsize=(10, 5))
    plt.bar(years, counts, color="skyblue", edgecolor="black")
    plt.title("Number of Earthquakes per Year (2000–2018)")
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


def plot_number_per_year(earthquakes):
    """Plot average magnitude per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    avg_mags = [sum(magnitudes_per_year[y]) / len(magnitudes_per_year[y]) for y in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, avg_mags, marker="o", color="orange", linewidth=2)
    plt.title("Average Earthquake Magnitude per Year (2000–2018)")
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)