from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
from trakberry.forms import login_Form
from datetime import datetime
import MySQLdb
import time

import smtplib
import datetime as dt



    
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
	x = 7
	label_name = "layered_"
	for i in range (1,10):
		label_str = label_name + str(i)
		request.session[label_str]='nbsp'
		
	label_str = label_name + str(x)	
		
	request.session[label_str]='#9899'

	return render(request, "layered_audits/50-2407.html")
