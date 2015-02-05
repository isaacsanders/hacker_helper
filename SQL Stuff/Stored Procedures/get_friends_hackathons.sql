drop function get_friends_hackathons(int);
CREATE OR REPLACE FUNCTION public.get_friends_hackathons(_id int)
  RETURNS table(friend_id int, hackathon_id int)
AS
$$
begin
  return QUERY
  (select hackathons_user_is_attending.hacker_id, hackathon.id
   FROM hackathon, hackathons_user_is_attending
   WHERE hackathon.id = hackathons_user_is_attending.hackathon_id
         and exists(select id from get_friends(_id) where hackathons_user_is_attending.hacker_id = id));
end
$$
LANGUAGE plpgsql VOLATILE;


-- testing code
select * from get_friends_hackathons(2);