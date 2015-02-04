CREATE OR REPLACE FUNCTION public.get_friends(_id int)
  RETURNS table(id int, email varchar(30), location varchar(30))
AS
$$
begin
  return QUERY
  (select hacker.id as id, hacker.email as email, hacker.location as location from (select second_hacker_id as id from friendship where first_hacker_id = _id
                                   union
                                   select first_hacker_id as id from friendship where second_hacker_id = _id) as friend_id, hacker
  WHERE
    hacker.id = friend_id.id);
end
$$
LANGUAGE plpgsql VOLATILE;