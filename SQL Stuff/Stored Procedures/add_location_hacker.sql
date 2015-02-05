CREATE OR REPLACE FUNCTION public.add_location_hacker(_hacker_id int,_street_address varchar, _state varchar, _city varchar, _zipcode int, _country varchar)
  RETURNS int4
AS
$BODY$
  declare
  iid int;
begin
  INSERT INTO public.locations (street_address, state, city, zipcode,country)
  VALUES (_street_address, _state, _city, _zipcode,_country)
  RETURNING location_id INTO iid;

  return iid;
end;
$BODY$
LANGUAGE plpgsql VOLATILE;
