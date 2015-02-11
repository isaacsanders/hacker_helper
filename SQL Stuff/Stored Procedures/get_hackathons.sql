DROP FUNCTION get_hackathons( INT );

CREATE OR REPLACE FUNCTION public.get_hackathons( )
  RETURNS TABLE(
  id INT
  , name VARCHAR(255)
  , logo_url VARCHAR(255)
  , cover_image_url VARCHAR(255)
  , start_date DATE
  , end_date DATE
  , instruction_path VARCHAR(255)
  , state VARCHAR(30)
  , city VARCHAR(30)
  , zipcode VARCHAR(10)
  , country VARCHAR(30)
  , street_number VARCHAR(30)
  , route VARCHAR(30))
AS
  $$
  BEGIN
    RETURN QUERY
    (
      SELECT
        H.id
        , H.name
        , H.logo_url
        , H.cover_image_url
        , H.start_date
        , H.end_date
        , H.instruction_path
        , L.state
        , L.city
        , L.zipcode
        , L.country
        , L.street_number
        , L.route
      FROM hackathon H, locations L
      WHERE H.location = L.location_id);
  END
  $$
LANGUAGE plpgsql VOLATILE;
