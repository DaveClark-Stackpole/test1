from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import sup_downForm, sup_dispForm, sup_closeForm, report_employee_Form, sup_vac_filterForm, sup_message_Form
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

from time import mktime
from datetime import datetime, date
from views_db import db_open


def kiosk(request):


#		if request.POST:
#			request.session["test"] = 999
#		a = request.POST
#		try:
#			b=int(a.get("one"))
#		except:
#			return render(request,'display_sup_refresh.html')	
#		if b == -1:
#			return done(request)
#		if b == -2:
#			request.session["call_route"] = 'supervisor'
#			request.session["url_route"] = 'main.html'
#			return done_tech(request)
#		if b == -3:
#			return done_elec(request)	
#		if b == -4:
#			return done_maint(request)		
#		request.session["index"] = b
#		#request.session["test"] = request.POST
#		return done_edit(request)
#	else:
#		form = sup_dispForm()
#	args = {}
#	args.update(csrf(request))
#	args['form'] = form
#	
	# *********************************************************************************************************
	# ******     Messaging portion of the Tech App  ************Not Working**********************************
	# *********************************************************************************************************
#	try:
#		N = request.session["login_name"]
#	except:
#		N = ''
#	R = 0
#	db, cur = db_open() 
#	try:
#		sql = "SELECT * FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)	
#		cur.execute(sql)
#		tmp44 = cur.fetchall()
#		tmp4 = tmp44[0]
#
#		request.session["sender_name"] = tmp4[2]
#		request.session["sender_name_last"] = tmp4[2]
#		request.session["message_id"] = tmp4[0]
#
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
#	Z_Value = 1
#	if cnt > 0 :
#		cnt = 1
#		request.session["refresh_sup"] = 3
#	 ********************************************************************************************************

#	cnt = 0
#	request.session["refresh_sup"] = 0
#	tmp4 =''
#	Z_Value = 1
#	tcur=int(time.time())

  # call up 'display.html' template and transfer appropriate variables.  
	#return render(request,"test3.html",{'total':tmp4,'Z':Z_Value,'})
#	return render(request,"kiosk.html",{'L':list,'N':n,'cnt':cnt,'M':tmp4,'Z':Z_Value,'TCUR':tcur,'args':args})

	return render(request,"kiosk.html")

