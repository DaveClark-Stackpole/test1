from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open

# *********************************************************************************************************
# MAIN KIOSK PAGE
# *********************************************************************************************************
# Kiosk Main Page.   Display buttons and route to action when they're pressed
def kiosk(request):
	
	# comment out below line to run local otherwise setting local switch to 0 keeps it on the network
	request.session["local_toggle"] = "/trakberry"
	
	db, cur = db_open()
	sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp
	db.close()
	request.session["tmp"] = tmp
	
	# Utilize variable route_1 and assign it a value to kick to another module.
	# that module needs to have a pattern defined in url.py because direction(request)
	# will route externally to it looking for the pattern.
	if request.POST:
		button_1 = request.POST
		button_pressed =int(button_1.get("kiosk_button1"))
		if button_pressed == -1:
			request.session["route_1"] = 'kiosk' # disable when ready to run
			#request.session["route_1"] = 'kiosk_job_assign' # enable when ready to run
			return direction(request)
			
		if button_pressed == -2:
			request.session["route_1"] = 'kiosk'   #disable when ready to run
			#request.session["route_1"] = 'kiosk_production' # enable when ready to run
			return direction(request)
			
		if button_pressed == -3:
			return kiosk_help(request)
		if button_pressed == -4:
			return kiosk_scrap(request)
			
		# If no button pressed...Probably should never get here
		return kiosk_none6(request)


	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,"kiosk/kiosk.html",{'args':args})

# *********************************************************************************************************
# Secondary Pages generated from Main Page Button Presses
# *********************************************************************************************************
# Kiosk Secondary page initiated by JOB button press on main page
def kiosk_job(request):
	if request.POST:
		button_1 = request.POST
		button_pressed = int(button_1.get("kiosk_button1"))
		if button_pressed == -1:
			request.session["route_1"] = 'kiosk_job_assign'
			return direction(request)
		if button_pressed == -2:
			request.session["route_1"] = 'kiosk_job_leave'
			return direction(request)
		return kiosk_done4(request)
	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_job.html",{'args':args})


def kiosk_production(request):
	job = ['' for x in range(6)]
	TimeOut = -1
	
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		request.session["clock"] = ""
		request.session["variable1"] = ""
		request.session["variable2"] = ""
		request.session["variable3"] = ""
		request.session["variable4"] = ""
		request.session["variable5"] = ""
		request.session["variable6"] = ""
		
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button2"))
			if kiosk_button1 == -2:
				request.session["route_1"] = 'kiosk'
				return direction(request)
		except:
			dummy = 1
			
