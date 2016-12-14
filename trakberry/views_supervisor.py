from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import sup_downForm, sup_dispForm, sup_closeForm, report_employee_Form, sup_vac_filterForm
from trakberry.views import done
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
from django.http import QueryDict
import MySQLdb
import json
import time 

from time import mktime
from datetime import datetime, date

from views_db import db_open

from django.core.context_processors import csrf

def hour_check():
	# obtain current date from different module to avoid datetime style conflict

	h = 7
	m = 0
	ch = 0
	send_email = 0
	t=int(time.time())
	tm = time.localtime(t)
	min = tm[4]
	hour = tm[3]
	current_date = find_current_date()
	#if min > m:
	if hour >= h and min > m:
		ch = 1

	db, cursor = db_open()  
	try:
		sql = "SELECT checking FROM tkb_email_conf where date='%s'" %(current_date)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		checking = tmp2[0]
	except:
		checking = 0
		cursor.execute('''INSERT INTO tkb_email_conf(date) VALUES(%s)''', (current_date))
		db.commit()
		tmp2 = 0

	if ch == 1 and checking == 0:
		checking = 1
		pql =( 'update tkb_email_conf SET checking="%s" WHERE date="%s"' % (checking,current_date))
		cursor.execute(pql)
		db.commit()
		tql = "SELECT sent FROM tkb_email_conf where date='%s'" %(current_date)
		cursor.execute(tql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		sent = tmp2[0]
		if sent == 0:
			sent = 1
			rql =( 'update tkb_email_conf SET sent="%s" WHERE date="%s"' % (sent,current_date))
			cursor.execute(rql)
			db.commit()
			send_email = 1				
	db.close()	
	return send_email
	
def supervisor_display(request):

#   Below is a check to send an email for downtime once a day.  
#   It is disabled now as a crontab has been put in place on the server side
#	send_email = hour_check()
#	if send_email == 1:
#		return render(request, "email_downtime.html")
	try:
		request.session["login_supervisor"] 	
	except:
		request.session["login_supervisor"] = "none"
		
  # initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
	c = []
	date = []
	prob = []
	job = []
	priority = []
	id = []
	machine = []
	count = []
	tmp2=[]
	smp2=[]
	mach_cnt = []
	whos = []
	box_colour = []
   
  # Select prodrptdb db 
	# Select prodrptdb db located in views_db
	db, cursor = db_open()

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	
	c = ["tech","Jim Barker"]

	
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	SQ_Sup = "SELECT * FROM pr_downtime1 where closed IS NULL" 

	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	
	ctr = 0
	for x in tmp:
	
		
		clr = "blue"
		if ctr > 3:
			clr = "red"
		tmp2 = (tmp[ctr])
		# assign job date and time to dt
		dt = tmp2[2]
		dt_t = time.mktime(dt.timetuple())
		# assign current date and time to dtemp
		dtemp = vacation_temp()
		dtemp_t = time.mktime(dtemp.timetuple())
		# assign d_diff to difference in unix
		d_diff = dtemp_t - dt_t
		
		if d_diff < 1801:
			clr = "green"
		elif d_diff < 3601:
			clr = "yellow"
		elif d_diff < 10801:
			clr = "red"
		elif d_diff < 86400:
			clr = "black"
		else:
			clr = "#DB2602"
			
		temp1_job = tmp2[0]
		temp2_job = temp1_job[:15]
		job.append(temp2_job)
		prob.append(tmp2[1])
		
		priority.append(tmp2[3])
		id.append(tmp2[11])
		whos.append(tmp2[4])
		box_colour.append(clr)
		ctr = ctr + 1
		
	for i in range(0, ctr-1):
		for ii in range(i+1, ctr):
			if (priority[ii]) < (priority[i]):
				jjob = job[i]
				job[i] = job[ii]
				job[ii] = jjob
				pprob = prob[i]
				prob[i] = prob[ii]
				prob[ii] = pprob
				pprior = priority[i]
				priority[i] = priority[ii]
				priority[ii] = pprior
				iid = id[i]
				id[i] = id[ii]
				id[ii]= iid
				wwhos = whos[i]
				whos[i] = whos[ii]
				whos[ii] = wwhos
				bbox_colour = box_colour[i]
				box_colour[i] = box_colour[ii]
				box_colour[ii] = bbox_colour
	
	list = zip(job,prob,id,whos,priority,box_colour)	
	db.close()
	n = "none"
	
	# Set Form Variables 
	if request.POST:
		request.session["test"] = 999
		a = request.POST
		b=int(a.get("one"))
		if b == -1:
			return done(request)
		if b == -2:
			request.session["call_route"] = 'supervisor'
			request.session["url_route"] = 'main.html'
			return done_tech(request)
		if b == -3:
			return done_elec(request)	
		request.session["index"] = b
		#request.session["test"] = request.POST
		return done_edit(request)
	else:
		form = sup_dispForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
		
		
  # call up 'display.html' template and transfer appropriate variables.  
	return render(request,"supervisor.html",{'L':list,'N':n,'args':args})
def sup_d(request):
	return supervisor_display(request)
	
def supervisor_tech_call(request):
	request.session["whoisonit"] = 'tech'
	
	return supervisor_down(request)

def supervisor_elec_call(request):
	request.session["whoisonit"] = 'maintenance'
	return supervisor_down(request)

def supervisor_main_call(request):
	request.session["whoisonit"] = 'maintenance'
	return supervisor_down(request)	
	
def supervisor_down(request):	

	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		whoisonit = request.session["whoisonit"]
		
		# call external function to produce datetime.datetime.now()
		t = vacation_temp()
		
		# Select prodrptdb db located in views_db
		db, cur = db_open()
		cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime) VALUES(%s,%s,%s,%s,%s)''', (machinenum,problem,priority,whoisonit,t))
		db.commit()
		db.close()
		
		return done(request)
		
	else:
		request.session["machinenum"] = "692"
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	rlist = machine_list_display()
	#request.session["login_tech"] = "none"
	return render(request,'supervisor_down.html', {'List':rlist,'args':args})	


# Module to edit entry	
def supervisor_edit(request):	
	index = request.session["index"]
	# Select prodrptdb db located in views_db
	db, cursor = db_open()
	SQ_Sup = "SELECT * FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	tmp2=tmp[0]
	request.session["machinenum"] = tmp2[0]
	request.session["problem"] = tmp2[1]
	request.session["priority"] = tmp2[3]
	db.close()	
	
	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		whoisonit = 'tech'
		
		a = request.POST
		b=int(a.get("one"))
		
		db, cursor = db_open()
		cur = db.cursor()
		
		if b==-3:
			mql =( 'update pr_downtime1 SET machinenum="%s" WHERE idnumber="%s"' % (machinenum,index))
			cur.execute(mql)
			db.commit()
			tql =( 'update pr_downtime1 SET problem="%s" WHERE idnumber="%s"' % (problem,index))
			cur.execute(tql)
			db.commit()
			uql =( 'update pr_downtime1 SET priority="%s" WHERE idnumber="%s"' % (priority,index))
			cur.execute(uql)
			db.commit()
			db.close()

		if b==-2:
			tc = "Troubleshooting"
			request.session["tech_comment"] = tc
			t = vacation_temp()
			sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
			cur.execute(sql)
			db.commit()
			tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
			cur.execute(tql)
			db.commit()
			db.close()
		
		if b==-1:
			return done_sup_close(request)
		

		return done(request)
#		return render(request, "test.html", {'machine':machinenum , 'y':b})
		
	else:	
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'supervisor_edit.html', args)		

def done_tech(request):
	#request.session["test"] = 78
	return render(request, "done_tech.html")
def done_elec(request):
	#request.session["test"] = 78
	return render(request, "done_elec.html")	
def done_edit(request):
	return render(request, "done_edit.html")	
	
def done_sup_close(request):
	return render(request, "done_sup_close.html")	
	
def sup_close(request):
	if request.POST:
		tc = request.POST.get("reason")	
		index = request.session["index"]
		t = vacation_temp()
		# Select prodrptdb db located in views_db
		db, cur = db_open()
		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
		cur.execute(tql)
		db.commit()
		db.close()		

		return done(request)
		
	else:
		form = sup_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'sup_close.html', args)			
	
def employee_vac_enter_init(request, index):	
	tmp = index
	month = request.session["current_month"]
	try:
		year_st = request.session["current_year"]
	except:
		year_st = 2016

	
	if int(month)<10:
		current_first = str(year_st) + "-" + "0" + str(month) 
	else:
		current_first = str(year_st) + "-" + str(month) 	
		
	if int(tmp)<10:
		current_first = current_first + "-" + "0" + str(tmp)
	else:
		current_first = current_first + "-" + str(tmp)
		
	request.session["current_first"] = current_first
	return employee_vac_enter(request)

def employee_vac_enter_init2(request):	
	current_first = vacation_set_current2()
	request.session["current_first"] = current_first
	return employee_vac_enter(request)
	
	
# Employee Vacation Entry Form **************************	
def employee_vac_enter(request):
	curr = request.session["current_first"]
	try:
		request.session["date_st"]
		request.session["date_en"]
		request.session["employee"]
		request.session["shift"]
		request.session["typee"]
#		request.session["Id"]
		
	except:
		request.session["date_st"] = ""
		request.session["date_en"] = ""
		request.session["employee"]= ""
		request.session["shift"]= ""
		request.session["typee"] = ""
#		request.session["Id"] = ""	
	
	if request.POST:

		request.session["date_st"] = request.POST.get("date_st")
		request.session["date_en"] = request.POST.get("date_en")
		request.session["employee"] = request.POST.get("employee")
		request.session["shift"] = request.POST.get("shift")
		request.session["typee"] = request.POST.get("typee")

#		request.session["Id"] = request.POST.get("Id")
		
		return vacation_entry(request)
		
	else:
		form = report_employee_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'employee_vac_form.html',{'Curr':curr,'args':args})		



def vacation_entry(request):	
    
	st = request.session["date_st"]
	fi = request.session["date_en"]
	employee = request.session["employee"]
	shift = request.session["shift"]
	typee = request.session["typee"]
#	idn = request.session["Id"]
	if typee == 'cover':
		ty = 1
	else:
		ty = 0	
		
	date_st = datetime.strptime(st, '%Y-%m-%d')
	try:
		date_fi = datetime.strptime(fi, '%Y-%m-%d')
	except:
		date_fi = datetime.strptime(st, '%Y-%m-%d')
			
	month_st = date_st.month
	year_st = date_st.year
	day_st = int(date_st.day)
	day_fi = int(date_fi.day)
	mnt_start = int(date_st.month)
	mnt_end = int(date_fi.month)

	one = 1
	one_end = 31
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_last = str(year_st) + "-" + str(month_st) + "-" + str(one_end)
	
	# Set variables so Calander will start on this month and year after the edit.
	request.session["month"] = month_st
	request.session["year"] = year_st
	request.session["month_pick"] = 1
	
	#if int(day_st)<10:
	
	#	day_st = '0'+ day_st
	
	
	
	
	# Select prodrptdb db located in views_db
	
	#if day_st > day_fi:
	#	day_fi_temp = 31
	#	db, cur = db_open() 
	#	cur.execute('''INSERT INTO vacation(employee,shift,start,end,day_start,day_end,type) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (employee,shift,st,fi,day_st,day_fi_temp,ty))
	#	db.commit()
	#	db.close()
	#	day_st = 1
	
	
		
	db, cur = db_open() 	
	cur.execute('''INSERT INTO vacation(employee,shift,start,end,day_start,day_end,type,month_start,month_end) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (employee,shift,st,fi,day_st,day_fi,ty,mnt_start,mnt_end))
	db.commit()
	
	sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	
#	for x in tmp:
#		x_date = x[3]
		#x_date = datetime.strptime(x[3], '%Y-%m-%d')
#		x_day = x_date.day
#		x[3] = x_day

	# return to vacation_display once update is complete
	
	# Below code to reset Filter to Login Name's default every time
	#login_name = request.session["login_name"]
	#login_initial(request,login_name)
	
	
	#return vacation_display(request)
	return render(request,'testtest.html')
	
	# The below code was old code for entry finish but
	# it caused unfavourable results
	
	#dday, ctr, mnth = vacation_calander_init(month_st)
	#List = zip(ctr,dday)
	#return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Tmp':tmp,'Month_Number':month_st})


def vacation_month_fix(request):
	db, cur = db_open()
	
	
	a = 0
	
	
	cur.execute("SELECT * FROM vacation where month_start = '%s'" %(a))
	
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	num = cur.rowcount

	
	for x in xrange(0,num):
		
		tmp2 = tmp[x]
		ds = tmp2[2]
		de = tmp2[3]
		h = 999
		i = tmp2[6]
		h = ds.month
		try:
			j = de.month
		except:
			j = h
		if j == 0:
			j = h
		
		cur.execute("UPDATE vacation SET month_start = '%s', month_end = '%s' WHERE id_number = '%s'"% (h,j,i))
		db.commit()
		
	#db.commit()
	db.close()
	i = h
	
	return render(request,'test4.html',{'X':h})
	
	#for k in range(city_count):
    #cur.execute("UPDATE hqstock SET citylastprice = '%s' WHERE id = '%s'"% (CITYPRICE[k],   tID[k]))
    #cur.commit()

def reset_sfilter(request):
	request.session["sfilter1"] = ''
	request.session["sfilter2"] = ''
	request.session["sfilter3"] = ''
	request.session["sfilter4"] = ''
	request.session["sfilter5"] = ''
	request.session["sfilter6"] = ''
	request.session["sfilter7"] = ''
	request.session["sfilter8"] = ''
	request.session["sfilter9"] = ''
	request.session["sfilter10"] = ''
	request.session["sfilter11"] = ''
	request.session["sfilter12"] = ''
	request.session["sfilter13"] = ''
	request.session["sfilter14"] = ''
	return
	
def vacation_display_initial(request):
	request.session["month_pick"] = 0
	return vacation_display(request)
	
	
def vacation_display(request):	
	
	# Call current datetime using external function because it would conflict with from datetime import datetime
	t = vacation_temp()

	month_st = t.month
	year_st = t.year
	day_st = t.day
	

	
	
	
	try:
		if request.session["month_pick"] == 1:
			month_st = int(request.session["month"])
			year_st = int(request.session["year"])
			#request.session["month_pick"] = 0
			
	except:
		request.session["month_pick"] = 0		
	
	
	
	

	one = 1
	one_end = 31
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_last = str(year_st) + "-" + str(month_st) + "-" + str(one_end)
	request.session["current_first"] = current_first
	request.session["current_last"] = current_last
	request.session["current_day"] = day_st
	request.session["current_day_b"] = day_st
	request.session["current_month"] = month_st
	mm = int(month_st)
	try:
		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		shift11 = request.session["shift11"]
		shift12 = request.session["shift12"]
		shift13 = request.session["shift13"]
		shift14 = request.session["shift14"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"
			
	# Select prodrptdb db located in views_db
	db, cur = db_open() 
	
	if shift1 == "All":
		sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	else:
		#sql = "SELECT * FROM vacation where shift = '%s' or shift = '%s' or shift = '%s' or shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, current_first, current_last)
		#sql = "SELECT * FROM vacation where shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, current_first, current_last)
		sql = "SELECT * FROM vacation where (start between '%s' and '%s') and (shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s')" %( current_first, current_last,shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14)
		
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	
	#return render(request,'test993.html',{'monkey':month_st,'len_monkey':year_st})
	
	
	if year_st == 2017:
		dday, ctr, mnth = vacation_calander_init_2017(month_st)
	else:
		dday, ctr, mnth = vacation_calander_init(month_st)
		
	request.session["current_month"] = month_st
	List = zip(ctr,dday)
	
	# Set Form Variables 
	if request.POST:
		#request.session["shift"] = request.POST.get("shift")
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'
			
		if request.POST.get("shift11"):
			request.session["shift11"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
		else:
			request.session["shift11"] = '--'

		if request.POST.get("shift12"):
			request.session["shift12"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
		else:
			request.session["shift12"] = '--'

		if request.POST.get("shift13"):
			request.session["shift13"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
		else:
			request.session["shift13"] = '--'

		if request.POST.get("shift14"):
			request.session["shift14"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'

		else:
			request.session["shift14"] = '--'

		xy = request.POST.get("month")
		xy = int(xy)
		jj = xy
		if xy > 12:
			request.session["year"] = 2017
			request.session["month"] = xy - 12
		else:
			request.session["year"] = 2016
			request.session["month"] = xy
		
		#return render(request,'test998.html',{'t':year_st,'month':month_st})
		request.session["month_pick"] = 1
		

		return render(request,'vacation_shift.html')
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	try:
		request.session["shift"]
	except:
		request.session["shift"] = "All"
			
#	return render(request,'test4.html',{'Tmp':tmp,'Mnth':mnth,'M':month_st,'List':List})	
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})

def vacation_display_jump(request):
	return vacation_display(request)
	
def vacation_display_increment(request):	
	try:
		current_first = request.session["current_first"]
	except:
		current_first, shift_filter = vacation_set_current()

	try:

		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		shift11 = request.session["shift11"]
		shift12 = request.session["shift12"]
		shift13 = request.session["shift13"]
		shift14 = request.session["shift14"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"

			
	date_st = datetime.strptime(current_first, '%Y-%m-%d')
	

	# Increment the Month by one.  Increment Year by 1 if Month is 12
	month_st = date_st.month
	year_st = date_st.year
	if month_st == 12:
		month_st = 1
		year_st = year_st + 1
	else:
		month_st = month_st + 1
	

	one = 1
	one_end = 31
	ma = str(month_st)
	if len(ma)<2:
		ma = '0' + ma
	current_first = str(year_st) + "-" + str(ma) + "-" + "01"
	current_last = str(year_st) + "-" + str(ma) + "-" + str(one_end)
	request.session["current_first"] = current_first
	
	
	
	
	if request.session["current_month"] == month_st:
		request.session["current_day"] = request.session["current_day_b"]
	else:
		request.session["current_day"] = 99	

	mm = int(month_st)
	

	# Select prodrptdb db located in views_db
	db, cur = db_open() 
	if shift1 == "All":
		#sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
		sql = "SELECT * FROM vacation where start between '%s' and '%s'" %(current_first, current_last)
	else:
		#sql = "SELECT * FROM vacation where shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14, current_first, current_last)
		sql = "SELECT * FROM vacation where (start between '%s' and '%s') and (shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s')" %( current_first, current_last,shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14)
	

	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	if year_st == 2017:
		dday, ctr, mnth = vacation_calander_init_2017(month_st)
	else:
		dday, ctr, mnth = vacation_calander_init(month_st)

	
	# Below re route is for testing break
	if month_st == 21:
		x = len(monkey)
		y = len(current_first)
		return render(request,'test993.html',{'monkey':monkey,'len_monkey':x,'current_first':current_first,'len_first':y})
	
	
	request.session["current_month"] = month_st
	request.session["current_year"] = year_st
	request.session["month"] = month_st
	request.session["year"] = year_st
	List = zip(ctr,dday)

	# Set Form Variables 
	if request.POST:
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'

		if request.POST.get("shift11"):
			request.session["shift11"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
		else:
			request.session["shift11"] = '--'

		if request.POST.get("shift12"):
			request.session["shift12"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
		else:
			request.session["shift12"] = '--'

		if request.POST.get("shift13"):
			request.session["shift13"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
		else:
			request.session["shift13"] = '--'

		if request.POST.get("shift14"):
			request.session["shift14"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'
		else:
			request.session["shift14"] = '--'			
		
		return render(request,'vacation_shift.html')
			
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})
#	return render(request,'vacation_display.html',{'Tmp':tmp})	

def vacation_display_decrement(request):	
	try:
		current_first = request.session["current_first"]
	except:
		current_first, shift_filter = vacation_set_current()

	try:

		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		shift11 = request.session["shift11"]
		shift12 = request.session["shift12"]
		shift13 = request.session["shift13"]
		shift14 = request.session["shift14"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"

			
	date_st = datetime.strptime(current_first, '%Y-%m-%d')
	
	# Decrement the Month by one.  Decrement Year by 1 if Month is 1
	month_st = date_st.month
	year_st = date_st.year
	if month_st == 1:
		month_st = 12
		year_st = year_st - 1
	else:
		month_st = month_st - 1
		
	one = 1
	one_end = 31
	ma = str(month_st)
	if len(ma) < 2:
		ma = '0'+ ma
		
	current_first = str(year_st) + "-" + str(ma) + "-" + "01"
	current_last = str(year_st) + "-" + str(ma) + "-" + str(one_end)
	request.session["current_first"] = current_first
	
	if request.session["current_month"] == month_st:
		request.session["current_day"] = request.session["current_day_b"]
	else:
		request.session["current_day"] = 99	

	mm = int(month_st)
	# Select prodrptdb db located in views_db
	db, cur = db_open() 
	if shift1 == "All":
		sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	else:		
		sql = "SELECT * FROM vacation where (start between '%s' and '%s') and (shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s')" %( current_first, current_last,shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11, shift12, shift13, shift14)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	
	if year_st == 2017:
		dday, ctr, mnth = vacation_calander_init_2017(month_st)
	else:
		dday, ctr, mnth = vacation_calander_init(month_st)
		
	request.session["current_month"] = month_st
	request.session["current_year"] = year_st
	List = zip(ctr,dday)

	# Set Form Variables 
	if request.POST:
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'

		if request.POST.get("shift11"):
			request.session["shift11"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
		else:
			request.session["shift11"] = '--'

		if request.POST.get("shift12"):
			request.session["shift12"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
		else:
			request.session["shift12"] = '--'

		if request.POST.get("shift13"):
			request.session["shift13"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
		else:
			request.session["shift13"] = '--'

		if request.POST.get("shift14"):
			request.session["shift14"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'
		else:
			request.session["shift14"] = '--'	
			
		return render(request,'vacation_shift.html')
			
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Year':year_st,'M':mm,'Tmp':tmp,'args':args})
	
	
def BB_vacation_display_decrement(request):	

	try:
		current_first = request.session["current_first"]
	except:
		current_first, shift_filter = vacation_set_current()
		
	try:

		#shift_filter = request.session["shift"]
		shift1 = request.session["shift1"]
		shift2 = request.session["shift2"]
		shift3 = request.session["shift3"]
		shift4 = request.session["shift4"]
		shift5 = request.session["shift5"]
		shift6 = request.session["shift6"]
		shift7 = request.session["shift7"]
		shift8 = request.session["shift8"]
		shift9 = request.session["shift9"]
		shift10 = request.session["shift10"]
		
	except:
		shift_filter = "All"
		shift1 = "All"
		request.session["shift1"] = "All"
			
	date_st = datetime.strptime(current_first, '%Y-%m-%d')

	month_st = date_st.month
	year_st = date_st.year
	month_st = month_st - 1

	one = 1
	one_end = 31
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_last = str(year_st) + "-" + str(month_st) + "-" + str(one_end)
	request.session["current_first"] = current_first
	if request.session["current_month"] == month_st:
		request.session["current_day"] = request.session["current_day_b"]
	else:
		request.session["current_day"] = 99	
	
	# Select prodrptdb db located in views_db
	db, cur = db_open() 
	if shift1 == "All":
		sql = "SELECT * FROM vacation where start >= '%s' and start <= '%s'" %(current_first, current_last)
	else:
		sql = "SELECT * FROM vacation where shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' OR shift = '%s' and start >= '%s' and start <= '%s'" %(shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, current_first, current_last)
		
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	dday, ctr, mnth = vacation_calander_init(month_st)
	request.session["current_month"] = month_st
	List = zip(ctr,dday)

	# Set Form Variables 
	if request.POST:
		reset_sfilter(request)
		
		if request.POST.get("shift1"):
			request.session["shift1"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			
		else:
			request.session["shift1"] = '--'
			
		if request.POST.get("shift2"):
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
		else:
			request.session["shift2"] = '--'
		if request.POST.get("shift3"):
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
		else:
			request.session["shift3"] = '--'	
		if request.POST.get("shift4"):
			request.session["shift4"] = 'Cont A Nights'
			request.session["sfilter4"] = 'checked'
		else:
			request.session["shift4"] = '--'
				
		if request.POST.get("shift5"):
			request.session["shift5"] = 'Cont A Days'
			request.session["sfilter5"] = 'checked'
		else:
			request.session["shift5"] = '--'	
			
		if request.POST.get("shift6"):
			request.session["shift6"] = 'Cont B Nights'
			request.session["sfilter6"] = 'checked'
		else:
			request.session["shift6"] = '--'

		if request.POST.get("shift7"):
			request.session["shift7"] = 'Cont B Days'
			request.session["sfilter7"] = 'checked'
		else:
			request.session["shift7"] = '--'
			
		if request.POST.get("shift8"):
			request.session["shift8"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
		else:
			request.session["shift8"] = '--'
			
		if request.POST.get("shift9"):
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
		else:
			request.session["shift9"] = '--'
			
		if request.POST.get("shift10"):
			request.session["shift10"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
		else:
			request.session["shift10"] = '--'
	else:
		form = sup_vac_filterForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'vacation_display.html',{'List':List,'Mnth':mnth,'Tmp':tmp,'args':args})	

def vacation_edit(request, index):	
	tmp = index
	request.session["index"] = index
	db, cur = db_open() 
	try:
		sql = "SELECT * FROM vacation where id_number = '%s'" %(tmp)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
	except:
		tmp="No"	
	db.close()
	return render(request,'vacation_delete.html',{'Tmp':tmp2})
		
		

def vacation_delete(request):
	index = request.session["index"]
	db, cur = db_open()
	dql = ('DELETE FROM vacation WHERE id_number="%s"' % (index))
	cur.execute(dql)
	db.commit()
	db.close()
	request.session["shift"] = 'All'
	return vacation_display(request)
	#return render(request,'test4.html',{'Tmp':tmp2})	

	
	
	
def vacation_calander_init(month_st):
	dte = []
	ctr = []
	mnt = []
#	for x in range(0,12):
		#dte[x] = []
		#ctr[x] = []
#		dte[x] = ['' for i in range(40)]
#		ctr[x] = [0 for ii in range(40)]
		
#	dte.append([''])
#	dte.append(['-','-','-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
#	dte.append(['-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29'])
#	dte.append(['-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
#	dte.append(['-','-','-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'])
#	dte.append(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
#	dte.append(['-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'])
#	dte.append(['-','-','-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
#	dte.append(['-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
#	dte.append(['-','-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'])
#	dte.append(['-','-','-','-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
#	dte.append(['-','-''1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'])
#	dte.append(['-','-','-','-','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'])
		
	dte.append([0])
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	
	ctr.append([0])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,33])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])	
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,32])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,34])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35])

	
	mnt.append( '')
	mnt.append( 'January')
	mnt.append( 'February')
	mnt.append('March')
	mnt.append('April')
	mnt.append('May')
	mnt.append('June')
	mnt.append('July')
	mnt.append('August')
	mnt.append('September')
	mnt.append('October')
	mnt.append('November')
	mnt.append('December')
	
	days = dte[month_st]
	cctr = ctr[month_st]
	mnth = mnt[month_st]
	#return render(request,'test4323.html')
	return days,cctr,mnth

def vacation_calander_init_2017(month_st):
	dte = []
	ctr = []
	mnt = []
		
	dte.append([0])
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	dte.append([0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
	dte.append([0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	
	ctr.append([0])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])	
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33])
	ctr.append([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])

	
	mnt.append( '')
	mnt.append( 'January')
	mnt.append( 'February')
	mnt.append('March')
	mnt.append('April')
	mnt.append('May')
	mnt.append('June')
	mnt.append('July')
	mnt.append('August')
	mnt.append('September')
	mnt.append('October')
	mnt.append('November')
	mnt.append('December')
	
	days = dte[month_st]
	cctr = ctr[month_st]
	mnth = mnt[month_st]
	#return render(request,'test4323.html')
	return days,cctr,mnth



