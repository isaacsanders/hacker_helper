DROP FUNCTION get_friends_hackathons( INT );

CREATE OR REPLACE FUNCTION public.get_friends_hackathons(_id INT)
  RETURNS TABLE(friend_id INT, hackathon_id INT)
AS
  $$
  BEGIN
    RETURN QUERY
    (SELECT
       hackathons_user_is_attending.hacker_id,
       hackathon.id
     FROM hackathon, hackathons_user_is_attending
     WHERE hackathon.id = hackathons_user_is_attending.hackathon_id
           AND exists(SELECT id
                      FROM get_friends(_id)
                      WHERE hackathons_user_is_attending.hacker_id = id));
  END
  $$
LANGUAGE plpgsql VOLATILE;


-- testing code
SELECT *
FROM get_friends_hackathons(2);