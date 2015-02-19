DROP FUNCTION  get_questions_for_hackathon(INTEGER, INTEGER);

CREATE OR REPLACE FUNCTION get_questions_for_hackathon( _hacker_id INTEGER, _hackathon_id INTEGER )
  RETURNS TABLE(question_id INTEGER, question TEXT, answer TEXT) AS
  $$
  BEGIN
    IF NOT exists (SELECT *
                   FROM hacker
                   WHERE hacker.id = _hacker_id)
       OR NOT exists (SELECT *
                      FROM hackathon
                      WHERE hackathon.id = _hackathon_id)
    THEN RETURN;
    END IF;

    RETURN QUERY (
      SELECT questions.question_id
        , questions.question
        , answer.answer
      FROM
        (
          SELECT question.question
            , question.id AS question_id
          FROM question, hackathon_has_questions
          WHERE question.id = hackathon_has_questions.question_id
                AND hackathon_has_questions.hackathon_id = _hackathon_id) AS questions LEFT JOIN answer
          ON questions.question_id = answer.question_id
      WHERE answer.hacker_id = _hacker_id OR answer.hacker_id IS NULL);
  END
  $$
LANGUAGE plpgsql VOLATILE;


select * from get_questions_for_hackathon(5, 75);