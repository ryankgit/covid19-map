# Gathers updated Covid-19 data and displays it at the county level
#
# Covid-19 data gathered from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
import pandas as pd
import json
import plotly.express as px
from urllib.request import urlopen
from datetime import date, timedelta


def main():
    county_choropleth_map()


def get_previous_date():
    # get yesterdays date to insure data exists
    prev_date = date.today() - timedelta(days=1)
    prev_date = prev_date.strftime("%m/%d/%y")

    # remove leading zero from day
    if prev_date[3] == '0':
        prev_date = prev_date[:3] + prev_date[4:]
        print(prev_date)
    # remove leading zero from month
    prev_date = prev_date.lstrip('0')

    return prev_date


def get_county_covid_data(prev_date):
    # read yesterday's Covid-19 data
    data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
                       'csse_covid_19_time_series/time_series_covid19_deaths_US.csv',
                       dtype={'FIPS': str},
                       usecols=[
                           'FIPS',
                           'Admin2',
                           'Province_State',
                           prev_date])
    # remove '.0' from FIPS
    data['FIPS'] = data['FIPS'].str[:-2]
    # combine county and state for figure label
    data['Admin2'] = data.Admin2 + ' Country, ' + data.Province_State
    return data


def get_us_counties():
    # get US counties geojson
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        return json.load(response)


def county_choropleth_map():
    prev_date = get_previous_date()
    covid_data = get_county_covid_data(prev_date)
    map_title = 'Total Covid-19 Deaths by US County as of ' + prev_date

    # create choropleth figure
    fig = px.choropleth(
        covid_data,
        # title=map_title,    # TODO: fix map title (displays behind fig)
        geojson=get_us_counties(),
        locations='FIPS',
        color=prev_date,
        color_continuous_scale='reds',
        range_color=(0, max(covid_data[prev_date])),
        # scope='usa',
        hover_name='Admin2',
        labels={
            prev_date: 'Deaths'
        }
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


if __name__ == '__main__':
    main()
