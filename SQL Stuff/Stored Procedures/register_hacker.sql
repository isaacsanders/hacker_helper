CREATE OR REPLACE FUNCTION register_hacker(_email VARCHAR(30), _location VARCHAR(30), _fb_oauth_token VARCHAR(60))
  RETURNS INTEGER AS
$RETVAL$
declare
    retval integer;
begin
  if exists(select 1 from hacker where hacker.email = _email)
    THEN
      retval = 1;
      return retval;
    ELSE
      INSERT INTO hacker (email, location, fb_oauth_access_token)
      VALUES (_email, _location, _fb_oauth_access_token);
      retval = 0;
      return retval;
    END IF;
end
$RETVAL$
LANGUAGE plpgsql VOLATILE
COST 100;