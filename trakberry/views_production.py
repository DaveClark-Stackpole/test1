from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
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
from datetime import datetime 

# *********************************************************************************************************
# MAIN Production View
# This is the main Administrator View to tackle things like cycle times, view production etc.
# *********************************************************************************************************

def mgmt(request):
	return render(request, "mgmt.html")

# Reset the password so it logs out
def mgmt_logout(request):
	request.session["mgmt_login_password"] = " "
	return render(request, "mgmt.html")

def mgmt_login_form(request):	

#	if request.POST:
	if 'button1' in request.POST:


		login_name = request.POST.get("login_name")
		login_password = request.POST.get("login_password")

		if len(login_name) < 5:
			login_password = 'wrong'

		request.session["mgmt_login_name"] = login_name
		request.session["mgmt_login_password"] = login_password
	
		return mgmt(request)
		
	elif 'button2' in request.POST:
		
		return render(request,'login/reroute_lost_password.html')

	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'mgmt_login_form.html', args)	

def mgmt_production_hourly(request):

	db, cur = db_open()
	s1 = "SELECT * FROM sc_prod_hour ORDER BY id DESC limit 20" 
	cur.execute(s1)
	tmp = cur.fetchall()
	db.close()

	return render(request,'mgmt_production_hourly.html', {'tmp':tmp})	




