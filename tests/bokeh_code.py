import pandas as pd
from bokeh.models import ColumnDataSource

def read_data_and_build_datasource():

    test_pokemon_dict = {
        'Name': ["PokemonA", "PokemonB"],
        'Type 1': ["TypeA", "TypeB"],
        'Total': [50, 100],
        'HP': [50, 100],
        'Attack': [50, 100],
        'Defense': [50, 100],
        'Speed': [50, 100],
        'image_urls': ["URLA", "URLB"]
         }

    df = pd.DataFrame(data=test_pokemon_dict)

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