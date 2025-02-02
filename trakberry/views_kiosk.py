from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5
from views_vacation import vacation_set_current77
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
import decimal
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open, db_set
from views_mod1 import kiosk_lastpart_find, kiosk_email_initial
from datetime import datetime

# *********************************************************************************************************
# MAIN KIOSK PAGE
# *********************************************************************************************************
# Kiosk Main Page.   Display buttons and route to action when they're pressed
def kiosk(request):
	request.session["route_1"] = 'kiosk_menu' # enable when ready to run
	return direction(request)


	# comment out below line to run local otherwise setting local switch to 0 keeps it on the network
	request.session["local_toggle"] = "/trakberry"
	request.session["kiosk_menu_screen"] = 1
	request.session["cycletime1"] = 0
	request.session["cycletime2"] = 0
	request.session["cycletime3"] = 0
	request.session["cycletime4"] = 0
	request.session["cycletime5"] = 0
	request.session["cycletime6"] = 0

	db, cur = db_set(request)
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
			#request.session["route_1"] = 'kiosk' # disable when ready to run
			request.session["route_1"] = 'kiosk_job_assign' # enable when ready to run
			
			return direction(request)
			
		if button_pressed == -2:
			#request.session["route_1"] = 'kiosk'   #disable when ready to run
			request.session["route_1"] = 'kiosk_production' # enable when ready to run
			return direction(request)
			
		if button_pressed == -3:
			request.session["route_1"] = 'hrly_display' # enable when ready to run

			return direction(request)
		if button_pressed == -4:
			request.session["route_1"] = 'kiosk_help_button' # enable when ready to run
			return direction(request)


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
	request.session["machine1"] = "1"
	request.session["machine2"] = "2"
	request.session["machine3"] = "3"
	request.session["machine4"] = "4"
	request.session["machine5"] = "5"
	request.session["machine6"] = "6"
	
	dummy2 = 1
	
	if dummy2 == 1:
#	if request.POST:
		kiosk_clock = request.session["current_clock"]
#		kiosk_clock = request.POST.get("clock")
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
				if request.session["kiosk_main_screen"] == 1:
					request.session["route_1"] = 'kiosk'
				else:
					request.session["route_1"] = 'kiosk_menu'
				return direction(request)
		except:
			dummy = 1
			
			
		db, cur = db_set(request)

		sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		tmp1 = tmp2[0]
		ppp = tmp1[4]

		try:
			sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp1 = tmp2[0]

			# Call kiosk_lastpart_find (in views_mod1 to get last part for all 6 parts  ***COOL CODE)
			# if no lastpart found then default to  "" for part 
			prt1 = kiosk_lastpart_find (tmp1[4])
			prt2 = kiosk_lastpart_find (tmp1[5])
			prt3 = kiosk_lastpart_find (tmp1[6])
			prt4 = kiosk_lastpart_find (tmp1[7])
			prt5 = kiosk_lastpart_find (tmp1[8])
			prt6 = kiosk_lastpart_find (tmp1[9])

			# ***************************************************************************************

			try:
				pn_len = 3
				request.session["variable1"] = int(tmp1[4])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[4],prt1)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part1"] = prt1
				request.session["machine1"] = tmpp[5]
				try:
					request.session["cycletime1"] = str(tmpp[4])
				except:
					request.session["cycletime1"] = 0

			except:
				request.session["part1"] = "None"
				request.session["machine1"] = "XX"
				if len(tmp1[4])<2:
					request.session["variable1"] = 99
			try:
				request.session["variable2"] = int(tmp1[5])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[5],prt2)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part2"] = prt2
				request.session["machine2"] = tmpp[5]
				try:
					request.session["cycletime2"] = str(tmpp[4])
				except:
					request.session["cycletime2"] = 0
	
			except:
				request.session["part2"] = "None"
				request.session["machine2"] = "XX"
				# request.session["variable2"] = int(tmp1[5])
				if len(tmp1[5]) < 2:
					request.session["variable2"] = 99
			try:
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s'" %(int(tmp1[6]))
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part3"] = prt3
				request.session["machine3"] = tmpp[5]
				request.session["variable3"] = int(tmp1[6])
				try:
					request.session["cycletime3"] = str(tmpp[4])
				except:
					request.session["cycletime3"] = 0
			except:
				request.session["part3"] = "None"
				request.session["machine3"] = "XX"
				if len(tmp1[6]) < 2:
					request.session["variable3"] = 99
					
			try:
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s'" %(int(tmp1[7]))
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part4"] = prt4
				request.session["machine4"] = tmpp[5]
				request.session["variable4"] = int(tmp1[7])
				try:
					request.session["cycletime4"] = str(tmpp[4])
				except:
					request.session["cycletime4"] = 0
			except:
				request.session["part4"] = "None"
				request.session["machine4"] = "XX"
				if len(tmp1[7]) < 2:
					request.session["variable4"] = 99
			try:
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s'" %(int(tmp1[8]))
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part5"] = prt5
				request.session["machine5"] = tmpp[5]
				request.session["variable5"] = int(tmp1[8])
				try:
					request.session["cycletime5"] = str(tmpp[4])
				except:
					request.session["cycletime5"] = 0
			except:
				request.session["part5"] = "None"
				request.session["machine5"] = "XX"
				if len(tmp1[8]) < 2:
					request.session["variable5"] = 99
			try:
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s'" %(int(tmp1[9]))
				cur.execute(sql)
				tmp = cur.fetchall()     
				tmpp = tmp[0]
				request.session["part6"] = prt6
				request.session["machine6"] = tmpp[5]
				request.session["variable6"] = int(tmp1[9])
				try:
					request.session["cycletime6"] = str(tmpp[4])
				except:
					request.session["cycletime6"] = 0
			except:
				request.session["part6"] = "None"
				request.session["machine6"] = "XX"
				if len(tmp1[9]) < 2:
					request.session["variable6"] = 99

			
			db.close()
			
			# return render(request, "kiosk/kiosk_test2.html")
			
			request.session["clock"] = kiosk_clock
			request.session["route_1"] = 'kiosk_production_entry'

			return direction(request)
	
	
		except:	
			#Problem is above
			request.session["route_1"] = 'kiosk_menu'
			return direction(request)
	
	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_production.html",{'args':args})

def manual_production_entry6(request):
	return render(request, "kiosk/kiosk_test.html")

