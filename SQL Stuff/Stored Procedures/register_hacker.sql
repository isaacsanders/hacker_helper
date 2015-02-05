CREATE OR REPLACE FUNCTION public.register_hacker(_email varchar, _fb_oauth_token varchar, _name varchar)
  RETURNS int4
AS
$BODY$
  declare
    retval integer;
begin
  if exists(select 1 from hacker where hacker.email = _email)
    THEN
      retval = 1;
      return retval;
    ELSE
      INSERT INTO hacker (email , fb_oauth_access_token, name)
      VALUES (_email, _fb_oauth_token, _name);
      retval = 0;
      return retval;
    END IF;
end
$BODY$
LANGUAGE plpgsql VOLATILE;
