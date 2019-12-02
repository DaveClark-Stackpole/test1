from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views_global_mods import machine_rates, Metric_OEE

from time import strftime
from datetime import datetime
import MySQLdb
import time


def testB(request):

	return render(request, "testB.html")	
	
	
def fup(x):
	xx = x[1]
	xy = str(xx)
	yy = xy[-4:]
	return yy

def iup(x):
	return x[0]
		
def frup(x):
	return x[11]	

def gup(x):
	return x[5]
	
def nup(x):
	return x[4]

def tup(x):
	global tst, down_time
	tst.append(str(x[5]))

	
def eup(x):
		global st, nt
		nt.append(str(x[2]))
		h = 1
		st.append(str(h))

		# st.append(str(x[5]))

def mup(x):
		global dt
		dt.append(str(x[7]))
		
def pup(x):
	global lt
	lt.append(str(x[11]))
	
# *******************************************************
# *******************************************************
# *  Determine Graph Data
# *******************************************************
def Graph_Data(t,u,machine,tmp):
	global tst, down_time
	cc = 0
	cr = 0
	cm = 0
	# last_by used for comparison
	last_by = 0
	temp_ctr = 0
	brk1 = 0
	brk2 = 0
	
	tm_sh = int((t-u)/60)
	px = [0 for x in range(tm_sh)]
	by = [0 for x in range(tm_sh)]
	ay = [0 for x in range(tm_sh)]
	cy = [0 for x in range(tm_sh)]
	for ab in range(0,tm_sh):

		px[ab] =u + (cc*60)
		yy = px[ab]
		cc = cc + 1
		cr = cr + .83
		cm = cr * .85
		tst = []
		[tup(x) for x in tmp if fup(x) == machine and nup(x) < yy]
		by[ab] = sum(int(i) for i in tst)
		ay[ab] = int(cr)
		cy[ab] = int(cm)
		
		# *** Calculate the longest break time in minutes
		# *** and assign to brk_ctr
		if by[ab] == last_by:
			temp_ctr = temp_ctr + 1
		else:
			if temp_ctr > brk1:
				brk1 = temp_ctr
			elif temp_ctr > brk2:
				brk2 = temp_ctr
			temp_ctr = 0
			last_by = by[ab]
		# ************************************************

	tm_sh = tm_sh - 1
	lby = by[tm_sh]
	lay = ay[tm_sh]
	lpx = px[tm_sh]
	gr_list = zip(px,by,ay,cy)	
	
	#return gr_list, brk1, brk2, tm_sh
	return gr_list, brk1, brk2
# *******************************************************
def display_AB1V(request):
	
  try:
	live_bit = int(request.session["live"])	
  except:
	live_bit = 1
   
  if live_bit == 1:
	  t=int(time.time())
  else:
	  t=int(request.session["snapshot_time"])	  
  
	
	
  rx=[0 for i in range(11)]
  
  gx=[0 for i in range(11)]
  a1=[0 for i in range(4)]
  a2=[0 for i in range(4)]
  a3=[0 for i in range(4)]
  a4=[0 for i in range(4)]
  a5=[0 for i in range(4)]
  a6=[0 for i in range(4)]
  a7=[0 for i in range(4)]
  a8=[0 for i in range(4)]
  a9=[0 for i in range(4)]
  b1=[0 for i in range(4)]
  b2=[0 for i in range(4)]
  b3=[0 for i in range(4)]
  b4=[0 for i in range(4)]
  b5=[0 for i in range(4)]
  b6=[0 for i in range(4)]
  b7=[0 for i in range(4)]
  b8=[0 for i in range(4)]  
  b9=[0 for i in range(4)]	
  c1=[0 for i in range(4)]
  c2=[0 for i in range(4)]
  c3=[0 for i in range(4)]
  c4=[0 for i in range(4)]
  c5=[0 for i in range(4)]
  c6=[0 for i in range(4)]
  c7=[0 for i in range(4)]
  c8=[0 for i in range(4)]
  c9=[0 for i in range(4)]  
  OA=[0 for i in range(12)]
  Actr= 0
  Bctr= 0
  Cctr= 0
  
  rx[0], rx[1], rx[2], rx[3], rx[4], rx[5], rx[6], rx[7], rx[8], rx[9], rx[10] = "0%", "45%", "47%", "52%", "57%", "65%", "72%", "79%", "85%", "90%", "100%" 
  gx[0], gx[1], gx[2], gx[3], gx[4], gx[5], gx[6], gx[7], gx[8], gx[9], gx[10]= "0%", "15%", "18%", "23%", "30%", "40%", "43%", "47%", "50%", "60%", "100%"   
  
  rate = float(7)
  machine_list = ['5399','5404','5401','989','998','998','998','999','995','996','997','998']
  graph_link = ['/trakberry/graph677/','/trakberry/graph748/','/trakberry/graph749/','/trakberry/graph750/','/trakberry/graph615/','/trakberry/graph614/','/trakberry/graph629/','/trakberry/graph620/','/trakberry/graph574/','/trakberry/graph755/','/trakberry/graph756/','/trakberry/graph686/']
  mc2 = ['756','686','574','755']
  mc3 = ['629','620','615','614']
  info = ['','','','','','','','','','','','']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [12,54,49,55]
  machine_rate2 = [49,49,45,50]
  aaa = 0
  bbb = 0
  ccc = 0
  aoa = 0
  boa = 0
  coa = 0
  tm = time.localtime(t)
  
  
  count =[0,0,0,0,0,0,0,0,0,0,0,0]
  down_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  diff_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  part = [0,0,0,0,0,0,0,0,0,0,0,0]
  machine_rate = [0,0,0,0,0,0,0,0,0,0,0,0]
  diff = [0,0,0,0,0,0,0,0,0,0,0,0]
  required =[0,0,0,0,0,0,0,0,0,0,0,0]
  projection = [0,0,0,0,0,0,0,0,0,0,0,0]
  running_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  target = [0,0,0,0,0,0,0,0,0,0,0,0]
  hrate =[0,0,0,0,0,0,0,0,0,0,0,0]
  cycle =[0,0,0,0,0,0,0,0,0,0,0,0]
  OEE = [0,0,0,0,0,0,0,0,0,0,0,0]
  yellow = [0,0,0,0,0,0,0,0,0,0,0,0]
  red = [0,0,0,0,0,0,0,0,0,0,0,0]
  green = [0,0,0,0,0,0,0,0,0,0,0,0]
  gry = [0,0,0,0,0,0,0,0,0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst

  
  # Determine initial Shift Start value based on current time
  # Initialize shift_start as -1 to represent 11pm so all 24hr numbers calculate properly
  shift_start = -1
  if tm[3]<23 and tm[3]>=15:
	shift_start = 15
  elif tm[3]<15 and tm[3]>=7:
	shift_start = 7
  cur_hour = tm[3]
  if cur_hour == 23:
	cur_hour = -1
  
  # Shift Start EPOCH TIME designation  
  # Set u to the epoch time for the beginning of the shift of current day.  Either 23, 7 or 15	
  u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])




