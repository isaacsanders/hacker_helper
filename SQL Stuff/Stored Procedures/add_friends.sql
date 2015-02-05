CREATE OR REPLACE FUNCTION add_friends(_friender VARCHAR(30), _friendee VARCHAR(30))
  RETURNS INTEGER AS
$RETVAL$
declare
  retval integer;
  friender_id INT;
  friendee_id INT;
begin
  friender_id := (select id from hacker where hacker.email = _friender);
  friendee_id := (select id from hacker where hacker.email = _friendee);

  if not exists(select * from friendship where (first_hacker_id = friender_id and second_hacker_id = friendee_id) union select * from friendship where (first_hacker_id = friendee_id and second_hacker_id = friender_id))
    THEN
      INSERT INTO friendship (first_hacker_id, second_hacker_id)
      VALUES (friender_id, friendee_id);
      retval := 0;
    ELSE
      retval := 1;
  END IF;

  return retval;
end
$RETVAL$
LANGUAGE plpgsql VOLATILE
COST 100;