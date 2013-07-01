create table twitterdata (
twitterid varchar(100) PRIMARY KEY NOT NULL,
tweet_text varchar(255),
favorite_count int,
retweet_count int,
date_created DATETIME,
user_id int
);
