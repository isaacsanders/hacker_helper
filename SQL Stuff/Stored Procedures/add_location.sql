CREATE OR REPLACE FUNCTION public.add_location_hacker(street_address, state, city, zipcode, country)
    RETURNS INTEGER AS
$FUNC$
declare
  retval integer;
begin
  if exists(select 1 from hackathon where hackathon.name = _name)
    THEN
      retval = 1;
      return retval;
    ELSE
      INSERT INTO hackathon (name, logo_url, cover_image_url, location, start_date, end_date, instruction_path)
      VALUES (_name, _logo_url, _cover_image_url, _location, _start_date, _end_date, _instruction_path);
      retval = 0;
      return retval;
    END IF;
end
 $FUNC$
