DROP FUNCTION get_my_location(INTEGER);

CREATE OR REPLACE FUNCTION public.get_my_location(_hacker_id int4)
  RETURNS table(
  loc_id int
  , state varchar(30)
  , city varchar(30)
  , zipcode varchar(10)
  , country varchar(30)
  , street_number varchar(30)
  , route varchar(30))
AS
$BODY$
  begin
return QUERY
    (Select L.location_id, L.state, L.city, L.zipcode, L.country, L.street_number, L.route from locations as L, hacker where hacker.id=_hacker_id and L.location_id = hacker.location);
end
$BODY$
LANGUAGE plpgsql VOLATILE;

select * from get_my_location(2);