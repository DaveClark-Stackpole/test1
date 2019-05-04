from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime 
from views_db import db_open

  
  
def back_db(request):
	#db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
	db = MySQLdb.connect(host="127.0.0.1",user="dg417",passwd="dg",db='prodrptdb')
	cursor = db.cursor()	
	sql = "SELECT * FROM pr_parts"
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close()
	
	# Uncomment below line to switch to new server PMDS3 and comment above line out
	db2 = MySQLdb.connect(host="10.4.10.160",user="localhost",passwd="dg",db='prodrptdb')
	cur = db2.cursor()
	
	
	#cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee(Id INT PRIMARY KEY AUTO_INCREMENT,Part CHAR(30), OP CHAR(30), Machine INT(10))""")
	#cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime) VALUES(%s,%s,%s,%s,%s)''', (machinenum,problem,priority,whoisonit,t)
	
	
	
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
	#month_st = month_st - 1
	year_st = t.year
	day_st = t.day
	
	#day_st = 10
	
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first

def vacation_set_current6(t):
	month_st = t.month
	year_st = t.year
	day_st = t.day
	day_st = day_st


	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first



def vacation_set_current5():  # Use this one to set Kiosk Date properly

	t = vacation_temp()


	month_st = t.month
	year_st = t.year
	day_st = t.day
	day_st = day_st
	hour_st = t.hour

	if int(hour_st) >= 3 and int(hour_st) <= 11:
		shift = "Mid"
	if int(hour_st) >11 and int(hour_st) <=19:
		shift = "Day"
	if int(hour_st) > 19 and int(hour_st) <24: 
		shift = "Aft"
	if int(hour_st) <3:
		shift = "Aft"
		day_st = day_st - 1
		

	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first, shift
	
def vacation_set_current3():

	t = vacation_temp()
	month_st = t.month
	#month_st = month_st - 1
	year_st = t.year
	day_st = t.day
	
	# Force it to start from June 19
	day_st = 19
	month_st = 7
	
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first

def vacation_set_current4(t):

	#t = vacation_temp()
	month_st = t.month
	#month_st = month_st - 1
	year_st = t.year
	day_st = t.day
	
	#day_st = 12
	
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
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation_backup""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS vacation_backup LIKE vacation""")
	#cursor.execute('''INSERT vacation_backup Select * From vacation''')

	#db.commit()
	db.close()
	return render(request,'done_test.html')

def vacation_rebuild(request):

	# backup Vacation Table
	db, cursor = db_open()  
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation_backup2""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS vacation_backup2 LIKE vacation_backup""")
	#cursor.execute('''INSERT vacation_backup2 Select * From vacation_backup''')

	#db.commit()
	db.close()
	return render(request,'done_test.html')
	
def vacation_restore(request):

	# backup Vacation Table
	db, cursor = db_open()  
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS vacation LIKE vacation_backup""")
	#cursor.execute('''INSERT vacation Select * From vacation_backup''')

	#db.commit()
	db.close()
	return render(request,'done_test.html')
	
def vacation_purge(request):

	# distinquish vacation entries that have different months
	db, cursor = db_open()  
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation_purge""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS vacation_purge LIKE vacation_backup2""")
	
	
	#cursor.execute('''INSERT vacation_purge Select * From vacation_backup2 where month_start != month_end ''')

	#db.commit()
	#db.close()
	return render(request,'done_test.html')
	
def vacation_purge_delete(request):

	# delete all entries with wrap dates
	db, cursor = db_open()  
	#dql = ('DELETE FROM vacation WHERE month_start != month_end ' )
	#cursor.execute(dql)
	#db.commit()
	db.close()

	return render(request,'done_test.html')

def message_create(request):

	# create Message Table
	db, cursor = db_open()  
	
	cursor.execute("""DROP TABLE IF EXISTS tkb_inventory_fixed""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_inventory_fixed LIKE tkb_jobs_test""")
	#cursor.execute('''INSERT vacation_backup Select * From vacation''')

	db.commit()
	db.close()
	return render(request,'done_test.html')

