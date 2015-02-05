CREATE OR REPLACE FUNCTION public.register_hackathon(_name varchar, _logo_url varchar, _cover_image_url varchar, _start_date date, _end_date date, _instruction_path varchar)
  RETURNS int4
AS
$BODY$
  -- declare
    -- retval integer;
begin
  if exists(select 1 from hackathon where hackathon.name = _name)
    THEN
      -- retval := 1;
      return 1;
    ELSE
      INSERT INTO hackathon (name, logo_url, cover_image_url, location, start_date, end_date, instruction_path)
      VALUES (_name, _logo_url, _cover_image_url, 0, _start_date, _end_date, _instruction_path);
      -- retval := 0;
      return 0;
    END IF;
end
$BODY$
LANGUAGE plpgsql VOLATILE;
