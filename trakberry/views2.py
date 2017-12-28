from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
from views_mod1 import find_current_date
from views_test import layer_choice_init
from trakberry.forms import login_Form
from datetime import datetime
import MySQLdb
import time
from django.core.context_processors import csrf

def fup(x):
	return x[2]
def frup(x):
	return x[11]	

def gup(x):
	return x[5]
	
def nup(x):
	return x[4]

def tup(x):
	global tst, down_time
	tst.append(str(x[5]))

	
def eup(x):
		global st, nt
		nt.append(str(x[4]))
		st.append(str(x[5]))

def mup(x):
		global dt
		dt.append(str(x[7]))
		
def pup(x):
	global lt
	lt.append(str(x[11]))
	
	
# Call Main Login screen
def main_login(request):
	
	return render(request, "main_log.html")

def login_initial(request,login_name):
	
		request.session["shift1"] = ''
		request.session["shift2"] = ''
		request.session["shift3"] = ''
		request.session["shift4"] = ''
		request.session["shift5"] = ''
		request.session["shift6"] = ''
		request.session["shift7"] = ''
		request.session["shift8"] = ''
		request.session["shift9"] = ''
		request.session["shift10"] = ''
		request.session["shift11"] = ''
		request.session["shift12"] = ''
		request.session["shift13"] = ''
		request.session["shift14"] = ''
		
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
		request.session["shift_primary"] = 'Cont A Days'
		
		if login_name == 'Grant Packham':
			request.session["shift_primary"] = 'Cont A Days'
			request.session["matrix_shift"] = 'Cont A Days CSD 2'
			request.session["sfilter1"] = 'checked'
			request.session["sfilter5"] = 'checked'
			request.session["shift1"] = 'CSD2 Day'
			request.session["shift5"] = 'Cont A Days'
			
		elif login_name == 'Dave Clark':
			request.session["matrix_shift"] = 'Cont A Nights CSD 2'
			request.session["shift_primary"] = 'Cont A Nights'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter4"] = 'checked'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["shift4"] = 'Cont A Nights'
			
						
		elif login_name == 'Tim Sanzosti':
			request.session["matrix_shift"] = 'Cont B Nights CSD 2'
			request.session["shift_primary"] = 'Cont B Nights'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter6"] = 'checked'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["shift6"] = 'Cont B Nights'
						
		elif login_name == 'Scott McMahon':
			request.session["matrix_shift"] = 'Aft CSD 2'
			request.session["shift_primary"] = 'CSD2 Aft'
			request.session["sfilter2"] = 'checked'
			request.session["shift2"] = 'CSD2 Aft'
			request.session["sfilter8"] = 'checked'
			request.session["shift8"] = 'Forklift'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'			
									
		elif login_name == 'Frank Ponte':
			request.session["matrix_shift"] = 'Day CSD 2'
			request.session["shift_primary"] = 'CSD2 Day'
			request.session["sfilter1"] = 'checked'
			request.session["sfilter5"] = 'checked'
			request.session["sfilter7"] = 'checked'
			request.session["shift1"] = 'CSD2 Day'
			request.session["shift5"] = 'Cont A Days'
			request.session["shift7"] = 'Cont B Days'
	
									
		elif login_name == 'Karl Edwards':
			request.session["matrix_shift"] = 'Mid CSD 2'
			request.session["shift_primary"] = 'CSD2 Mid'
			request.session["sfilter3"] = 'checked'
			request.session["sfilter4"] = 'checked'
			request.session["sfilter6"] = 'checked'
			request.session["shift6"] = 'Cont B Nights'
			request.session["shift4"] = 'Cont A Nights'
			request.session["shift3"] = 'CSD2 Mid'
			request.session["sfilter8"] = 'checked'
			request.session["shift8"] = 'Forklift'			
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'		
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'				
			
		elif login_name == 'Rick Wurm':
			request.session["matrix_shift"] = 'Cont B Days CSD 2'
			request.session["matrix_shift"] = ''
			request.session["sfilter1"] = 'checked'
			request.session["sfilter7"] = 'checked'
			request.session["shift1"] = 'CSD2 Day'
			request.session["shift7"] = 'Cont B Days'
			
		elif login_name == 'Don Barber':
			request.session["shift_primary"] = 'Forklift'
			request.session["sfilter8"] = 'checked'
			request.session["shift8"] = 'Forklift'
			
		elif login_name == 'Kevin Baker':
			request.session["shift_primary"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'
			
		elif login_name == 'Steven Koehler':
			request.session["shift_primary"] = 'Press Setter'
			request.session["sfilter10"] = 'checked'
			request.session["shift10"] = 'Press Setter'	
			
		elif login_name == 'Brad Sproat':
			request.session["shift_primary"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'
		
		elif login_name == 'Mark Phillips':
			request.session["shift_primary"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'
			
		elif login_name == 'John Seagram':
			request.session["shift_primary"] = 'Maintenance'
			request.session["sfilter9"] = 'checked'
			request.session["shift9"] = 'Maintenance'	
			
		elif login_name == 'Norm Buuck':
			request.session["shift_primary"] = 'ToolRoom'
			request.session["sfilter14"] = 'checked'
			request.session["shift14"] = 'ToolRoom'			
			
		elif login_name == 'Ken Frey':
			request.session["shift_primary"] = 'CSD1 Mid'
			request.session["sfilter13"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift13"] = 'CSD1 Mid'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'		
		elif login_name == 'Scott Brownlee':
			request.session["shift_primary"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift11"] = 'CSD1 Day'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'				
		elif login_name == 'Mike Clarke':
			request.session["shift_primary"] = 'CSD1 Aft'
			request.session["sfilter12"] = 'checked'
			request.session["sfilter8"] = 'checked'
			request.session["sfilter9"] = 'checked'
			request.session["shift12"] = 'CSD1 Aft'
			request.session["shift8"] = 'Forklift'
			request.session["shift9"] = 'Maintenance'
			
		elif login_name == 'Kelly Crowder':
			request.session["shift_primary"] = 'CSD1 Day'
			request.session["sfilter11"] = 'checked'
			request.session["shift11"] = 'CSD1 Day'

				
		else:
			dummy_yy = 'meaningless'
#			request.session["shift_primary"] = 'Cont A Days'
#			request.session["sfilter1"] = 'checked'
#			request.session["shift1"] = 'CSD2 Day'	
			
		return
					
	
# Login for Main Program
def main_login_form(request):	

	if request.POST:
        			
		login_name = request.POST.get("login_name")
		login_password = request.POST.get("login_password")

	
		request.session["login_name"] = login_name
		request.session["login_password"] = login_password
		
		login_initial(request,login_name)
	
		
								
		return main(request)

		
	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'main_login_form.html', args)	
	
	
def main_A(request):
	return main(request)
	
def main(request):
	# Check if it's local running or not and if not then force the path as /trakberry
	# Run switch_net to set it back to network or switch_local for local use
	try:
		if request.session["local_switch"] == 1:
			request.session["local_toggle"] = ""
		else:
			request.session["local_toggle"] = "/trakberry"
	except:
		request.session["local_toggle"] = "/trakberry"
	# ******************************************************************************
	
#	Check if login_name and login_password have been entered.

	try:
		password = request.session["login_password"]
		name = request.session["login_name"]

	except:
		password = 'no'
		name = ""
		

		
	# how to delete a session variable
	#del request.session['mykey']
	log_pass = 0
	
	# Administrator Password
	if name == 'Dave Clark':
		if password == 'Jaden2008':
			log_pass = 1
	elif password == 'stackberry':
		log_pass = 1

		
		
	# Code for checking if layered audit needs to be sent.  Make 
	if log_pass == 1:
	
		# use below line to bypass for testing
		return render(request, "main.html")
		
		
		
		
		#request.session.set_expiry(1800)
		#Check if layered audit required

		ID_1 = layered_audit_check(name)

		if ID_1 == 4:
			#return render(request,'done_test1.html')
			return layer_choice_init(request)
		# Check for Layered Audit done or not.
		layer_check = 1
		try:
			layer_check = int(request.session["layer_audit_check"])
		except:
			request.session["layer_audit_check"] = 1
		
		# Below statement determines if a layered audit message needs to occur using layer_check variable
		# Use 6 as dummy number until ready to run then use 0
		if layer_check == 0 and name == 'Dave Clark':
			return layer_choice_init(request)
		
		return render(request, "main.html")
	else:
		return main_login(request)	
		
# Reset Login_Password  and re route back to main for re login
def main_logout(request):
	
	try:
		del request.session['login_password']
	except:
		request.session['login_password'] = ' '
	return main(request)		

# Check if Layered Audit has been entered for this name and todays date
def layered_audit_check(name):

	current_date = find_current_date()
	t = int(time.time())

	db, cursor = db_open()  
	try:
		sql = "SELECT * FROM tkb_layered where Name = '%s'" %(name)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		ts = tmp2[6]
		
		ID_1 = tmp2[0]

	except:
		ID_1 = 4

	db.close()
		
	return ID_1
  
def switch_local(request):
	request.session["local_switch"] = 1
	return main(request)
	
def switch_net(request):
	request.session["local_switch"] = 0
	return main(request)
	
	
