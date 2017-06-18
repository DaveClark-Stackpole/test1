from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
#from views2 import main_A
from trakberry.forms import login_Form,layered_entry_Form
from datetime import datetime
import MySQLdb
import time
from django.core.context_processors import csrf
import smtplib
import datetime as dt
from smtplib import SMTP
from django.template.loader import render_to_string  #To render html content to string

	
def email_test_2 (request):

	message_text = ' Hello There'
	message_subject = 'TestEmail'
	
	
	x = 7
	label_name = "layered_"
	
	# Assign space to all request.session.layered_# 
	for i in range (1,10):
		label_str = label_name + str(i)
		request.session[label_str]='nbsp'
	
	# ASCII Code 9899 for Dot assigned to request.session.layered_x
	label_str = label_name + str(x)	
	request.session[label_str]='#9899'


	html_content = render_to_string('layered_audits/LA_0786.html')
	
	toaddrs = 'dclark@stackpole.com'
	fromaddr = 'stackpole@stackpole.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('dave7995@gmail.com', 'benny6868')
	message = "From: %s\r\n" % frname + "To: %s\r\n" % toaddrs + "Subject: %s\r\n" % message_subject + "\r\n" + html_content
	

	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	return render(request, "done_test.html")



#from django.core.mail import EmailMultiAlternatives
#from django.template.loader import render_to_string
#from django.utils.html import strip_tags

#subject, from_email, to = 'Hi', 'from@x.com', 'to@x.com'

#html_content = render_to_string('the_template.html', {'varname':'value'}) # ...
#text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

# create the email, and attach the HTML version as well.
#msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#msg.attach_alternative(html_content, "text/html")
#msg.send()

    
def email_test_1(request):
#	sender = 'dclark@stackpole.com'
#	receivers = ['dclark@stackpole.com']

#	message = """From: From Person <from@fromdomain.com>
#	To: To Person <to@todomain.com>
#	Subject: SMTP e-mail test
#
#	This is a test e-mail message.
#	"""
#
#	try:
#		smtpObj = smtplib.SMTP('localhost')
#		smtpObj.sendmail(sender, receivers, message)         
#		l = "Successfully sent email"
#	except:
#		l =  "Error: unable to send email"
	
	return render(request, "email_downtime_test.html")
 
def place_test(request):
	for key in request.session.keys():
		del request.session[key]
	E = 'DONE'
#	i = ''
#	E=[0 for i in range(5)] 
#	E[1] = ['X','Y','Z']
#	E[2] = ['W','Z']
#	E[3] = ['W','X']
#	E[4] = ['Y','X']
#	
	return render(request, "test_a.html", {'List':E})
	 
def vacation_set_current():
	t = vacation_temp()
	month_st = t.month
	year_st = t.year
	one = 1
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	
	current_shift = 'All'
	
	return current_first, current_shift

def test_list(request):
	list2 = request.session['list_test']
	qq = request.session['qq']
	r3 = request.session['r3']
	
	return render(request,'display_schedule.html',{'list':list2,'qq':qq,'T':r3})
	
	 