#   u = 1575027098    # TEMPORARY VALUE

  
  #ik = 1130000
  #u = u - 28800
  
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)
  hql = "SELECT MIN(id) FROM barcode where scrap >= '%d'" %(u)
  cursor.execute(hql)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  iik = tmp2[0]
  

  
  # Assign Min Id value in db so we only search required data
  try:
	if u != request.session["start_unix"]:
		request.session["start_unix"] = u
		hql = "SELECT MIN(id) FROM barcode where scrap >= '%d'" %(u)
		cursor.execute(hql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		ik = tmp2[0]
		request.session["start_id"] = ik
		BB=1
	else:
		ik = request.session["start_id"]
		BB=2
	
  except:
	request.session["start_unix"] = u
	hql = "SELECT MIN(id) FROM barcode where scrap >= '%d'" %(u)
	cursor.execute(hql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	ik = tmp2[0]
	request.session["start_id"] = ik
	BB=3
  # ***********************************************************
  			
  ik = iik
#   qqq=request.session["dddd"]
  #sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d' and Id > '%d'" %(u,t,ik)
 
  #Decide if we select data for Live Tracking or for Snapshot
  if live_bit == 1:
	  sql = "SELECT * FROM barcode where id >= '%d'" %(ik)
  else:
	  sql = "SELECT * FROM barcode where id >= '%d' and scrap < '%d'" %(ik,t)
	  	
  cursor.execute(sql)
  tmp = cursor.fetchall()
  
  db.close()
  #return render(request, "test99_1.html", {'test': ik})
  rate = 0.00790

 
  # find totals of each non zero part for each machine
  for y in range(0, 12):
	st = []
	nt = []
	pt = []
	dt = []

	# Make gup look for > 0 so we can force a number in there to alter that count
	[eup(x) for x in tmp if fup(x) == machine_list[y]]
	count[y] = sum(int(i) for i in st)

	# ****** Graph Variables Code ---place in gr_list   ***************************************************************
	kk=int((t-u)/60)
	if machine_list[y] == request.session["machine_chart"]:
		gr_list, brk1, brk2  = Graph_Data(t,u,machine_list[y],tmp)
	# ****************************************************************************************************************
	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
#	if part[y] == '50-3632':
#		machine_rate[y] = machine_rate1[y]
#	elif part[y] == '50-0786':
#		machine_rate[y] = machine_rate2[y]
#	else:
#		machine_rate[y] = 0

	# Call module machine_rates to retrive the machine rate  mrate
	machine_rate[y] = machine_rates(part[y],machine_list[y])
	#machine_rate[y] = 75
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
	
	# # old downtime calculation.   Need a new one to figure out
	# [mup(x) for x in tmp if fup(x) == machine_list[y]]
	# down_time[y] = sum(int(i) for i in dt)

	down_time[y] = 0

#	if machine_list[y]=='614':
#		return render(request,"test5.html",{'MC':machine_list[y],'DT':down_time[y]})
		
	
	# Using Metric_OEE from 'views_global_mods.py'
	running_time[y] = t-u
	running_time[y] = running_time[y] - down_time[y]
	target_prod = running_time[y] / float(machine_rate[y])
	
	#try:
	#	OEE [ y ] = count[y] / float(target_prod)
	#except:
	#	OEE [ y ] = 0
	
	MOEE = Metric_OEE(t, u, down_time[y], count[y], machine_rate[y])
	OA [ y ] = MOEE				
	if MOEE > 0 :
		OEE [ y ] = str ( MOEE ) + "%"
	else:
		OEE [ y ] = '00.0%'

	# Determine idle time
	if (diff[y]>cycle[y]):
		idle = diff [ y ] - cycle [ y ]
	else:
		idle = 0
	# *****************************************************

	try:
		request.session["details_gf6op30"]
	except:
		request.session["details_gf6op30"] = 0
		
	# calculate projected shift target
#	t = int(time.time())
	time_ran = t - int(u)
	rate = (count[y]/float(time_ran))
	projection[y] = round(rate * 28800,0)
	required[y] = round(machine_rate[y]*8,0)
	target[y] = round((machine_rate[y]/float(3600))*time_ran,0)
	hrate[y] = round(rate *3600,2)
	total = total + count[y]	
	
	rmix = " #18BA20 "
	gmix = " yellow "

	
	if idle > 0  and idle < 180:
		# percentage of Green / Yellow
		idle = (idle / float(180)) * 100
	elif idle > 179 and idle < 900:
		# percentage of Yellow / Red
		idle = ((idle - 180)/ float(720))*100
		rmix = " yellow "
		gmix = " red "
	elif idle >899:
		# all red
		rmix = " yellow "
		gmix = " red "
		idle = 100

	idle = int(round(idle / 10))
	
	red[y] = rmix + rx[idle]
	green[y] = gmix + gx[idle] 
	gry[y] = " #858585 100%"
	
#	red[y]=900
#	yellow[y]=180
	for xx in range(0,12):
		yellow[xx] = red[xx]

	info[y] = "Part:&nbsp;&nbsp;"+str(part[y])+"<br>Production:&nbsp;&nbsp;"+ str(count[y])+"<br>Projection:&nbsp;&nbsp;"+str(target[y])+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])
 # tm=int(time.time())
 
		
  request.session["track_start"] = t

  
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th
  
  mlist = zip(machine_list,count)
  #list = zip(machine_list,info,red,yellow,green,mc2,mc3,gry,graph_link,count)
  list = zip(machine_list,info,red,yellow,green,gry,graph_link,count)
  for y in range(0, 12):
		if y == 0:
			a1[y] = machine_list[y]
			a2[y] = info[y]
			a3[y] = red[y]
			a4[y] = yellow[y]
			a5[y] = green[y]
			a6[y] = gry[y]
			a7[y] = graph_link[y]
			a8[y] = count[y]
			a9[y] = OEE[y]
			aaa = aaa + count[y]
			aoa = aoa + OA [ y ]
			if OA [ y ] >5:
				Actr = Actr + 1
			#aoa = aoa + OEE[y]
			
		if y == 1:
			b1[y-4] = machine_list[y]
			b2[y-4] = info[y]
			b3[y-4] = red[y]
			b4[y-4] = yellow[y]
			b5[y-4] = green[y]
			b6[y-4] = gry[y]
			b7[y-4] = graph_link[y]
			b8[y-4] = count[y]
			b9[y-4] = OEE[y]
			bbb = bbb + count[y]
			boa = boa + OA [ y ]
			if OA [ y ] > 5:
				Bctr = Bctr + 1
			
		if y == 2:
			c1[y-6] = machine_list[y]
			c2[y-6] = info[y]
			c3[y-6] = red[y]
			c4[y-6] = yellow[y]
			c5[y-6] = green[y]
			c6[y-6] = gry[y]
			c7[y-6] = graph_link[y]
			c8[y-6] = count[y]
			c9[y-6] = OEE[y]	
			ccc = ccc + count[y]
			coa = coa + OA [ y ]
			if OA [ y ] > 5:
				Cctr = Cctr + 1
  
  try:
	  aoa = int((float(aoa/Actr))*10)/10
  except:
	  aoa = 0 	  
  try:
	  boa = int((float(boa/Bctr))*10)/10
  except:
	  boa = 0 		
  try:
	  coa = int((float(coa/Cctr))*10)/10
  except:
	  coa = 0	
  				
  nlist = zip(a1,a2,a3,a4,a5,a6,a7,a8,b1,b2,b3,b4,b5,b6,b7,b8,c1,c2,c3,c4,c5,c6,c7,c8,a9,b9,c9) 					
  
  
  xlist = zip(machine_list,count,OEE,machine_rate,down_time,running_time)
