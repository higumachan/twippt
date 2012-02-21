USE twippt;

CREATE TABLE tag(
	id INTEGER,
	text CHAR(100)
);

CREATE TABLE tweet(
	id INTEGER,
	text CHAR(255),
	flag BOOLEAN,
	time DATETIME,
	slide_id INTEGER
);

CREATE TABLE slide(
	id INTEGER,
	name CHAR(255),
	url CHAR(255)
);

CREATE TABLE tag_slide_relation (
	id INTEGER,
	slide_id INTEGER,
	tag_id INTEGER
);

CREATE TABLE tag_tweet_relation (
	id INTEGER,
	tag_id INTEGER,
	tweet_id INTEGER
);

