CREATE OR REPLACE FUNCTION public.register_user_for_hackathon( _hackathon_id INT, _hacker_id INT )
  RETURNS INT
AS
  $$
  BEGIN
    START TRANSACTION;
    IF EXISTS (SELECT *
               FROM hackathons_user_is_attending H
               WHERE H.hackathon_id = _hackathon_id AND H.hacker_id = _hacker_id)
    THEN
      ROLLBACK TRANSACTION;
      RETURN 1;
    END IF;

    INSERT INTO hackathons_user_is_attending (hackathon_id, hacker_id)
    VALUES (_hackathon_id, _hacker_id);

    RETURN 0;
    COMMIT;
  END
  $$
LANGUAGE plpgsql VOLATILE;
