from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_mod2 import seperate_string, create_new_table,generate_string
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
from views_supervisor import supervisor_tech_call
import MySQLdb

from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
import time 

#import datetime as dt 
from django.core.context_processors import csrf


# Login for Maintenance Manager App
def forklift_login_form(request):	

	request.session["login_department"] = 'Forklift'
	request.session["forklift_names"] = forklift_manpower(request)
	request.session["forklift_login_name"] = ""
	request.session["forklift_switch"] = 0
	

#	if request.POST:
	if 'button1' in request.POST:
		request.session["forklift_login_name"] = request.POST.get("login_name")
		request.session["login_forklift_check"] = 1
		request.session["refresh_forklift"] = 1
		return render(request,'redirect_forklift.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop

	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["forlift_login_name"] = ""
	request.session['forklift_names'] = forklift_manpower(request)
	return render(request,'forklift_login_form.html', {'args':args})	

def forklift_logout(request):
	request.session["forklift_login_name"] = ''
	request.session["login_forklift_check"] = 0
	request.session["refresh_forklift"] = 0
	return render(request,'redirect_forklift.html')

def forklift_table_check(request):
	db, cursor = db_set(request)  
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_forklift(Id INT PRIMARY KEY AUTO_INCREMENT,employee CHAR(50), kiosk_id CHAR(50), area CHAR(50), message CHAR(100), call_time datetime, received_time datetime, closed TINYINT(10) default NULL,driver CHAR(100))""")
	db.commit()
	db.close()
	return 

def forklift_manpower(request):
	db, cursor = db_set(request)  
	dep = request.session['login_department']
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50),active1 INT(10) default 0)""")
	db.commit()
	sql = "SELECT user_name FROM tkb_logins WHERE department = '%s' ORDER BY user_name ASC" %(dep)  # Select only those in the department  (dep)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	return tmp

def forklift_close(request,index):
	request.session["forklift_index"] = index
	request.session["bounce3_switch"] = 1
	request.session["refresh_forklift"] = 0
	return render(request,'redirect_forklift.html')

def forklift_close_item(request):
	index=request.session["forklift_index"]
	driver = request.session["forklift_login_name"]
	db, cur = db_set(request)  		
	t = vacation_temp()
	tc = 1
	sql =( 'update tkb_forklift SET closed="%s" WHERE Id="%s"' % (tc,index))
	cur.execute(sql)
	db.commit()
	tql =( 'update tkb_forklift SET received_time="%s" WHERE Id="%s"' % (t,index))
	cur.execute(tql)
	db.commit()
	tql =( 'update tkb_forklift SET driver="%s" WHERE Id="%s"' % (driver,index))
	cur.execute(tql)
	db.commit()
	db.close()
	return render(request,"redirect_forklift.html")

def forklift(request):
	forklift_table_check(request)   #Check table exists
	# Initialize Request Sessions if they don't exist
	try:
		request.session["bounce3"] 
	except:
		request.session["bounce3"] = 0
	try:
		request.session["bounce3_switch"] 
	except:
		request.session["bounce3_switch"] = 0
	try:
		request.session["login_forklift"] 
	except:
		request.session["login_forklift"] = "none"
	try:
		request.session["login_forklift_check"] 
	except:
		request.session["login_forklift_check"] = 0
	try:
		request.session["refresh_forklift"] 
	except:
		request.session["refresh_forklift"] = 0

	# bounce2_switch is indicator if a message should pop up.  
	if request.session["bounce3_switch"] == 1:
		request.session["bounce3"] = 1
		request.session["bounce3_switch"] = 0
		request.session["refresh_forklift"] = 0
	
	else:
		request.session["bounce3"] = 0
		request.session["refresh_forklift"] = 1

	db, cursor = db_set(request)   
	sqlT = "Select Id,employee,kiosk_id,area,message,closed from tkb_forklift where closed IS NULL"
	cursor.execute(sqlT)
	request.session['forklift_jobs'] = cursor.fetchall()
	db.close()
	return render(request,"forklift.html")
