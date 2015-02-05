DROP FUNCTION get_friends( INT );

CREATE OR REPLACE FUNCTION public.get_friends( _id INT )
  RETURNS TABLE(id INT, email VARCHAR(30), location INT)
AS
  $$
  BEGIN
    RETURN QUERY
    (
      SELECT hacker.id       AS id
        ,    hacker.email    AS email
        ,    hacker.location AS location
      FROM (SELECT second_hacker_id AS id
            FROM friendship
            WHERE first_hacker_id = _id
            UNION
            SELECT first_hacker_id AS id
            FROM friendship
            WHERE second_hacker_id = _id) AS friend_id, hacker
      WHERE
        hacker.id = friend_id.id);
  END
  $$
LANGUAGE plpgsql VOLATILE;

-- testing code

SELECT first_hacker_id
  , second_hacker_id
FROM friendship
UNION SELECT second_hacker_id AS sid
        ,    first_hacker_id  AS fid
      FROM friendship
ORDER BY first_hacker_id, second_hacker_id;