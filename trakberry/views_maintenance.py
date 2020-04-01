from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_mod2 import seperate_string, create_new_table,generate_string
from views_email import e_test
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
from views_supervisor import supervisor_tech_call
from trakberry.views_testing import machine_list_display
from mod1 import hyphon_fix, multi_name_breakdown
import MySQLdb

from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
import time 


#import datetime as dt 
from django.core.context_processors import csrf


def maint_mgmt(request):

	request.session["main_screen_color"] = "#abad97"  # Color of Background in APP
	request.session["main_menu_color"] = "#f8fcd7"    # Color of Menu Bar in APP
	request.session["main_body_color"] = "#EBF0CB"
	request.session["main_body_menu_color"] = "#D2D2D2"

	wildcard = int(request.session["wildcard1"])
	
	whoisonit1 = 'tech'
	whoisonit2 = 'Engineering'
	db, cursor = db_set(request)  
	SQ_Sup = "SELECT * FROM pr_downtime1 where closed IS NULL and whoisonit != '%s' and whoisonit != '%s' ORDER BY priority ASC" % (whoisonit1,whoisonit2) 
	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	db.close()

	if wildcard == 1:
		ch1 = request.session["maint_mgmt_login_password_check"]
		# t=9/0

	if request.POST:
		selected1 = request.POST
		try:
			selected2 = int(selected1.get("one"))
		except:
			return maint_mgmt(request)
		request.session["index"] = selected2
		return render(request, "maint_edit.html")
		# return done_edit(request)
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form


	return render(request, "maint_mgmt.html",{'index':tmp,'args':args})



# Login for Maintenance Manager App
def maint_mgmt_login_form(request):	

	Maint_Mgmt_Manpower = []
	request.session["login_department"] = 'Maintenance Manager'
	Maint_Mgmt_Manpower = maint_mgmt_manpower(request)
	request.session["maint_mgmt_login_name"] = ""
	request.session["maint_mgmt_login_password"] = ""
	request.session["maint_mgmt_login_password_check"] = 'False'

#	if request.POST:
	if 'button1' in request.POST:

		request.session["login_name"] = request.POST.get("login_name")
		request.session["login_password"] = request.POST.get("login_password")
		request.session["login_password_check"] = ''
		login_password_check(request)
		check = request.session["login_password_check"]
		request.session["maint_mgmt_login_password_check"]

	
		# if len(login_name) < 5:
		# 	login_password = 'wrong'
		if check != 'false':
			request.session["maint_mgmt_login_name"] = request.session["login_name"]
			request.session["maint_mgmt_login_password"] = request.session["login_password"]
			request.session["maint_mgmt_login_password_check"] = 'True'
		else:
			request.session["maint_mgmt_login_password_check"] = 'False'

		ch2 = request.session["maint_mgmt_login_password_check"]
		request.session["wildcard1"] = 1
	
		return render(request,'redirect_maint_mgmt.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop

		
	elif 'button2' in request.POST:
		request.session["password_lost_route1"] = "maint_mgmt.html"
		return render(request,'login/reroute_lost_password.html')

	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["maint_mgmt_login_name"] = ""
	request.session["maint_mgmt_login_password"] = ""


	return render(request,'maint_mgmt_login_form.html', {'args':args,'MList':Maint_Mgmt_Manpower})	

def maint_mgmt_manpower(request):
	db, cursor = db_set(request)  
	dep = request.session['login_department']
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50))""")
	db.commit()
	sql = "SELECT * FROM tkb_logins WHERE department = '%s' ORDER BY user_name ASC" %(dep)  # Select only those in the department  (dep)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	return tmp

def maint_manpower(request):
	db, cursor = db_set(request)  
	dep = request.session['login_department']
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50))""")
	# cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_maint_list LIKE tkb_tech_list""")
	db.commit()
	sql = "SELECT user_name FROM tkb_logins WHERE department = '%s' ORDER BY user_name ASC" %(dep)  # Select only those in the department  (dep)
	# sql = "SELECT Tech FROM tkb_maint_list"
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	# maint = ['Allan Meunier','Andrew McArthur','Arnold Olszewski','Brad Haase','Brian Willert','Bruce Riehl','Chris Meidlinger','Curtis Mitchell','Dale Robinson','David Selvey','Dorin Tumac','Doug Huard','Dusko Farkic','Gary Tune','George Stamas','Greg Mroczek','Harold Kuepfer','Jeff Jacobs','Jeff Saunders','Jeremy Arthur','Jim Green','John Reissner','Kevin Faubert','Lyuben Shivarov','Matthew Kuttschrutter','Michael Cella','Milos Nikolic','Mladen Stosic','Peter Nguyen','Richard Clifford','Robin Melville','Royce Laycox','Shawn Gilbert','Steven Niu','Terry Higgs','Wesley Guest']
	db.close()
	return tmp

