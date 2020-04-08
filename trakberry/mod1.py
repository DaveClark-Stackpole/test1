from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date, mgmt_display, mgmt_display_edit
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5,vacation_set_current6
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
from views_db import db_open, db_set
from views_production import mgmt_users_logins_edit
from datetime import datetime 

def hyphon_fix(tx):
    tps = list(tx)
    if (tx.find("'"))>0:
        ty = list(tx)
        ta = tx.find("'")
        ty[ta] = ""
        tc = "".join(ty)
    else:
        tc = tx

    return tc

def multi_name_breakdown(n):
    nm = []
    tx = n
    if (tx.find("|"))>0:
        while True:
            len_tx = len(tx)
            ty = list(tx)
            ta = tx.find("|")
            ta = ta - 1
            lft = tx[:ta]
            nm.append(lft)
            ta = ta + 3
            ta_right = len_tx - ta
            tx = tx[-ta_right:]
            len_tx = len(tx)
            if (tx.find("|"))<0:
                break
        nm.append(tx)
    return nm


def index_template(request, index):
	page1 = request.session["page_edit"]
	request.session["current_index"] = index
	db, cur = db_set(request)

	if page1 == 'user login':
		request.session["user_logins1"] = ""
		request.session["password"] = "Stackpole1"
		request.session["department"] = ""

		if int(index) == 0:
			return render(request,'production/redirect_mgmt_users_logins_add.html')

		sql1 = "SELECT * FROM tkb_logins where Id='%s'" % (index)
		cur.execute(sql1)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		request.session["current_tmp"] = tmp2
		request.session["user_logins1"] = tmp2[1]
		request.session["password"] = tmp2[2]
		request.session["department"] = tmp2[3]
		a = request.session["user_logins1"]

		return render(request,'production/redirect_mgmt_users_logins_edit.html')

	db.close()

	return done_test(request)