#  return render(request,"test.html",{'list':xlist})
  
  if request.session["machine_chart"]=="nope":
	#return render(request,"gf6input.html",{'list':list})
	return render(request,"gf6input.html",{'list':nlist,'totalA':aaa,'totalB':bbb,'totalC':ccc,'COA':coa,'BOA':boa,'AOA':aoa})
	#return render(request,"test.html",{'list':nlist})
  else:  
	#return render(request,"gf6input.html",{'list':list,'GList':gr_list})
	return render(request,"gf6input.html",{'list':nlist,'GList':gr_list})

			
	#return render(request,"test.html",{'list':nlist})

def display2(request):
  try:
	live_bit = int(request.session["live"])	
  except:
	live_bit = 1
   
  if live_bit == 1:
	  t=int(time.time())
  else:
	  t=int(request.session["snapshot_time"])	  
  

	
  rx=[0 for i in range(11)]
  gx=[0 for i in range(11)]
  a1=[0 for i in range(4)]
  a2=[0 for i in range(4)]
  a3=[0 for i in range(4)]
  a4=[0 for i in range(4)]
  a5=[0 for i in range(4)]
  a6=[0 for i in range(4)]
  a7=[0 for i in range(4)]
  a8=[0 for i in range(4)]
  a9=[0 for i in range(4)]
  b1=[0 for i in range(4)]
  b2=[0 for i in range(4)]
  b3=[0 for i in range(4)]
  b4=[0 for i in range(4)]
  b5=[0 for i in range(4)]
  b6=[0 for i in range(4)]
  b7=[0 for i in range(4)]
  b8=[0 for i in range(4)]  
  b9=[0 for i in range(4)]	
  c1=[0 for i in range(4)]
  c2=[0 for i in range(4)]
  c3=[0 for i in range(4)]
  c4=[0 for i in range(4)]
  c5=[0 for i in range(4)]
  c6=[0 for i in range(4)]
  c7=[0 for i in range(4)]
  c8=[0 for i in range(4)]
  c9=[0 for i in range(4)]  
  OA=[0 for i in range(12)]
  Actr= 0
  Bctr= 0
  Cctr= 0
  
  rx[0], rx[1], rx[2], rx[3], rx[4], rx[5], rx[6], rx[7], rx[8], rx[9], rx[10] = "0%", "45%", "47%", "52%", "57%", "65%", "72%", "79%", "85%", "90%", "100%" 
  gx[0], gx[1], gx[2], gx[3], gx[4], gx[5], gx[6], gx[7], gx[8], gx[9], gx[10]= "0%", "15%", "18%", "23%", "30%", "40%", "43%", "47%", "50%", "60%", "100%"   
  
  rate = float(7)
  machine_list = ['Trilobe','996','995','989','Optimize','998','1515','1501','995','996','997','998']
  graph_link = ['/trakberry/graph677/','/trakberry/graph748/','/trakberry/graph749/','/trakberry/graph750/','/trakberry/graph615/','/trakberry/graph614/','/trakberry/graph629/','/trakberry/graph620/','/trakberry/graph574/','/trakberry/graph755/','/trakberry/graph756/','/trakberry/graph686/']
  mc2 = ['756','686','574','755']
  mc3 = ['629','620','615','614']
  info = ['','','','','','','','','','','','']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [12,54,49,55]
  machine_rate2 = [49,49,45,50]
  aaa = 0
  bbb = 0
  ccc = 0
  aoa = 0
  boa = 0
  coa = 0
  tm = time.localtime(t)
  
  
  count =[0,0,0,0,0,0,0,0,0,0,0,0]
  down_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  diff_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  part = [0,0,0,0,0,0,0,0,0,0,0,0]
  machine_rate = [0,0,0,0,0,0,0,0,0,0,0,0]
  diff = [0,0,0,0,0,0,0,0,0,0,0,0]
  required =[0,0,0,0,0,0,0,0,0,0,0,0]
  projection = [0,0,0,0,0,0,0,0,0,0,0,0]
  running_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  target = [0,0,0,0,0,0,0,0,0,0,0,0]
  hrate =[0,0,0,0,0,0,0,0,0,0,0,0]
  cycle =[0,0,0,0,0,0,0,0,0,0,0,0]
  OEE = [0,0,0,0,0,0,0,0,0,0,0,0]
  yellow = [0,0,0,0,0,0,0,0,0,0,0,0]
  red = [0,0,0,0,0,0,0,0,0,0,0,0]
  green = [0,0,0,0,0,0,0,0,0,0,0,0]
  gry = [0,0,0,0,0,0,0,0,0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst

  
  # Determine initial Shift Start value based on current time
  # Initialize shift_start as -1 to represent 11pm so all 24hr numbers calculate properly
  shift_start = -1
  if tm[3]<23 and tm[3]>=15:
	shift_start = 15
  elif tm[3]<15 and tm[3]>=7:
	shift_start = 7
  cur_hour = tm[3]
  if cur_hour == 23:
	cur_hour = -1
  
  # Shift Start EPOCH TIME designation  
  # Set u to the epoch time for the beginning of the shift of current day.  Either 23, 7 or 15	
  u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])
  
  #ik = 1130000
  #u = u - 28800
  
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)
  hql = "SELECT MIN(Id) FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
  cursor.execute(hql)
  tmp = cursor.fetchall()
  tmp2 = tmp[0]
  iik = tmp2[0]
  
  
  # Assign Min Id value in db so we only search required data
  try:
	if u != request.session["start_unix"]:
		request.session["start_unix"] = u
		hql = "SELECT MIN(Id) FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
		cursor.execute(hql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		ik = tmp2[0]
		request.session["start_id"] = ik
		BB=1
	else:
		ik = request.session["start_id"]
		BB=2
	
  except:
	request.session["start_unix"] = u
	hql = "SELECT MIN(Id) FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
	cursor.execute(hql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	ik = tmp2[0]
	request.session["start_id"] = ik
	BB=3
  # ***********************************************************
  			
  ik = iik
  #sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d' and Id > '%d'" %(u,t,ik)
 
  #Decide if we select data for Live Tracking or for Snapshot
  if live_bit == 1:
	  sql = "SELECT * FROM tkb_prodtrak where Id >= '%d'" %(ik)
  else:
	  sql = "SELECT * FROM tkb_prodtrak where Id >= '%d' and part_timestamp < '%d'" %(ik,t)
	  	
  cursor.execute(sql)
  tmp = cursor.fetchall()
  
  db.close()
  #return render(request, "test99_1.html", {'test': ik})
  rate = 0.00790
  # find totals of each non zero part for each machine
  for y in range(0, 12):
	st = []
	nt = []
	pt = []
	dt = []
	# Make gup look for > 0 so we can force a number in there to alter that count
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) > 0]
	count[y] = sum(int(i) for i in st)
	
	# TEST
	#if machine_list[y] == '1506':
	#	return render(request, "test8.html", {'A': count[y],'B': y, 'C': machine_list[y],'D':st})
	
	
	
	# ****** Graph Variables Code ---place in gr_list   ***************************************************************
	kk=int((t-u)/60)
	if machine_list[y] == request.session["machine_chart"]:
		gr_list, brk1, brk2  = Graph_Data(t,u,machine_list[y],tmp)
	# ****************************************************************************************************************
	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
