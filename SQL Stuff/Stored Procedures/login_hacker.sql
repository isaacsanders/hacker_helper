-- Given the json response from logging into Facebook 
-- (I assume this is GET /me), either login this person or create a new 
-- hacker in Hacker table
CREATE FUNCTION login_hacker(hacker jsonb)
	RETURNS type AS
DECLARE fb_oauth_access_token text;
DECLARE hacker_email text;
DECLARE fullName text; -- add to schema
DECLARE location text;
BEGIN
	fb_oauth_access_token := jsonb_extract_path_text(jsonb, 'id');
	hacker_email := jsonb_extract_path_text(jsonb, 'email');
	fullName := jsonb_extract_path_text(jsonb, 'name');
	location := jsonb_extract_path_text(jsonb, 'location', 'name');

	-- if hacker is in database, log them in. Otherwise, create a hew hacker
	if((select count(*) from Hacker where email = hacker_email) = 0)
	BEGIN
		insert into Hacker (email, location, fb_oauth_access_token)
		values (hacker_email, location, fb_oauth_access_token);
		-- login
	END;
	ELSE
	BEGIN
		-- login
	END;
END;
LANGUAGE plpgsql; --??