CREATE OR REPLACE FUNCTION public.get_hacker(_id INTEGER)
  RETURNS table(name varchar(255), fb_oauth_access_token varchar(255))
AS

$BODY$
  BEGIN
    RETURN QUERY (
      SELECT h.name, h.fb_oauth_access_token
      FROM hacker h
      WHERE h.id = _id
      LIMIT 1
    );
  END
$BODY$
LANGUAGE plpgsql VOLATILE;
