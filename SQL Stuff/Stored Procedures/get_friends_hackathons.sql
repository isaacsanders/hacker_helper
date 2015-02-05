CREATE OR REPLACE FUNCTION public.get_friends_hackathons(_id int)
  RETURNS table(friend_id int, hackathon_id int)
AS
$$
begin
  return QUERY
  (select hacker.id, hackathon.id
   FROM hackathon, hackathons_user_is_attending
   WHERE hackathon.id = hackathons_user_is_attending.hackathon_id
         and hackathons_user_is_attending.hacker_id in (select id from get_friends(_id)));
end
$$
LANGUAGE plpgsql VOLATILE;
