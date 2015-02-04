CREATE OR REPLACE FUNCTION public.get_friends(_id INT)
  RETURNS table(id INT)
  --RETURNS table(id INT, name VARCHAR(255), location VARCHAR(30))
AS
$BODY$
declare
  retval table(id INT);
  --retval table(id INT, name VARCHAR(255), location VARCHAR(30));
begin
  retval := (select second_hacker_id from friendship where first_hacker_id = _id union select first_hacker_id from friendship where second_hacker_id = _id);
    RETURN retval;
end
$BODY$
LANGUAGE plpgsql VOLATILE;


CREATE OR REPLACE FUNCTION public.get_friends(_id INT)
  RETURNS table(id INT)
  --RETURNS table(id INT, name VARCHAR(255), location VARCHAR(30))
AS
$BODY$
  --declare
   -- retval;
    --retval table(id INT, name VARCHAR(255), location VARCHAR(30));
begin
  return QUERY (select second_hacker_id from friendship where first_hacker_id = _id);
   -- RETURN retval;
end
$BODY$
LANGUAGE plpgsql VOLATILE;
