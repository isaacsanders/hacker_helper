CREATE OR REPLACE FUNCTION public.get_hacker(_id INTEGER)
  RETURNS hacker%ROWTYPE
AS
$BODY$
  BEGIN
    RETURN (
      SELECT name, fb_oauth_access_token
      FROM hacker
      WHERE hacker.id = _id
      LIMIT 1
    );
  END
$BODY$
LANGUAGE plpgsql VOLATILE;