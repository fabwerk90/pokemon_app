# import necessary libraries
import streamlit as st
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import TextInput
from bokeh.models.widgets import RangeSlider, RadioButtonGroup, CheckboxGroup

# read in pokemon stats
pokemon_df = pd.read_csv("data/pokemon_250_stats_and_imageurls.csv")

# define a datasource, which bokeh can use to create a plot
datasource = ColumnDataSource(
    data={
        "name": pokemon_df["Name"],
        "main_type": pokemon_df["Type 1"],
        "overall": pokemon_df["Total"],
        "health": pokemon_df["HP"],
        "attack": pokemon_df["Attack"],
        "defense": pokemon_df["Defense"],
        "speed": pokemon_df["Speed"],
        "imgs": pokemon_df["image_urls"],
    }
)

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

# define toolbox, which will be available to navigate the plot
toolbox = ["pan,wheel_zoom,box_zoom,reset,save,crosshair"]

# build the plot canvas
plot = figure(
    x_axis_label="Attack",
    y_axis_label="Defense",
    plot_width=800,
    plot_height=800,
    tooltips=TOOLTIPS,
    tools=toolbox,
    toolbar_location="below",
)

# draw points onto the plot
plot.circle("attack", "defense", size=10, source=datasource)

# build navigation elements
hp_slider = RangeSlider(start = 10, end = 255, step = 1, value = (10,255), title = 'Pokemon Health')

overall_slider = RangeSlider(start = 180, end = 680, step = 1, value = (180,680), title = 'Pokemon Overall Strength')

main_types = pokemon_df["Type 1"].unique().tolist()
types_checkbox = CheckboxGroup(labels=main_types, active = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

pokemon_textbox = TextInput(title="Name or substring of Pokemon")

datasource_choice = RadioButtonGroup(labels=["Generation 1", "Generation 2", "Generation 1 & 2"], active=2)

### build two functions to structure plot-updates
# one which select the new data source based on user input ("select_df()")
# and one which updates the plot ("update_plot()")

# function 1 - build new dataframe, based on user input and return this dataframe
def select_df():

    lower_boundary_hp = hp_slider.value[0]
    upper_boundary_hp = hp_slider.value[1]

    lower_boundary_overall = overall_slider.value[0]
    upper_boundary_overall = overall_slider.value[1]

    selected_types = [types_checkbox.labels[i] for i in types_checkbox.active]

    textbox_input = pokemon_textbox.value.strip()

    datasource_selection = datasource_choice.active

    if datasource_selection == 0:

        new_df = pokemon_df[
            (pokemon_df["HP"] >= lower_boundary_hp) &
            (pokemon_df["HP"] <= upper_boundary_hp) &
            (pokemon_df["Total"] >= lower_boundary_overall) &
            (pokemon_df["Total"] <= upper_boundary_overall) &
            (pokemon_df["Type 1"].isin(selected_types)) &
            (pokemon_df["Name"].str.contains(textbox_input)) &
            (pokemon_df["Generation"]==1)
        ]

    elif datasource_selection == 1:

        new_df = pokemon_df[
            (pokemon_df["HP"] >= lower_boundary_hp) &
            (pokemon_df["HP"] <= upper_boundary_hp) &
            (pokemon_df["Total"] >= lower_boundary_overall) &
            (pokemon_df["Total"] <= upper_boundary_overall) &
            (pokemon_df["Type 1"].isin(selected_types)) &
            (pokemon_df["Name"].str.contains(textbox_input)) &
            (pokemon_df["Generation"]==2)
        ]

    else:

        new_df = pokemon_df[
            (pokemon_df["HP"] >= lower_boundary_hp) &
            (pokemon_df["HP"] <= upper_boundary_hp) &
            (pokemon_df["Total"] >= lower_boundary_overall) &
            (pokemon_df["Total"] <= upper_boundary_overall) &
            (pokemon_df["Type 1"].isin(selected_types)) &
            (pokemon_df["Name"].str.contains(textbox_input))
        ]

    return new_df

### execute function for new dataframe and then update the plot with it
def update_plot():

    df = select_df()

    datasource.data = dict(
        name = df["Name"],
        main_type = df["Type 1"],
        overall = df["Total"],
        health = df["HP"],
        attack = df["Attack"],
        defense = df["Defense"],
        speed = df["Speed"],
        imgs = df["image_urls"]
    )

# when user gives input to widgets, simultaneously execute updating function for all widgets
# we have to do this separately for widgets, which rely on value input and which rely on activation input
value_changes = [hp_slider, overall_slider, pokemon_textbox]
for change in value_changes:
    change.on_change('value', lambda attr, old, new: update_plot())

active_changes = [types_checkbox, datasource_choice]
for change in active_changes:
    change.on_change('active', lambda attr, old, new: update_plot())

# add all widgets and the plot to layout
layout = row(column(datasource_choice, hp_slider, overall_slider, types_checkbox, pokemon_textbox), plot)
curdoc().add_root(layout)