#	if part[y] == '50-3632':
#		machine_rate[y] = machine_rate1[y]
#	elif part[y] == '50-0786':
#		machine_rate[y] = machine_rate2[y]
#	else:
#		machine_rate[y] = 0

	# Call module machine_rates to retrive the machine rate  mrate
	machine_rate[y] = machine_rates(part[y],machine_list[y])
	#machine_rate[y] = 75
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
		
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
#	if machine_list[y]=='614':
#		return render(request,"test5.html",{'MC':machine_list[y],'DT':down_time[y]})
		
	
	# Using Metric_OEE from 'views_global_mods.py'
	running_time[y] = t-u
	running_time[y] = running_time[y] - down_time[y]
	target_prod = running_time[y] / float(machine_rate[y])
	
	#try:
	#	OEE [ y ] = count[y] / float(target_prod)
	#except:
	#	OEE [ y ] = 0
	
	MOEE = Metric_OEE(t, u, down_time[y], count[y], machine_rate[y])
	OA [ y ] = MOEE				
	if MOEE > 0 :
		#MOEE = int (MOEE*10)
		#MOEE = float(MOEE / 10)
		#MOEE = str ( MOEE ) 
		#TOEE = MOEE[:2] + '.' + MOEE[1:]
		#MOEE = MOEE[:2] + '.' + MOEE[1:] + '%' 
		OEE [ y ] = str ( MOEE ) + "%"
		#MOEE = int (MOEE * 1000)
		#MOEE = str ( MOEE ) 
		#MOEE = MOEE[:2] + '.' + MOEE[1:] + '%' 
		#OEE [ y ] = MOEE
	else:
		OEE [ y ] = '00.0%'
				
#	OEE [ y ] = Metric_OEE(t,u,down_time[y],count[y],machine_rate[y])
	#OEE [ y ] = int(OEE[y]*10000)/float(100)
	#OEE [ y ] = "("+str(OEE[y])+"%" + ")"


	# Determine idle time
	if (diff[y]>cycle[y]):
		idle = diff [ y ] - cycle [ y ]
	else:
		idle = 0
	# *****************************************************

		
#	try:
#		m, s = divmod(down_time[y],60)
#		h, m = divmod(m, 60)
#		down_time[y] ="%d:%02d:%02d" % (h,m,s)
#	except:
#		down_time[y] = 0
		
	try:
		request.session["details_gf6op30"]
	except:
		request.session["details_gf6op30"] = 0
		
	# calculate projected shift target
