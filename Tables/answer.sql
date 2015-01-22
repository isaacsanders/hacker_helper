CREATE TABLE 'Answer' (
  hacker_id integer,
  question_id integer,
  answer text NOT NULL,

  PRIMARY KEY (hacker_id, question_id),
  FOREIGN KEY (hacker_id) REFERENCES hackers(id)
  FOREIGN KEY (question_id) REFERENCES questions(id)
);
