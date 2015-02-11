CREATE OR REPLACE FUNCTION add_team( _hacker_id INTEGER, _team_id INTEGER )
  RETURNS INTEGER AS
  $$
  BEGIN
    START TRANSACTION;

    IF exists (SELECT *
               FROM teams_hacker_is_member_of T
               WHERE T.hacker_id = _hacker_id AND T.team_id = _team_id)
    THEN
      ROLLBACK TRANSACTION;
      return 1;
    END IF;

    INSERT INTO teams_hacker_is_member_of (hacker_id, team_id) VALUES (_hacker_id, _team_id);

    COMMIT TRANSACTION;
    RETURN 0;
  END
  $$
LANGUAGE plpgsql VOLATILE;