#	t = int(time.time())
	time_ran = t - int(u)
	rate = (count[y]/float(time_ran))
	projection[y] = round(rate * 28800,0)
	required[y] = round(machine_rate[y]*8,0)
	target[y] = round((machine_rate[y]/float(3600))*time_ran,0)
	hrate[y] = round(rate *3600,2)
	total = total + count[y]	
	
	rmix = " #18BA20 "
	gmix = " yellow "

	
	if idle > 0  and idle < 180:
		# percentage of Green / Yellow
		idle = (idle / float(180)) * 100
	elif idle > 179 and idle < 900:
		# percentage of Yellow / Red
		idle = ((idle - 180)/ float(720))*100
		rmix = " yellow "
		gmix = " red "
	elif idle >899:
		# all red
		rmix = " yellow "
		gmix = " red "
		idle = 100

	idle = int(round(idle / 10))
	
	red[y] = rmix + rx[idle]
	green[y] = gmix + gx[idle] 
	gry[y] = " #858585 100%"
	
#	red[y]=900
#	yellow[y]=180
	for xx in range(0,12):
		yellow[xx] = red[xx]

	info[y] = "Part:&nbsp;&nbsp;"+str(part[y])+"<br>Production:&nbsp;&nbsp;"+ str(count[y])+"<br>Projection:&nbsp;&nbsp;"+str(target[y])+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])
 # tm=int(time.time())
 
		
  request.session["track_start"] = t
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th
  
  mlist = zip(machine_list,count)
  #list = zip(machine_list,info,red,yellow,green,mc2,mc3,gry,graph_link,count)
  list = zip(machine_list,info,red,yellow,green,gry,graph_link,count)
  for y in range(0, 12):
		if y < 4:
			a1[y] = machine_list[y]
			a2[y] = info[y]
			a3[y] = red[y]
			a4[y] = yellow[y]
			a5[y] = green[y]
			a6[y] = gry[y]
			a7[y] = graph_link[y]
			a8[y] = count[y]
			a9[y] = OEE[y]
			aaa = aaa + count[y]
			aoa = aoa + OA [ y ]
			if OA [ y ] >5:
				Actr = Actr + 1
			#aoa = aoa + OEE[y]
			
		if y >3 and y<6:
			b1[y-4] = machine_list[y]
			b2[y-4] = info[y]
			b3[y-4] = red[y]
			b4[y-4] = yellow[y]
			b5[y-4] = green[y]
			b6[y-4] = gry[y]
			b7[y-4] = graph_link[y]
			b8[y-4] = count[y]
			b9[y-4] = OEE[y]
			bbb = bbb + count[y]
			boa = boa + OA [ y ]
			if OA [ y ] > 5:
				Bctr = Bctr + 1
			
		if y >5 and y <8:
			c1[y-6] = machine_list[y]
			c2[y-6] = info[y]
			c3[y-6] = red[y]
			c4[y-6] = yellow[y]
			c5[y-6] = green[y]
			c6[y-6] = gry[y]
			c7[y-6] = graph_link[y]
			c8[y-6] = count[y]
			c9[y-6] = OEE[y]	
			ccc = ccc + count[y]
			coa = coa + OA [ y ]
			if OA [ y ] > 5:
				Cctr = Cctr + 1
  
  try:
	  aoa = int((float(aoa/Actr))*10)/10
  except:
	  aoa = 0 	  
  try:
	  boa = int((float(boa/Bctr))*10)/10
  except:
	  boa = 0 		
  try:
	  coa = int((float(coa/Cctr))*10)/10
  except:
	  coa = 0	
  				
  nlist = zip(a1,a2,a3,a4,a5,a6,a7,a8,b1,b2,b3,b4,b5,b6,b7,b8,c1,c2,c3,c4,c5,c6,c7,c8,a9,b9,c9) 					
  
  
  xlist = zip(machine_list,count,OEE,machine_rate,down_time,running_time)
#  return render(request,"test.html",{'list':xlist})
  
  if request.session["machine_chart"]=="nope":
	#return render(request,"gf6input.html",{'list':list})
	return render(request,"gf6input.html",{'list':nlist,'totalA':aaa,'totalB':bbb,'totalC':ccc,'COA':coa,'BOA':boa,'AOA':aoa})
	#return render(request,"test.html",{'list':nlist})
  else:  
	#return render(request,"gf6input.html",{'list':list,'GList':gr_list})
	return render(request,"gf6input.html",{'list':nlist,'GList':gr_list})

			
	#return render(request,"test.html",{'list':nlist})


def create_table(request):
  # Construct tkb_prodtrak format
  # Select prodrptdbtest db 
  
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)  
  
#  cursor.execute("""DROP TABLE IF EXISTS tkb_prodtrak""")
#  cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_prodtrak(Id INT PRIMARY KEY AUTO_INCREMENT,pi_id INT(10), machine CHAR(30), part_timestamp INT(20), qty INT(2), pcount INT(20), downtime INT(20), cycletime INT(10), status VARCHAR(25))""")
#  cursor.execute("""DROP TABLE IF EXISTS tkb_employee""")
  cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_techs(Id INT PRIMARY KEY AUTO_INCREMENT,tech CHAR(50))""")
  
  db.commit()
#  t = int(time.time())
#  m1 = '750'
#  m2 = '749'
#  m3 = '677'
#  m4 = '748'
#  tb = 101
#  qty = 0
#  perp = 0
#  sqA =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m1,t,qty,perp) )
#  sqB =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m2,t,qty,perp) )
#  sqC =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m3,t,qty,perp) )
#  sqD =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m4,t,qty,perp) )
#  cursor.execute(sqA)
#  cursor.execute(sqB)
#  cursor.execute(sqC)
#  cursor.execute(sqD)
#  db.commit()
  db.close()
  return render(request,'done_test3.html')
 
def create_test_table(request):
  # Construct tkb_test format
  # Select prodrptdbtest db 
  
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)  
  cursor = db.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_test(Id INT PRIMARY KEY AUTO_INCREMENT,message CHAR(30),stime INT(20),ftime INT(20),ctime INT(20))""")
  db.commit()
  m1 = 'BEGIN MESSAGES'
  st = 0
  ft = 0  
  ct = 999
  db.commit()
  sqA =( 'insert into tkb_test(message,stime,ftime,ctime) values("%s","%d","%d","%d")' % (m1,st,ft,ct))
  cursor.execute(sqA)
  db.commit()
  db.close()
  return render(request,'done.html')

  # Alter a column name in a table 
