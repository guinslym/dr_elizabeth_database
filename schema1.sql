CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	screen_name VARCHAR(250) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE profile (
	id INTEGER NOT NULL, 
	verified INTEGER, 
	location INTEGER, 
	default_profile INTEGER, 
	default_profile_image INTEGER, 
	favourites_count INTEGER, 
	listed_count INTEGER, 
	followers_count INTEGER, 
	statuses_count INTEGER, 
	friends_count INTEGER, 
	created_at VARCHAR(250), 
	time_zone VARCHAR(250), 
	profile_image_url VARCHAR(250), 
	description VARCHAR(250), 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE tweet (
	id INTEGER NOT NULL, 
	tweet VARCHAR(250) NOT NULL, 
	lang VARCHAR(7), 
	in_reply_to_user_id INTEGER, 
	coordinates INTEGER, 
	geo INTEGER, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE picture (
	id INTEGER NOT NULL, 
	profile_image_url VARCHAR(250) NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE url (
	id INTEGER NOT NULL, 
	expanded_url VARCHAR(250) NOT NULL, 
	shortened_url VARCHAR(250) NOT NULL, 
	tweet_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tweet_id) REFERENCES tweet (id)
);
CREATE TABLE mention (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	screen_name VARCHAR(250) NOT NULL, 
	tweet_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tweet_id) REFERENCES tweet (id)
);
CREATE TABLE hashtag (
	id INTEGER NOT NULL, 
	text VARCHAR(250) NOT NULL, 
	tweet_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tweet_id) REFERENCES tweet (id)
);
