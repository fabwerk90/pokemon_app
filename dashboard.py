# import necessary libraries
import streamlit as st
import pandas as pd
from bokeh.themes import built_in_themes
from bokeh.io import curdoc

from dashboard_functions import update_dataframe, draw_plot


# set path, where raw data is located and create dataframe with it
DATA_PATH = "data/pokemon_250_stats_and_imageurls.csv"
df = pd.read_csv(DATA_PATH)

# write header for app
st.header("Pokémon Dashboard")

# build checkboxes for selection based on Pokémin generation
st.sidebar.header("Select Pokémon generation(s)")

gen1 = st.sidebar.checkbox("Generation 1 Pokémon", value=True)
gen2 = st.sidebar.checkbox("Generation 2 Pokémon", value=True)

generation_selection = {"gen1": gen1,
                        "gen2": gen2}

# build textbox for individual Pokémon search
st.sidebar.header("Search for specific Pokémon")

text_input = st.sidebar.text_input("Search by full name or substring")

# build multi-select for all Pokémon Types
st.sidebar.header("Select main type(s)")

all_main_types = df["Type 1"].unique()
type_selection = st.sidebar.multiselect("Select one or multiple",
                                        options=all_main_types,
                                        default=["Grass", "Fire", "Water"])

# build sliders for attack, defense, HP and overall strength value intervals
st.sidebar.header("Overall Strength Range")

overall = st.sidebar.slider("Select Interval", 0, 700, (0, 700))

slider_values = {"overall_value": overall}


# update datasource and draw plot with it
updated_datasource = update_dataframe(df,
                                      generation_selection,
                                      text_input,
                                      type_selection,
                                      slider_values
                                      )

plot = draw_plot(updated_datasource)

# add dark theme
doc = curdoc()
doc.theme = "dark_minimal"
doc.add_root(plot)

st.bokeh_chart(plot)
