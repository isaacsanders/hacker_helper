CREATE OR REPLACE FUNCTION public.register_user_for_hackathon(_hackathon_id int, _hacker_id int)
  RETURNS void
AS
$BODY$
begin
      INSERT INTO hackathon_user_is_attending(hackathon_id, hacker_id)
      VALUES(_hackathon_id, _hacker_id)
end
$BODY$
LANGUAGE plpgsql VOLATILE;
