DROP FUNCTION get_hacker_from_oauth( VARCHAR(100) );

CREATE OR REPLACE FUNCTION public.get_hacker_from_oauth( _oauth VARCHAR(100) )
  RETURNS TABLE(id INT, email VARCHAR(30), location INT, name VARCHAR(255))
AS
  $$
  BEGIN
    RETURN QUERY
    (
      SELECT
        H.id
        , H.email
        , H.location
        , H.name
      FROM hacker AS H
      WHERE H.fb_oauth_access_token = _oauth);
  END
  $$
LANGUAGE plpgsql VOLATILE;


-- testing code
SELECT *
FROM get_hacker_from_oauth ('638364292977015');