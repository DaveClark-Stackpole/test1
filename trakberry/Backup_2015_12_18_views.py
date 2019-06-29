from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from time import strftime
from datetime import datetime
import MySQLdb
import time

def fup(x):
	return x[2]

def gup(x):
	return x[5]
	
def nup(x):
	return x[4]

def tup(x):
	global tst, down_time
	tst.append(str(x[5]))

	
def eup(x):
		global st, nt
		nt.append(str(x[4]))
		st.append(str(x[5]))
		
def mup(x):
		global dt
		dt.append(str(x[7]))
		
# *******************************************************
# *  Determine Metrics OEE , Availability and Performance
# *******************************************************
def Metric_OEE(t,u,down_time,count):

	# Calculate Planned Availability
	#PT = 28800 - down_time[y]
	PT = (t-u) - down_time
	A = (PT / float((t-u)))
	# Calculate Performance
	P = count * (60/45)*60
	try:
		P = P / float(PT)
	except:
		P = 0
	# Calculate OEE
	OEE = (int((A * P)*10000))/float(100)
	
	return OEE
# *******************************************************

def Graph_Data(t,u,machine,tmp):
	global tst, down_time
	cc = 0
	cr = 0
	cm = 0
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
	
	tm_sh = tm_sh - 1
	lby = by[tm_sh]
	lay = ay[tm_sh]
	lpx = px[tm_sh]
	gr_list = zip(px,by,ay,cy)	
	
	return gr_list
	
	
def display2(request):

  t=int(time.time())


  rx=[0 for i in range(11)]
  gx=[0 for i in range(11)]
  rx[0] = "0%"
  rx[1] = "45%"
  rx[2] = "47%"
  rx[3] = "52%"
  rx[4] = "57%"
  rx[5] = "65%"
  rx[6] = "72%"
  rx[7] = "79%"
  rx[8] = "85%"
  rx[9] = "90%"
  rx[10]="100%"
  
  gx[0] = "0%"
  gx[1] = "15%"
  gx[2]= "18%"
  gx[3]="23%"
  gx[4]="30%"
  gx[5]="40%"
  gx[6] = "43%"
  gx[7] = "47%"
  gx[8] = "50%"
  gx[9] = "60%" 
  gx[10]="100%"
  
  
  
  
  rate = float(7)
  machine_list = ['677','748','749','750']
  graph_link = ['/trakberry/graph677/','/trakberry/graph748/','/trakberry/graph749/','/trakberry/graph750/']
  mc2 = ['756','686','574','755']
  mc3 = ['629','620','615','614']
  info = ['','','','']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [54,54,49,55]
  machine_rate2 = [49,49,45,50]
  tm = time.localtime(t)
  count =[0,0,0,0]
  down_time = [0,0,0,0]
  diff_time = [0,0,0,0]
  part = [0,0,0,0]
  machine_rate = [0,0,0,0]
  diff = [0,0,0,0]
  required = [0,0,0,0]
  projection = [0,0,0,0]
  
  target = [0,0,0,0]
  hrate = [0,0,0,0]
  cycle = [0,0,0,0]
  OEE = [0,0,0,0]  
  yellow = [0,0,0,0]
  red = [0,0,0,0]
  green = [0,0,0,0]
  gry = [0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst
  
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
  for y in range(0, 4):
	st = []
	nt = []
	pt = []
	dt = []
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 1]
	count[y] = sum(int(i) for i in st)
	
	# ******Graph Variables Code ***************************************************************
	if request.session["machine_chart"] <> "none":
		#t=int(time.time())
		kk=int((t-u)/60)
		if machine_list[y] == request.session["machine_chart"]:
			cc = 0
			cr = 0
			cm = 0
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
				[tup(x) for x in tmp if fup(x) == machine_list[y] and nup(x) < yy]
				by[ab] = sum(int(i) for i in tst)
				ay[ab] = int(cr)
				cy[ab] = int(cm)
	
			tm_sh = tm_sh - 1
			
			lby = by[tm_sh]
			lay = ay[tm_sh]
			lpx = px[tm_sh]
			gr_list = zip(px,by,ay,cy)	
			
	# ******************************************************************************	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
	if part[y] == '50-3632':
		machine_rate[y] = machine_rate1[y]
	elif part[y] == '50-0786':
		machine_rate[y] = machine_rate2[y]
	else:
		machine_rate[y] = 0
	
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
		
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	OEE [ y ] = Metric_OEE(t,u,down_time[y],count[y])

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
	
	yellow[0] = red[0]
	yellow[1] = red[1]
	yellow[2] = red[2]
	yellow[3] = red[3]	
	
	info[y] = "Part:&nbsp;&nbsp;"+str(part[y])+"<br>Production:&nbsp;&nbsp;"+ str(count[y]) +"<br>Projection:&nbsp;&nbsp;"+str(target[y])+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])
 # tm=int(time.time())
  
		
  request.session["track_start"] = t
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th
  
  
  list = zip(machine_list,info,red,yellow,green,mc2,mc3,gry,graph_link)
  
  if request.session["machine_chart"]=="nope":
	return render(request,"gf6input.html",{'list':list})
  else:  
	return render(request,"gf6input.html",{'list':list,'GList':gr_list})


