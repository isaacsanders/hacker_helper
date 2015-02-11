DROP FUNCTION get_hackathons_attending_from_hacker_id( integer );

CREATE OR REPLACE FUNCTION get_hackathons_attending_from_hacker_id( _hacker_id INTEGER )
  RETURNS TABLE(hackathon_id INT, hackathon_name VARCHAR(255))
AS
  $$
  BEGIN
    RETURN QUERY
    (
      SELECT H.id
        , H.name
      FROM hackathon AS H, hackathons_user_is_attending A
      WHERE A.hacker_id = _hacker_id
            AND H.id = A.hackathon_id);
  END
  $$
LANGUAGE plpgsql VOLATILE;


-- testing code
SELECT *
FROM get_hackathons_attending_from_hacker_id (2);