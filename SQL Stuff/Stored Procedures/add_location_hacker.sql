CREATE OR REPLACE FUNCTION public.add_location_hacker(_hacker_id varchar(100), _route varchar, _street_number varchar, _state varchar, _city varchar, _zipcode int4, _country varchar)
  RETURNS int4
AS
$BODY$
  declare
  iid integer;
begin
  INSERT INTO public.locations (route, street_number, state, city, zipcode, country)
  VALUES (_route,_street_number, _state, _city, _zipcode, _country)
  RETURNING location_id INTO iid;
  UPDATE hacker SET location=iid
  WHERE fb_oauth_access_token=_hacker_id;
  return 0;
end;
$BODY$
LANGUAGE plpgsql VOLATILE;
