## Project Description

This is a simple weather forecast project. It comprises two functions: the first of which takes a city name as input and produces a weather forecast. The second function takes a country name as input and generates forecasts for the five largest cities. Results are displayed in categorical graphs.


### Aim: 

- Data extraction from the web and importation into SQL.
- Learning to connect PostgreSQL database with Python to establish an API.
- Familiarization with Python libraries such as numpy, pandas, matplotlib and psycopg2.

### Files:

1. `worldcities.csv`: A dataset containing columns such as city name, latitude, longitude, country name, and population.
2. `weather_project2.sql`: A script that creates a database named `cities_api` and imports the data to the Postgres server.
3. Python code first establishes connections with the OpenMeteo API and the `cities_api` database. 
    - **`city_name(var)`**: Searches for the 'city' variable in the database using an SQL query. If not found, it prints a misspelling error. If found, it retrieves necessary data from the PostgreSQL server, passes it to the OpenMeteo API as a Python object, and prints the 7-day forecast of the city in a pandas DataFrame.
   - **`country_name(var)` Function**: Selects the five highest populated cities in the input country from the SQL database, saves the data as a Python object, and passes it to the OpenMeteo API to display and print the 7-day weather forecast.
   
   The final code draws a bar graph of the 7-day maximum and minimum temperature forecasts of the largest five cities.

### Results:

- `city_name('Isstanbul')` and `city_name('Istanbul')`
- `country_name('Austria')`
- `country_name('Germany')`
- `country_name('Netherlands')`
