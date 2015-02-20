CREATE OR REPLACE FUNCTION get_teammates( _hacker_id INTEGER )
  RETURNS TABLE(teammate_id INTEGER, teammate_name VARCHAR(255), team_id INTEGER, team_name VARCHAR(255)) AS
  $$
  BEGIN
    RETURN QUERY (
      SELECT DISTINCT hacker.id
        , hacker.name
        , team.id AS team_id
        , team.name AS team_name
      FROM hacker
        JOIN teams_hacker_is_member_of
          ON teams_hacker_is_member_of.hacker_id = hacker.id
        JOIN team
          ON team.id = teams_hacker_is_member_of.team_id
      WHERE hacker.id <> _hacker_id
    );
  END
  $$
LANGUAGE plpgsql VOLATILE;