def manual_production_entry3(request):
	
	current_first, shift  = vacation_set_current5()
	#request.session["current_first"] = current_first
	
	
	kiosk_job = ['' for x in range(0)]
	kiosk_part = ['' for x in range(0)]
	kiosk_prod = ['' for x in range(0)]
	kiosk_hrs = ['' for x in range(0)]
	kiosk_dwn = ['' for x in range(0)]
	kiosk_clock = ['' for x in range(0)] 
	
	if request.POST:
		
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
		sheet_id = 'kiosk'
		db, cur = db_set(request)
		
		for i in range(0,6):
			job = kiosk_job[i]
			part = kiosk_part[i]
			prod = kiosk_prod[i]
			hrs = kiosk_hrs[i]
			dwn = kiosk_dwn[i]
			clock_number = request.session["clock"]
			
			try:
				dummy = len(job)
				cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,xy,zy,zy,zy,zy,zy,zy))
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
		
		request.session["route_1"] = 'manual_production_entry'
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/manual_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift})
	
def manual_production_entry(request):
	pn_len = 3
	db, cur = db_set(request)
	current_first, shift  = vacation_set_current5()

	aql = "SELECT MAX(id)  FROM sc_production1" 
	cur.execute(aql)
	tmp3 = cur.fetchall()
	tmp4 = tmp3[0]
	tmp5 = tmp4[0]
	
	bql = "Select shift From sc_production1 WHERE id = '%d'" %(tmp5)
	cur.execute(bql)
	tmp3 = cur.fetchall()
	tmp4 = tmp3[0]
	kshift = tmp4[0]
	
	try:
		dql = "Select pdate From sc_production1 WHERE id = '%d'" %(tmp5)
		cur.execute(dql)
		tmp3 = cur.fetchall()
		tmp4 = tmp3[0]
		dt = tmp4[0]
		ddt = str(dt)
		current_first = ddt
	except:
		dummy = 1 
	
	if kshift=="3pm-11pm":
		shift="Aft"
	if kshift=="7am-3pm":
		shift="Day"
	if kshift=="11pm-7am":
		shift="Mid"
			
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'manual_production_entry'
				return direction(request)
		except:
			clock = request.POST.get("clock")
			ddate = request.POST.get("date_en")
			shift = request.POST.get("shift")
			job = request.POST.get("job")
			
			request.session["clock"] = clock
			request.session["date"] = ddate
			request.session["shift"] = shift
			request.session["job"]= job
			pn_len = 3

			db, cur = db_set(request)

#			New Code to find the current operation using cycletime table (It works and use when ready)
#			try:
#				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s'" %(job)
#				cur.execute(sql)
#				tmp = cur.fetchall()
#				tmpp = tmp[0]
#				request.session["machine"] = tmpp[5]
#			except:
#				request.session["machine"] = "XX"
#			if len(request.session["machine"])<2:
#				request.session["machine"] = "XX"

#			Below is the old code to find the current operation using latest entry
			try:
				aql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' " % (job)

#				aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s' and LENGTH(partno)> '%d' ORDER BY %s %s" %(job,pn_len,'id','DESC')
				cur.execute(aql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["machine"] = tmp4[5]
				
			except:
				request.session["machine"] = "XX"
				


			try:
				aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s' and LENGTH(partno)> '%d' ORDER BY %s %s" %(job,pn_len,'id','DESC')

				
				cur.execute(aql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["part"] = tmp4[3]
				
			except:
				request.session["part"] = "XX"
			db.close()
#			request.session["machine"] ='GF7 Stop All'
		#	return render(request,"kiosk/kiosk_test2.html")
			request.session["route_1"] = 'manual_production_entry2'
			return direction(request)
	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/manual_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift})
	
def manual_production_entry2(request):
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'manual_production_entry'
				return direction(request)
		except:
			part = request.POST.get("part")
			prod = request.POST.get("prod")
			hrs = request.POST.get("hrs")
			dwn = request.POST.get("down")
			mch = request.session['machine']
			
			clock_number = request.session["clock"]
			kiosk_date = request.session["date"] 
			kiosk_shift = request.session["shift"] 
			job = request.session["job"]
			
			if kiosk_shift=="Aft":
				shift_time="3pm-11pm"
			if kiosk_shift=="Day":
				shift_time="7am-3pm"
			if kiosk_shift=="Mid":
				shift_time="11pm-7am"
			
			
			db, cur = db_set(request)
		
			try:
				xy = "_"
				zy = 0
				
				dummy = len(job)
				try:
					kiosk_id = request.session["kiosk_id"]
				except:
					kiosk_id = "Unknown Kiosk"
				cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id,kiosk_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,mch,zy,zy,zy,zy,zy,xy,kiosk_id))
				db.commit()
			except:
				dummy = 1
				
				
			db.close()
			request.session["route_1"] = 'manual_production_entry'
			return direction(request)
	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/manual_production_entry2.html",{'args':args})