#		pn_len = 3
#		a = '331'
#		db, cur = db_open()
#		bql = "SELECT * FROM sc_production1 WHERE asset_num = '%s' and LENGTH(partno)> '%d' ORDER BY %s %s" %(a,pn_len,'id','DESC')
#		cur.execute(bql)
#		tmp9 = cur.fetchall()
#		tmp8 = tmp9[0]
#		request.session["part17"] = tmp8[3]
#		db.close()		
#		return render(request, "kiosk/kiosk_test2.html",{'job':tmp9}) 
		
		
		try:
			db, cur = db_open()
			sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp1 = tmp2[0]
			
			
		
			try:
				pn_len = 3
				request.session["variable1"] = int(tmp1[4])
				aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s' and LENGTH(partno)> '%d' ORDER BY %s %s" %(int(tmp1[4]),pn_len,'id','DESC')
				cur.execute(aql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["part1"] = tmp4[3]
				
			except:
				request.session["part1"] = -1
				if len(tmp1[4])<2:
					request.session["variable1"] = 99
			try:
				request.session["variable2"] = int(tmp1[5])
				bql = "SELECT * FROM sc_production1 WHERE asset_num = '%s'ORDER BY %s %s" %(int(tmp1[5]),'id','DESC')
				cur.execute(bql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				tt = len(tmp4[3])
				if len(tmp4[3])>1:
					request.session["part2"] = tmp4[3]
				else:
					request.session["part2"] = -1
					
				#request.session["part2"] = tt
				#return render(request, "kiosk/kiosk_test2.html",{'ass':tt})
			
			except:
				request.session["part2"] = -1
				if len(tmp1[5]) < 2:
					request.session["variable2"] = 99
			try:
				request.session["variable3"] = int(tmp1[6])
				aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s'ORDER BY %s %s" %(int(tmp1[6]),'id','DESC')
				cur.execute(aql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				if len(tmp4[3])<1:
					request.session["part3"] = 0
				else:
					request.session["part3"] = tmp4[3]
				
			except:
				request.session["variable3"] = 99
			try:
				request.session["variable4"] = int(tmp1[7])
				dql = "SELECT * FROM sc_production1 WHERE asset_num = '%s'ORDER BY %s %s" %(int(tmp1[7]),'id','DESC')
				cur.execute(dql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["part4"] = tmp4[3]
				
			except:
				request.session["variable4"] = 99
				request.session["part4"] = -1
			try:
				request.session["variable5"] = int(tmp1[8])
				dql = "SELECT * FROM sc_production1 WHERE asset_num = '%s'ORDER BY %s %s" %(int(tmp1[8]),'id','DESC')
				cur.execute(dql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["part5"] = tmp4[3]
			except:
				request.session["variable5"] = 99
				request.session["part5"] = -1
			try:
				request.session["variable6"] = int(tmp1[9])
				dql = "SELECT * FROM sc_production1 WHERE asset_num = '%s'ORDER BY %s %s" %(int(tmp1[9]),'id','DESC')
				cur.execute(dql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["part6"] = tmp4[3]
			except:
				request.session["variable6"] = 99
				request.session["part6"] = -1
			
			db.close()
			
			#return render(request, "kiosk/kiosk_test2.html")
			
			request.session["clock"] = kiosk_clock
			request.session["route_1"] = 'kiosk_production_entry'
			return direction(request)
	
	
		except:
			#db, cur = db_open()
			#sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
			#cur.execute(sql)
			#tmp2 = cur.fetchall()
			#tmp1 = tmp2[0]
			
		
		
			#try:
	#		request.session["variable1"] = int(tmp1[4])
	#		aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s'ORDER BY %s %s" %(int(tmp1[4]),'id','DESC')
	#		cur.execute(aql)
	#		tmp3 = cur.fetchall()
	#		tmp4 = tmp3[0]
	#		request.session["part1"] = tmp4[2]
			
			request.session["route_1"] = 'kiosk_error_badclocknumber'
			return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_production.html",{'args':args})

def kiosk_production_entry(request):
	
	current_first, shift  = vacation_set_current5()
	#request.session["current_first"] = current_first
	
	
	kiosk_job = ['' for x in range(0)]
	kiosk_part = ['' for x in range(0)]
	kiosk_prod = ['' for x in range(0)]
	kiosk_hrs = ['' for x in range(0)]
	kiosk_dwn = ['' for x in range(0)]
	
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'kiosk'
				return direction(request)
		except:
			dummy = 1
			
		x_job = "job"
		x_part = "part"
		x_prod = "prod"
		x_hrs = "hrs"
		x_dwn = "dwn"
		
		kiosk_date = request.POST.get("date_en")
		kiosk_shift = request.POST.get("shift")
		
		for i in range(1,7): # Read in all the data entered for production into appropriate variables
		#try:
			x_job = x_job + str(i)
			x_part = x_part + str(i)
			x_prod = x_prod + str(i)
			x_hrs = x_hrs + str(i)
			x_dwn = x_dwn + str(i)
			kiosk_job.append(request.POST.get(x_job))
			kiosk_part.append(request.POST.get(x_part))
			kiosk_prod.append(request.POST.get(x_prod))
			kiosk_hrs.append(request.POST.get(x_hrs))
			kiosk_dwn.append(request.POST.get(x_dwn))
			
			x_job = "job"
			x_part = "part"
			x_prod = "prod"
			x_hrs = "hrs"
			x_dwn = "dwn"
			
		shift_time = "None"
		#except:
		#	dummy = 1
		if kiosk_shift=="Aft":
			shift_time="3pm-11pm"
		if kiosk_shift=="Day":
			shift_time="7am-3pm"
		if kiosk_shift=="Mid":
			shift_time="11pm-7am"
			
		#pprod = int(kiosk_prod[1])
		#pprod2 = int(kiosk_prod[0])
		
		# Empty variables
		xy = "_"
		zy = 0
		db, cur = db_open()
		
		for i in range(0,6):
			job = kiosk_job[i]
			part = kiosk_part[i]
			prod = kiosk_prod[i]
			hrs = kiosk_hrs[i]
			dwn = kiosk_dwn[i]
			clock_number = request.session["clock"]
			
			try:
				dummy = len(job)
				cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,xy,zy,zy,zy,zy,zy,xy))
				db.commit()
			except:
				dummy = 1
		
		TimeStamp = int(time.time())
		TimeOut = - 1
		cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,clock_number,TimeOut))
		cur.execute(cql)
		db.commit()
	
		db.close()
		

		
		# Below is to test variables
		#return render(request, "kiosk/kiosk_test2.html",{'job':kiosk_job,'part':pprod2,'prod':pprod,'hrs':kiosk_hrs,'dwn':kiosk_dwn}) 
		
		request.session["route_1"] = 'kiosk'
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/kiosk_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift})
	
def kiosk_help(request):
	return render(request, "kiosk/kiosk_help.html")

def flex_test(request):
	return render(request, "kiosk/flex_test.html")
	
