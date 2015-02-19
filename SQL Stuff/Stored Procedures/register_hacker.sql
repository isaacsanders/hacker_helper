CREATE OR REPLACE FUNCTION public.register_hacker( _email VARCHAR, _fb_oauth_token VARCHAR, _name VARCHAR )
  RETURNS INT4
AS
  $BODY$
  DECLARE
    retval INTEGER;
  BEGIN
    IF exists (SELECT 1
               FROM hacker
               WHERE hacker.email = _email)
    THEN
      retval = 1;
      RETURN retval;
    ELSE
      INSERT INTO hacker (email, fb_oauth_access_token, name)
      VALUES (_email, _fb_oauth_token, _name);
      retval = 0;
      RETURN retval;
    END IF;
  END
  $BODY$
LANGUAGE plpgsql VOLATILE;
