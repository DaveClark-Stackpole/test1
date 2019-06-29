from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views_global_mods import machine_rates, Metric_OEE

from time import strftime
from datetime import datetime
import MySQLdb
import time


	  
def fix_time(request):
	db, cursor = db_set(request)
	a = 2268996
	b = 2287243
	data = []
	tb = []
	mc = []
	tm = []
	pid = []
	for x in range(a,b):
		asql = "SELECT pi_id,machine,part_timestamp,Id FROM tkb_prodtrak where Id = '%s'" %(x)

		cursor.execute(asql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		data.append(tmp2)
	
	for y in data:
		ts = y[2]
		if y[0] == 102:
			c = y[3]-1
			while True:
				bsql = "SELECT pi_id,part_timestamp FROM tkb_prodtrak where Id = '%s'" %(c)
				cursor.execute(bsql)
				tmp = cursor.fetchall()
				tmp2 = tmp[0]
				if tmp2[0] == 101:
					ts = tmp2[1]
					break
				c = c - 1
				
		tb.append(y[0])
		mc.append(y[1])
		pid.append(y[3])
		tm.append(ts)
		
		sql2 = ('update tkb_prodtrak SET part_timestamp ="%s" WHERE Id ="%s"' % (ts,y[3]))
		cursor.execute(sql2)
		db.commit()
		


	data2 = zip(tb,mc,tm,pid)
	db.close()
	test = 'Hello'
	return render(request,"test99.html",{'test':data,'data2':data2})
  
	
  
	

  
  