# Module to edit entry	
def maintenance_edit(request):	
	index = request.session["index"]
	Maint_Manpower = []
	request.session["login_department"] = 'Maintenance'
	Maint_Manpower = maint_manpower(request)

	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)
	SQ_Sup = "SELECT * FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	tmp2=tmp[0]
	request.session["machinenum"] = tmp2[0]
	request.session["problem"] = tmp2[1]
	request.session["priority"] = tmp2[3]
	request.session["manpower"] = tmp2[4]

	nm = multi_name_breakdown(tmp2[4])  # put all the names in a list that are seperated by a   |

	db.close()	
	

	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		manpower = request.POST.get("manpower")
		whoisonit = 'tech'
		
		a = request.POST
		try:
			b=int(a.get("one"))
			manpower = request.session["manpower"]
		except:
			manpower = generate_string(request.session["manpower"],manpower)
			b=-4

		problem = hyphon_fix(problem)  # Send text to rid it of nasty hyphon glitches  :)
		db, cursor = db_set(request)
		cur = db.cursor()

		if b==-4:
			mql =( 'update pr_downtime1 SET machinenum="%s" WHERE idnumber="%s"' % (machinenum,index))
			cur.execute(mql)
			db.commit()
			tql =( 'update pr_downtime1 SET problem="%s" WHERE idnumber="%s"' % (problem,index))
			cur.execute(tql)
			db.commit()
			uql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (manpower,index))
			cur.execute(uql)
			db.commit()
			db.close()
			return render(request,'redirect_maint_edit.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop

		
		if b==-3:
			mql =( 'update pr_downtime1 SET machinenum="%s" WHERE idnumber="%s"' % (machinenum,index))
			cur.execute(mql)
			db.commit()
			tql =( 'update pr_downtime1 SET problem="%s" WHERE idnumber="%s"' % (problem,index))
			cur.execute(tql)
			db.commit()
			db.close()
			return render(request,'redirect_maint_mgmt.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop


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
			return render(request,'redirect_maint_mgmt.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop

		if b==-1:
			dummy = 3
			return done_sup_close(request)
		
	


		return done(request)
	else:	
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'maintenance_edit.html',{'args':args,'MList':Maint_Manpower})	


def login_password_check(request):
	db, cursor = db_set(request)
	user_name = request.session["login_name"]
	user_pwd = request.session["login_password"]
	user_dep = request.session["login_department"]
	pwd_check = 'false'
	try:
		sql = "SELECT * FROM tkb_logins WHERE user_name = '%s' and password = '%s' and department ='%s'" % (user_name, user_pwd,user_dep)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		pwd_check = 'true'
	except:
		pwd_check = 'false'

	request.session["login_password_check"] = pwd_check
	return

def hour_check():
	# obtain current date from different module to avoid datetime style conflict

	h = 2
	m = 2
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

	db, cursor = db_set(request)  
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
	
def reset_call_route(request):
	request.session["call_route"] = 'supervisor'
	return render(request, "out.html")

def tech_email_test(request):
	send_email = hour_check()
	if send_email == 1:
		return render(request, "email_downtime.html")
		
	return render(request, "email_downtime_cycle.html")
		
def maint(request):
	request.session["refresh_maint"] = 0
	try:
		request.session["login_maint"] 
	except:
		request.session["login_maint"] = "none"
	try:
		request.session["maint_ctr"] 
	except:
		request.session["maint_ctr"] = 0
  
	request.session["refresh_maint"] = 0
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
	tch = []
	nm = []
	maint = ["Rich Clifford","Wes Guest","Shawn Gilbert","Jeff Jacobs","Steven Niu"]



	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)   

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	# Retrieve information from Database and put 2 columns in array {list}
	# then send array to Template machinery.html
	c = ["tech","Jim Barker"]
	j = "electrician"
	jj = "millwright"
	a1 = "Chris Dufton"
	a2 = "Rich Clifford | Wes Guest"
	a3 = "Wes Guest"
	a4 = "Gike Maspar"
	a5 = "Jeff Jacobs"
	a6 = "Shawn Gilbert"
	a7 = "Steven Niu"
	a8 = "-------"
	a9 =  "-------"
	a10 = "-------"
	
	sqlT = "Select * From pr_downtime1 where closed IS NULL"
	cursor.execute(sqlT)
	tmp = cursor.fetchall()



	


	# d1 = '2015-05-01'
	# d2 = '2015-07-01'
	# sqlT = "SELECT * FROM pr_downtime1 where closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s'" %(j,jj,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10)

	# cursor.execute(sqlT)
	# tmp = cursor.fetchall()
	
	ctr = 0
	ctr2 = 0
	for x in tmp:

		add_job = 0   # Determines if we add this job to list to display
		tmp2 = (tmp[ctr2])
		temp_pr = tmp2[3]
		# if temp_pr == "A":
		# 	tp = 1
		# elif temp_pr =="c":
		# 	tp = 3
		# elif temp_pr =="b" :
		# 	tp = 2
		# elif temp_pr =="B" :
		# 	tp = 2
		# elif temp_pr =="C" :
		# 	tp = 3
		# elif temp_pr =="D"	:
		# 	tp = 4
		# elif temp_pr =="E":
		# 	tp = 5
		
		
		tmp3 = tmp2[4]

		if tmp3 == "Electrician":
			
			tmp3 = "Maintenance"
			# kkkk = request.session["opopop"]
			add_job = 1
		if tmp3 == "Millwright":
			tmp3 = "Maintenance"
			# kkkk = request.session["opopop"]	
			add_job = 1

		nm = seperate_string(tmp2[4])

		for h1 in nm:
			for h2 in maint:
				if h1[0] == h2[0]:
					add_job = 1
					break 
			if add_job == 1:
				break
		# Do this if we need to assign to display tuple
		if add_job == 1:
			job.append(tmp2[0])  # Assign machine to job
			prob.append(tmp2[1]) # Assign problem to prob
			priority.append(int(tmp2[3]))  #Assign priority number to priority
			id.append(tmp2[11])  # Assign idnumber to id
			tch.append(tmp3)   # Assign Name to tch
			ctr = ctr + 1
		ctr2 = ctr2 + 1


	for i in range(0, ctr-1):
		for ii in range(i+1, ctr):
			if int(priority[ii]) < int(priority[i]):
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
				ttch = tch[i]
				tch[i] = tch[ii]
				tch[ii] = ttch
	if request.session["maint_ctr"] == ctr:
		request.session["maint_alarm"] = "/media/clock2.wav"
	else:
		request.session["maint_alarm"] = "/media/clock.wav"
		request.session["maint_ctr"] = ctr
	list = zip(job,prob,id,tch,priority)
	
	db.close()
	n = "none"
	if request.session["login_maint"] == "Chris Dufton":
		request.session["login_image"] = "/static/media/tech_jim.jpg"
		request.session["login_back"] = "/static/media/back_jim.jpg"
	elif request.session["login_maint"] == "Rich Clifford":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/tech_training.jpg"
	elif request.session["login_maint"] == "Shawn Gilbert":
		request.session["login_image"] = "/static/media/tech_scott.jpg"
		request.session["login_back"] = "/static/media/back_scott.jpg"
	elif request.session["login_maint"] == "Gike Maspar":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_maint"] == "Wes Guest":
		request.session["login_image"] = "/static/media/tech_woodrow.jpg"
		request.session["login_back"] = "/static/media/back_woodrow.jpg"
	elif request.session["login_maint"] == "Jeff Jacobs":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"			
	elif request.session["login_maint"] == "Steven Niu":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"			
	elif request.session["login_maint"] == "-----":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"				
	else:
		request.session["login_image"] = "/static/media/tech_rick.jpg"
		request.session["login_back"] = "/static/media/back_rick.jpg"
		
		
	request.session["login_back"] = "/static/media/back_maint.jpg"
	request.session["login_image"] = "/static/media/maint.jpg"
	
  # call up 'display.html' template and transfer appropriate variables.  
  
  # *********************************************************************************************************
  # ******     Messaging portion of the Maint App  *********************  TODO  *****************************
  # *********************************************************************************************************
#	N = request.session["login_maint"]
#	R = 0
#	db, cur = db_set(request) 
#	try:
#		sql = "SELECT * FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)	
#		cur.execute(sql)
#		tmp44 = cur.fetchall()
#		tmp4 = tmp44[0]
#
#		request.session["sender_name"] = tmp4[2]
#		request.session["message_id"] = tmp4[0]

#		aql = "SELECT COUNT(*) FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)
#		cur.execute(aql)
#		tmp2 = cur.fetchall()
#		tmp3 = tmp2[0]
#		cnt = tmp3[0]
#	except:
#		cnt = 0
#		tmp4 = ''
#		request.session["sender_name"] = ''
#		request.session["message_id"] = 0
#	db.close()
#	Z = 1
#	if cnt > 0 :
#		cnt = 1
#		request.session["refresh_tech"] = 3
	# ********************************************************************************************************
	
	M = 'Need Millwright'
	E = 'Maintenance'
	
	return render(request,"maint.html",{'L':list,'N':n,'M':M,'E':E})

def tech_message_close(request):
	request.session["refresh_tech"] = 0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return tech(request)

def tech_message_reply1(request):
	request.session["refresh_tech"]=0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return tech_message_reply2(request)
	
	
def maint_call(request, index):	
    
	tec = request.session["login_maint"]
	db, cur = db_set(request)  
	sql1 = "SELECT whoisonit FROM pr_downtime1 where idnumber='%s'" %(index)
	cur.execute(sql1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[0]
	t = generate_string(tmp3,tec)

	sql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (t,index))
	cur.execute(sql)
	db.commit()
	db.close()

	return maint(request)

def maint_close(request, index):	
	

	# Select prodrptdb db located in views_db
	db, cur = db_set(request)  
		
	tc = "Closed by Maintenance"
	request.session["tech_comment"] = tc
	t = vacation_temp()
	sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
	cur.execute(sql)
	db.commit()
	tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
	cur.execute(tql)
	db.commit()
	db.close()
			
	
	return maint(request)

def maint_names(request):
	Maint_Manpower = []
	Maint_Manpower = maint_manpower(request)
	if request.POST:
		name1 = request.POST.get('tech')
		return maint_names_reload(request)
	else:
		form=toggletest_Form
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,"maint_names_form.html",{'Maint_Manpower':Maint_Manpower,'args':args})

		
def maint_logout(request):	
	Maint_Manpower = []
	request.session["login_department"] = 'Maintenance'
	Maint_Manpower = maint_manpower(request)

	if request.POST:
        			
		tec = request.POST.get("user")
		pwd = request.POST.get("pwd")

	
		request.session["login_maint"] = tec
		request.session["login_maint_check"] = 1
		

		return maint(request)
		
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_maint"] = "none"
	request.session["login_maint_check"] = 0
	return render(request,'maint_login.html',{'args':args,'MList':Maint_Manpower})	

	
