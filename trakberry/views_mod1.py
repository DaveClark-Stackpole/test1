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

# Generic Templay kickout for mtemp (headers) and mgmt_table_call which calls the sql required matching headers count
def mgmt_display(request):

	#request.session["mgmt_table_call"] = "SELECT id,asset_num,machine,partno,actual_produced,down_time,comments,pdate,shift,shift_hours_length,target FROM sc_production1"
	s1 = "SELECT "

	for a in request.session["table_variables"]:
		s1 = s1 + a + ','
	s1 = s1[:-1]
	s1 = s1 + ' FROM ' + request.session["mgmt_table_name"] + " ORDER BY id DESC limit 20"

	db, cur = db_open()
	cur.execute(s1)
	tmp = cur.fetchall()
	db.close()
	return render(request,'mgmt_display.html', {'tmp':tmp})	