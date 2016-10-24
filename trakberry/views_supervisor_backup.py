from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import sup_downForm
import MySQLdb
import time
from time import mktime
import datetime

from django.core.context_processors import csrf


def supervisor_display(request):
	try:
		request.session["login_supervisor"] 
		
	except:
		request.session["login_supervisor"] = "none"
  

  # initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
	c = []
	date = []
	prob = []
	job = []
	priority = []
	id = []
	machine = []
	count = []
	tmp2=[]
	smp2=[]
	mach_cnt = []
	whos = []
	box_colour = []
   
  # Select prodrptdb db 
	db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
	cursor = db.cursor()

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	
	c = ["tech","Jim Barker"]

	
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	SQ_Sup = "SELECT * FROM pr_downtime1 where closed IS NULL" 

	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	
	ctr = 0
	for x in tmp:
	
		
		clr = "blue"
		if ctr > 3:
			clr = "red"
		tmp2 = (tmp[ctr])
		# assign job date and time to dt
		dt = tmp2[2]
		dt_t = time.mktime(dt.timetuple())
		# assign current date and time to dtemp
		dtemp = datetime.datetime.now()
		dtemp_t = time.mktime(dtemp.timetuple())
		# assign d_diff to difference in unix
		d_diff = dtemp_t - dt_t
		
		if d_diff < 1801:
			clr = "white"
		elif d_diff < 3601:
			clr = "#F5DF9F"
		elif d_diff < 10801:
			clr = "#F2AABF"
		elif d_diff < 86400:
			clr = "#DA67E0"
		else:
			clr = "#F54545"
			
		temp1_job = tmp2[0]
		temp2_job = temp1_job[:15]
		job.append(temp2_job)
		prob.append(tmp2[1])
		
		priority.append(tmp2[3])
		id.append(tmp2[11])
		whos.append(tmp2[4])
		box_colour.append(clr)
		ctr = ctr + 1
		
	for i in range(0, ctr-1):
		for ii in range(i+1, ctr):
			if (priority[ii]) < (priority[i]):
				jjob = job[i]
				job[i] = job[ii]
				job[ii] = jjob
				pprob = prob[i]
				prob[i] = prob[ii]
				prob[ii] = pprob
				pprior = priority[i]
				priority[i] = priority[ii]
				priority[ii] = pprior
				iid = id[i]
				id[i] = id[ii]
				id[ii]= iid
				wwhos = whos[i]
				whos[i] = whos[ii]
				whos[ii] = wwhos
				bbox_colour = box_colour[i]
				box_colour[i] = box_colour[ii]
				box_colour[ii] = bbox_colour
	
	list = zip(job,prob,id,whos,priority,box_colour)
	
	db.close()
	n = "none"
  # call up 'display.html' template and transfer appropriate variables.  
	return render(request,"supervisor.html",{'L':list,'N':n})

def supervisor_tech_call(request):
	request.session["whoisonit"] = 'tech'
	return supervisor_down(request)

def supervisor_elec_call(request):
	request.session["whoisonit"] = 'maintenance'
	return supervisor_down(request)

def supervisor_main_call(request):
	request.session["whoisonit"] = 'maintenance'
	return supervisor_down(request)	
	
def supervisor_down(request):	

	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		whoisonit = request.session["whoisonit"]
		t = datetime.datetime.now()
		
		db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
		cur = db.cursor()
		cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime) VALUES(%s,%s,%s,%s,%s)''', (machinenum,problem,priority,whoisonit,t))
		db.commit()
		db.close()
		
		return supervisor_display(request)
		
	else:
		request.session["machinenum"] = "692"
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	#request.session["login_tech"] = "none"
	return render(request,'supervisor_down.html', args)	

# Module to edit entry	
def supervisor_edit(request,index):	
	db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
	cursor = db.cursor()
	SQ_Sup = "SELECT * FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(SQ_Sup)
	tmp = cursor.fetchall()
	tmp2=tmp[0]
	request.session["machinenum"] = tmp2[0]
	request.session["problem"] = tmp2[1]
	request.session["priority"] = tmp2[3]
	db.close()	
	
	if request.POST:
        			
		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		whoisonit = 'tech'
		
		db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
		cur = db.cursor()
		mql =( 'update pr_downtime1 SET machinenum="%s" WHERE idnumber="%s"' % (machinenum,index))
		cur.execute(mql)
		db.commit()
		tql =( 'update pr_downtime1 SET problem="%s" WHERE idnumber="%s"' % (problem,index))
		cur.execute(tql)
		db.commit()
		uql =( 'update pr_downtime1 SET priority="%s" WHERE idnumber="%s"' % (priority,index))
		cur.execute(uql)
		db.commit()
		db.close
		#db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
		#cur = db.cursor()
		#cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit) VALUES(%s,%s,%s,%s)''', (machinenum,problem,priority,whoisonit))
		#db.commit()
		#db.close()
		
		return supervisor_display(request)
		#return render(request, "test.html", {'machine':machinenum , 'index':index})
		
	else:	
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'supervisor_edit.html', args)		

	
	