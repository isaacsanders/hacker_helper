drop function get_hacker_from_oauth(varchar(100));
CREATE OR REPLACE FUNCTION public.get_hacker_from_oauth(_oauth varchar(100))
  RETURNS table(id int, email varchar(30), location int, fb_oauth_access_token varchar(100), name varchar(255))
AS
$$
begin
  return QUERY
  (select H.id, H.email, H.location, H.fb_oauth_access_token, H.name from hacker as H where H.fb_oauth_access_token = _oauth);
end
$$
LANGUAGE plpgsql VOLATILE;

