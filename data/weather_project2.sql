-- Import the data and clean/update

-- Note: This data is neither complete nor up to date. 


CREATE DATABASE cities_api;
\c cities_api

CREATE TABLE cities_table (
city VARCHAR,
city_ascii VARCHAR,
lat NUMERIC,
lng NUMERIC,
country VARCHAR,
iso2 VARCHAR,
iso3 VARCHAR,
admin_name VARCHAR,
capital VARCHAR,
population NUMERIC,
id INTEGER
);

SET CLIENT_ENCODING TO 'utf8';
--Import the csv file

\COPY cities_table FROM '\\path\worldcities.csv' DELIMITER ',' csv header;

--Drop unnecessary columns
ALTER TABLE cities_table DROP COLUMN capital;
ALTER TABLE cities_table DROP COLUMN id;

--A small update on the database so that Tilburg is not the highest populated city in the Netherlands :)

UPDATE cities_table SET population=211648 WHERE city='Tilburg';
