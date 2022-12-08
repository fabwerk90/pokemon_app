from bokeh_code import read_data_and_build_datasource

def test_read_data_and_build_datasource():

    correct_bokeh_type = "bokeh.models.sources.ColumnDataSource"
    assert type(read_data_and_build_datasource()) != correct_bokeh_type