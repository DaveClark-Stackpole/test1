from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime 
from views_db import db_open


# Methods for opening database for all and returning db and cur
def vacation_temp():
	
	t = datetime.datetime.now()
#	t = dt.datetime.today().strftime("%m/%d/%Y")
#	t = dt.datetime.today().strftime("%Y-%m-%d")
#	Change host , username , password and db to suit 
#	x=t.strftime('%Y-%m-%d')
	return t

def vacation_set_current():

	t = vacation_temp()
	month_st = t.month
	year_st = t.year
	one = 1
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_shift = 'All'
	
	return current_first, current_shift

def vacation_set_current2():

	t = vacation_temp()
	month_st = t.month
	year_st = t.year
	day_st = t.day
	
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first

def vacation_backup(request):

	# backup Vacation Table
	db, cursor = db_open()  
	
	cursor.execute("""DROP TABLE IF EXISTS vacation_backup""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS vacation_backup LIKE vacation""")
	cursor.execute('''INSERT vacation_backup Select * From vacation''')

	db.commit()
	db.close()
	return render(request,'done_test.html')
	
	
	
