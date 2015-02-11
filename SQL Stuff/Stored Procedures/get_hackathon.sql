DROP FUNCTION get_hackathon( INT );

CREATE OR REPLACE FUNCTION public.get_hackathon( _hackathon_id INTEGER )
  RETURNS TABLE(
  id INT
  , name VARCHAR(255)
  , logo_url VARCHAR(255)
  , cover_image_url VARCHAR(255)
  , start_date DATE
  , end_date DATE
  , state VARCHAR(30)
  , city VARCHAR(30)
  , zipcode VARCHAR(10)
  , country VARCHAR(30)
  , street_number VARCHAR(30)
  , route VARCHAR(30)
  , website VARCHAR(255))
AS
  $$
  BEGIN
    RETURN QUERY
    (
      SELECT H.id
        , H.name
        , H.logo_url
        , H.cover_image_url
        , H.start_date
        , H.end_date
        , L.state
        , L.city
        , L.zipcode
        , L.country
        , L.street_number
        , L.route
        , H.website
      FROM hackathon H, locations L
      WHERE H.location = L.location_id
            AND H.id = _hackathon_id);
  END
  $$
LANGUAGE plpgsql VOLATILE;

SELECT *
FROM get_hackathon (38)