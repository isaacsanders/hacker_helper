CREATE TABLE hacker
(
    id SERIAL DEFAULT nextval('table_name_id_seq'::regclass) NOT NULL,
    email VARCHAR(30) DEFAULT NULL NOT NULL,
    location VARCHAR(30) DEFAULT NULL,
    fb_oauth_access_token VARCHAR(60) DEFAULT NULL NOT NULL,
    name VARCHAR(255) NOT NULL
);
