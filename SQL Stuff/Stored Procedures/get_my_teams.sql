CREATE OR REPLACE FUNCTION get_my_teams( _hacker_id INTEGER )
  RETURNS TABLE(team_id INTEGER, team_name VARCHAR(255)) AS
  $$
  BEGIN
    START TRANSACTION;
    RETURN QUERY (
      SELECT T.id
        , T.name
      FROM teams_hacker_is_member_of THMO, team T
      WHERE THMO.hacker_id = _hacker_id AND T.id = THMO.team_id);
    COMMIT TRANSACTION;
  END
  $$
LANGUAGE plpgsql VOLATILE;