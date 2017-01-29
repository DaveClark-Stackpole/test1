from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
import MySQLdb
import time
import datetime as dt 

# Module to Check if we need to send downtime report out
# via email.   This goes out through the Tech App refreshing	

def find_current_date():
	current_date = dt.datetime.today().strftime("%Y-%m-%d")
	return current_date

def table_copy(request):

	# backup Vacation Table
	db, cursor = db_open()  
	
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee_temp LIKE tkb_employee""")

	db.commit()
	db.close()
	return render(request,'done_test.html')
						  

def time_output():
	tm = int(time.time())
	time.sleep(1.4)
	return tm
	
