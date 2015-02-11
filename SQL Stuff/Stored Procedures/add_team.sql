CREATE OR REPLACE FUNCTION add_team( _creator_id INTEGER, _name VARCHAR(255) )
  RETURNS INTEGER AS
  $$
  DECLARE
    _team_id INTEGER;
  BEGIN
    START TRANSACTION;

    INSERT INTO team (name) VALUES (_name)
    RETURNING _team_id;

    INSERT INTO teams_hacker_is_member_of (hacker_id, team_id) VALUES (_creator_id, _team_id);

    COMMIT TRANSACTION;
    RETURN _team_id;
  END
  $$
LANGUAGE plpgsql VOLATILE;