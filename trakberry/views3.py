from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
from trakberry.forms import login_Form, login_password_update_Form
from datetime import datetime
import MySQLdb
import time
import os
import smtplib
from smtplib import SMTP


def excel_test(request):

	t=int(time.time())
	u = t - 1800
	global st, pt_ctr,nt, pt, dt, tst
	db, cursor = db_open()
	
  
	#sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp> '%d'" %(u)
	cursor.execute(sql)
	tmp = cursor.fetchall()

	st = []
	nt = []
	pt = []
	dt = []
	df = []
	[eup(x) for x in tmp if fup(x) == '574' and gup(x) == 1]
	#count[y] = sum(int(i) for i in st)

	lst = int(min(nt))

	for y in nt:
		diff = int(y) - int(lst)
		df.append(str(diff))
		lst = y
	
	# sort data
#	ct = len(nt)
#	for x in range(0, ct-1):
#		for xx in range(x+1, ct):
#			if int(df[xx])< int(df[x]):
#				ddf = df[x]
#				df[x] = df[xx]
#				df[xx] = ddf
#				nnt = nt[x]
#				nt[x] = nt[xx]
#				nt[xx] = nnt
				
		

	mlist = zip(nt,df)
	return render(request,"test5.html",{'list':mlist})
 