def kiosk_scrap(request):
	return render(request, "kiosk/kiosk_scrap.html")
# *********************************************************************************************************


# *********************************************************************************************************
# Third Tier Pages generated from Secondary Page Button Presses
# *********************************************************************************************************
# Kiosk Third Tier page initiated by Job | Assign button press on Secondary Page
def kiosk_job_assign(request):

	db, cur = db_open()
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		kiosk_job1 = request.POST.get("job1")
		kiosk_job2 = request.POST.get("job2")
		kiosk_job3 = request.POST.get("job3")
		kiosk_job4 = request.POST.get("job4")
		kiosk_job5 = request.POST.get("job5")
		kiosk_job6 = request.POST.get("job6")
#		kiosk_job7 = request.POST.get("job7")
		
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'kiosk_job_assign'
				return direction(request)
		except:
			dummy = 1
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button2"))
			if kiosk_button1 == -2:
				request.session["route_1"] = 'kiosk'
				return direction(request)
		except:
			dummy = 1
		# Finished and reroute

		# Check if clock number is already assigned or not a valid clock number
		if kiosk_clock == "":
			request.session["route_1"] = 'kiosk_error_badclocknumber'
			return direction(request)
		#Assigned already Check
		ch = 0
		try:
			TimeOut = -1
			sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp1 = tmp2[0]
			ch = 1
		except:
			ch = 0
		if ch == 1:
			request.session["route_1"] = 'kiosk_error_assigned_clocknumber'
			return direction(request)
	
		# ???  Also add code here to see if this clock number is already on a job  ???
		#
		# ???  Also add code to see if this is a valid clock number   ???
		#
		# *********************************************************************
			
		# Check if any entry was one with a non numerical value.  If so reroute back to reset kiosk job assign
		job_empty = 0
		
		J = ['343' for x in range(6)]
		
		
	#	try:
		if kiosk_job1 !="":
			job_empty = 1
			request.session["kiosk_job1"] = (kiosk_job1)
			J[0] = kiosk_job1
		if kiosk_job2 !="":
			job_empty = 1
			request.session["kiosk_job2"] = (kiosk_job2)
			J[1] = kiosk_job2
		if kiosk_job3 !="":
			job_empty = 1
			request.session["kiosk_job3"] = (kiosk_job3)
			J[2] = kiosk_job3
		if kiosk_job4 !="":
			job_empty = 1
			request.session["kiosk_job4"] = (kiosk_job4)
			J[3] = kiosk_job4
		if kiosk_job5 !="":
			job_empty = 1
			request.session["kiosk_job5"] = (kiosk_job5)
			J[4] = kiosk_job5
		if kiosk_job6 !="":
			job_empty = 1
			request.session["kiosk_job6"] = (kiosk_job6)
			J[5] = kiosk_job6
			
			# Assign the request variables so they're stored upon transfer to other module
		request.session["kiosk_clock"] = kiosk_clock
		request.session["kiosk_job1"] = kiosk_job1
		request.session["kiosk_job2"] = kiosk_job2
		request.session["kiosk_job3"] = kiosk_job3
		request.session["kiosk_job4"] = kiosk_job4
		request.session["kiosk_job5"] = kiosk_job5
		request.session["kiosk_job6"] = kiosk_job6
			
		job_chk = 0
		try:
#				TimeOut = -1
			for i in range(0,5):
				request.session["kiosk_error"] = J[i]
				sql = "SELECT * FROM vw_asset_eam_lp WHERE left(Asset,4) = '%s'" %(J[i])
				cur.execute(sql)
				tmp2 = cur.fetchall()
				tmp1 = tmp2[0]
#				ch = 1
#			except:
#				ch = 0

	
			
			
		except:
			request.session["route_1"] = 'kiosk_error_badjobnumber'
			return direction(request)
#			request.session["route_1"] = 'kiosk_error_badjobnumber'
#			return direction(request)
		if job_empty == 0:
			request.session["route_1"] = 'kiosk_error_badjobnumber'
			return direction(request)
		# ***************************************************************************************************
		db.close()
		return kiosk_job_assign_enter(request)

	else:
		form = kiosk_dispForm3()
		
	
#	sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
#	cur.execute(sql)
#	tmp = cur.fetchall()
#	tmp2 = tmp
	db.close()
	tmp = request.session["tmp"]
	
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_job_assign.html",{'tmp':tmp,'args':args})

def kiosk_error_badjobnumber(request):
	request.session["route_1"] = 'kiosk_job_assign'
	return render(request, "kiosk/kiosk_error_badjobnumber.html")
def kiosk_error_badclocknumber(request):
	request.session["route_1"] = 'kiosk_job_assign'
	return render(request, "kiosk/kiosk_error_badclocknumber.html")
def kiosk_error_assigned_clocknumber(request):
	request.session["route_1"] = 'kiosk_job_assign'
	return render(request, "kiosk/kiosk_error_assigned_clocknumber.html")

