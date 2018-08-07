from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import sup_downForm, sup_dispForm, sup_closeForm, report_employee_Form, sup_vac_filterForm, sup_message_Form,job_dispForm,kiosk_dispForm1,kiosk_dispForm2
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

from time import mktime
from datetime import datetime, date
from views_db import db_open

# Kiosk Main Page.   Display buttons and route to action when they're pressed
def kiosk(request):

	if request.POST:
		button_t = request.POST
#		try:
		
		button_pressed =int(button_t.get("kiosk_button1"))
#		except:
#			return kiosk_none1(request)

		# If button pressed is Job (Tagged as -1 )
		if button_pressed == -1:
			return kiosk_job(request)
		# If button pressed is Production (Tagged as -2)
		if button_pressed == -2:
			return kiosk_production(request)
		# If button pressed is Help (Tagged as -3)
		if button_pressed == -3:
			return kiosk_help(request)
		# If button pressed is Scrap (Tagged as -4)
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


def kiosk_job(request):

	return render(request, "kiosk/kiosk_job.html")

def kiosk_job2(request):
	if request.POST:
		button_tag = request.POST
#		try:
		button_pressed2 = int(button_tag.get("kb"))
#		except:
#			return kiosk_none(request)
		
		# If button pressed is StartJob (Tagged as -1)
		if button_pressed2 == -1:
			return kiosk_job_assign(request)
		if button_pressed2 == -2:
			return kiosk_job_leave(request)
		return kiosk_done4(request)
	else:
		form = kiosk_dispForm2()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_job2.html",{'args':args})
	
	
def kiosk_production(request):
	return render(request, "kiosk/kiosk_production.html")
def kiosk_help(request):
	return render(request, "kiosk/kiosk_help.html")
def kiosk_job_assign(request):
	return render(request, "kiosk/kiosk_job_assign.html")
def kiosk_job_leave(request):
	return render(request, "kiosk/kiosk_job_leave.html")
def kiosk_scrap(request):
	return render(request, "kiosk/kiosk_scrap.html")
def kiosk_none(request):
	return render(request, "kiosk/kiosk_none.html")	
def kiosk_none1(request):
	return render(request, "kiosk/kiosk_none1.html")	
