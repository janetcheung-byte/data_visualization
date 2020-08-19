# initial imports

from dotenv import load_dotenv
load_dotenv()
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
import os
import pandas as pd
import matplotlib.pyplot as plt
import hvplot.pandas
import panel as pn
import plotly.express as px
from pathlib import Path


# Initialize the Panel Extensions (for Plotly)
pn.extension('plotly')
# Read the Mapbox API key
mapbox= os.getenv('mapbox_token')


# Import the CSVs to Pandas DataFrames
file_path = Path("Data/sfo_neighborhoods_census_data.csv")
df = pd.read_csv(file_path, infer_datetime_format=True, parse_dates=True, index_col="year").dropna()

file_path = Path("Data/neighborhoods_coordinates.csv")
df_neighborhood_locations = pd.read_csv(file_path)

df.head()
df_neighborhood_locations.head()
# Define Panel Visualization Functions
def housing_units_per_year():
    """Housing Units Per Year."""
    
    # YOUR CODE HERE!
    housing_units = df["housing_units"].groupby([df.index.year]).mean().reset_index()
    housing_units.columns=["Year","Housing Units"]
    min = housing_units.min()['Housing Units']
    max = housing_units.max()['Housing Units']
    padding = 5000
    housing_unit=housing_units.hvplot.bar(x='Year',ylim=(min-padding,max+padding),
                                         title="Housing Units in SanFran from 2010 to 2016", 
                                         rot=90).opts(yformatter="%.0f")
    return housing_unit

def average_gross_rent():
    """Average Gross Rent in San Francisco Per Year."""
    
    # YOUR CODE HERE!
    average_sale_price_sqr_foot = df["sale_price_sqr_foot"].groupby([df.index.year]).mean()
    average_gross_rent = df["gross_rent"].groupby([df.index.year]).mean()

    average_grossrent_saleprice = (
    pd.concat([average_sale_price_sqr_foot, average_gross_rent], axis=1).dropna().reset_index()
    )
    avg_grossrent_plot=average_grossrent_saleprice.hvplot( x='year', y='gross_rent', title="Average Gross Rent in San Francisco")

    return avg_grossrent_plot


def average_sales_price():
    """Average Sales Price Per Year."""
    
    # YOUR CODE HERE!
    average_sale_price_sqr_foot = df["sale_price_sqr_foot"].groupby([df.index.year]).mean()
    average_gross_rent = df["gross_rent"].groupby([df.index.year]).mean()

    average_grossrent_saleprice = (
    pd.concat([average_sale_price_sqr_foot, average_gross_rent], axis=1).dropna().reset_index()
    )
    avg_salesprice=average_grossrent_saleprice.hvplot(x='year', y='sale_price_sqr_foot', title="Average Sales Price per Square Foot in San Francisco")

    return avg_salesprice


def average_price_by_neighborhood():
    """Average Prices by Neighborhood."""
    
    # YOUR CODE HERE!
    average_price_neighborhood = df["sale_price_sqr_foot"].groupby([df['neighborhood'],df.index.year]).mean()

    average_price_neighborhood.to_frame()
    avg_price_neighborhood=average_price_neighborhood.hvplot(x='year',groupby='neighborhood')
    return avg_price_neighborhood


def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""
    
    # YOUR CODE HERE!
    top10 = df["sale_price_sqr_foot"].groupby([df['neighborhood']]).mean()
    top10=top10.sort_values(ascending=False).head(10)
    top10.to_frame()
    top10_plot=top10.hvplot.bar(rot=90,ylabel= "Avg Sale Price per Square Foot", title="Top expensive neighborhoods in SFO")
    return top10_plot


def parallel_coordinates():
    """Parallel Coordinates Plot."""
    
    # YOUR CODE HERE!
    avg= df.groupby([df['neighborhood']]).mean()
    parallel_plot=px.parallel_coordinates(avg, color='sale_price_sqr_foot')
    return parallel_plot
    
def parallel_categories():
    """Parallel Categories Plot."""
    
    # YOUR CODE HERE!
    avg= df.groupby([df['neighborhood']]).mean()
    avg2=avg.sort_values(by='sale_price_sqr_foot', ascending=False).head(10)
    parallel_cat=px.parallel_categories(avg2.reset_index().round(1),
                                  dimensions=['neighborhood','sale_price_sqr_foot', 'housing_units', 'gross_rent'],
                                  color="sale_price_sqr_foot",
                                  color_continuous_scale=px.colors.sequential.Inferno)
    return parallel_cat


def neighborhood_map():
    """Neighborhood Map"""
    
    # YOUR CODE HERE!
    file_path = Path("Data/neighborhoods_coordinates.csv")
    df_neighborhood_locations = pd.read_csv(file_path)
    df_neighborhood_locations.set_index('Neighborhood', inplace=True)
    df_neighborhood_locations.index.names = ['neighborhood']
    avg= df.groupby([df['neighborhood']]).mean()
    combined = pd.concat([df_neighborhood_locations,avg], axis="columns", join="inner")
    mapbox= os.getenv('mapbox_token')
    px.set_mapbox_access_token(mapbox)
    
    map_plot=px.scatter_mapbox(combined,
                             lat="Lat",
                             lon="Lon",
                             size="sale_price_sqr_foot",
                             color="gross_rent",
                             color_continuous_scale=px.colors.cyclical.mrybm,
                             zoom=10)
    return map_plot

    # YOUR CODE HERE!

welcome = pn.Column(
    "### Janet Cheung's Dashboard",
    "### This dashboard presents a visual analysis of historical prices of house units, sale price per square foot and gross rent in San Francisco, California from 2010 to 2016. You can navigate through the tabs above to explore more details about the evolution of the real estate market on The Golden City across these years",
    neighborhood_map())


yearly = pn.Column(
    "## Yearly Data",
    housing_units_per_year(), average_gross_rent(), average_sales_price())

parallel_plot = pn.Column(
    "## Parallel Plot Analysis",
    parallel_coordinates(),
    parallel_categories())


neighbor = pn.Column(
    "## Neighborhood",
    average_price_by_neighborhood(),
    top_most_expensive_neighborhoods()
)

panel = pn.Tabs(
    ("Welcome", welcome),
    ("Yearly Market Analysis", yearly),
    ("Neighborhood Analysis", neighbor),
    ("Parallel Plot Analysis", parallel_plot)
    
)

panel

panel.servable()