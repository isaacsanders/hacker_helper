CREATE OR REPLACE FUNCTION add_friends( _friender VARCHAR(30), _friendee VARCHAR(30) )
  RETURNS INTEGER AS
  $RETVAL$
  DECLARE
    retval      INTEGER;
    friender_id INT;
    friendee_id INT;
  BEGIN
    friender_id := (
      SELECT id
      FROM hacker
      WHERE hacker.email = _friender);

    friendee_id := (
      SELECT id
      FROM hacker
      WHERE hacker.email = _friendee);

    IF NOT exists (SELECT *
                   FROM friendship
                   WHERE (first_hacker_id = friender_id AND second_hacker_id = friendee_id)
                   UNION SELECT *
                         FROM friendship
                         WHERE (first_hacker_id = friendee_id AND second_hacker_id = friender_id))
    THEN
      INSERT INTO friendship (first_hacker_id, second_hacker_id)
      VALUES (friender_id, friendee_id);
      retval := 0;
    ELSE
      retval := 1;
    END IF;

    RETURN retval;
  END
  $RETVAL$
LANGUAGE plpgsql VOLATILE;

select * from add_friends('dax.earl@gmail.com', 'isaac@isaacbfsanders.com');