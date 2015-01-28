CREATE TABLE answer
(
    hacker_id INT NOT NULL,
    question_id INT NOT NULL,
    answer VARCHAR NOT NULL,

    PRIMARY KEY (hacker_id, question_id),
    FOREIGN KEY (hacker_id) REFERENCES hacker (id),
    FOREIGN KEY (question_id) REFERENCES question (id)
);