def alter_table_name(request):  
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)
  cursor.execute("""ALTER TABLE tkb_prodtrak RENAME COLUMN pcount to perpetual_counter""")
  db.commit() 
  return render(request,'done.html')
  
  
def db_write(request):
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request) 
  
  first = "Dave"
  last = "Clark"
  number = 4955
  t = datetime.datetime.now()
  

  # Below is example of inserting text into coloumns of gpio table
  #sql = '''INSERT into gpio (Machine, Date) VALUES ('Willie', 'Wonka')'''

  # Below is example of inserting variables into columns of gpio table.  (use tuple %d for integers)
  cursor.execute('''INSERT INTO vacation(first,last,start,end,number) VALUES(%s,%s,%s,%s,%s)''', (first,last,t,t,number))
  
  sql =( 'insert into gpio(Machine,Date) values("%s","%s")' % (A,B) )
  
  cursor.execute(sql)
  db.commit()

  db.close()
  return render(request,'done.html')


def test(request):

	# Time Conversions.  Timestamp - DateTime and vica versa **********
	
	x=[]
	# takes a unix timestamp
	t = int(time.time())
	x=[0 for i in range(9)] 
	# converts timestamp to a tuple with format
	tm = time.localtime(t)
	
	# take an assigned tuple
	x[0] = 2015
	x[1] = 8
	x[2] = 8
	x[3] = 3
	x[4] = 1
	x[5] = 45
	# and convert to a unix time
	y = time.mktime(x)
	# ******************************************************************


#	dif = (tm[3]-15)*60*60
#	dif = dif + (tm[4]*60)+tm[5]
#	u=t-dif
#	tx = time.localtime(u)
	
	#call each variable in tuple as needed Ex  tm[3] = hours
	#h = request.session["s_date"]
	#xm = time.mktime(h)
	
	
	# ***Convert formated datetime '2015-09-01T15:09' and convert to timestamp and tuple
	# *** s_date is string used
	
	start_date = request.session["s_date"]
	
	temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")
	#   Time Stamp
	start_stamp = int(time.mktime(temp.timetuple()))
	#   Time Tuple
	start_tuple = time.localtime(start_stamp)
	




	
	return render(request, "test_1.html", {'Hour': tm,'Time': t, 'Time2': y, 'Stamp':start_stamp, 'Tuple':start_tuple})

def done(request):
	try:
		callroute = request.session["call_route"]
	except:
		callroute = "sup"	
	if callroute == "tech":
		request.session["refresh_tech"] = '1'
		return render(request, "tech.html")
	else:
		return render(request, "done.html")
		
	
# Module to expand / retract details on Live Tracking	
def details_session(request):
	temp = int(request.session["details_gf6op30"])
	if temp == 1:
		request.session["details_gf6op30"] = 0
	else:
		request.session["details_gf6op30"] = 1
		
	return display(request)

def details_track(request):
	try:
		temp = int(request.session["details_track"])
	except:
		temp = 1

	if temp == 1:
		tm=int(time.time())
		# Set the time in seconds for timeout on Display mode
		en = tm + 7200
		
		request.session["track_end"] = en
		request.session["details_track"] = 0
	else:
		request.session["details_track"] = 1
		
	return display(request)	
	
# Run initialize module on first click of Live Track 	
def display_initialize(request):


	# Check if it's local running or not and if not then force the path as /trakberry
	# Run switch_net to set it back to network or switch_local for local use
	try:
		if request.session["local_switch"] == 1:
			request.session["local_toggle"] = ""
		else:
			request.session["local_toggle"] = "/trakberry"
	except:
		request.session["local_toggle"] = "/trakberry"
	# ******************************************************************************
	
	try:
		request.session["login_name"]
	except:
		request.session["login_name"] = "John Seagram"
		

	en = (int(time.time())) + 800
	request.session["track_end"] = en
	request.session["details_track"] = 0
	request.session["live"] = 1
	
	# uncomment below when running 
	return display(request)
	
	# use below to test value of track_end on display_initialize call
	#return render(request, "test99.html")


	
def display(request):
	try:
		st = int(time.time())
		en = int(request.session["track_end"])
	except:
		st=int(time.time())
		# Set the time in seconds for timeout on Display mode
		en = st + 7200
		
		request.session["track_end"] = en
		request.session["display_track"] = 0
	
	if st > en:
		request.session["details_track"] = 1
		
	return display_AB1V(request)	
	
def tech_reset(request):
	request.session["call_route"] = ''
	request.session["url_route"] = ''
	return render(request,'done_test.html')
	return main(request)
	
def main(request):
	try:
		password = request.session["login_password"]
	except:
		password = 'incorrect'
		
	if password == 'stackberry':
		return render(request, "main.html")
	else:	
		return main_login(request)
	
	
def graph749(request):
	request.session["machine_chart"] = "749"
	return display(request)
def graph749_snap(request):
	request.session["machine_chart"] = "749"
	return display_time(request)	
	
def graph748(request):
	request.session["machine_chart"] = "748"
	return display(request)
def graph748_snap(request):
	request.session["machine_chart"] = "748"
	return display_time(request)	

def graph750(request):
	request.session["machine_chart"] = "750"
	return display(request)
def graph750_snap(request):
	request.session["machine_chart"] = "750"
	return display_time(request)	

def graph677(request):
	request.session["machine_chart"] = "677"
	return display(request)	
def graph677_snap(request):
	request.session["machine_chart"] = "677"
	return display_time(request)		

def graph_close(request):
	request.session["machine_chart"] = "nope"
	return display(request)		

def graph_close_snap(request):
	request.session["machine_chart"] = "nope"
	return display_time(request)		
	
def reports(request):

	return render(request, "reports.html")	


# Call Graph

		
def test44(request):
	#request.session["test"] = 78
	return render(request, "test4.html")
	
def scheduler(request):

	return render(request, "scheduler.html")
