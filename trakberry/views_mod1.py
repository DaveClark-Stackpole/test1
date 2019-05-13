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

def kiosk_lastpart_find(asset):
	db, cur = db_open()  
	a1sql = "SELECT MAX(id)  FROM sc_production1 WHERE asset_num = '%s'" %(asset) 
	cur.execute(a1sql)
	tp3 = cur.fetchall()
	tp4 = tp3[0]
	tp5 = tp4[0]
	a2sql = "Select partno From sc_production1 WHERE id = '%d'" %(tp5)
	cur.execute(a2sql)
	tp3 = cur.fetchall()
	tp4 = tp3[0]
	part = tp4[0]
	db.close()
	return part
	
