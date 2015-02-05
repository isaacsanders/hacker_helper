DROP FUNCTION get_hackathons(int);

CREATE OR REPLACE FUNCTION public.get_hackathons()
  RETURNS table(
  id int
  , name varchar(255)
  , logo_url varchar(255)
  , cover_image_url varchar(255)
  , start_date DATE
  , end_date DATE
  , instruction_path varchar(255)
  , state varchar(30)
  , city varchar(30)
  , zipcode varchar(10)
  , country varchar(30)
  , street_number varchar(30)
  , route varchar(30))
AS
$$
begin
  return QUERY
  (select H.id, H.name, H.logo_url, H.cover_image_url, H.start_date, H.end_date, H.instruction_path, L.state, L.city, L.zipcode, L.country, L.street_number, L.route
  from hackathon H, locations L
  where H.location = L.location_id);
end
$$
LANGUAGE plpgsql VOLATILE;
