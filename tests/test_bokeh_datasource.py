import pandas as pd
from bokeh.models import ColumnDataSource

DATA_PATH = "../data/pokemon_250_stats_and_imageurls.csv"

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

def test_read_data_and_build_datasource():
    correct_bokeh_type = "bokeh.models.sources.ColumnDataSource"
    assert type(read_data_and_build_datasource(DATA_PATH)) == correct_bokeh_type