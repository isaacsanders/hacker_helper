CREATE OR REPLACE FUNCTION public.register_hackathon( _name            VARCHAR, _logo_url VARCHAR,
                                                      _cover_image_url VARCHAR, _location VARCHAR, _start_date DATE,
                                                      _end_date        DATE, _instruction_path VARCHAR )
  RETURNS INT4
AS
  $BODY$
  DECLARE
    retval INTEGER;
  BEGIN
    IF exists(SELECT 1
              FROM hackathon
              WHERE hackathon.name = _name)
    THEN
      retval = 1;
      RETURN retval;
    ELSE
      INSERT INTO hackathon (name, logo_url, cover_image_url, location, start_date, end_date, instruction_path)
      VALUES (_name, _logo_url, _cover_image_url, _location, _start_date, _end_date, _instruction_path);
      retval = 0;
      RETURN retval;
    END IF;
  END
  $BODY$
LANGUAGE plpgsql VOLATILE;