def inventory(request):

	return render(request, "inventory.html")		


def production_report(request):

	machine_list = [677,748,749,750]
	total = [0,0,0,0]
	part = [0,0,0,0]
	
	start_date = request.session["s_date"]
	end_date = request.session["e_date"]
	
	temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")
	start_stamp = int(time.mktime(temp.timetuple()))
	start_tuple = time.localtime(start_stamp)

	temp = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")
	end_stamp = int(time.mktime(temp.timetuple()))
	end_tuple = time.localtime(end_stamp)	

	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)
	
	for i in range(0, 4):
	
		sql = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine_list[i], start_stamp, end_stamp)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		total[i] = tmp2[0]
		
		sqm = "SELECT (part_number) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine_list[i], start_stamp, end_stamp)
		cursor.execute(sqm)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		part[i] = tmp2[0]
	
	list = zip(machine_list,total,part)
	return render(request, "report_page.html", {'List':list , 'S':start_tuple, 'E':end_tuple})

def test_time(request):

	# initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
	
	#request.session["local_time"] = tm

	shift_start = -1
	if tm[3]<23 and tm[3]>=15:
		shift_start = 15
	elif tm[3]<15 and tm[3]>=7:
		shift_start = 7
	
	#request.session["shift_start"] = shift_start

	u = t - (((tm[3]-shift_start)*60*60)+(tm[4]*60)+tm[5])
	d = t - u
	#request.session["unix_time"] = u
	
	
	return render(request, "test_time.html", {'Tm': tm,'S':shift_start,'U':u,'D':d})
	
	
def new(request):

	return render(request, "new.html")
	
	

		
def graph(request):

	return render(request, "graph.html")	
def graph2(request):
	x = 91
	y = 21
	return render(request, "graph2.html",{'X':x,'Y':y})		
	
def graph3(request):
	x = 2
	y = 21
	return render(request, "graph3.html",{'X':x,'Y':y})		

def fade_in(request):
  
  return render(request,'fade_in.html')
  
def fade2(request):
  
  return render(request,'fade2.html')  

def ttip(request):
	machine = [0,0,0,0]
	count=[0,0,0,0]
	machine[1]="677"
	count[1]=343
	machine[2]="749"
	count[2]=312
	machine[2]=machine[1]+"<br>"+"Hello"
	return render(request,'tooltip.html',{'machine':machine,'count':count})  

  	
def display_time(request):
  
  #  Working Time, uncomment when not testing
  t=int(time.time())
  
  start_date = request.session["s_date"]
  temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")
  start_stamp = int(time.mktime(temp.timetuple()))

  # Set time. 
  t = start_stamp

  rx=[0 for i in range(11)]
  gx=[0 for i in range(11)]
  a1=[0 for i in range(4)]
  a2=[0 for i in range(4)]
  a3=[0 for i in range(4)]
  a4=[0 for i in range(4)]
  a5=[0 for i in range(4)]
  a6=[0 for i in range(4)]
  a7=[0 for i in range(4)]
  a8=[0 for i in range(4)]
  b1=[0 for i in range(4)]
  b2=[0 for i in range(4)]
  b3=[0 for i in range(4)]
  b4=[0 for i in range(4)]
  b5=[0 for i in range(4)]
  b6=[0 for i in range(4)]
  b7=[0 for i in range(4)]
  b8=[0 for i in range(4)]  
  c1=[0 for i in range(4)]
  c2=[0 for i in range(4)]
  c3=[0 for i in range(4)]
  c4=[0 for i in range(4)]
  c5=[0 for i in range(4)]
  c6=[0 for i in range(4)]
  c7=[0 for i in range(4)]
  c8=[0 for i in range(4)]  
  
  rx[0], rx[1], rx[2], rx[3], rx[4], rx[5], rx[6], rx[7], rx[8], rx[9], rx[10] = "0%", "45%", "47%", "52%", "57%", "65%", "72%", "79%", "85%", "90%", "100%" 
  gx[0], gx[1], gx[2], gx[3], gx[4], gx[5], gx[6], gx[7], gx[8], gx[9], gx[10]= "0%", "15%", "18%", "23%", "30%", "40%", "43%", "47%", "50%", "60%", "100%"  
   
  rate = float(7)
  machine_list = ['677','748','749','750','615','614','629','620','574','755','756','686']
  graph_link = ['/trakberry/graph677_snap/','/trakberry/graph748_snap/','/trakberry/graph749_snap/','/trakberry/graph750_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/','/trakberry/graph748_snap/']
  mc2 = ['756','686','574','755']
  mc3 = ['629','620','615','614']
  info = ['','','','','','','','','','','','']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [54,54,49,55]
  machine_rate2 = [49,49,45,50]
  tm = time.localtime(t)
  count =[0,0,0,0,0,0,0,0,0,0,0,0]
  brk3 =[0,0,0,0,0,0,0,0,0,0,0,0]
  brk4 =[0,0,0,0,0,0,0,0,0,0,0,0]
  down_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  diff_time = [0,0,0,0,0,0,0,0,0,0,0,0]
  part = [0,0,0,0,0,0,0,0,0,0,0,0]
  machine_rate = [0,0,0,0,0,0,0,0,0,0,0,0]
  diff = [0,0,0,0,0,0,0,0,0,0,0,0]
  required = [0,0,0,0,0,0,0,0,0,0,0,0]
  projection = [0,0,0,0,0,0,0,0,0,0,0,0]
  
  target = [0,0,0,0,0,0,0,0,0,0,0,0]
  hrate = [0,0,0,0,0,0,0,0,0,0,0,0]
  cycle = [0,0,0,0,0,0,0,0,0,0,0,0]
  OEE = [0,0,0,0,0,0,0,0,0,0,0,0]  
  yellow = [0,0,0,0,0,0,0,0,0,0,0,0]
  red = [0,0,0,0,0,0,0,0,0,0,0,0]
  green = [0,0,0,0,0,0,0,0,0,0,0,0]
  gry = [0,0,0,0,0,0,0,0,0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst, lt
  
  # Testing
  #request.session["machine_chart"] = "749"
  
  # Determine initial Shift Start value based on current time
  # Initialize shift_start as -1 to represent 11pm so all 24hr numbers calculate properly
  shift_start = -1
  if tm[3]<23 and tm[3]>=15:
	shift_start = 15
  elif tm[3]<15 and tm[3]>=7:
	shift_start = 7
  cur_hour = tm[3]
  if cur_hour == 23:
	cur_hour = -1
  
  # Shift Start EPOCH TIME designation  
  # Set u to the epoch time for the beginning of the shift of current day.  Either 23, 7 or 15	
  u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])
  #u = u - 28800

  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)
  
  #sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
  sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d'" %(u,t)
  cursor.execute(sql)
  tmp = cursor.fetchall()

  rate = 0.00790
  # find totals of each non zero part for each machine
  for y in range(0,12):
	st = []
	nt = []
	pt = []
	dt = []
	lt = []
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 1]
	count[y] = sum(int(i) for i in st)
	
	#max(n for n in alist if n!=max(alist))
	
	
	[pup(x) for x in tmp if fup(x) == machine_list[y] and nup(x) > (u+1800)]

	try:
		t_brk = max(int(i) for i in lt)
		brk3[y] = int(t_brk/float(60))
	except:
		brk3[y] = 19
		t_brk = 0

	lt = []
	[pup(x) for x in tmp if fup(x) == machine_list[y] and nup(x) > (u+1800) and frup(x) < t_brk]
		
	try:
		brk4[y] = max(int(i) for i in lt)
		brk4[y] = int(brk4[y]/float(60))
	except:
		brk4[y] = 19

		
	# ******Graph Variables Code ---place in gr_list   ***************************************************************
	kk=int((t-u)/60)
	if machine_list[y] == request.session["machine_chart"]:
		gr_list, brk1, brk2  = Graph_Data(t,u,machine_list[y],tmp)
	# ****************************************************************************************************************

	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
