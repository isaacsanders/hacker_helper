CREATE OR REPLACE FUNCTION make_friends(_p1 INT, _p2 INT)
  RETURNS INTEGER AS
$RETVAL$
declare
    retval integer;
begin
  if not exists(select * from friendship where (first_hacker_id = _p1 and second_hacker_id = _p2) union select * from friendship where (first_hacker_id = _p2 and second_hacker_id = _p1))
    THEN
      INSERT INTO friendship (first_hacker_id, second_hacker_id)
      VALUES (_p1, _p2);
      retval = 0;
    ELSE
      retval = 1;
  END IF;

  return retval;
end
$RETVAL$
LANGUAGE plpgsql VOLATILE
COST 100;