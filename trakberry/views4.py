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


def ios_test(request):
	# Creates a new backup table of tkb_cycletimes
	db, cur = db_open()  
	s1 = "SELECT p_cell FROM sc_prod_hr_target"
	cur.execute(s1)
	tmp = cur.fetchall()

	db.commit()
	db.close()
	return render(request, "kiosk/kiosk_test4.html",{'tmp':tmp})	

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

def ios_test1(request):
	# Searches all in sc_production1 unique asset num with machine >1
	l = 1
	len_part = 5
	id_start = 237056
	pd = '2019-05-29'
	po = '50-9341'
	lft = 'OP'
	shf = '11pm-7am'
	dte = []
	db, cur = db_open()
	sql = "SELECT DISTINCT comments FROM sc_production1 where partno = '%s' and pdate  = '%s' and left(machine,2) = '%s' and shift  = '%s' " %(po,pd,lft,shf)
#	sql = "SELECT DISTINCT asset_num, machine, partno FROM sc_production1  where LENGTH(asset_num) >'%d' and LENGTH(machine) >'%d' ORDER BY %s %s,%s %s" %(l,l,'asset_num','ASC','id','DESC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]

	ctr = 0
	for i in tmp:
		ctr = ctr + 1


	return render(request, "kiosk/kiosk_test4.html",{'tmp':ctr})

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

def NotDone(request):
#	shift = '11pm-7am'
#	shift = '7am-3pm'
	shift = '3pm-11pm'

	pdate = '2019-05-23'
	job_missed = ['' for z in range(0)]
	part_missed = ['' for z in range(0)]

	db, cur = db_open()
	s1ql = "SELECT DISTINCT asset FROM tkb_cycletime"
	cur.execute(s1ql)
	tmp1 = cur.fetchall()
	

	s2ql = "SELECT asset_num FROM sc_production1 where shift = '%s' and pdate = '%s'" %(shift,pdate)
	cur.execute(s2ql)
	tmp2 = cur.fetchall()
	

	xx = 0
	for x in tmp1:
		ch = 0
		a = x[0]
		for y in tmp2:
			xx = xx + 1
			b = y[0]

			if a == b:
				ch = 1
#				job_missed.append(b)
#				part_missed.append(c)
#				hh = request.session["hh"]
		if ch == 0:
			job_missed.append(a)
#			part_missed.append(c)
#	List = zip(job_missed,part_missed)


	return render(request, "kiosk/kiosk_test4.html",{'tmp':job_missed})

def IsDone(request):
	id1 = 1
	name1 = '"Dave"'
#	name1 = str(name1)

#	cur.execute("""SELECT COUNT(*) FROM test WHERE attribute = %s AND unit_id IN %s""", (a, unit_ids))
	
#	cql =" ('update role SET name="%s" WHERE Id="%s" ' %(name1,id1)) "

	name1 = '"Dave"'
	cql = ("""update role SET name = %s WHERE Id = %s""" % (name1,id1))
	dql = str(cql)

	yy = request.session["ymym"]
#	cql = ('update role SET name="%s" WHERE Id="%s"' %(name1,id1))
	db, cur = db_open()
	cur.execute(dql)
	db.commit()
	db.close()

	return render(request, "kiosk/kiosk_test5.html")


	shift = '11pm-7am'
#	shift = '7am-3pm'
#	shift = '3pm-11pm'
	y = request.session['helpppee']
	pdate = '2019-05-10'
	job_missed = ['' for z in range(0)]
	part_missed = ['' for z in range(0)]

	db, cur = db_open()
	s1ql = "SELECT DISTINCT asset FROM tkb_cycletime"
	cur.execute(s1ql)
	tmp1 = cur.fetchall()
	
	s2ql = "SELECT asset_num,partno FROM sc_production1 where shift = '%s' and pdate = '%s'" %(shift,pdate)
	cur.execute(s2ql)
	tmp2 = cur.fetchall()
	
	xx = 0
	for x in tmp1:
		ch = 0
		a = x[0]
		for y in tmp2:
			xx = xx + 1
			b = y[0]
			c = y[1]
			if a == b:
				ch = 1
				job_missed.append(b)
				part_missed.append(c)
#				hh = request.session["hh"]
		if ch == 0:
			dummy = 1
#			job_missed.append(a)
#			part_missed.append(c)
	List = zip(job_missed,part_missed)


	return render(request, "kiosk/kiosk_test5.html",{'tmp':List})
	

def target_fix1(request):

	db, cur = db_open()  
	pr = '27'
	pid = 450276

	sql = "Select * From sc_production1 where id > '%d' and LEFT(asset_num,2) != '%s' " %(pid,pr) # Get latest entry for p_cell
	cur.execute(sql)
	tmp = cur.fetchall()
	ccct = 0

	for i in tmp:
		try:
			asset = i[1]
			hrs = i[12]
			id1 = i[0]
			s1ql = "Select * from tkb_cycletime where asset = '%s' " % (asset)
			cur.execute(s1ql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			tmp4 = tmp3[4]
			ct = str(tmp4)
			ct = float(ct)
			h = float(hrs)
			target1 = ((h * 60 * 60) / (ct))
			cql = ('update sc_production1 SET target = "%s" WHERE id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			ccct = ccct + 1

		except:
			dummy = 1
#		if ccct > 0:
#	uu = request.session['kkeee']
		


	return render(request, "kiosk/kiosk_test6.html",{'tmp':tmp})