def kiosk_job_assign_enter(request):
	
	db, cur = db_open()
	
	# Make the table if it's never been created
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_kiosk(Id INT PRIMARY KEY AUTO_INCREMENT,Clock INT(30), TimeStamp_In Int(20), TimeStamp_Out Int(20), Job1 CHAR(30), Job2 CHAR(30) , Job3 CHAR(30) , Job4 CHAR(30) , Job5 CHAR(30) , Job6 CHAR(30) )""")
	# Use below line as a break point to check things out
	#return render(request, "kiosk/kiosk_test.html")
	kiosk_clock = request.session["kiosk_clock"]
	kiosk_job1 = request.session["kiosk_job1"]
	kiosk_job2 = request.session["kiosk_job2"]
	kiosk_job3 = request.session["kiosk_job3"]
	kiosk_job4 = request.session["kiosk_job4"]
	kiosk_job5 = request.session["kiosk_job5"]
	kiosk_job6 = request.session["kiosk_job6"]
	TimeOut = -1
	
	
	
	TimeStamp = int(time.time())
	cur.execute('''INSERT INTO tkb_kiosk(Clock,Job1,Job2,Job3,Job4,Job5,Job6,TimeStamp_In,TimeStamp_Out) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (kiosk_clock,kiosk_job1,kiosk_job2,kiosk_job3,kiosk_job4,kiosk_job5,kiosk_job6,TimeStamp,TimeOut))
	db.commit()
	db.close()
	
	request.session["route_1"] = 'kiosk'
	return direction(request)

def kiosk_job_leave(request):
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		
		# Assign the request variables so they're stored upon transfer to other module
		request.session["kiosk_clock"] = kiosk_clock
		return kiosk_job_leave_enter(request)
	else:
		form = kiosk_dispForm3()

	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk/kiosk_job_leave.html",{'args':args})

def kiosk_job_leave_enter(request):
	db, cur = db_open()
	# Make the table if it's never been created
	
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_kiosk(Id INT PRIMARY KEY AUTO_INCREMENT,Clock INT(30), TimeStamp_In Int(20), TimeStamp_Out Int(20), Job1 CHAR(30), Job2 CHAR(30) , Job3 CHAR(30) , Job4 CHAR(30) , Job5 CHAR(30) , Job6 CHAR(30) )""")
	
	kiosk_clock = request.session["kiosk_clock"]
	
	TimeOut = -1
	#sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
	#cur.execute(sql)
	#tmp2 = cur.fetchall()
	#tmp1 = tmp2[0]

	#return render(request, "kiosk/kiosk_test.html",{'tmp':tmp})
	
	TimeStamp = int(time.time())
	cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,kiosk_clock,TimeOut))
	cur.execute(cql)
	db.commit()
	db.close()
	
	
	request.session["route_1"] = 'kiosk'
	return direction(request)
	
def manpower_layout(request):

	db, cur = db_open()
	TimeOut = -1
	id_limit = 211738
	part = '50-9341'
	sql = "SELECT DISTINCT asset_num,machine FROM sc_production1 WHERE partno = '%s' and id > '%s' ORDER BY %s %s " %(part,id_limit,'machine','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	
	TimeOut = -1
	mql = "SELECT Clock,Job1,Job2,Job3,Job4,Job5,Job6 FROM tkb_kiosk WHERE TimeStamp_Out = '%s'" %(TimeOut)
	cur.execute(mql)
	tmp2 = cur.fetchall()
	
	J = [[] for x in range(len(tmp))]
	ctr = 0
	for i in tmp:
		J[ctr].append(i[0])
		a = '---'
		
		for ii in tmp2:
			if ii[1] == i[0]:
				J[ctr].append(ii[0])
			else:
				J[ctr].append(a)
		ctr = ctr + 1
	
	return render(request, "kiosk/kiosk_test.html",{'tmp':J})
	
	
def manual_entry(request):	

	if request.POST:
        			
		asset_num = request.POST.get("asset_num")
		machine = request.POST.get("machine")
		priority = request.POST.get("priority")
		whoisonit = request.session["whoisonit"]
		partno = "50-6175"
		target = 215
		
		
		
		
		# call external function to produce datetime.datetime.now()
		createdtime = vacation_temp()
		
		# Select prodrptdb db located in views_db
		db, cur = db_open()
		cur.execute('''INSERT INTO sc_production1(asset_num,machine,partno,pdate,shift,shift_hours_length,target,createdtime,updatedtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (asset_num,machine,partno,pdate,shift,shift_hours_length,target,createdtime,createdtime))
		db.commit()
		db.close()
		
		return done(request)
		
	else:
		#request.session["machinenum"] = "692"
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'manual_entry.html', {'args':args})	
	
