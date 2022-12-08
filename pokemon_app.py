# import necessary libraries
import streamlit as st
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.themes import built_in_themes
from bokeh.io import curdoc

# set path, where raw data is located
DATA_PATH = "data/pokemon_250_stats_and_imageurls.csv"


def read_data_and_build_datasource(data_path):
    df = pd.read_csv(data_path)

    datasource = ColumnDataSource(
        data={
            "name": df["Name"],
            "main_type": df["Type 1"],
            "overall": df["Total"],
            "health": df["HP"],
            "attack": df["Attack"],
            "defense": df["Defense"],
            "speed": df["Speed"],
            "imgs": df["image_urls"],
        }
    )

    return datasource


def build_bokeh_plot():

    datasource = read_data_and_build_datasource(DATA_PATH)

    # define toolbox, which will be available to navigate the plot
    TOOLBOX = ["pan,wheel_zoom,box_zoom,reset,save,crosshair"]

    # html code to access pokemon images
    TOOLTIPS = """
    <div>
        <div>
            <img
                src="@imgs" height="100" alt="@imgs" width="100"
                border="2"
            ></img>
        </div>
        <div>
                <span style="font-size: 18px; font-weight: bold;">@name</span>
        </div>
        <div>
                <span style="font-size: 14px;">Overall Strength - @overall</span>
        </div>
        <div>
                <span style="font-size: 14px;">Overall Health Points - @health</span>
        </div>
    """

    # build the plot canvas
    plot = figure(
        x_axis_label="Attack",
        y_axis_label="Defense",
        x_range=[0,140],
        y_range=[0,250],
        x_minor_ticks=50,
        width=800,
        height=800,
        tooltips=TOOLTIPS,
        tools=TOOLBOX,
        toolbar_location="below",
    )

    # draw points onto the plot
    plot.circle("attack",
                "defense",
                size=10,
                fill_color='white',
                line_color="cornflowerblue",
                source=datasource)

    # add dark theme
    doc = curdoc()
    doc.theme = "dark_minimal"
    doc.add_root(plot)

    return plot


### build streamlit layout
# start with header
st.header("Pokémon Dashboard")

st.bokeh_chart(build_bokeh_plot())
