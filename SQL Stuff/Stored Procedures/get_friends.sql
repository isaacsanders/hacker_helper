CREATE OR REPLACE FUNCTION public.get_friends( _id INT )
  RETURNS table(id int, email varchar(30), name varchar(30), location int)
AS
  $$
  BEGIN
    RETURN QUERY
    (
      SELECT hacker.id       AS id
        ,    hacker.email    AS email
        ,    hacker.name     AS name
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

SELECT *
FROM get_friends(5);
