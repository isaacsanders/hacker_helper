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
      SELECT question.id AS question_id
        , question.question
        , answer.answer
FROM hackathon_has_questions
  JOIN question
  ON question.id = hackathon_has_questions.question_id
  LEFT JOIN answer
  ON answer.question_id = question.id
  AND (answer.hacker_id = _hacker_id
      OR answer.hacker_id IS NULL)
WHERE hackathon_has_questions.hackathon_id = _hackathon_id);
  END
  $$
LANGUAGE plpgsql VOLATILE;


select * from get_questions_for_hackathon(5, 75);