'''

DB_NAME = yelp. This variable is defined in DB.py

'''

import json
from DB import DB, DB_NAME

def main():
	businesses = []

	for line in open('../yelp_academic_dataset_business.json'):
		try: 
			businesses.append(json.loads(line))
		except:
			pass

	users = []

	#for line in open('../yelp_academic_dataset_user.json'):
	#	try:
	#		users.append(json.loads(line))
	#	except:
	#		pass
	
	reviews = []

	#for line in open('../yelp_academic_dataset_review.json'):
	#	try:
	#		reviews.append(json.loads(line))
	#	except:
	#		pass


	db = DB(DB_NAME)
	create_tables(db)
	load_yelp(db, businesses, users, reviews)

def create_tables(db):
	con = db.connection()
	cur = db.cursor()

	d1 = 'drop table if exists yelp_business;'
	d2 = 'drop table if exists yelp_user;'
	d3 = 'drop table if exists yelp_review;'

	q1 = 'create table yelp_business(business_id varchar(32), categories varchar(64)[], city varchar(64), state varchar(16), stars real, review_count integer);'
	q2 = 'create table yelp_user(user_id varchar(32), average_stars real, review_count integer);'
	q3 = 'create table yelp_review(business_id varchar(32), user_id varchar(32), stars real, text text, date date);'

	#for q in [d1, d2, d3, q1, q2, q3]:
	for q in [d1, q1]:
		cur.execute(q)
	con.commit()
		

def load_yelp(db, businesses, users, reviews):
	con = db.connection()
	cur = db.cursor()
	
	for b in businesses:
		cur.execute("insert into yelp_business VALUES (%s, %s, %s, %s, %s, %s)", (b['business_id'], b['categories'], b['city'], b['state'], b['stars'], b['review_count']))

	#for u in users:
	#	cur.execute("insert into yelp_user VALUES (%s, %s, %s)", (u['user_id'], u['average_stars'], u['review_count']))
	
	#for r in reviews:
	#	cur.execute("insert into yelp_review VALUES (%s, %s, %s, %s, %s)", (r['business_id'], r['user_id'], r['stars'], r['text'], r['date']))
	con.commit()

if __name__ == '__main__':
	main()
	
