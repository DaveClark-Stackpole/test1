from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
from views_routes import direction
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
import MySQLdb
import time
from django.core.context_processors import csrf
import datetime as dt 
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current6, vacation_set_current5

def hrly_display(request):
    hourly = ['' for x in range(0)]
    db, cur = db_open()  
    s1 = "SELECT p_cell FROM sc_prod_hr_target"
    cur.execute(s1)
    tmp = cur.fetchall()
    p_cell = tmp[0]
    db.commit()

    for i in tmp:
        pc = i[0]
#aql = "SELECT MAX(id) FROM sc_prod_hour where p_cell = '%s'" %(pc)" 
	#    cur.execute(aql)
#	    tmp3 = cur.fetchall()
#	    tmp4 = tmp3[0]
#	    tmp5 = tmp4[0]

        ii = request.session['jjiie']
    ii = request.session['jjiie']
    db.close()
    return render(request,'kiosk/kiosk_test4.html', {'tmp':tmp})	

