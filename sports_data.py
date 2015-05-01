from DB import DB, DB_NAME

'''

This program uses the database to extract all yelp reviews from Phoenix (not completely direct because 
the review table doesn't contain a city field) and then puts them in a list which is then iterated
over to check if its 'categories' array contains 'Sports Bar'. These reviews are put in a new table.
Queries and code is then used to create three JSONs of sports bar reviews from Phoenix, those that
occurred on a winning day, a losing day, and a non game day.

'''

def main():
	db = DB(DB_NAME)
	con = db.connection()
	cur = db.cursor()
	
	q_city = 'select yelp_review.date, yelp_review.stars, yelp_business.categories, yelp_business.business_id from yelp_business join yelp_review on yelp_review.business_id=yelp_business.business_id where yelp_business.city=\'Phoenix\' and yelp_business.state=\'AZ\';'

	sports_bars = []

	city = db.query(q_city)
	
	for line in city:
		if 'Sports Bars' in line[2]:
			sports_bars.append((line[0].isoformat(), line [1]))

	#d1 = 'drop table if exists sports_bar_reviews;'
	#q1 = 'create table sports_bar_reviews(date varchar(16), stars real);'

	#for review in sports_bars:
	#	cur.execute("insert into sports_bar_reviews VALUES (%s, %s)", (review[0], review[1]))
	
	#con.commit()
	

	q = 'select sports_bar_reviews.date, count(sports_bar_reviews.stars), avg(sports_bar_reviews.stars) from sports_bar_reviews join nfl_games on sports_bar_reviews.date=nfl_games.date where loser=\'Arizona\' group by sports_bar_reviews.date order by sports_bar_reviews.date;'

	data = db.query(q)
	
	count = 0

	for line in data:
		count += int(line[1])
		print '{\"date\":\"' + line[0] + '\",\"number_of_reviews\":' + str(line[1]) + ',\"average_stars\":' + str(line[2]) + '}'

	print count


	#print sports_bars[0][0]
	
	q_wins = 'select date from nfl_games where winner=\'Arizona\';'
	q_losses = 'select date from nfl_games where loser=\'Arizona\';'
	
	wins_raw = db.query(q_wins)
	losses_raw = db.query(q_losses)

	wins = []
	losses = []

	for win in wins_raw:
		wins.append(win[0])
	for loss in losses_raw:
		losses.append(loss[0])
	
	q = 'select sports_bar_reviews.date, count(sports_bar_reviews.stars), avg(sports_bar_reviews.stars) from sports_bar_reviews group by sports_bar_reviews.date order by sports_bar_reviews.date;'
	
	data = db.query(q)

	count = 0

	for line in data:
		if not line[0] in wins and not line[0] in losses:
			count += int(line[1])
			print '{\"date\":\"' + line[0] + '\",\"number_of_reviews\":' + str(line[1]) + ',\"average_stars\":' + str(line[2]) + '}'
	print count

	#win_reviews = []
	#loss_reviews = []
	#gameless_reviews = []

	#for review in sports_bars:
	#	if not review[0] in wins and not review[0] in losses:
	#		gameless_reviews.append(review[1])

	#for win in wins:
	#	for review in sports_bars:
	#		if win == review[0]:
	#			win_reviews.append(review[1])

	#for loss in losses:
	#	for review in sports_bars:
	#		if loss == review[0]:
	#			loss_reviews.append(review[1])
				
	#print len(sports_bars)
	#print len(win_reviews)
	#print len(loss_reviews)
	#print len(gameless_reviews)
	
	#print 'Wins:'
	#print win_reviews
	#print 'Losses:'
	#print loss_reviews
	#print 'Gameless Days:'
	#print gameless_reviews

if __name__ == '__main__':
	main()

