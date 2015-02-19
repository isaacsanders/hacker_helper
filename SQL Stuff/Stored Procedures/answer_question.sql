DROP FUNCTION answer_question( INTEGER, INTEGER, VARCHAR );
CREATE OR REPLACE FUNCTION answer_question( _hacker_id INTEGER, _question_id INTEGER, _answer TEXT )
  RETURNS INTEGER AS
  $$
  --DECLARE
  --  _team_id INTEGER;
  BEGIN

    IF NOT exists (SELECT *
                   FROM hacker H
                   WHERE H.id = _hacker_id)
       OR NOT exists (SELECT *
                      FROM question Q
                      WHERE Q.id = _question_id)
    THEN
      RETURN 1;
    END IF;

    IF exists (SELECT *
               FROM answer A
               WHERE A.hacker_id = _hacker_id AND A.question_id = _question_id)
    THEN
      DELETE FROM answer
      WHERE answer.hacker_id = _hacker_id AND answer.question_id = _question_id;
    END IF;

    INSERT INTO answer (hacker_id, question_id, answer) VALUES (_hacker_id, _question_id, _answer);

    RETURN 0;
  END
  $$
LANGUAGE plpgsql VOLATILE;

SELECT *
FROM answer_question (5, 6, 'I DONT HAVE A LINKEDIN SUCKERS2')