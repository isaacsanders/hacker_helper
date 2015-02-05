CREATE TABLE friendship
(
    first_hacker_id INT NOT NULL,
    second_hacker_id INT NOT NULL,
    FOREIGN KEY (first_hacker_id) REFERENCES hacker (id),
    FOREIGN KEY (second_hacker_id) REFERENCES hacker (id)
);
