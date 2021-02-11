DROP DATABASE IF EXISTS used_cars;
CREATE DATABASE used_cars;
-- CREATE USER admin WITH password 'admin';
-- GRANT ALL privileges ON DATABASE used_cars TO postgres;
-- GRANT ALL privileges ON DATABASE used_cars TO admin;

Alter USER postgres with password '1234';

\c used_cars;

-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "admin";

CREATE TABLE Craigslist_region
(
	Id SERIAL PRIMARY KEY,
	Region VARCHAR(511),
	Region_url VARCHAR(511)
);

CREATE TABLE  Manufacturer
(
	Id SERIAL PRIMARY KEY,
	Manufacturer VARCHAR(511)
);

CREATE TABLE Model
(
	Id SERIAL PRIMARY KEY,
	Model VARCHAR(511)
);

CREATE TABLE Condition
(
	Id SERIAL PRIMARY KEY,
	Condition VARCHAR(511)
);

CREATE TABLE Fuel
(
	Id SERIAL PRIMARY KEY,
	Fuel VARCHAR(511)
);

CREATE TABLE Title_status
(
	Id SERIAL PRIMARY KEY,
	Title_status VARCHAR(511)
);

CREATE TABLE Transmission
(
	Id SERIAL PRIMARY KEY,
	Transmission VARCHAR(511)
);

CREATE TABLE Drive
(
	Id SERIAL PRIMARY KEY,
	Drive VARCHAR(511)
);

CREATE TABLE Sizes
(
	Id SERIAL PRIMARY KEY,
	Sizes VARCHAR(511)
);

CREATE TABLE Types
(
	Id SERIAL PRIMARY KEY,
	Types VARCHAR(511)
);

CREATE TABLE Paint_color
(
	Id SERIAL PRIMARY KEY,
	Paint_color VARCHAR(511)
);

CREATE TABLE Country
(
	Id SERIAL PRIMARY KEY,
	Country VARCHAR(511)
);

CREATE TABLE State
(
	Id SERIAL PRIMARY KEY,
	State VARCHAR(511)
);

CREATE TABLE Driver
(
	Id SERIAL PRIMARY KEY,
	Name VARCHAR(511),
	Login VARCHAR(511),
	Password VARCHAR(511)
);

CREATE TABLE General_characteristics
(
    Id SERIAL PRIMARY KEY,
	Manufacturer INTEGER REFERENCES Manufacturer (Id) ON DELETE SET NULL,
    Model INTEGER REFERENCES Model (Id) ON DELETE SET NULL,
	Cylinders VARCHAR(511),
    Types INTEGER REFERENCES Types (Id) ON DELETE SET NULL,
    Transmission INTEGER REFERENCES Transmission (Id) ON DELETE SET NULL,
    Fuel INTEGER REFERENCES Fuel (Id) ON DELETE SET NULL,
    Drive INTEGER REFERENCES Drive (Id) ON DELETE SET NULL,
    Sizes INTEGER REFERENCES Sizes (Id) ON DELETE SET NULL
);

CREATE TABLE Listing_location
(
    Id SERIAL PRIMARY KEY, 
	State INTEGER REFERENCES State (Id) ON DELETE SET NULL,
    Country INTEGER REFERENCES Country (Id) ON DELETE SET NULL,
    Longtitude VARCHAR(511),
	Latitude VARCHAR(511)
);

CREATE TABLE Used_car
(
    Id SERIAL PRIMARY KEY,
	Driver INTEGER REFERENCES Driver (Id) ON DELETE SET NULL,
    Url VARCHAR(511),
    Craigslist_region INTEGER REFERENCES Craigslist_region (Id) ON DELETE SET NULL,
    Price INTEGER,
    Year INTEGER,
    General_characteristics INTEGER REFERENCES General_characteristics (Id) ON DELETE SET NULL,
    Condition INTEGER REFERENCES Condition (Id) ON DELETE SET NULL,
    Odometer INTEGER,
    Title_status INTEGER REFERENCES Title_status (Id) ON DELETE SET NULL,
    VIN VARCHAR(511),
	Image_url VARCHAR(511),
    Paint_color INTEGER REFERENCES Paint_color (Id) ON DELETE SET NULL,
    Description VARCHAR(511),
	Listing_location INTEGER REFERENCES Listing_location (Id) ON DELETE SET NULL
);

\copy Driver FROM './driver.csv' DELIMITER ',' CSV HEADER;
\copy Craigslist_region FROM './region.csv' DELIMITER ',' CSV HEADER;
\copy Manufacturer FROM './manufacturer.csv' DELIMITER ',' CSV HEADER;
\copy Model FROM './model.csv' DELIMITER ',' CSV HEADER;
\copy Condition FROM './condition.csv' DELIMITER ',' CSV HEADER;
\copy Fuel FROM './fuel.csv' DELIMITER ',' CSV HEADER;
\copy Title_status FROM './title_status.csv' DELIMITER ',' CSV HEADER;
\copy Transmission FROM './transmission.csv' DELIMITER ',' CSV HEADER;
\copy Drive FROM './drive.csv' DELIMITER ',' CSV HEADER;
\copy Sizes FROM './size.csv' DELIMITER ',' CSV HEADER;
\copy Types FROM './type.csv' DELIMITER ',' CSV HEADER;
\copy Paint_color FROM './paint_color.csv' DELIMITER ',' CSV HEADER;
\copy Country FROM './country.csv' DELIMITER ',' CSV HEADER;
\copy State FROM './state.csv' DELIMITER ',' CSV HEADER;
\copy General_characteristics FROM './general_characteristics.csv' DELIMITER ',' CSV HEADER;
\copy Listing_location FROM './listing_location.csv' DELIMITER ',' CSV HEADER;
\copy Used_car FROM './used_car.csv' DELIMITER ',' CSV HEADER;
