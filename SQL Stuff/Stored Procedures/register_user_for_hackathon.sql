CREATE OR REPLACE FUNCTION public.register_user_for_hackathon( _hackathon_id INT, _hacker_id INT )
  RETURNS VOID
AS
  $BODY$
  BEGIN
    INSERT INTO hackathons_user_is_attending (hackathon_id, hacker_id)
    VALUES (_hackathon_id, _hacker_id);
  END
  $BODY$
LANGUAGE plpgsql VOLATILE;
