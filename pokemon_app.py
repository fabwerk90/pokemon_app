# import necessary libraries
import streamlit as st
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.themes import built_in_themes
from bokeh.io import curdoc


def update_dataframe(old_df, slider_values, type_selection, generation_selection, text_input):

    # unpack all slider values
    hp_value = slider_values["hp_value"]
    overall_value = slider_values["overall_value"]

    # build filters from slider values
    hp_filter = f"{hp_value[0]} <= HP <= {hp_value[1]}"
    overall_filter = f"{overall_value[0]} <= Total <= {overall_value[1]}"

    # update on attack and defense slider
    slider_updated_df = old_df.query(f"{hp_filter} & {overall_filter}")

    # update on main type
    type_updated_df = slider_updated_df[slider_updated_df["Type 1"].isin(type_selection)]

    # update on pokémon generation
    gen1 = generation_selection["gen1"]
    gen2 = generation_selection["gen2"]

    gen1_filter = "Generation == 1"
    gen2_filter = "Generation == 2"
    both_gen_filter = "1 <= Generation <= 2"

    if gen1 and gen2:
        generation_updated_df = type_updated_df.query(both_gen_filter)
    elif gen1:
        generation_updated_df = type_updated_df.query(gen1_filter)
    else:
        generation_updated_df = type_updated_df.query(gen2_filter)

    # filter on specific Pokémon and pass final dataframe for creating the updated data source
    generation_updated_df['Name'] = generation_updated_df['Name'].str.lower()
    if text_input:
        clean_string = text_input.strip()
        text_filtered_df = generation_updated_df[generation_updated_df['Name'].str.contains(clean_string)]
        final_df = text_filtered_df
    else:
        final_df = generation_updated_df


    datasource = ColumnDataSource(
    data={
        "name": final_df["Name"].str.capitalize(),
        "main_type": final_df["Type 1"],
        "overall": final_df["Total"],
        "health": final_df["HP"],
        "attack": final_df["Attack"],
        "defense": final_df["Defense"],
        "speed": final_df["Speed"],
        "imgs": final_df["image_urls"],
        }
    )
    return datasource


def draw_plot(datasource):
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
        x_range=[0,150],
        y_range=[0,250],
        x_minor_ticks=50,
        width=700,
        height=600,
        tooltips=TOOLTIPS,
        tools=TOOLBOX,
        toolbar_location="below",
    )

    plot.circle("attack",
                "defense",
                size=10,
                fill_color='white',
                line_color="cornflowerblue",
                source=datasource)

    return plot

# set path, where raw data is located and create dataframe with it
DATA_PATH = "data/pokemon_250_stats_and_imageurls.csv"
df = pd.read_csv(DATA_PATH)

# write header for app
st.header("Pokémon Dashboard")

# build sliders for attack, defense, HP and overall strength value intervals
hp = st.sidebar.slider("Select Life Points Range", 0, 260, (0, 260))
overall = st.sidebar.slider("Select Overall Strength Range", 0, 700, (0, 700))

slider_values = {"hp_value": hp,
                 "overall_value": overall}


# build multi-select for all Pokémon Types
all_main_types = df["Type 1"].unique()
type_selection = st.sidebar.multiselect("Select Main Type(s)",
                                        options=all_main_types,
                                        default=all_main_types)

# build checkboxes for selection based on Pokémin generation
gen1 = st.sidebar.checkbox("Generation 1 Pokémon", value=True)
gen2 = st.sidebar.checkbox("Generation 2 Pokémon", value=True)

generation_selection = {"gen1": gen1,
                        "gen2": gen2}

# build textbox for individual Pokémon search
text_input = st.sidebar.text_input("Search for specific Pokémon")

# update datasource and draw plot with it
updated_datasource = update_dataframe(df,
                                      slider_values,
                                      type_selection,
                                      generation_selection,
                                      text_input)

plot = draw_plot(updated_datasource)

# add dark theme
doc = curdoc()
doc.theme = "dark_minimal"
doc.add_root(plot)

st.bokeh_chart(plot)