def create_table(request):
  # Construct tkb_prodtrak format
  # Select prodrptdbtest db 
  
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  cursor.execute("""DROP TABLE IF EXISTS tkb_prodtrak""")
  cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_prodtrak(Id INT PRIMARY KEY AUTO_INCREMENT,pi_id INT(10), machine CHAR(30), part_timestamp INT(20), qty INT(2), pcount INT(20), downtime INT(20), cycletime INT(10), status VARCHAR(25))""")
  db.commit()
  t = int(time.time())
  m1 = '750'
  m2 = '749'
  m3 = '677'
  m4 = '748'
  tb = 101
  qty = 0
  perp = 0
  db.commit()
  sqA =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m1,t,qty,perp) )
  sqB =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m2,t,qty,perp) )
  sqC =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m3,t,qty,perp) )
  sqD =( 'insert into tkb_prodtrak(pi_id,machine,part_timestamp,qty,pcount) values("%d","%s","%d","%d","%d")' % (tb,m4,t,qty,perp) )
  cursor.execute(sqA)
  cursor.execute(sqB)
  cursor.execute(sqC)
  cursor.execute(sqD)
  db.commit()
  db.close()
  return render(request,'done.html')
 
def create_test_table(request):
  # Construct tkb_test format
  # Select prodrptdbtest db 
  
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
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
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
  cursor = db.cursor()
  cursor.execute("""ALTER TABLE tkb_prodtrak RENAME COLUMN pcount to perpetual_counter""")
  db.commit() 
  return render(request,'done.html')
  
  
def db_write(request):
  # Select prodrptdbtest db 
  db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdbtest')
  cur = db.cursor()
  
  A = "TrialRun"
  B = "TestValue"

  # Below is example of inserting text into coloumns of gpio table
  #sql = '''INSERT into gpio (Machine, Date) VALUES ('Willie', 'Wonka')'''

  # Below is example of inserting variables into columns of gpio table.  (use tuple %d for integers)
  sql =( 'insert into gpio(Machine,Date) values("%s","%s")' % (A,B) )
  
  cur.execute(sql)
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
	#request.session["test"] = 78
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
		en = tm + 600
		
		request.session["track_end"] = en
		request.session["details_track"] = 0
	else:
		request.session["details_track"] = 1
		
	return display(request)	

def display(request):
	try:
		st = int(time.time())
		en = int(request.session["track_end"])
	except:
		st=int(time.time())
		# Set the time in seconds for timeout on Display mode
		en = st + 800
		
		request.session["track_end"] = en
		request.session["display_track"] = 0
	
	if st > en:
		request.session["details_track"] = 1
	return display2(request)	
	
	
def main(request):

	return render(request, "main.html")
	
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


# ****************************************************************************
# *******  Test module to display past info and resemble live information ****
# ****************************************************************************	
def display_past(request):
	
  t=int(time.time())
  rate = float(7)
  machine_list = ['677','748','749','750']
  information = ['hello','hithere','Bonjour','Ahola']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [54,54,49,55]
  machine_rate2 = [49,49,45,50]
  tm = time.localtime(t)
  count =[0,0,0,0]
  down_time = [0,0,0,0]
  diff_time = [0,0,0,0]
  part = [0,0,0,0]
  machine_rate = [0,0,0,0]
  diff = [0,0,0,0]
  required = [0,0,0,0]
  target = [0,0,0,0]
  projection = [0,0,0,0]
  hrate = [0,0,0,0]
  cycle = [0,0,0,0]
  OEE = [0,0,0,0]
  yellow = [0,0,0,0]
  red = [0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst
  
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
  # Select prodrptdb db 
  u  = 1444849200
  uu = 1444878000
  
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)

  sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' AND part_timestamp < '%d'" %(u, uu)
 
  cursor.execute(sql)
  tmp = cursor.fetchall()

  rate = 0.00790
  # find totals of each non zero part for each machine
  for y in range(0, 4):
	st = []
	nt = []
	pt = []
	dt = []
	det = []
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 1]
	count[y] = sum(int(i) for i in st)
	
	#[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 0]
	
	# experimental code ***************************************************************
	if request.session["machine_chart"] <> "none":
		
		#t=int(time.time())
		t = uu
		kk=int((t-u)/60)
		if machine_list[y] == request.session["machine_chart"]:
			cc = 0
			cr = 0
			cm = 0
			tm_sh = int((t-u)/60)
			px = [0 for x in range(tm_sh)]
			by = [0 for x in range(tm_sh)]
			ay = [0 for x in range(tm_sh)]
			cy = [0 for x in range(tm_sh)]
			dt_total = [0 for x in range(tm_sh)]
			for ab in range(0,tm_sh):

				px[ab] =u + (cc*60)
				yy = px[ab]
				cc = cc + 1
				cr = cr + .83
				cm = cr * .85
				tst = []
				
				[tup(x) for x in tmp if fup(x) == machine_list[y] and nup(x) < yy]
				by[ab] = sum(int(i) for i in tst)
				ay[ab] = int(cr)
				cy[ab] = int(cm)
	
			tm_sh = tm_sh - 1
			
			lby = by[tm_sh]
			lay = ay[tm_sh]
			lpx = px[tm_sh]
			gr_list = zip(px,by,ay,cy)	
			
	# ******************************************************************************	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
	if part[y] == '50-3632':
		machine_rate[y] = machine_rate1[y]
	elif part[y] == '50-0786':
		machine_rate[y] = machine_rate2[y]
	else:
		machine_rate[y] = 0
	
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
		
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	#[vup(x) for x in tmp if fup(x) == machine_list[y] amd kup(x) == 
	
	# *******************************************************
	# *  Determine Metrics OEE , Availability and Performance
	# *******************************************************
	# Calculate Planned Availability
	PT = 28800 - down_time[y]
	A = (PT / float(28800))
	# Calculate Performance
	P = count[y] * (60/45)*60
	try:
		P = P / float(PT)
	except:
		P = 0
	# Calculate OEE
	OEE [ y ] = (int((A * P)*10000))/float(100)
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
	t = int(time.time())
	time_ran =uu - int(u)
	rate = (count[y]/float(time_ran))
	projection[y] = round(rate * 28800,0)
	required[y] = round(machine_rate[y]*8,0)
	target[y] = round((machine_rate[y]/float(3600))*time_ran,0)
	hrate[y] = round(rate *3600,2)
	
	total = total + count[y]	
	red[y]=900
	yellow[y]=180
	#det[y] = "Part:"+part[y]+" Production:"+ count[y] +"<br>Projection:"+target[y]+" OEE:"+OEE[y]
	det[y] = "Hello"
  tm=int(time.time())
  
	
  request.session["track_start"] = tm
  

	
  #return render(request,"graph4.html",{'gr_list':list,'lay':lay,'lby':lby,'lpx':lpx,'kk':kk})
  #request.session["details_gf6op30"] = 1
  if request.session["machine_chart"]=="nope":
	return render(request,"gf6input.html",{'Count':count,'Diff':diff, 'Yellow':yellow, 'Red':red, 'Diff_time':diff_time, 'Machine':machine_list, 'Total':total, 'Cycle':cycle, 'Hrate':hrate, 'Downtime':down_time, 'Projection':target, 'information':information, 'OEE':OEE, 'Part':part})
  else:
	return render(request,"gf6input.html",{'Count':count,'Diff':diff, 'Yellow':yellow, 'Red':red, 'Diff_time':diff_time, 'Machine':machine_list, 'Total':total, 'det':det, 'Hrate':hrate, 'Downtime':down_time, 'Projection':target, 'Part':part,'List':gr_list,'lay':lay,'lby':lby,'lpx':lpx,'kk':kk, 'OEE':OEE,'information':information})
  


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


def display_settime(request):
  # Below is the proper code, uncomment to stop debug mode	
  #t=int(time.time())
  
  # Using below fixed time 't' for testing purposes	
  t = 1449266440

  rx=[0 for i in range(11)]
  gx=[0 for i in range(11)]
  rx[0] = "0%"
  rx[1] = "45%"
  rx[2] = "47%"
  rx[3] = "52%"
  rx[4] = "57%"
  rx[5] = "65%"
  rx[6] = "72%"
  rx[7] = "79%"
  rx[8] = "85%"
  rx[9] = "90%"
  rx[10]="100%"
  
  gx[0] = "0%"
  gx[1] = "15%"
  gx[2]= "18%"
  gx[3]="23%"
  gx[4]="30%"
  gx[5]="40%"
  gx[6] = "43%"
  gx[7] = "47%"
  gx[8] = "50%"
  gx[9] = "60%" 
  gx[10]="100%"
  
  
  
  
  rate = float(7)
  machine_list = ['677','748','749','750']
  mc2 = ['756','686','574','755']
  mc3 = ['629','620','615','614']
  info = ['','','','']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [54,54,49,55]
  machine_rate2 = [49,49,45,50]
  tm = time.localtime(t)
  count =[0,0,0,0]
  down_time = [0,0,0,0]
  diff_time = [0,0,0,0]
  part = [0,0,0,0]
  machine_rate = [0,0,0,0]
  diff = [0,0,0,0]
  required = [0,0,0,0]
  projection = [0,0,0,0]
  
  target = [0,0,0,0]
  hrate = [0,0,0,0]
  cycle = [0,0,0,0]
  OEE = [0,0,0,0]  
  yellow = [0,0,0,0]
  red = [0,0,0,0]
  green = [0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst
  
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
  # Select prodrptdb db 
  # Select prodrptdb db located in views_db
  db, cursor = db_set(request)
  
  #sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
  sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d'" %(u,t)
  cursor.execute(sql)
  tmp = cursor.fetchall()

  rate = 0.00790
  # find totals of each non zero part for each machine
  for y in range(0, 4):
	st = []
	nt = []
	pt = []
	dt = []
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 1]
	count[y] = sum(int(i) for i in st)
	
	# ******Graph Variables Code ***************************************************************
	if request.session["machine_chart"] <> "none":
		#t=int(time.time())
		kk=int((t-u)/60)
		if machine_list[y] == request.session["machine_chart"]:
			cc = 0
			cr = 0
			cm = 0
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
				[tup(x) for x in tmp if fup(x) == machine_list[y] and nup(x) < yy]
				by[ab] = sum(int(i) for i in tst)
				ay[ab] = int(cr)
				cy[ab] = int(cm)
	
			tm_sh = tm_sh - 1
			
			lby = by[tm_sh]
			lay = ay[tm_sh]
			lpx = px[tm_sh]
			gr_list = zip(px,by,ay,cy)	
			
	# ******************************************************************************	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
	if part[y] == '50-3632':
		machine_rate[y] = machine_rate1[y]
	elif part[y] == '50-0786':
		machine_rate[y] = machine_rate2[y]
	else:
		machine_rate[y] = 0
	
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
		
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	# *******************************************************
	# *  Determine Metrics OEE , Availability and Performance
	# *******************************************************
	# Calculate Planned Availability
	#PT = 28800 - down_time[y]
	PT = (t-u) - down_time[y]
	A = (PT / float((t-u)))
	# Calculate Performance
	P = count[y] * (60/45)*60
	try:
		P = P / float(PT)
	except:
		P = 0
	# Calculate OEE
	OEE [ y ] = (int((A * P)*10000))/float(100)
	
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
	
#	red[y]=900
#	yellow[y]=180
	
	yellow[0] = red[0]
	yellow[1] = red[1]
	yellow[2] = red[2]
	yellow[3] = red[3]	
	
	info[y] = "Part:&nbsp;&nbsp;"+str(part[y])+"<br>Production:&nbsp;&nbsp;"+ str(count[y]) +"<br>Projection:&nbsp;&nbsp;"+str(target[y])+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])
 # tm=int(time.time())
  
		
  request.session["track_start"] = t
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th
  
  
  list = zip(machine_list,info,red,yellow,green,mc2,mc3)
  return render(request,"gf6input.html",{'list':list})
	
	
  #return render(request,"graph4.html",{'gr_list':list,'lay':lay,'lby':lby,'lpx':lpx,'kk':kk})
  #request.session["details_gf6op30"] = 1
  
  
  #if request.session["machine_chart"]=="nope":
	#return render(request,"gf6input.html",{'Count':count,'Diff':diff, 'Yellow':yellow, 'Red':red, 'Diff_time':diff_time, 'Machine':machine_list, 'Total':total, 'Cycle':cycle, 'Hrate':hrate, 'Downtime':down_time, 'Projection':target, 'Part':part, 'OEE':OEE,'info':info})
  #else:
	#return render(request,"gf6input.html",{'Count':count,'Diff':diff, 'Yellow':yellow, 'Red':red, 'Diff_time':diff_time, 'Machine':machine_list, 'Total':total, 'Cycle':cycle, 'Hrate':hrate, 'Downtime':down_time, 'Projection':target, 'Part':part,'List':gr_list,'lay':lay,'lby':lby,'lpx':lpx,'kk':kk, 'OEE':OEE,'info':info})
  	
def display_time(request):
  
  #  Working Time, uncomment when not testing
  t=int(time.time())
  
  
  start_date = request.session["s_date"]
  
  temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")



#  temp = datetime.strptime(start_date,"%Y-%m-%d")
  start_stamp = int(time.mktime(temp.timetuple()))
#  start_tuple = time.localtime(start_stamp)

  
  # Set time.  Use this EPOCH to test 
  t = start_stamp
#  t = 1450146000
 # t = request.session["s_date"]
  rx=[0 for i in range(11)]
  gx=[0 for i in range(11)]
  rx[0] = "0%"
  rx[1] = "45%"
  rx[2] = "47%"
  rx[3] = "52%"
  rx[4] = "57%"
  rx[5] = "65%"
  rx[6] = "72%"
  rx[7] = "79%"
  rx[8] = "85%"
  rx[9] = "90%"
  rx[10]="100%"
  
  gx[0] = "0%"
  gx[1] = "15%"
  gx[2]= "18%"
  gx[3]="23%"
  gx[4]="30%"
  gx[5]="40%"
  gx[6] = "43%"
  gx[7] = "47%"
  gx[8] = "50%"
  gx[9] = "60%" 
  gx[10]="100%"
  
  
  
  
  rate = float(7)
  machine_list = ['677','748','749','750']
  graph_link = ['/trakberry/graph677_snap/','/trakberry/graph748_snap/','/trakberry/graph749_snap/','/trakberry/graph750_snap/']
  mc2 = ['756','686','574','755']
  mc3 = ['629','620','615','614']
  info = ['','','','']
  # Machine Rates for 1:50-3632  2:50-0786
  machine_rate1 = [54,54,49,55]
  machine_rate2 = [49,49,45,50]
  tm = time.localtime(t)
  count =[0,0,0,0]
  down_time = [0,0,0,0]
  diff_time = [0,0,0,0]
  part = [0,0,0,0]
  machine_rate = [0,0,0,0]
  diff = [0,0,0,0]
  required = [0,0,0,0]
  projection = [0,0,0,0]
  
  target = [0,0,0,0]
  hrate = [0,0,0,0]
  cycle = [0,0,0,0]
  OEE = [0,0,0,0]  
  yellow = [0,0,0,0]
  red = [0,0,0,0]
  green = [0,0,0,0]
  gry = [0,0,0,0]
  total = 0
  
  try:
	request.session["machine_chart"]
  except:
	request.session["machine_chart"] = "nope"

  global st, pt_ctr,nt, pt, dt, tst
  
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
  for y in range(0, 4):
	st = []
	nt = []
	pt = []
	dt = []
	[eup(x) for x in tmp if fup(x) == machine_list[y] and gup(x) == 1]
	count[y] = sum(int(i) for i in st)
	
	# ******Graph Variables Code ***************************************************************

	kk=int((t-u)/60)
	if machine_list[y] == request.session["machine_chart"]:
		gr_list = Graph_Data(t,u,machine_list[y],tmp)
		
		
		# Uncomment below if call to Graph_Data fails
#		cc = 0
#		cr = 0
#		cm = 0
#		tm_sh = int((t-u)/60)
#		px = [0 for x in range(tm_sh)]
#		by = [0 for x in range(tm_sh)]
#		ay = [0 for x in range(tm_sh)]
#		cy = [0 for x in range(tm_sh)]
#		for ab in range(0,tm_sh):

#			px[ab] =u + (cc*60)
#			yy = px[ab]
#			cc = cc + 1
#			cr = cr + .83
#			cm = cr * .85
#			tst = []
#			[tup(x) for x in tmp if fup(x) == machine_list[y] and nup(x) < yy]
#			by[ab] = sum(int(i) for i in tst)
#			ay[ab] = int(cr)
#			cy[ab] = int(cm)
	
#		tm_sh = tm_sh - 1
#		lby = by[tm_sh]
#		lay = ay[tm_sh]
#		lpx = px[tm_sh]
#		gr_list = zip(px,by,ay,cy)	
			
	# ******************************************************************************	
	try:
		diff[y] = t - int(max(nt))
		cycle[y] =sum([item[10] for item in tmp if item[4]==int(max(nt))])
		part[y] = "\n".join([item[3] for item in tmp if item[4]==int(max(nt))])
		
	except:
		diff[y] = t-u
		cycle[y] = 0
	
	# Determine what machine and part and assign the rate to 'machine_rate'
	if part[y] == '50-3632':
		machine_rate[y] = machine_rate1[y]
	elif part[y] == '50-0786':
		machine_rate[y] = machine_rate2[y]
	else:
		machine_rate[y] = 0
	
	try:
		m, s = divmod(diff[y],60)
		h, m = divmod(m, 60)
		diff_time[y]="%d:%02d:%02d" % (h,m,s)
	except:
		diff_time[y]= "0"
		
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	OEE [ y ] = Metric_OEE(t,u,down_time[y],count[y])
	
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
	
	yellow[0] = red[0]
	yellow[1] = red[1]
	yellow[2] = red[2]
	yellow[3] = red[3]	
	
	info[y] = "Part:&nbsp;&nbsp;"+str(part[y])+"<br>Production:&nbsp;&nbsp;"+ str(count[y]) +"<br>Projection:&nbsp;&nbsp;"+str(target[y])+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])


  request.session["track_start"] = t
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th
  

  
  list = zip(machine_list,info,red,yellow,green,mc2,mc3,gry,graph_link)
  
  if request.session["machine_chart"]=="nope":
	return render(request,"gf6input_fixed.html",{'list':list, 'S':temp})
  else:  
	return render(request,"gf6input_fixed.html",{'list':list,'GList':gr_list,'S':temp})
	

  
  