#	if part[y] == '50-3632':
#		machine_rate[y] = machine_rate1[y]
#	elif part[y] == '50-0786':
#		machine_rate[y] = machine_rate2[y]
#	else:
#		machine_rate[y] = 0
	machine_rate[y] = machine_rates(part[y],machine_list[y])
	machine_rate[y]= 75
	
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
	
	machine_rate[y] = 75	
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	# Test Section
	
	tu = t-u
	x = (t-u)-down_time[y]
	targget = x / machine_rate[y]
	if x < 0 or x == 0:
		OEE[y] = 0
	else:
		OEE[y] = (count[y] / float(targget))*100

	#OEE [ y ] = Metric_OEE(t,u,down_time[y],count[y],machine_rate[y])
	
	# Determine idle time
	if (diff[y]>cycle[y]):
		idle = diff [ y ] - cycle [ y ]
	else:
		idle = 0
	# *****************************************************

		
	try:
		m, s = divmod(down_time[y],60)
		h, m = divmod(m, 60)
		down_time[y] ="%d:%02d:%02d" % (h,m,s)
	except:
		down_time[y] = 0
		
	try:
		request.session["details_gf6op30"]
	except:
		request.session["details_gf6op30"] = 0
		
	# calculate projected shift target
#	t = int(time.time())
	time_ran = t - int(u)
	rate = (count[y]/float(time_ran))
	projection[y] = round(rate * 28800,0)
	required[y] = round(machine_rate[y]*8,0)
	target[y] = targget
#	target[y] = round((machine_rate[y]/float(3600))*x,0)
	hrate[y] = round(rate *3600,2)
	total = total + count[y]	
	
	rmix = " #18BA20 "
	gmix = " yellow "
	if idle > 0  and idle < 180:
		# percentage of Green / Yellow
		idle = (idle / float(180)) * 100
	elif idle > 179 and idle < 900:
		# percentage of Yellow / Red
		idle = ((idle - 180)/ float(720))*100
		rmix = " yellow "
		gmix = " red "
	elif idle >899:
		# all red
		rmix = " yellow "
		gmix = " red "
		idle = 100

	idle = int(round(idle / 10))
	
	red[y] = rmix + rx[idle]
	green[y] = gmix + gx[idle] 
	gry[y] = " #858585 100%"
	
#	red[y]=900
#	yellow[y]=180
     
	for xx in range(0,12):
		yellow[xx] = red [xx]
		
		
	t_part = str(part[y])[:7]
	info[y] = "Part:&nbsp;&nbsp;"+str(t_part)+"<br>Production:&nbsp;&nbsp;"+ str(count[y]) +"<br>Projection:&nbsp;&nbsp;"+str(targget)+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])


  request.session["track_start"] = t
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th

  for y in range(0, 12):
		if y < 4:
			a1[y] = machine_list[y]
			a2[y] = info[y]
			a3[y] = red[y]
			a4[y] = yellow[y]
			a5[y] = green[y]
			a6[y] = gry[y]
			a7[y] = graph_link[y]
			a8[y] = count[y]
		if y >3 and y<8:
			b1[y-4] = machine_list[y]
			b2[y-4] = info[y]
			b3[y-4] = red[y]
			b4[y-4] = yellow[y]
			b5[y-4] = green[y]
			b6[y-4] = gry[y]
			b7[y-4] = graph_link[y]
			b8[y-4] = count[y]
		if y >7:
			c1[y-8] = machine_list[y]
			c2[y-8] = info[y]
			c3[y-8] = red[y]
			c4[y-8] = yellow[y]
			c5[y-8] = green[y]
			c6[y-8] = gry[y]
			c7[y-8] = graph_link[y]
			c8[y-8] = count[y]		
  nlist = zip(a1,a2,a3,a4,a5,a6,a7,a8,b1,b2,b3,b4,b5,b6,b7,b8,c1,c2,c3,c4,c5,c6,c7,c8)

 # return render(request,"test57.html",{'list':nlist})
  if request.session["machine_chart"]=="nope":
	  return render(request,"gf6input_fixed.html",{'list':nlist, 'S':temp})
  else:
	  return render(request,"gf6input_fixed.html",{'list':nlist,'GList':gr_list,'S':temp,'BrkA':brk1,'BrkB':brk2})	  
	  
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
  
	
  
	

  
  
