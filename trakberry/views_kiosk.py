from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
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
	# Utilize variable route_1 and assign it a value to kick to another module.
	# that module needs to have a pattern defined in url.py because direction(request)
	# will route externally to it looking for the pattern.
	if request.POST:
		button_1 = request.POST
		button_pressed =int(button_1.get("kiosk_button1"))
		if button_pressed == -1:
			request.session["route_1"] = 'kiosk_job'
			return direction(request)
		if button_pressed == -2:
			return kiosk_production(request)
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
	return render(request, "kiosk/kiosk_production.html")
def kiosk_help(request):
	return render(request, "kiosk/kiosk_help.html")
def kiosk_scrap(request):
	return render(request, "kiosk/kiosk_scrap.html")
# *********************************************************************************************************


# *********************************************************************************************************
# Third Tier Pages generated from Secondary Page Button Presses
# *********************************************************************************************************
# Kiosk Third Tier page initiated by Job | Assign button press on Secondary Page
def kiosk_job_assign(request):
	if request.POST:
		kiosk_clock = request.POST.get("clock")
		kiosk_job1 = request.POST.get("job1")
		kiosk_job2 = request.POST.get("job2")
		kiosk_job3 = request.POST.get("job3")
		kiosk_job4 = request.POST.get("job4")
		
		# Finished and reroute
		return kiosk_job_assign_enter(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_job_assign.html",{'args':args})
	
	
def kiosk_job_leave(request):
	return render(request, "kiosk/kiosk_job_leave.html")
	
	
	
	
	
	
	
	
