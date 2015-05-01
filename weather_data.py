from DB import DB, DB_NAME
from datetime import date
'''

Sports data

'''

def main():
	db = DB(DB_NAME)
	con = db.connection()
	cur = db.cursor()
	
	q_city = 'select yelp_review.date, count(yelp_review.stars), avg(yelp_review.stars) from yelp_business join yelp_review on yelp_review.business_id=yelp_business.business_id where yelp_business.city=\'Pittsburgh\' and yelp_business.state=\'PA\' group by yelp_review.date order by yelp_review.date;'

	reviews = db.query(q_city)

	bad_weathers = []
	
	for line in open('../storm_data_pittsburgh.csv'):
                        try:
                                row = line.split(',')
                                date_raw = row[3]
				date_parts = date_raw.split('/')
                                bad_weathers.append(date_parts[2] + '-' + date_parts[0] + '-' + date_parts[1])
                        except:
                                pass
	
	count = 0

	for line in reviews:
		if line[0].isoformat() in bad_weathers:
			count += int(line[1])
			print '{\"date\":\"' + line[0].isoformat() + '\",\"number_of_reviews\":' + str(line[1]) + ',\"average_stars\":' + str(line[2]) + ',\"bad_weather\":true}'
		elif line[0] > date(2008,1,30) and line[0] < date(2014,8,12):
			count += int(line[1])
			print '{\"date\":\"' + line[0].isoformat() + '\",\"number_of_reviews\":' + str(line[1]) + ',\"average_stars\":' + str(line[2]) + ',\"bad_weather\":false}'

	print count

if __name__ == '__main__':
	main()

