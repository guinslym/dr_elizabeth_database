PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	screen_name VARCHAR(250) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "user" VALUES(19203412,'Greg MacEachern','gmacofglebe');
INSERT INTO "user" VALUES(111713801,'MP Tweets','canadamptweets');
INSERT INTO "user" VALUES(894381348,'DEM','MoleskiDorothy');
INSERT INTO "user" VALUES(1072715886,'Scott Duquette','srduquette3');
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
INSERT INTO "profile" VALUES(1,0,'Windsor, Ontario',1,0,4019,NULL,291,12789,412,'Wed Jan 09 03:36:09 +0000 2013','0','http://pbs.twimg.com/profile_images/378800000208617846/a06f34d07b3e05c421713900846c0b30_normal.jpeg','Windsor booster, Educator and Life-Long Learner. Animal lover. Raised on family farm founded by Mom''s immigrant great/grandfather. History buff.',1072715886);
INSERT INTO "profile" VALUES(2,0,'Ottawa, Ontario',0,0,3716,NULL,6072,36336,2448,'Mon Jan 19 21:35:31 +0000 2009','1','http://pbs.twimg.com/profile_images/626271626838077440/39P_E-mS_normal.jpg','Ottawa-based Bluenoser, GR/Comms guy, recovering politico; political commentator, weekly on CTV''s PowerPlay, and on CBC Radio and other media. Tweets are mine.',19203412);
INSERT INTO "profile" VALUES(3,0,NULL,1,0,1591,NULL,118,4983,700,'Sun Oct 21 01:33:17 +0000 2012','0','http://pbs.twimg.com/profile_images/2808616756/603a157c257867d2451139bc31da453b_normal.jpeg','Retweets not always an endorsement.',894381348);
INSERT INTO "profile" VALUES(4,0,'Ottawa, Ontario',0,0,0,NULL,1382,22734,1775,'Fri Feb 05 22:36:43 +0000 2010','1','http://pbs.twimg.com/profile_images/668847093126066177/f8UfT2Pq_normal.jpg','Tweets from all Federal MPs, across all parties. Enjoy this handy resource provided by Jordan St Jacques from @mydigitera, the agency for all things digital!',111713801);
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
INSERT INTO "tweet" VALUES(727497782479572992,'RT @mdentandt: I think I too am ''stuck in this whole balanced budget thing,'' sadly. #retrograde #neanderthal  https://t.co/o7x2mIy1Fr','en',NULL,0,0,894381348);
INSERT INTO "tweet" VALUES(727527540907069440,'@pdmcleod Oh. Must have had my SickBurn Dectector(TM) set too low.','en',NULL,0,0,19203412);
INSERT INTO "tweet" VALUES(729818231972704261,'@natnewswatch @IvisonJ Genocide recognition if necessary, but not necessarily genocide recognition.','en',NULL,0,0,1072715886);
INSERT INTO "tweet" VALUES(730042173383688193,'RT @CandiceBergenMP: Obama to JT, "U say nothing about Keystone XL to me, I''ll stay quiet on pulling out of ISIL fight,+ a State Dinner " h…','en',NULL,0,0,111713801);
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
INSERT INTO "url" VALUES(1,'https://twitter.com/althiaraj/status/727446094318170113','https://t.co/o7x2mIy1Fr',727497782479572992);
INSERT INTO "url" VALUES(2,'https://twitter.com/therebeltv/status/730039198489579520','https://t.co/2KVtI93tw4',730042173383688193);
CREATE TABLE mention (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	screen_name VARCHAR(250) NOT NULL, 
	tweet_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tweet_id) REFERENCES tweet (id)
);
INSERT INTO "mention" VALUES(1,'National Newswatch','natnewswatch',729818231972704261);
INSERT INTO "mention" VALUES(2,'John Ivison','IvisonJ',729818231972704261);
INSERT INTO "mention" VALUES(3,'Paul McLeod','pdmcleod',727527540907069440);
INSERT INTO "mention" VALUES(4,'Michael Den Tandt','mdentandt',727497782479572992);
INSERT INTO "mention" VALUES(5,'Candice Bergen','CandiceBergenMP',730042173383688193);
CREATE TABLE hashtag (
	id INTEGER NOT NULL, 
	text VARCHAR(250) NOT NULL, 
	tweet_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tweet_id) REFERENCES tweet (id)
);
INSERT INTO "hashtag" VALUES(1,'retrograde',727497782479572992);
INSERT INTO "hashtag" VALUES(2,'neanderthal',727497782479572992);
COMMIT;