def maint_pass(request, index):	
	
	db, cursor = db_set(request)  
	sql = "SELECT whoisonit FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	db.close()
	try:
		request.session["tech_comment"]
	except:
		request.session["tech_comment"] = ""

		
	if request.POST:

		tc = request.POST.get("comment")
		request.session["tech_comment"] = tc
		tp = request.POST.get("pass")
		request.session["tech_pass"] = tp
		t = datetime.datetime.now()
		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)

		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		db.close()
		
		db, cur = db_set(request)  
		tql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (tp,index))
		cur.execute(tql)
		db.commit()
		db.close()

		return tech(request)
		
	else:
		form = tech_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_pass.html', args)		

							  
def maint_job_history(request):

	name = request.session["login_maint"]
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM pr_downtime1 WHERE whoisonit = '%s' ORDER BY called4helptime DESC limit 60" %(name)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close

	job_assn = []
	job_date = []
	job_diff = []
	a = []
	b = []
	c = []
	d = []
	
	
	
	for x in tmp:
		# assign job date and time to dt
		dt = x[2]
		dt_t = time.mktime(dt.timetuple())
		# assign current date and time to dtemp
		dtemp = vacation_temp()
		dtemp_t = time.mktime(dtemp.timetuple())
		# assign d_diff to difference in unix
		d_dif = dtemp_t - dt_t
		if d_dif < 86400:
			job_assn.append(x[0])
			job_date.append(x[2])
			a.append(x[1])
			b.append(x[4])
			c.append(x[7])
			d.append(x[9])
			
			
			job_diff.append(str(d_dif))
		
	job_history = zip(job_assn,a,job_date,b,c,d)


	
	machine="Recent Machine Breakdowns"
	request.session["machine_search"] = machine
	request.session["maint_display"] = 1
	return render(request,"maint_job_history_display.html",{'machine':job_history})

