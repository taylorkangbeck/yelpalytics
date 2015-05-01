'''

DB_NAME = yelp. This variable is defined in DB.py

Loads 10 years of NFL data (from 10 sepearte csv files) into a Postgres table.

'''

import json
from DB import DB, DB_NAME

def main():

	file_stem = 'aux_datasets/nfl_season_stats_'

	rows = []

	for i in range(2005,2015):
		file_name = file_stem + str(i) + '.csv'
		for line in open(file_name):
			try:
				row = line.split(',')
				row[1] = get_date(row[2], i)
				rows.append(row)
			except:
				pass

	db = DB(DB_NAME)
	create_tables(db)
	load_nfl(db, rows)

def create_tables(db):
	con = db.connection()
	cur = db.cursor()

	d1 = 'drop table if exists nfl_games;'
	
	q1 = 'create table nfl_games(date varchar(16), winner varchar(32), loser varchar(32));'

	for q in [d1, q1]:
		cur.execute(q)
	con.commit()
		

def load_nfl(db, rows):
	con = db.connection()
	cur = db.cursor()
	
	for row in rows:
		date = row[1]
		winner = get_city(row[4])
		loser = get_city(row[6])
		cur.execute("insert into nfl_games VALUES (%s, %s, %s)", (date, winner, loser))

	con.commit()

def get_date(date, year):
	month_day = date.split(' ')
	
	day = month_day[1]
	
	if int(day) < 10:
		day = '0' + day
	
	month = '09'
	if month_day[0] == 'October':
		month = '10'
	elif month_day[0] == 'November':
		month = '11'
	elif month_day[0] == 'December':
		month = '12'
	elif month_day[0] == 'January':
		month = '01'

	return str(year) + '-' + month + '-' + day

def get_city(team):
	words = team.split(' ')
	if len(words) == 2:
		return words[0]

	city = 'Featheringill'
	for i in range(len(words) - 1):
		if i == 0:
			city = words[i]
		else:
			city = city + ' ' + words[i]
	return city

if __name__ == '__main__':
	main()
	
