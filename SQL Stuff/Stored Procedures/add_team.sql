CREATE OR REPLACE FUNCTION add_team( _creator_id INTEGER, _name VARCHAR(255) )
  RETURNS INTEGER AS
  $$
  DECLARE
    lid INTEGER;
  BEGIN
    START TRANSACTION;

    INSERT INTO team (name) VALUES (_name)
    RETURNING location_id
      INTO lid;

    INSERT INTO teams_hacker_is_member_of (hacker_id, team_id) VALUES (_creator_id, lid);

    COMMIT TRANSACTION;
    RETURN 0;
  END
  $$
LANGUAGE plpgsql VOLATILE;