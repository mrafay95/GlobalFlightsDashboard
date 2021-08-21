import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def cleandata(dataset, seriesCode):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data for the top 10 economies and data series of the seriesCode
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file
        seriesCode (str):  code of the data series e.g IS.AIR.DPRT

    Returns:
        df_melt (dataframe): cleaned data frame

    """    
    
    df = pd.read_csv(dataset)
    df = df[['Series Code', 'Country Name', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']]
    
    df = df[df['Series Code'] == seriesCode]

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']
    df = df[df['Country Name'].isin(top10country)]

    # melt year columns  and convert year to date time
    df_melt = df.melt(id_vars='Country Name', value_vars = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'])
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots Air transport, registered carrier departures worldwide from 2005 to 2015 in top 10 economies 
    # as a line chart
    
    
    graph_one = [] 
    df = cleandata('data/global_flights_data.csv', 'IS.AIR.DPRT')
    countrylist = df.country.unique().tolist()
    
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].variable.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Air transport, registered carrier departures worldwide',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Registered Carrier Departures Worldwide'),
                )

# second chart plots Air transport, freight (million ton-km) for 2005 to 2015 as a line chart    
    graph_two = []
    df = cleandata('data/global_flights_data.csv', 'IS.AIR.GOOD.MT.K1')
    countrylist = df.country.unique().tolist()
    
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].variable.tolist()
      graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_two = dict(title = 'Air transport, freight (million ton-km)',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Freight (million ton-km)'),
                )


# third chart plots Air transport, passengers carried from 2005 to 2015
    graph_three = []
    df = cleandata('data/global_flights_data.csv', 'IS.AIR.PSGR')
    countrylist = df.country.unique().tolist()
    
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].variable.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_three = dict(title = 'Air transport, passengers carried',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Passengers carried')
                       )
    
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures