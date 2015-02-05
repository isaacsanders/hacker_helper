CREATE OR REPLACE FUNCTION public.add_location_hacker( _hacker_id VARCHAR(100), _route VARCHAR, _street_number VARCHAR,
                                                       _state     VARCHAR, _city VARCHAR, _zipcode INT4,
                                                       _country   VARCHAR )
  RETURNS INT4
AS
  $$
  DECLARE
    iid INTEGER;
  BEGIN
    INSERT INTO public.locations (route, street_number, state, city, zipcode, country)
    VALUES (_route, _street_number, _state, _city, _zipcode, _country)
    RETURNING location_id
      INTO iid;
    UPDATE hacker
    SET location = iid
    WHERE fb_oauth_access_token = _hacker_id;
    RETURN 0;
  END;
  $$
LANGUAGE plpgsql VOLATILE;
