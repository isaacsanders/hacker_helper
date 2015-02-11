CREATE OR REPLACE FUNCTION public.register_hacker( _email VARCHAR, _fb_oauth_token VARCHAR, _name VARCHAR )
  RETURNS INT4
AS
  $BODY$
  DECLARE
    retval INTEGER;
  BEGIN
    START TRANSACTION;
    IF exists (SELECT 1
               FROM hacker
               WHERE hacker.email = _email)
    THEN
      ROLLBACK TRANSACTION;
      retval = 1;
      RETURN retval;
    ELSE
      INSERT INTO hacker (email, fb_oauth_access_token, name)
      VALUES (_email, _fb_oauth_token, _name);
      retval = 0;
      COMMIT TRANSACTION;
      RETURN retval;
    END IF;
  END
  $BODY$
LANGUAGE plpgsql VOLATILE;
