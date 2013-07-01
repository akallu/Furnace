import sys
import os
from twitter import *
import time
import sys
import os
import sqlite3 as lite
from twitter import *

# General Twitter Streaming Module
# Takes parameter duration (defaults to 3 hours)
# Stores tweets in sqlite database

def streamTweets(duration=10800):
	# Creates twitter app creditials
	MY_TWITTER_CREDS = os.path.expanduser('.my_app_credentials')
	if not os.path.exists(MY_TWITTER_CREDS):
		oauth_dance("My App Name", "uaN3P6jmoKs1O6x0E3cDQ", "Rr1GDxL8YWoKEbDzB2S4lTIToPNkkUrw1BeCtkZqRAk", MY_TWITTER_CREDS)
	
	# Connect to twitter stream
	oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
	twitter_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, "uaN3P6jmoKs1O6x0E3cDQ", "Rr1GDxL8YWoKEbDzB2S4lTIToPNkkUrw1BeCtkZqRAk"))
	iterator = twitter_stream.statuses.sample()
	
	
	try:
		## start time
		start = time.time()
	
		#record count
		i = 0
		
		#connect to database
		db = lite.connect('twitter.db')
		cur = db.cursor()
		while True:
			
			curr_time = time.time()
			
			# exit conditions
			if curr_time-start >= duration:
				db.commit()
				print str(i) + " records affected"
				db.close()
				sys.exit()
			
			it = iterator.next()
			
			# filter out incomplete tweet data
			if it.has_key("text"):
				i+=1
				user = it["user"]
				# run queries
				cur.execute("""
					INSERT INTO twitterdata VALUES(?,?,?,?,?,?) """,
					(it["id"], unicode(it["text"]), it["favorite_count"], it["retweet_count"], it["created_at"], user["id"]))
				cur.execute("""
					INSERT or replace INTO userdata VALUES(?,?,?,?) """,
					(user["id"], user["followers_count"], user["statuses_count"], user["verified"]))
	
	# error catch				
	except lite.Error, e:
		if db:
			db.rollback()
			print "Error encountered on query: " + str(e)
			sys.exit(1)


