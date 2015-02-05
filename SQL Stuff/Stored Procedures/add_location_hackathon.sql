CREATE OR REPLACE FUNCTION public.add_location_hacker(_street_address varchar, _state varchar, _city varchar, _zipcode varchar, _country varchar)
  RETURNS int4
AS
$BODY$
  declare
  ret integer;
begin
  INSERT INTO location (_street_address, _state, _city, _zipcode)
  VALUES (_street_address, _state, _city, _zipcode);
  return 0;
end;
$BODY$
LANGUAGE plpgsql VOLATILE;
