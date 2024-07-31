'''import libraries:
openmeteo: weather API
requests: request Web APIs
pandas: data analysis library
psycop2: connect to SQL database
matplotlib: visualization
numpy: creates nice arrays and matrices'''
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
url = "https://api.open-meteo.com/v1/forecast"


#Connect to the cities_api database 
connection = psycopg2.connect(
    database = "cities_api",
    user = "postgres",
    password = "12345",
    host = "localhost",
    port = "5433"
)

def city_name(var):
    '''Enter a city name'''
    #open a connection to the SQL server to extract coordinates
    cursor = connection.cursor()
    cursor.execute("SELECT city, country, lat, lng, admin_name FROM cities_table WHERE city=%s", (var,))
    dataset = cursor.fetchall()
    connection.commit()
    if len(dataset)==0:
        return("city cannot be found. Did you spell the city name correctly?")
    #loop over cities that have the same name
    for a_tuple in dataset:
        params = {
	    "latitude": a_tuple[2],
	    "longitude": a_tuple[3],
	    "daily": ["temperature_2m_max", "temperature_2m_min"]}
        #openmeteo API for daily weather forecasts
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_data = {"date": pd.date_range(
		    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		    freq = pd.Timedelta(seconds = daily.Interval()),
		    inclusive = "left"
	    )}
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        #collect data as DataFrame 
        daily_dataframe = pd.DataFrame(data = daily_data)
        #get rid of time, only keep the date
        daily_dataframe["date"]=pd.to_datetime(daily_dataframe["date"]).dt.date
        print(a_tuple[0],a_tuple[1],a_tuple[4],f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(daily_dataframe)

dfl=[] #data frame list
cl=[] #city list
def country_name(var):
    """Enter a country name"""
    cursor=connection.cursor()
    #SQL query that returns the highest populated 5 cities together with their coordinates
    cursor.execute("SELECT city, lat, lng, population FROM cities_table WHERE country=%s ORDER BY COALESCE(population,0) DESC LIMIT 5", (var,))
    dataset=cursor.fetchall()
    connection.commit()
    if len(dataset)==0:
        return("country cannot be found. Did you spell the country name correctly?")
    
    print(dataset)
    for a_tuple in dataset:
        params = {
	    "latitude": a_tuple[1],
	    "longitude": a_tuple[2],
	    "daily": ["temperature_2m_max", "temperature_2m_min"]}
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_data = {"date": pd.date_range(
		    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		    freq = pd.Timedelta(seconds = daily.Interval()),
		    inclusive = "left"
	    )}
        daily_data["max"] = daily_temperature_2m_max
        daily_data["min"] = daily_temperature_2m_min
        daily_dataframe = pd.DataFrame(data = daily_data)
        daily_dataframe['date']=pd.to_datetime(daily_dataframe["date"]).dt.date
        print(a_tuple[0], a_tuple[3],f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(a_tuple)
        print(daily_dataframe)
        dfl.append(daily_dataframe)
        cl.append(a_tuple[0])
if __name__ == "__main__":    
    country_name('Austria')
    #bunch of colors' hex code
    colors_list=[
        "#fd7f6f", "#7eb0d5", "#b2e061",
        "#bd7ebe", "#ffb55a", "#ffee65",
        "#beb9db", "#fdcce5", "#8bd3c7"]
    r1 = np.arange(len(dfl[0]['date']))
    for i in range(0,len(dfl)):
        plt.bar(r1+i*0.1,dfl[i]['max'],color='#F5F3C8',width=0.1, edgecolor='white')
        plt.bar(r1+i*0.1,dfl[i]['min'],color=colors_list[i],width=0.1, edgecolor='white', label=cl[i]) # type: ignore

    plt.xlabel('date')
    plt.ylabel('temp: min - max')
    plt.title('weather')
    plt.xticks(r1, dfl[0]['date'])

    plt.legend()
    plt.show()
