# Gathers updated Covid-19 data and displays it at the state level
#
# Covid-19 data gathered from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
import pandas as pd
import json
import plotly.express as px
from urllib.request import urlopen
from datetime import date, timedelta


def main():
    state_choropleth_map()


def get_file():
    # get yesterdays date to insure data exists
    prev_date = date.today() - timedelta(days=1)
    return prev_date.strftime("%m-%d-%Y") + '.csv'


def get_state_covid_data():
    # read yesterday's Covid-19 data
    covid_data_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
                     'csse_covid_19_daily_reports_us/' + get_file()
    data = pd.read_csv(
        covid_data_url,
        dtype={
            'FIPS': str
        },
        usecols=[
            'Province_State',
            'FIPS',
            'Deaths'])

    # remove '.0' from FIPS
    data['FIPS'] = data['FIPS'].str[:-2]
    return data


def get_us_states():
    # get US states geojson
    with urlopen(
            'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
        return json.load(response)


def state_choropleth_map():
    data = get_state_covid_data()
    us_states = get_us_states()

    # create choropleth figure
    fig = px.choropleth(
        data,
        geojson=us_states,
        locations='FIPS',
        color='Deaths',
        color_continuous_scale="reds",
        range_color=(0, max(data['Deaths'])),
        scope="usa",
        hover_name='Province_State',
        labels={
            'Deaths': 'Deaths'
        }
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


if __name__ == '__main__':
    main()
