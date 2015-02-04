CREATE OR REPLACE FUNCTION public.get_friends(_id INT)
  RETURNS table(id INT)
  --RETURNS table(id INT, name VARCHAR(255), location VARCHAR(30))
AS
$BODY$
begin
  return QUERY (select second_hacker_id from friendship where first_hacker_id = _id union select first_hacker_id from friendship where second_hacker_id = _id);
end
$BODY$
LANGUAGE plpgsql VOLATILE;
