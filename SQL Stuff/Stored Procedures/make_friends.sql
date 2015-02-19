CREATE OR REPLACE FUNCTION make_friends( _p1 INT, _p2 INT )
  RETURNS INTEGER AS
  $RETVAL$
  DECLARE
    retval INTEGER;
  BEGIN
    IF NOT exists (SELECT *
                   FROM friendship
                   WHERE (first_hacker_id = _p1 AND second_hacker_id = _p2)
                   UNION SELECT *
                         FROM friendship
                         WHERE (first_hacker_id = _p2 AND second_hacker_id = _p1))
    THEN
      INSERT INTO friendship (first_hacker_id, second_hacker_id)
      VALUES (_p1, _p2);
      retval = 0;
    ELSE
      retval = 1;
    END IF;

    RETURN retval;
  END
  $RETVAL$
LANGUAGE plpgsql VOLATILE
COST 100;