def maint_map(request):

	return render(request,"maint_map.html")	

def tech_history(request):	

	if request.POST:
        			
		machine = request.POST.get("machine")
		request.session["machine_search"] = machine
		db, cur = db_set(request)  		
		sql = "SELECT * FROM pr_downtime1 where LEFT(machinenum,3) = '%s' ORDER BY called4helptime DESC limit 20" %(machine)
		cur.execute(sql)
		tmp = cur.fetchall()
		db.close
		request.session["tech_display"] = 0
		return render(request,"tech_search_display.html",{'machine':tmp})
		
	else:
		
		form = tech_searchForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_search.html', args)		

def maint_call_call(request):
	if request.POST:	
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		name_who = request.POST.get["whoisonit"]
		
		# call external function to produce datetime.datetime.now()
		t = vacation_temp()
		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime) VALUES(%s,%s,%s,%s,%s)''', (machinenum,problem,priority,name_who,t))
		db.commit()
		db.close()
		
		return done_maint_app(request)
		
	else:
		request.session["machinenum"] = "692"
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	rlist = machine_list_display()
	request.session["refresh_maint"] = 3
	return render(request,'maint_call.html', {'List':rlist,'args':args})	
	
	return render(request,'maint_call.html')	
						  

def tech_message(request):	
	A = 'Chris Strutton'
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()

	db.close()

	if request.POST:
        			
		a = request.session["login_tech"]
		b = request.POST.get("name")
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return tech(request)
		#return done(request)
		
	else:
		form = tech_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'tech_message_form.html', {'List':tmp,'A':A,'args':args})	

def tech_message_reply2(request):	
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	if request.POST:
        			
		a = request.session["login_tech"]
		b = request.POST.get("name")
		b = request.session["sender_name"]
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return tech(request)
		#return done(request)
		
	else:
		form = tech_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'tech_message_reply_form.html', {'List':tmp,'args':args})	
	
def modal_test(request):	
	a = 1
	b = 1
	request.session["modal_1"] = a
	return render(request,'modal_test.html',{'b':b})
