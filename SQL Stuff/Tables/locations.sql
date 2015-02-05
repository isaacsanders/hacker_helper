CREATE TABLE locations
(
    location_id SERIAL PRIMARY KEY NOT NULL,
    state VARCHAR(30) NOT NULL,
    city VARCHAR(30) NOT NULL,
    zipcode INT NOT NULL,
    country VARCHAR(30) NOT NULL,
    route VARCHAR(30) DEFAULT NULL,
    street_number INT
);
