CREATE TABLE 'hackathon' (
	id serial PRIMARY KEY
	name varchar(255) NOT NULL
	logo_url varchar(255) NOT NULL 
	cover_image_url varchar(255) NOT NULL
	location varchar(255) NOT NULL
	start_date data NOT NULL
	end_date data NOT NULL
	instruction_path varchar(255) NOT NULL
);