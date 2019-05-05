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
from views_db import db_open
from datetime import datetime


def ios_test1(request):
	# Creates a new backup table of tkb_cycletimes
	db, cursor = db_open()  
	
	cursor.execute("""DROP TABLE IF EXISTS sc_prod_parts_backup""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS sc_prod_parts_backup LIKE sc_prod_parts""")
	cursor.execute('''INSERT sc_prod_parts_backup Select * From sc_prod_parts''')
	db.commit()
	db.close()
	return render(request, "kiosk/kiosk_test4.html")	

def ios_test2(request):
	# Searches all in sc_production1 unique asset num with machine >1
	l = 1
	len_part = 5
	id_start = 237056
	db, cur = db_open()

	sql = "SELECT DISTINCT partno FROM sc_production1 where LENGTH(partno) > '%d' and id > '%d' ORDER BY %s %s" %(len_part,id_start,'partno','ASC')


#	sql = "SELECT DISTINCT asset_num, machine, partno FROM sc_production1  where LENGTH(asset_num) >'%d' and LENGTH(machine) >'%d' ORDER BY %s %s,%s %s" %(l,l,'asset_num','ASC','id','DESC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	return render(request, "kiosk/kiosk_test4.html",{'tmp':tmp})

def ios_test(request):
	# Searches all in sc_production1 unique asset num with machine >1
	l = 1
	len_part = 5
	id_start = 237056
	dte = []
	db, cur = db_open()
	sql = "SELECT DISTINCT partno FROM sc_production1 where LENGTH(partno) > '%d' and id > '%d' ORDER BY %s %s" %(len_part,id_start,'partno','ASC')
#	sql = "SELECT DISTINCT asset_num, machine, partno FROM sc_production1  where LENGTH(asset_num) >'%d' and LENGTH(machine) >'%d' ORDER BY %s %s,%s %s" %(l,l,'asset_num','ASC','id','DESC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]

	for x in tmp:
#		asset = x[0]
#		machine = x[1]
		part = x[0]
		try:
			aql = "SELECT COUNT(*) FROM sc_prod_parts WHERE parts_no = '%s'" %(part)
			cur.execute(aql)
			t2 = cur.fetchall()
			t3 = t2[0]
			cnt = t3[0]
		except:
			cnt = 0
		if int(cnt) < 1:
			cur.execute('''INSERT INTO sc_prod_parts(parts_no) VALUES(%s)''',(part))
			db.commit()
		
	db.close()
	return render(request, "kiosk/kiosk_test4.html",{'tmp':tmp})

