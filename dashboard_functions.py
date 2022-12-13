import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

def update_dataframe(old_df, generation_selection, text_input, type_selection, slider_values):

    # unpack gen-selection values and update on pokémon generation
    gen1 = generation_selection["gen1"]
    gen2 = generation_selection["gen2"]

    gen1_filter = "Generation == 1"
    gen2_filter = "Generation == 2"
    both_gen_filter = "1 <= Generation <= 2"

    if gen1 and gen2:
        generation_updated_df = old_df.query(both_gen_filter)
    elif gen1:
        generation_updated_df = old_df.query(gen1_filter)
    else:
        generation_updated_df = old_df.query(gen2_filter)

    # filter on specific Pokémon
    generation_updated_df['Name'] = generation_updated_df['Name'].str.lower()
    if text_input:
        clean_string = text_input.strip()
        text_filtered_df = generation_updated_df[generation_updated_df['Name'].str.contains(clean_string)]
    else:
        text_filtered_df = generation_updated_df

    # update on main type
    type_updated_df = text_filtered_df[text_filtered_df["Type 1"].isin(type_selection)]

    # unpack all slider values, build filters from it and update on hp and overall values
    overall_value = slider_values["overall_value"]

    overall_filter = f"{overall_value[0]} <= Total <= {overall_value[1]}"

    slider_updated_df = type_updated_df.query(overall_filter)

    # pass final dataframe for creating the updated data source

    final_df = slider_updated_df

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