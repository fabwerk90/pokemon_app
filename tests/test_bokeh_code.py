import pytest
import bokeh_code

def test_read_data_and_build_datasource():

    correct_bokeh_type = "bokeh.models.sources.ColumnDataSource"
    assert type(bokeh_code.read_data_and_build_datasource()) != correct_bokeh_type