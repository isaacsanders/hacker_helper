DROP FUNCTION get_my_location(INTEGER)
CREATE OR REPLACE FUNCTION public.get_my_location(_id int4)
  RETURNS table(
  loc_id varchar(30),
  state varchar(30)
  , city varchar(30)
  , zipcode varchar(10)
  , country varchar(30)
  , street_number varchar(30)
  , route varchar(30))
AS
$BODY$
  begin
return QUERY
    (Select * from locations where location_id=_id);
end
$BODY$
LANGUAGE plpgsql VOLATILE;

