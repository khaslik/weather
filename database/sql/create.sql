CREATE TABLE raw_weather(
	id INT PRIMARY KEY,
	city VARCHAR(50),
	temperature FLOAT,
	humidity INT,
	pressure INT,
	wind_speed FLOAT,
	timestamp TIMESTAMP,
	load_dt TIMESTAMP DEFAULT NOW()
);