def sendAppointment(self, subj, description):
  # Timezone to use for our dates - change as needed
  tz = pytz.timezone("Europe/London")
  reminderHours = 1
  startHour = 7
  start = tz.localize(dt.datetime.combine(self.date, dt.time(startHour, 0, 0)))
  cal = icalendar.Calendar()
  cal.add('prodid', '-//My calendar application//example.com//')
  cal.add('version', '2.0')
  cal.add('method', "REQUEST")
  event = icalendar.Event()
  event.add('attendee', self.getEmail())
  event.add('organizer', "me@example.com")
  event.add('status', "confirmed")
  event.add('category', "Event")
  event.add('summary', subj)
  event.add('description', description)
  event.add('location', "Room 101")
  event.add('dtstart', start)
  event.add('dtend', tz.localize(dt.datetime.combine(self.date, dt.time(startHour + 1, 0, 0))))
  event.add('dtstamp', tz.localize(dt.datetime.combine(self.date, dt.time(6, 0, 0))))
  event['uid'] = getUniqueId() # Generate some unique ID
  event.add('priority', 5)
  event.add('sequence', 1)
  event.add('created', tz.localize(dt.datetime.now()))
 
  alarm = icalendar.Alarm()
  alarm.add("action", "DISPLAY")
  alarm.add('description', "Reminder")
  #alarm.add("trigger", dt.timedelta(hours=-reminderHours))
  # The only way to convince Outlook to do it correctly
  alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(reminderHours))
  event.add_component(alarm)
  cal.add_component(event)
 
  msg = MIMEMultipart("alternative")
 
  msg["Subject"] = subj
  msg["From"] = "{0}@example.com".format(self.creator)
  msg["To"] = self.getEmail()
  msg["Content-class"] = "urn:content-classes:calendarmessage"
 
  msg.attach(email.MIMEText.MIMEText(description))
 
  filename = "invite.ics"
  part = email.MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
  part.set_payload( cal.to_ical() )
  email.Encoders.encode_base64(part)
  part.add_header('Content-Description', filename)
  part.add_header("Content-class", "urn:content-classes:calendarmessage")
  part.add_header("Filename", filename)
  part.add_header("Path", filename)
  msg.attach(part)
 
  s = smtplib.SMTP('localhost')
  s.sendmail(msg["dclark@stackpole.com"], [msg["dclark@stackpole.com"]], msg.as_string())
  s.quit()

def toggle_1(request):

	return render(request, "toggle_1.html")

def layer_test(request):
	x = 8
	label_name = "layered_"
	
	# Assign space to all request.session.layered_# 
	for i in range (1,10):
		label_str = label_name + str(i)
		request.session[label_str]='nbsp'
	
	# ASCII Code 9899 for Dot assigned to request.session.layered_x
	label_str = label_name + str(x)	
	request.session[label_str]="#9899"

	return render(request, "layered_audits/50-2407.htm")

def layer_transfer_temp(request):

	# backup layered audit temp Table
	db, cursor = db_open()  
	type_use = request.session["layer_type_use"]
	
	dql = ('DELETE FROM tkb_audits_temp WHERE Type="%s"' % (type_use))
	cursor.execute(dql)
	db.commit()
	
	
	#cursor.execute("""DROP TABLE IF EXISTS tkb_audits_temp""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_audits_temp LIKE tkb_audits""")
	#cursor.execute('''INSERT tkb_audits_temp Select * From tkb_audits''')

	
	sql = "INSERT tkb_audits_temp Select * From tkb_audits where Type='%s'" % (type_use)
	cursor.execute(sql)


	db.commit()
	db.close()
	return render(request,'done.html')
	
def layer_entry(request):	

	if request.POST:
        			
		dept = request.POST.get("layered_type")
		part = request.POST.get("layered_part")
		op = request.POST.get("layered_op")
		pl = request.POST.get("layered_dep")
		desc = request.POST.get("layered_des")
		
		request.session['layered_type'] = dept
		request.session['layered_part'] = part
		request.session['layered_op'] = op
		request.session['layered_dep'] = pl
		
		# Select prodrptdb db located in views_db
		db, cur = db_open()
		cur.execute('''INSERT INTO tkb_audits(Type,Part,Op,Department,Description) VALUES(%s,%s,%s,%s,%s)''', (dept,part,op,pl,desc))
		db.commit()
		db.close()
		
		return render(request,'done.html')
		
	else:
		form = layered_entry_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'layered_audits/entry.html', {'args':args})

	
def layer_choice_init(request):
	request.session['layer_choice'] = 0
	request.session['layer_audit_check'] = 0
	return layer_choice(request)
	
