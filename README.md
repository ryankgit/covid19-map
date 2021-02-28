# covid19-map

Generates choropleth maps of total Covid-19 deaths at the county and state level using data gathered from the [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19).


# Dependencies
~~~
pip install pandas
pip install plotly
~~~

Install all dependencies at once with `pip install -r requirements.txt`

# Example Maps
**Example State Map:**

![Example state map](/example_maps/state_example.png)

_(based on 12/12/2020 data)_

**Example County Map:**

![Example county map](/example_maps/county_example.png)

_(based on 12/12/2020 data)_

# Future Work
* Find new data source that covers all US states
* Fix map title positioning
* Add base layer with state borders