def kiosk_production_entry(request):
	
	current_first, shift  = vacation_set_current5()
	msg1 = "Fail"
	#request.session["current_first"] = current_first
	try:
		checkA = request.session["oa_check"] 
	except:
		request.session["oa_problem"] = ""
		request.session["oa_check"] = ""
		a1 = "oa_part"
		a2 = "oa_machine"
		a3 = "oa_variable"
		for a in range(1,7):
			b1 = a1 + str(a)
			b2 = a2 + str(a)
			b3 = a3 + str(a)
			request.session[b1] = ""
			request.session[b2] = ""
			request.session[b3] = ""
	
	kiosk_job = ['' for x in range(0)]
	oa_prob = ['' for x in range(0)]
	kiosk_part = ['' for x in range(0)]
	kiosk_prod = ['' for x in range(0)]
	kiosk_hrs = ['' for x in range(0)]
	kiosk_dwn = ['' for x in range(0)]
	kiosk_machine = ['' for x in range(0)]
	kiosk_ppm = ['' for x in range(0)]
	kiosk_target = ['' for x in range(0)]
	kiosk_low_production = [0 for x in range(0)]
	
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				TimeStamp = int(time.time())
				TimeOut = - 1
				
				try:
					db, cur = db_set(request)
					cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,kiosk_clock,TimeOut))
					cur.execute(cql)
					db.commit()
					db.close()
				except:
					dummy = 1
				if request.session["kiosk_menu_screen"] == 1:
					request.session["route_1"] = 'kiosk'
				else:
					request.session["route_1"] = 'kiosk_menu'

				return direction(request)
		except:
			dummy = 1
			
		x_job = "job"
		x_part = "part"
		x_prod = "prod"
		x_hrs = "hrs"
		x_dwn = "dwn"
		x_ppm = "ppm"

		
		kiosk_date = request.POST.get("date_en")
		kiosk_shift = request.POST.get("shift")
		
		for i in range(1,7): # Read in all the data entered for production into appropriate variables
		#try:
			x_job = x_job + str(i)
			x_part = x_part + str(i)
			x_prod = x_prod + str(i)
			x_hrs = x_hrs + str(i)
			x_dwn = x_dwn + str(i)
			x_ppm =x_ppm + str(i)

			kiosk_job.append(request.POST.get(x_job))
			kiosk_part.append(request.POST.get(x_part))
			temp_prod = request.POST.get(x_prod)
			if temp_prod == None or temp_prod == "":
				temp_prod = 0
			kiosk_prod.append(temp_prod)
			kiosk_hrs.append(request.POST.get(x_hrs))
			kiosk_dwn.append(request.POST.get(x_dwn))
			kiosk_ppm.append(request.POST.get(x_ppm))
			
			
			
			
			x_job = "job"
			x_part = "part"
			x_prod = "prod"
			x_hrs = "hrs"
			x_dwn = "dwn"
			x_ppm = "ppm"


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
		oa_check = 0
		part_check = 0
		write_answer = 0
		try:
			sheet_id = request.session["kiosk_type"]
		except:
			sheet_id = 'kiosk'

		# db, cur = kiosk_email_initial(request) # This Check will ensure the new columns are in and if not will add them
		db, cur = db_set(request)

		

		
		for i in range(0,6):
			job = kiosk_job[i]
			part = kiosk_part[i]
			prod = kiosk_prod[i]
			hrs = kiosk_hrs[i]
			dwn = kiosk_dwn[i]
			ppm = kiosk_ppm[i]
			low_production_variable = 0
			target1 = 0
			machine = ""
			clock_number = request.session["clock"]
			if i == 0 :
				m = request.session["machine1"]
				ct = request.session["cycletime1"]
			elif i ==1:
				m = request.session["machine2"]
				ct = request.session["cycletime2"]
			elif i ==2:
				m = request.session["machine3"]
				ct = request.session["cycletime3"]
			elif i ==3:
				m = request.session["machine4"]
				ct = request.session["cycletime4"]
			elif i ==4:
				m = request.session["machine5"]
				ct = request.session["cycletime5"]
			elif i ==5:
				m = request.session["machine6"]
				ct = request.session["cycletime6"]
			
			# Use try except to determine if there's a job for this loop
			try:
				if len(job) > 2:
					write_variable = 1
				else:
					write_variable = 0
			except:
				write_variable = 0
			if write_variable == 1:
				try:
					# db, cur = db_set(request)
					uql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(job,part)
					cur.execute(uql)
					ymp = cur.fetchall()
					ymp2 = ymp[0]
					ct = ymp2[4]
					# db.close()
				except:
					dummy = 7

				try:
					ppm = float(ppm)
					ct = (60 / ppm)
				except:
					dummy = 1
				h = float(hrs)

				# Fix to make sure someone didn't put a null amount in for downtime.  If so then make it 0
				try:
					test1 = int(dwn)
				except:
					dwn = 0
				# End of Fix
				
				hh = (h * 60 * 60) - (int(dwn) * 60)
				try:
					ct = float(ct)
					target1 = ((h * 60 * 60) / (ct))
					target2 = (hh / (ct))
				except:
					target1 = int(int(prod) / .85)
					target2 = target1
				test_prod = prod
				# Place the OA Check Code here **********************
				
				if target2 > 0:
					OA = int((int(test_prod) / float(target2)) * 100)
				else:
					OA = 0
				# return render(request,'kiosk/kiosk_test.html', {'OA':OA,'test_prod':test_prod,'target1':target1})	
				kiosk_target.append(int(target1))
				kiosk_machine.append(m)
				
				if OA < 70:
					# return render(request,'kiosk/kiosk_test.html', {'OA':OA})	
					oa_check = 1
					# oa_problem = request.session["oa_problem"]
					oa_problem =  "(" + str(job) + "):" + str(test_prod) + ' for ' + str(hrs) + 'hrs and ' + str(kiosk_dwn[(i)]) + ' down should be ' + str(int(target2*.7)) 
					oa_prob.append(oa_problem)
					low_production_variable = 2
                    
					
					# request.session["oa_problem"] = oa_problem
						# test = str.replace(test, '\n', '\r\n')

				if len(part) < 2:
					part_check = 1	
					part_check_job = job
			
								
			else:
				dummy = 1
				kiosk_target.append(None)
				kiosk_machine.append("")

			kiosk_low_production.append(low_production_variable) # It will be either 0 or 2 at this point
		
		request.session["oa_problem"] = oa_prob
		# Set bounce level
		# yyy = request.session["srgg"]	
		request.session["bounce"] = 0

		if oa_check == 1: 
			# bounce = 1
			bounce = 0 #  bypass error display for now
			write_answer = 1
			request.session["error_title"] = "Low Production"
			request.session["error_message"] = "Make sure that count, hrs run and downtime are correct!"
			request.session["oa_problem2"] = request.session["oa_problem"]
		if part_check == 1:
			bounce = 2
			request.session["error_title"] = "Error !"
			request.session["error_message"] = "Must Have a Part for every Job !"
			request.session["oa_problem2"] = "Machine " + part_check_job + " has no part listed for it."
			request.session["oa_problem"] = ""

		if request.session["check1"] == 1:  # bypass the presses
			bounce = 0
			write_answer = 1

		if part_check!=1 and oa_check != 1:
			bounce = 0
			write_answer = 1
		
		if bounce == 1 and request.session["oa_check"] == "Fail":
			request.session["oa_check"] = ""
			write_answer = 1
			bounce = 0
		if bounce > 0:
			request.session["bounce"] = bounce
			if bounce == 2:
				request.session["oa_check"] = ""
			else:
				request.session["oa_check"] = "Fail"
			request.session["OA_Curr"] = kiosk_date
			request.session["OA_Shift"] = kiosk_shift
			a1 = "oa_dwn"
			a2 = "oa_prod"
			a3 = "oa_hrs"
			a4 = "part"
			for a in range(1,7):
				b1 = a1 + str(a)
				b2 = a2 + str(a)
				b3 = a3 + str(a)
				b4 = a4 + str(a)
				request.session[b1] = kiosk_dwn[(a-1)]
				request.session[b2] = kiosk_prod[(a-1)]
				request.session[b3] = kiosk_hrs[(a-1)]
				request.session[b4] = kiosk_part[(a-1)]
			# yyy = request.session["srgg"]	

			request.session["route_1"] = 'kiosk_production_entry'
			return direction(request)

		# if oa_check != 1:
		# 	write_answer = 1
		# else:
		# 	if request.session["oa_check"] == "Fail":
		# 		request.session["oa_check"] = ""
		# 		write_answer = 1
		# 	else:
		# 		request.session["oa_check"] = "Fail"
		# 		request.session["OA_Curr"] = kiosk_date
		# 		request.session["OA_Shift"] = kiosk_shift
		# 		a1 = "oa_dwn"
		# 		a2 = "oa_prod"
		# 		a3 = "oa_hrs"
		# 		for a in range(1,7):
		# 			b1 = a1 + str(a)
		# 			b2 = a2 + str(a)
		# 			b3 = a3 + str(a)
		# 			request.session[b1] = kiosk_dwn[(a-1)]
		# 			request.session[b2] = kiosk_prod[(a-1)]
		# 			request.session[b3] = kiosk_hrs[(a-1)]
		# 		request.session["route_1"] = 'kiosk_production_entry'
		# 		return direction(request)
		
		if write_answer == 1:
			for i in range(0,6):
				job = kiosk_job[i]
				low_production = kiosk_low_production[i]
				try:
					dummy = len(job)
					write_variable = 1
				except:
					write_variable = 0
				if write_variable == 1:
					part = kiosk_part[i]
					prod = kiosk_prod[i]
					hrs = kiosk_hrs[i]
					dwn = kiosk_dwn[i]
					ppm = kiosk_ppm[i]
					m = kiosk_machine[i]
					target1 = kiosk_target[i]
					if sheet_id == 'manual':  # Set the variable to determine if we had to enter manually so we can email 
						manual_sent = 0
					else:
						manual_sent = 1
					try:
						kiosk_id = request.session["kiosk_id"]
					except:
						kiosk_id = "Unknown Kiosk"
					# y = y / 0
					cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id,Updated,low_production,manual_sent,kiosk_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,m,zy,zy,zy,target1,zy,sheet_id,zy,low_production,manual_sent,kiosk_id))
					db.commit()


			TimeStamp = int(time.time())
			TimeOut = - 1
			cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,clock_number,TimeOut))
			cur.execute(cql)
			db.commit()
			db.close()

		


	#	Below will route to Kiosk Main if it's a joint ipad or kiosk if it's a lone one
		if request.session["kiosk_menu_screen"] == 1:
			request.session["route_1"] = 'kiosk_menu'
		else:
			request.session["route_1"] = 'kiosk_menu'
		return direction(request)
	#
	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	db, cur = db_set(request)
	sql = "SELECT DISTINCT parts_no FROM sc_prod_parts ORDER BY %s %s" %('parts_no','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	# Error Check to see if this is the 2nd time through with a warning on OA 
	try:
		checkA = request.session["oa_check"] 
	except:
		request.session["oa_check"] = ""
		kiosk_defaults(request)

	if request.session["bounce"] > 0:
		current_first = request.session["OA_Curr"]
		shift = request.session["OA_Shift"]
	else:
		kiosk_defaults(request)


	# # #  Debug End Point   ************************************
	# debug_start = (request.session["debug_start"])
	
	# debug_end = (time.time())

	

	# request.session["debug_end"] = debug_end
	# debug_time = debug_end - debug_start
	# request.session["debug_time"] = debug_time
	# return render(request,'kiosk/kiosk_test2.html')
	# # *******************************************************

	#return render(request, "kiosk/kiosk_test5.html")
	try:
		oa_prob = request.session["oa_problem"]
	except:
		oa_prob = ""
	# Check if it's a CSD2 press .  If so go to kiosk_production_entryP where we use ppm otherwise kiosk_production_entry
	if request.session["check1"] == 1:
		return render(request, "kiosk/kiosk_production_entryP.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift,'Parts':tmp,'Msg1':msg1,'oa_problem':oa_prob})

	return render(request, "kiosk/kiosk_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift,'Parts':tmp,'Msg1':msg1,'oa_problem':oa_prob})
	
def kiosk_defaults(request):
	request.session["oa_check"] = ""
	request.session["oa_problem"] = ""
	a1 = "oa_dwn"
	a2 = "oa_prod"
	a3 = "oa_hrs"
	for a in range(1,7):
		b1 = a1 + str(a)
		b2 = a2 + str(a)
		b3 = a3 + str(a)
		request.session[b1] = 0
		request.session[b2] = None
		request.session[b3] = 8
	return

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

	request.session["ppm_check"] = 0
	request.session["check1"] = 0
	request.session["press1"] = 0
	request.session["press2"] = 0
	request.session["press3"] = 0
	request.session["press4"] = 0
	request.session["press5"] = 0
	request.session["press6"] = 0
	db, cur = db_set(request)
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		kiosk_job1 = request.POST.get("job1")
		kiosk_job2 = request.POST.get("job2")
		kiosk_job3 = request.POST.get("job3")
		kiosk_job4 = request.POST.get("job4")
		kiosk_job5 = request.POST.get("job5")
		kiosk_job6 = request.POST.get("job6")

		


	
		#check to see if it's a CSD2 Press entry and add PPM field for entry if it is.  Only look at 2 first characters as 27 is necessary
		if kiosk_job1[:2] == '27':
			request.session["check1"] = 1
			request.session["press1"] = 1
		if kiosk_job2[:2] == '27':
			request.session["check1"] = 1
			request.session["press2"] = 1
		if kiosk_job3[:2] == '27':
			request.session["check1"] = 1
			request.session["press3"] = 1
		if kiosk_job4[:2] == '27':
			request.session["check1"] = 1
			request.session["press4"] = 1
		if kiosk_job5[:2] == '27':
			request.session["check1"] = 1
			request.session["press5"] = 1
		if kiosk_job6[:2] == '27':
			request.session["check1"] = 1
			request.session["press6"] = 1	


		if kiosk_job1[:2] == '90':
			request.session["check1"] = 3
			request.session["insp1"] = 3
		if kiosk_job2[:2] == '90':
			request.session["check1"] = 3
			request.session["insp2"] = 3
		if kiosk_job3[:2] == '90':
			request.session["check1"] = 3
			request.session["insp3"] = 3
		if kiosk_job4[:2] == '90':
			request.session["check1"] = 3
			request.session["insp4"] = 3
		if kiosk_job5[:2] == '90':
			request.session["check1"] = 3
			request.session["insp5"] = 3
		if kiosk_job6[:2] == '90':
			request.session["check1"] = 3
			request.session["insp6"] = 3				


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
				
				if request.session["kiosk_menu_screen"] == 1:
					request.session["route_1"] = 'kiosk'
					
				else:
					request.session["route_1"] = 'kiosk_menu'
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
		
		
		# Commented out the check to see if someone is in kiosk and not signed out
#		try:
#			TimeOut = -1
#			sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
#			cur.execute(sql)
#			tmp2 = cur.fetchall()
#			tmp1 = tmp2[0]
#			ch = 1
#		except:
#			ch = 0
#		if ch == 1:
#			request.session["route_1"] = 'kiosk_error_assigned_clocknumber'
#			return direction(request)
#       End of section to check if someone is in kiosk and not signed out.

	

			
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
			dummy = 1
#				TimeOut = -1
			for i in range(0,5):
				request.session["kiosk_error"] = J[i]
#				sql = "SELECT * FROM vw_asset_eam_lp WHERE left(Asset,4) = '%s'" %(J[i])
#				cur.execute(sql)
#				tmp2 = cur.fetchall()
#				tmp1 = tmp2[0]
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

		return kiosk_job_assign_enter(request)

	else:
		form = kiosk_dispForm3()
		
	


	#sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
	sql = "SELECT asset FROM tkb_cycletime"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp
	db.close()
	request.session["tmp"] = tmp


#	sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
#	cur.execute(sql)
#	tmp = cur.fetchall()
#	tmp2 = tmp
	
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
	
	request.session["debug_start"] = time.time()

	db, cur = db_set(request)
	
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
	
	
	request.session["current_clock"] = kiosk_clock
	request.session["bounce"] = 0
	request.session["route_1"] = 'kiosk_production' # enable when ready to run

	return direction(request)
			
			
#	request.session["route_1"] = 'kiosk'
#	return direction(request)

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
	db, cur = db_set(request)
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

def tenr_fix2(request):
	db, cur = db_set(request)
	id1 = 418767
	part1 = '50-9341'
	asset = '1502'
	
	
	
	hql = "SELECT MAX(Id) FROM sc_production1 where partno = '%s'" %(part1)
	cur.execute(hql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[0]
	
	
	request.session["testvariable1"] = tmp3
	request.session["testvariable2"] = id1
	
	sql = "SELECT * FROM sc_production1 WHERE Id >= '%d' and Id<= '%d' and partno = '%s'" %(id1,tmp3,part1)
	cur.execute(sql)
	tmp2 = cur.fetchall()
	tmp1 = tmp2[0]
	
	for i in tmp2:
		asset1 = i[1]
		runtime1 = i[12]
		id1 = i[0]

		try:
			sql = "SELECT cycletime FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(asset1,part1)
			cur.execute(sql)
			tmp = cur.fetchall()
			tmpp = tmp[0]
			ct = tmpp[0]
			
			target1 = (runtime1 * 60 * 60) / ct
			
			cql = ('update sc_production1 SET target = "%s" WHERE Id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			

		except:
			dummy = 2

	return render(request, "done_update.html")
	
def tenr_fix3(request):
	# new
	prt = ['50-5128','50-5145','50-5132']

	db, cur = db_set(request)
	id1 = 437584
	
	for j in range (0,3):
		id1 = 437584
		part1 = prt[j]
		asset = '788'
#		if j == 2 :
#			return render(request, "done_update.html",{'temp1':part1})
		hql = "SELECT MAX(Id) FROM sc_production1 where partno = '%s'" %(part1)
		cur.execute(hql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		tmp3 = tmp2[0]

		sql = "SELECT * FROM sc_production1 WHERE Id >= '%d' and Id<= '%d' and partno = '%s'" %(id1,tmp3,part1)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		tmp1 = tmp2[0]

		for i in tmp2:
			asset1 = i[1]
			id1 = i[0]

			try:
				sql = "SELECT machine FROM tkb_cycletime WHERE asset = '%s'" %(asset1)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				ct = tmpp[0]
				cql = ('update sc_production1 SET machine = "%s" WHERE Id ="%s"' % (ct,id1))
				cur.execute(cql)
				db.commit()
			except:
				dummy = 2

	return render(request, "done_update.html")
	
def tenr_fix(request):
	db, cur = db_set(request)
	id1 = 438347
	p1 = '50-9341'
	sh1 = '01-10R'
	
	
	
	cql = ('update sc_production1 SET sheet_id = "%s" WHERE partno ="%s" and id > "%s"' % (sh1,p1,id1))
	cur.execute(cql)
	db.commit()
	
	
	#trg1 = 0
	#m1 = 'OP30'
	#cql = ('update sc_production1 SET target = "%s" WHERE partno ="%s" and id > "%s" and machine = "%s"' % (trg1,p1,id1,m1))
	#cur.execute(cql)
	#db.commit()
	
	

	return render(request, "done_update.html")


def manpower_layout(request):

	db, cur = db_set(request)
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
		db, cur = db_set(request)
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
	
def entry_recent(request):
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM sc_production ORDER BY id DESC limit 50" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close
	machine="Recent Machine Breakdowns"
	request.session["machine_search"] = machine
	request.session["tech_display"] = 1
	return render(request,"entry_recent_display.html",{'machine':tmp})
	

def manual_cycletime_table(request):
	
	db, cur = db_set(request)
	
	# Make the table if it's never been created
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_cycletime(Id INT PRIMARY KEY AUTO_INCREMENT,asset CHAR(30), timest Int(20), cycletime Int(20))""")


	db.commit()
	db.close()
	
	return render(request, "kiosk/kiosk_test.html")

def kiosk_sub_menu(request):
	if request.POST:
		button1 = request.POST
		bp1 = int(button1.get("kiosk_button1"))
		
		if bp1 == -1:
			pcell = 'TRI'
			hourly_title = 'Hourly Trilobe'
		if bp1 == -2:
			pcell = '10ROP30'
			hourly_title = 'Hourly 10ROP30'
		if bp1 == -3:
			pcell = '10R'
			hourly_title = 'Hourly 10R'
		if bp1 == -4:
			pcell = '9HP'
			hourly_title = 'Hourly 9HP'
		if bp1 == -5:
			pcell = '6LOutput'
			hourly_title = 'Hourly 6L Output'
		if bp1 == -6:
			pcell = 'GF9'
			hourly_title = 'Hourly GF9'
		if bp1 == -7:
			pcell = 'AB1V-INPUT'
			hourly_title = 'Hourly AB1V-Input'
		if bp1 == -8:
			pcell = 'AB1V-REACTION'
			hourly_title = 'Hourly AB1V-Reaction'
		if bp1 == -9:
			pcell = 'AB1V-OVERDRIVE'
			hourly_title = 'Hourly AB1V-Overdrive'


		request.session["pcell"] = pcell
		request.session["hourly_title"] = hourly_title



		request.session["route_1"] = 'kiosk_hourly_entry'
		return direction(request)

		


		
	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,"kiosk/kiosk_sub_menu.html",{'args':args})
	
		
def kiosk_menu(request):
	db, cursor = db_set(request) # This just sets the local link and DB 
	db.close()
	request.session["kiosk_menu_screen"] = 2
	request.session["cycletime1"] = 0
	request.session["cycletime2"] = 0
	request.session["cycletime3"] = 0
	request.session["cycletime4"] = 0
	request.session["cycletime5"] = 0
	request.session["cycletime6"] = 0
	try:
		test1 = request.session["whiteboard_message"] 
	except:
		request.session["whiteboard_message"] = ""

	if request.POST:
		button_1 = request.POST
		button_pressed =int(button_1.get("kiosk_button1"))
		if button_pressed == -1:  # This is the button for the white board
			try:
				y = request.session["dddd"]
				#request.session["pcell"]
			except:
				# Reroute to the submenu to pick the different cells
				# request.session["route_1"] = 'kiosk_menu'
				request.session["route_1"] = 'kiosk_sub_menu'
				return direction(request)

			#request.session["route_1"] = 'kiosk' # disable when ready to run
			request.session["route_2"] = 2
			request.session["route_3"] = 1
			request.session["route_1"] = 3 # enable when ready to run
			return direction(request)
			
		if button_pressed == -2:  # This is the button for the Production Entry
			request.session["route_3"] = 2
			#request.session["route_1"] = 'kiosk'   #disable when ready to run
			request.session["route_2"] = 2
			kiosk_defaults(request)
			request.session["route_1"] = 'kiosk_job_assign' # enable when ready to run
			# request.session["route_1"] = 'kiosk_name' # enable when ready to run
			return direction(request)

		if button_pressed == -3:
			return render(request, "kiosk/route_1.html")


		if button_pressed == -4:
			return render(request, "kiosk/route_2.html")
			

	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,"kiosk/kiosk_menu.html",{'args':args})


def ab1v_manpower(request):

	db, cur = db_set(request)  
	
	cur.execute("""DROP TABLE IF EXISTS tkb_ab1v""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_ab1v(Id INT PRIMARY KEY AUTO_INCREMENT,asset_num CHAR(30), machine CHAR(30), partno CHAR(30), actual_produced Int(20), comments CHAR(30), pdate date, shift CHAR(30)) """)

	id1 = 438221
	pd = '2019-04-00'
	part1 = '50-5145'
	part2 = '50-5132'
	part3 = '50-5128'
	machine1 = 'Cremer Furnace'
	sql = "SELECT * FROM sc_production1 WHERE partno = '%s' or partno = '%s' or partno = '%s'" %(part1,part2,part3)
	cur.execute(sql)
	tmp2 = cur.fetchall()

	for tmp1 in tmp2:
		cur.execute('''INSERT INTO tkb_ab1v(asset_num,machine,partno,actual_produced,comments,pdate,shift) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (tmp1[1],tmp1[2],tmp1[3],tmp1[4],tmp1[9],tmp1[10],tmp1[11]))
		db.commit()
		cday = tmp1[10]

	sql = "SELECT * FROM tkb_ab1v WHERE pdate > '%s' and machine != '%s' ORDER BY %s %s " %(pd,machine1,'pdate','ASC')
	cur.execute(sql)
	tmp2 = cur.fetchall()
	
	cur.execute("""DROP TABLE IF EXISTS tkb_ab1v""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_ab1v(Id INT PRIMARY KEY AUTO_INCREMENT,asset_num CHAR(30), machine CHAR(30), partno CHAR(30), actual_produced Int(20), comments CHAR(30), pdate date, shift CHAR(30)) """)


	for tmp1 in tmp2:
		day1 = tmp1[6]
		if tmp1[2] == "OP_Insp":
			total1 = tmp1[4]
		elif tmp1[2][:4] == 'OP10' :
			total1 = tmp1[4]
		
		else:
			total1 = 0
		if tmp1[2] == 'OP100':
			total1 = 0
		comments = tmp1[4]

		cur.execute('''INSERT INTO tkb_ab1v(asset_num,machine,partno,actual_produced,comments,pdate,shift) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (tmp1[1],tmp1[2],tmp1[3],total1,comments,tmp1[6],tmp1[7]))
		db.commit()

	db.close()
	return render(request, "done_update.html")

def kiosk_hourly_entry(request):
	request.session["hourly_drop"] = 'Hourly Trilobe'
	current_first, shift  = vacation_set_current5()
#	request.session["pcell"] = '10ROP30'

	if request.POST:
		kiosk_hourly_clock = request.POST.get("clock")
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				if request.session["kiosk_menu_screen"] == 1:
					request.session["route_1"] = 'kiosk'
				else:
					request.session["route_1"] = 'kiosk_menu'
				return direction(request)
		except:
			dummy = 1

		request.session["kiosk_hrs"] = 1

		kiosk_hourly_pcell = request.session["pcell"]

		#if request.session["pcell"] == "AB1V-INPUT":
	#		kiosk_hourly_pcell = request.POST.get("pcell")

		kiosk_hourly_date = request.POST.get("date_en")
		kiosk_hourly_shift = request.POST.get("shift")
		kiosk_hourly_clock = request.POST.get("clock")
		kiosk_hourly_hour = request.POST.get("hrs")
		kiosk_hourly_qty = request.POST.get("qty")
		kiosk_hourly_dtcode = request.POST.get("dtcode")
		kiosk_hourly_dtmin = request.POST.get("dtmin")
		kiosk_hourly_dtreason = request.POST.get("dtreason")

		# Easter Egg:  If you enter -2 for parts made (qty) then it takes Downtime Reason (dtreason) 
		# as the new kiosk_id then reverts back to main Kiosk Screen
		if int(kiosk_hourly_qty) == -2:
			request.session["kiosk_id"] = kiosk_hourly_dtreason
			request.session["route_1"] = 'kiosk_menu'
			return direction(request)


		
		# Store the data in request variables so we can reroute
		request.session["kiosk_hourly_pcell"] = kiosk_hourly_pcell
		request.session["kiosk_hourly_clock"] = kiosk_hourly_clock
		request.session["kiosk_hourly_date"] = kiosk_hourly_date
		request.session["kiosk_hourly_shift"] = kiosk_hourly_shift
		request.session["kiosk_hourly_hour"] = kiosk_hourly_hour
		request.session["kiosk_hourly_qty"] = kiosk_hourly_qty
		request.session["kiosk_hourly_dtcode"] = kiosk_hourly_dtcode
		request.session["kiosk_hourly_dtmin"] = kiosk_hourly_dtmin
		request.session["kiosk_hourly_dtreasonq"] = kiosk_hourly_dtreason

		kiosk_hourly_target = 1
		shift_target = 1
		shift_actual = 1
		shift_time = "None"
		sheet_id = 'kiosk'

		db, cur = db_set(request)
		stopp = "None"
		hr_var = int(kiosk_hourly_hour) # Set current hour looking at
		# try: # Check if there's an entry for this one already
		# 	hr_check = hr_var
		# 	sql = "SELECT * FROM sc_prod_hour WHERE p_cell = '%s' and p_date = '%s' and p_shift = '%s' and p_hour = '%s'" %(kiosk_hourly_pcell,kiosk_hourly_date,kiosk_hourly_shift,hr_check)
  		# 	cur.execute(sql)
  		# 	tmp2 = cur.fetchall()
		# 	tmp3 = tmp2[0]
		# 	stopp = "Duplicate"
		# except:
		# 	dummy = 1

		try: # Check if there's earlier entries
			hr_check = hr_var -1
			sql = "SELECT * FROM sc_prod_hour WHERE p_cell = '%s' and p_date = '%s' and p_shift = '%s' and p_hour = '%s'" %(kiosk_hourly_pcell,kiosk_hourly_date,kiosk_hourly_shift,hr_check)
  			cur.execute(sql)
  			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			stopp = "Earlier 1"
		except:
			dummy = 1

		# y = request.session["dkdd"]
		request.session["whiteboard_message"] = ""
		try:
			cur.execute('''INSERT INTO sc_prod_hour(p_cell,initial,p_date,p_shift,p_hour,hourly_actual,downtime_code,downtime_mins,downtime_reason) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (kiosk_hourly_pcell,kiosk_hourly_clock,kiosk_hourly_date,kiosk_hourly_shift,kiosk_hourly_hour,kiosk_hourly_qty,kiosk_hourly_dtcode,kiosk_hourly_dtmin,kiosk_hourly_dtreason))
			db.commit()
		except:
			dummy = 1
			request.session["whiteboard_message"] = "duplicate"
		db.close()

	
	#	Below will route to Kiosk Main if it's a joint ipad or kiosk if it's a lone one
		if request.session["kiosk_menu_screen"] == 1:
			request.session["route_1"] = 'kiosk'
		else:
			request.session["route_1"] = 'kiosk_menu'
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	p_cell = request.session["pcell"]

	db, cur = db_set(request)
	s1 = "SELECT MAX(id)  FROM sc_prod_hour WHERE p_cell = '%s'" %(p_cell) 
	cur.execute(s1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[0]

	s2 = "SELECT * From sc_prod_hour WHERE id = '%s'" %(tmp3) 
	cur.execute(s2)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[2]


	request.session["clock"] = tmp3

	# Below will set hrs , shift and date to current one using 30min past hour as flip point
	hrs, shift2, current_first = vacation_set_current77()

	# hrs = int(tmp2[6])
	# hrs = hrs + 1
	# hrs = ah


	# if hrs > 8:
	# 	if request.session["hourly_title"] == 'Hourly Trilobe':
	# 		if hrs > 12:
	# 			hrs = 1
	# 	else:
	# 		hrs = 1

	request.session["hrs"] = str(hrs)
	kiosk_hourly_shift = tmp2[5]
	#h = request.session["bugbug"]

	request.session["shift"] = tmp2[5]
	request.session["shift"] = shift2
#	if kiosk_hourly_shift=="4D":
#		request.session["shift"] = "Day"
#	elif kiosk_hourly_shift == "3N":
#		request.session["shift"] = "Mid"
#	elif kiosk_hourly_shift == "2CD":
#		request.session["shift"] = "Day"
#	elif kiosk_hourly_shift == "5A":
#		request.session["shift"] = "Aft"
	db.close()


	return render(request, "kiosk/kiosk_hourly_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first})

def tenr1(request):
	request.session["pcell"] = '10ROP30'
	request.session["hourly_title"] = 'Hourly 10ROP30'
	request.session["mgmt_login_password"] = 'bort'
	request.session["mgmt_login_name"] = 'Dave'
	return render(request, "done_update2.html")
def trilobe(request):
	request.session["pcell"] = 'TRI'
	request.session["hourly_title"] = 'Hourly Trilobe'
	request.session["kiosk_label"] = 'B'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")
def tenr2(request):
	request.session["pcell"] = '10R'
	request.session["hourly_title"] = 'Hourly 10R'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")

def kiosk_initial_6L_Output(request):
	request.session["pcell"] = '6LOutput'
	request.session["hourly_title"] = 'Hourly 6L Output'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_9HP(request):
	request.session["pcell"] = '9HP'
	request.session["hourly_title"] = 'Hourly 9HP'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_6L_IN(request):
	request.session["pcell"] = '6L_IN'
	request.session["hourly_title"] = 'Hourly 6L Input'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_GF9(request):
	request.session["pcell"] = 'GF9'
	request.session["hourly_title"] = 'Hourly GF9'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_AB1V(request):
	request.session["pcell"] = 'AB1V-INPUT'
	request.session["hourly_title"] = 'Hourly AB1V'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	

def error_hourly_duplicate(request):
	return render(request, "error_hourly_duplicate.html")	

def kiosk_fix55(request):
	ts = 1562849834
	ty = -1
	db, cur = db_set(request)
	cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE TimeStamp_Out ="%s"' % (ts,ty))
	cur.execute(cql)
	db.commit()
	return render(request, "error_hourly_duplicate.html")	

def kiosk_manual(request):
	request.session["kiosk_type"] = "manual"
	request.session["route_1"] = 'kiosk_menu'
	return direction(request)
def kiosk_kiosk(request):
	request.session["kiosk_type"] = "kiosk"
	request.session["route_1"] = 'kiosk_menu'
	return direction(request)


def kiosk_fix44(request):
	db, cur = db_set(request)
	ml = 4
	id1 = 475199

	s1 = "SELECT * From sc_production1 WHERE length(partno) < '%s' and id > '%d'" %(ml,id1)
	# s1 = "SELECT MAX(id)  FROM sc_prod_hour WHERE p_cell = '%s'" %(p_cell) 
	cur.execute(s1)
	tmp = cur.fetchall()
	

	for i in tmp:
		machine1 = i[1]
		id2 = i[0]
		prt1 = kiosk_lastpart_find (machine1)
		cql = ('update sc_production1 SET partno = "%s" WHERE id ="%d"' % (prt1,id2))
		cur.execute(cql)
		db.commit()
	db.close()



	# request.session["tmp6"] = tmp
	# tmp3 = tmp2[0]

	# s2 = "SELECT * From sc_prod_hour WHERE id = '%s'" %(tmp3) 
	# cur.execute(s2)
	# tmp = cur.fetchall()
	# tmp2 = tmp[0]
	# tmp3 = tmp2[2]
	# uu = request.session["ddss"]


	return render(request, "kiosk/kiosk_test5.html",{'tmp1':tmp})	


def kiosk_help(request):
	db, cursor = db_set(request)  
	closed1 = 0
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_help(Id INT PRIMARY KEY AUTO_INCREMENT,employee CHAR(50), kiosk_id CHAR(50), supervisor CHAR(50), help_message CHAR(100), help_date datetime, closed INT(10) default 0)""")
	db.commit()
	sql = "SELECT * FROM tkb_help WHERE closed = '%d' ORDER BY help_date ASC" %(closed1)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	return tmp

def kiosk_help_close(request):    # Close out kiosk help message
	kiosk_help_index = int(request.session['bounce_help_index'])
	kiosk_closed = 1
	db, cursor = db_set(request)  
	cql = ('update tkb_help SET closed = "%s" WHERE Id ="%d"' % (kiosk_closed, kiosk_help_index))
	cursor.execute(cql)
	db.commit()
	db.close()
	request.session['bounce_help'] = 0
	return render(request, "redirect_supervisor.html")

def kiosk_help_form(request):
	# Hard Code Supervisors for now.   Will use a DB List eventually
	supervisors = ['Karl Edwards','Andrew Smith','Scott McMahon','Gary Harvey','Pete Murphy','Raid Biram', 'Scott Brownlee','Ken Frey','Mike Clarke']
	request.session['supervisor_list'] = supervisors
	length_fail = 0
	tmp = kiosk_help(request)  # Retieve unclosed files and initialize table for kiosk_help
	if request.POST:
		help_employee = request.POST.get("help_employee")
		help_supervisor = request.POST.get("help_supervisor")
		help_message = request.POST.get("help_message")

		if len(help_supervisor) < 3 :length_fail = 1
		if len(help_employee) < 1 :length_fail = 1

		if length_fail == 1 : return render(request, "redirect_kiosk_help.html")
		try:
			help_kiosk_id = request.session["kiosk_id"]
		except:
			help_kiosk_id = 'unknown'
		t = vacation_temp()
		db, cursor = db_set(request) 
		cursor.execute('''INSERT INTO tkb_help(employee,supervisor,help_date,kiosk_id,help_message) VALUES(%s,%s,%s,%s,%s)''', (help_employee,help_supervisor,t,help_kiosk_id,help_message))
		db.commit()
		db.close()

		return render(request, "redirect_kiosk.html")
		# return kiosk_help_send(request)

	else:
		form = kiosk_dispForm3()

	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk_help_form.html",{'args':args})

def kiosk_forklift(request):
	db, cursor = db_set(request)  
	closed1 = 0
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_forklift(Id INT PRIMARY KEY AUTO_INCREMENT,employee CHAR(50), kiosk_id CHAR(50), area CHAR(50), message CHAR(100), call_time datetime, received_time datetime, closed TINYINT(10) default NULL,driver CHAR(100))""")
	db.commit()
	sql = "SELECT * FROM tkb_forklift WHERE closed = '%d' ORDER BY call_time ASC" %(closed1)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	return tmp

def kiosk_forklift_form(request):
	length_fail = 0
	tmp = kiosk_forklift(request)  # Retieve unclosed files and initialize table for kiosk_help
	if request.POST:
		forklift_employee = request.POST.get("forklift_employee")
		forklift_area = request.POST.get("forklift_area")
		forklift_message = request.POST.get("forklift_message")

		if len(forklift_employee) < 3 :length_fail = 1
		if len(forklift_area) < 3 :length_fail = 1

		if length_fail == 1 : return render(request, "redirect_kiosk_help.html")
		try:
			forklift_kiosk_id = request.session["kiosk_id"]
		except:
			forklift_kiosk_id = 'unknown'
		t = vacation_temp()
		db, cursor = db_set(request) 
		cursor.execute('''INSERT INTO tkb_forklift(employee,kiosk_id,area,message,call_time) VALUES(%s,%s,%s,%s,%s)''', (forklift_employee,forklift_kiosk_id,forklift_area,forklift_message,t))
		db.commit()
		db.close()

		return render(request, "redirect_kiosk.html")
		# return kiosk_help_send(request)

	else:
		form = kiosk_dispForm3()

	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk_forklift_form.html",{'args':args})

def set_test1(request):
	d = 0
	try:
		d = 1
		dummy = request.session["route_a6"] 
	except:
		d = 2
		request.session["route_a6"] = 1


	x = int(request.session["route_a6"])
	x = x + 1
	y = (x % 3) + 1
	request.session["route_a6"] = y

	# re = request.session["jjek"]

	return render(request,"done_update2.html")