def layer_choice(request):

	# variable to determine if choosing for first time.
	layer_choice = int(request.session['layer_choice'])

	# Hard coding Supervisors in.   In future make it variable using DB table
	type_use = 'CNC'
	if request.session['login_name'] == 'Dave Clark' or request.session['login_name'] == 'Grant Packham' or request.session['login_name'] == 'Rick Wurm' or request.session['login_name'] == 'Tim Sanzosti':
		type_use = 'CNC'
	elif request.session['login_name'] == 'Karl Edwards' or request.session['login_name'] == 'Frank Ponte' or request.session['login_name'] == 'Scott McMahon':
		type_use = 'Production'
	# ***********************************************************************
	request.session["layer_type_use"] = type_use
	db, cur = db_open()
	
	if layer_choice == 0:
		sql1 = "SELECT MIN(Id) FROM tkb_audits_temp WHERE Type = '%s'" % (type_use) 
		cur.execute(sql1)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		id_use = tmp2[0]
		request.session['layer_id_start'] = id_use
		request.session['layer_choice'] = 1
	
	else:

		id_start = int(request.session['layer_id_start'])
		sql1 = "SELECT MIN(Id) FROM tkb_audits_temp WHERE Id > '%s' and Type = '%s'" % (id_start,type_use)
		cur.execute(sql1)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		id_use = tmp2[0]
		request.session['layer_id_start'] = id_use

	

	try:
		sql2 = "SELECT * from tkb_audits_temp WHERE Id = '%s'" % (id_use)
		cur.execute(sql2)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
	except:
		return layer_choice_init(request)
	
	db.close()
	request.session['layered_audit_id'] = id_use
	
	return render(request,'layered_audits/audit_current.html', {'tmp2':tmp2})

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# This mod will choose the current layered audit and email link to the current supervisor
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def layer_select(request):
	# Current supervisor will be request.session.login_name
	# Audit to use will be request.session.layered_audit_id
	
	name = request.session['login_name']
	audit = request.session['layered_audit_id']
	
	# retrieve left first character of login_name only
	name_temp1 = name[:1]
	# retrieve last name of login name only 
	name_temp2 = name.split(" ",1)[1]
	
	# set request.session.email_name as the full email address for link
	email_name = name_temp1 + name_temp2 + '@stackpole.com'
	request.session['email_name'] = email_name
	
	# write selected layered audit info to table tkb_layered
	
	tm = int(time.time())
	db, cur = db_open()
	sql_1 = "Select * from tkb_audits_temp WHERE Id = '%s'" % (audit)
	cur.execute(sql_1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[2]
	
	cur.execute ('''INSERT INTO tkb_layered(Part,Op,Name,Description,Time_Stamp) VALUES(%s,%s,%s,%s,%s)''',(tmp2[2],tmp2[3],name,tmp2[5],tm))
	db.commit()
	
	# Delete the used Audit from the Temp list
	dql = ('DELETE FROM tkb_audits_temp WHERE Id="%s"' % (audit))
	cur.execute(dql)
	db.commit()

	db.close()
	
	request.session['layer_audit_check'] = 1
	
	
	# In link string must use  %20 to signify a space to be recognized in Microsoft Outlook
	if  tmp3 == '50-2407' or tmp3 == '50-2421' or tmp3 == '50-4916':
		# Use below link format if it's the original one otherwise use our test folder
		#label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\50-3627M%20&%2050-1713M%20LPA_Apr%2025%202017_New%20Format.xls'''
		label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\test\\50-2407_'''
		label_link = label_link + tmp2[3] + '''.xls'''
	if tmp3 == '50-3627' or tmp3 == '50-1713':
		label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\test\\50-3627_'''
		label_link = label_link + tmp2[3] + '''.xls'''
	if tmp3 == '50-3632' or tmp3 == '50-0786' or tmp3 == '50-1731':
		label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\test\\50-3632_'''
		label_link = label_link + tmp2[3] + '''.xls'''
	if tmp3 == '50-4900' or tmp3 == '50-6686' or tmp3 == '50-6729':
		label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\test\\50-4900_'''
		label_link = label_link + tmp2[3] + '''.xls'''
	if tmp3 == '50-4748':
		label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\test\\50-4748_'''
		label_link = label_link + tmp2[3] + '''.xls'''
	if tmp3 == '50-1448':
		label_link = '''\\\csd-server\Strat%20Common\Quality\Info\Layered%20Audit%20Forms\CSDII\\test\\50-1448_'''
		label_link = label_link + tmp2[3] + '''.xls'''		
		
	extra_line = "Lets see if this line works with a couple of spaces"	
	subject_line_1 = "Layered Audit"
	subject_line_2 = "Click link below for your daily layered audit sheet."
		
	# The link that gets emailed
	email_link = 'http://pmdsdata.stackpole.ca:8986/trakberry/layer_retrieve/get/'+str(tm)
	
	message_subject = 'Daily Layered Audit'
	


	
	toaddrs = email_name
	fromaddr = 'stackpole@stackpole.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('StackpolePMDS@gmail.com', 'stacktest6060')
	message = "From: %s\r\n" % frname + "To: %s\r\n" % toaddrs + "Subject: %s\r\n" % message_subject + "\r\n" + subject_line_1 + "\r\n\r\n" + subject_line_2 + "\r\n\r\n"+ label_link
	

	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	
	
	return render(request,'main_redirect.html')
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def layer_audit_check_reset(request):
	request.session['layer_audit_check'] = 0
	return render(request,'main_redirect.html')
	
	
# This Mod will activate when Layered Audit link is clicked
# It will update tkb_layered table so it's notified that it was clicked then 
# it will open a webpage with the data ready to print for the daily layered audit	
def layer_retrieve(request,index):

	# Retrieve the information for the layered audit required as per the link clicked
	request.session['layer_test'] = index
	db, cur = db_open()
	sql = "Select * from tkb_layered WHERE Time_Stamp = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	tmp3 = tmp2[1] # part number
	name = tmp2[4] # Auditor Name
	chk = tmp2[2]  # Check number


	x = chk
	label_name = "layered_"
	
	if tmp3 == '50-2407' or tmp3 == '50-2421' or tmp3 == '50-4916':
		label_link = "file:///\\csd-server\Strat Common\Quality\Info\Layered Audit Forms\CSDII\50-2407 & 50-2421 & 50-4916 LPA_Apr 25 2017_New Format.xls"
	if tmp3 == '50-3627' or tmp3 == '50-1713':
		label_link = "\\csd-server\Strat Common\Quality\Info\Layered Audit Forms\CSDII\50-3627M & 50-1713M LPA_Apr 25 2017_New Format.xls"
	if tmp3 == '50-3632' or tmp3 == '50-0786' or tmp3 == '50-1731':
		label_link = "\\csd-server\Strat Common\Quality\Info\Layered Audit Forms\CSDII\50-3632M & 50-0786M & 50-1731M LPA_Apr 25 2017_New Format.xls"
	if tmp3 == '50-4900' or tmp3 == '50-6686' or tmp3 == '50-6729':
		label_link = "\\csd-server\Strat Common\Quality\Info\Layered Audit Forms\CSDII\50-4900 & 50-6686 & 50-6729 LPA_Apr 25 2017_New Format.xls"
	#label_link = "\\csd-server\Strat Common\Quality\Info\Layered Audit Forms\CSDII\50-4748 LPA_Apr 25 2017_New Format.xls"	
	#label_link = "\\csd-server\Strat Common\Quality\Info\Layered Audit Forms\CSDII\50-1448 & 50-9641 LPA_Apr 28 2017_New Format.xls"	
	
	request.session['label_link'] = label_link
	
	# Assign space to all request.session.layered_# 
	#for i in range (1,10):
	#	label_str = label_name + str(i)
	#	request.session[label_str]='nbsp'
	
	# ASCII Code 9899 for Dot assigned to request.session.layered_x
	#label_str = label_name + str(chk)	
	#request.session[label_str]='#9899'
	#request.session[label_name] = name

	#template = "layered_audits/"+tmp3 +".htm"
	
	#return render(request,'layered_audits/test.html')
	return render(request,'reroute.html')
