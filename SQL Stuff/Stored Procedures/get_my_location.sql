DROP FUNCTION get_my_location( INTEGER );

CREATE OR REPLACE FUNCTION public.get_my_location(_hacker_id INT4)
  RETURNS TABLE(
  loc_id INT
  , state VARCHAR(30)
  , city VARCHAR(30)
  , zipcode VARCHAR(10)
  , country VARCHAR(30)
  , street_number VARCHAR(30)
  , route VARCHAR(30))
AS
  $BODY$
  BEGIN
    RETURN QUERY
    (SELECT
       L.location_id,
       L.state,
       L.city,
       L.zipcode,
       L.country,
       L.street_number,
       L.route
     FROM locations AS L, hacker
     WHERE hacker.id = _hacker_id AND L.location_id = hacker.location);
  END
  $BODY$
LANGUAGE plpgsql VOLATILE;

SELECT *
FROM get_my_location(2);