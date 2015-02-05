CREATE OR REPLACE FUNCTION public.get_friends_hackathons(_id int)
  RETURNS table(friend_id int, hackathon_id int)
AS
$$
begin
  return QUERY
  (select A.hacker_id as hackathon_id, H.id as friend_id
   FROM hackathon H, hackathons_user_is_attending A
   WHERE H.id = A.hackathon_id
         and exists(select id from get_friends(_id) where A.hacker_id = id));
end
$$
LANGUAGE plpgsql VOLATILE;


-- testing code
select * from get_friends_hackathons(2);