def display_time(request):
  
  #  Working Time, uncomment when not testing
  t=int(time.time())
  
  start_date = request.session["s_date"]
  
  temp = datetime.strptime(start_date,"%Y-%m-%dT%H:%M")


  start_stamp = int(time.mktime(temp.timetuple()))
#  start_tuple = time.localtime(start_stamp)

  
  # Set time. 
  t = start_stamp

  rx=[0 for i in range(11)]
  gx=[0 for i in range(11)]
  
  rx[0], rx[1], rx[2], rx[3], rx[4], rx[5], rx[6], rx[7], rx[8], rx[9], rx[10] = "0%", "45%", "47%", "52%", "57%", "65%", "72%", "79%", "85%", "90%", "100%" 
  gx[0], gx[1], gx[2], gx[3], gx[4], gx[5], gx[6], gx[7], gx[8], gx[9], gx[10]= "0%", "15%", "18%", "23%", "30%", "40%", "43%", "47%", "50%", "60%", "100%"  
   
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
  brk3 =[0,0,0,0]
  brk4 =[0,0,0,0]
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
  for y in range(0, 4):
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
	
	machine_rate[y] = 75	
	[mup(x) for x in tmp if fup(x) == machine_list[y]]
	down_time[y] = sum(int(i) for i in dt)	
	
	# Test Section
	
	tu = t-u
	x = (t-u)-down_time[y]
	targget = x / machine_rate[y]
	OEE[y] = (count[y] / float(targget))*100
	#return render(request,"test4.html",{'A':down_time[y], 'B':count[y],'C':machine_rate[y],'D':tu,'E':machine_list[y],'F':target,'G':OEE})
	
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
	
	yellow[0] = red[0]
	yellow[1] = red[1]
	yellow[2] = red[2]
	yellow[3] = red[3]	
	t_part = str(part[y])[:7]
	info[y] = "Part:&nbsp;&nbsp;"+str(t_part)+"<br>Production:&nbsp;&nbsp;"+ str(count[y]) +"<br>Projection:&nbsp;&nbsp;"+str(targget)+"<br>OEE:&nbsp;&nbsp;"+str(OEE[y])


  request.session["track_start"] = t
  tg = " green 30%"
  th = " yellow 31%"
  request.session["test_grad"] = tg
  request.session["test_hrad"] = th
  
  list = zip(machine_list,info,red,yellow,green,mc2,mc3,gry,graph_link,brk3,brk4)
  if request.session["machine_chart"]=="nope":
	  return render(request,"gf6input_fixed.html",{'list':list, 'S':temp})
  else:
	  return render(request,"gf6input_fixed.html",{'list':list,'GList':gr_list,'S':temp,'BrkA':brk1,'BrkB':brk2})	  

	  
  
	
  
	

  
  
