CREATE OR REPLACE FUNCTION public.add_location_hacker(_street_address VARCHAR, _state VARCHAR, _city VARCHAR,
                                                      _zipcode        VARCHAR, _country VARCHAR)
  RETURNS INT4
AS
  $$
  DECLARE
    ret INTEGER;
  BEGIN
    INSERT INTO location (_street_address, _state, _city, _zipcode)
    VALUES (_street_address, _state, _city, _zipcode);
    RETURN 0;
  END;
  $$
LANGUAGE plpgsql VOLATILE;
