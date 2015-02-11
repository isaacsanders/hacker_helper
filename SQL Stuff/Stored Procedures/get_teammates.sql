CREATE OR REPLACE FUNCTION get_teammates( _hacker_id INTEGER )
  RETURNS TABLE(teammate_id INTEGER, teammate_name VARCHAR(255), team_id INTEGER, team_name VARCHAR(255)) AS
  $$
  BEGIN
    START TRANSACTION;
    CREATE TEMP TABLE friends AS (
      SELECT id
      FROM get_friends (_hacker_id));

    CREATE TEMP TABLE teams_youre_in AS (
      SELECT T.team_id
      FROM teams_hacker_is_member_of T
      WHERE T.hacker_id = _hacker_id);


    RETURN QUERY (
      SELECT hacker.hacker_id
        , hacker.name
        , team.team_id
        , team.name
      FROM friends
        JOIN teams_hacker_is_member_of
          ON friends.friend_id = teams_hacker_is_member_of.hacker_id
        JOIN teams_youre_in
          ON teams_youre_in.team_id = team.id
        JOIN team
          ON teams_hacker_is_member_of.team_id = team.id
        JOIN hacker
          ON hacker.id = friends.friend_id);
    COMMIT TRANSACTION;
  END
  $$
LANGUAGE plpgsql VOLATILE;