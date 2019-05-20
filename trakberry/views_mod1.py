from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
from views_routes import direction
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
import MySQLdb
import time
from django.core.context_processors import csrf
import datetime as dt 
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current6, vacation_set_current5



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
	try:
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
	except:
		part = ""
	return part

# Generic Templay kickout for mtemp (headers) and mgmt_table_call which calls the sql required matching headers count
def mgmt_display(request):
	
	#request.session["mgmt_table_call"] = "SELECT id,asset_num,machine,partno,actual_produced,down_time,comments,pdate,shift,shift_hours_length,target FROM sc_production1"
	s1 = "SELECT "
	date_check = ['' for y in range(0)]
	ctr_var = 1
	request.session["date_check"] = 0
	for a in request.session["table_variables"]:
		s1 = s1 + a + ','
		if a == 'pdate':
			date_check.append(1)
		else:
			date_check.append(0)
		ctr_var = ctr_var + 1
	request.session["date_check"] = date_check
	s1 = s1[:-1]
	s1 = s1 + ' FROM ' + request.session["mgmt_table_name"] + " ORDER BY id DESC limit 20"
#	u = request.session['booboo']
	db, cur = db_open()

	cur.execute(s1)
	tmp = cur.fetchall()
	db.close()
	return render(request,'mgmt_display.html', {'tmp':tmp})	

def mgmt_display_edit(request,index):

	# request.session["table_headers"]  ==>  The name displayed on page 
	# request.session["table_variables"] ==> The name in the DB 

	p = ['' for y in range(0)]
	v = ['' for y in range(0)]
	datecheck = ['' for y in range(0)]
	a1 = ['' for y in range(0)]

	# call in to tmp the row to edit
	update_list = ''
	ctr = 0
	tmp_index = index
	db, cur = db_open() 
	sq1 = request.session["mgmt_table_call"] + "  where id = '%s'" %(tmp_index)
	cur.execute(sq1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]

	ptr = 1
	for x in tmp2:
		if type(x) is dt.date:
			y = vacation_set_current6(x)
#			current_first, shift  = vacation_set_current5()
			datecheck.append(1)
			v.append(y)
		else:
			datecheck.append(0)
			v.append(x)
		p.append(ptr)
		ptr = ptr + 1
		

	tmp3 = zip(p,v,datecheck)
	
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'mgmt_production_hourly'
				return direction(request)
		except:
			dummy = 1

#		return render(request,'kiosk/kiosk_test2.html',{'tmp':ddd})
		for i in tmp3:
			pst = str(i[0])
			b1 = request.POST.get(pst)
			b1=str(b1)
			c1 = '"' + b1 + '"'
			a1.append(c1)
		# Brilliant recursive algorithm to update known table with known variables
		tb1 = request.session["mgmt_table_name"]
		i1 = index
		db, cur = db_open()       # Open DB
		for x in request.session["table_variables"]:  # column names
			#  x ==>  name of column
			#  a1[ctr] ==> value of column
			col1 = x

			v1 = a1[ctr]
			v2 = v[ctr]
			if ctr == 0 :
				id1 = x
			if ctr > 0:
				zql = ("""update xx1 SET xx2=%s where xx3=%s"""%(v1,i1))
				index = zql.find('xx1')
				zql = zql[:index] + tb1 + zql[index+3:]
				index = zql.find('xx2')
				zql = zql[:index] + col1 + zql[index+3:]
				index = zql.find('xx3')
				zql = zql[:index] + id1 + zql[index+3:]
				cur.execute(zql)   # Execute SQL
				db.commit()
			ctr = ctr + 1
		db.close()
		request.session["route_1"] = request.session["mgmt_production_call"]
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request,'mgmt_display_edit.html', {'tmp':tmp3})	






