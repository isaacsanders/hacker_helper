CREATE TABLE hackathon
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    logo_url VARCHAR(255) NOT NULL,
    cover_image_url VARCHAR(255) NOT NULL,
    location int NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    instruction_path VARCHAR(255) NOT NULL
);
