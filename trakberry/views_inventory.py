from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import inventory_entry_Form
from views_db import db_open
from views_mod1 import find_current_date
from views_email import e_test
from views_supervisor import supervisor_tech_call
import MySQLdb
import time
import datetime
from django.core.context_processors import csrf
import smtplib
from smtplib import SMTP
from django.template.loader import render_to_string  #To render html content to string
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2

def push_button(request):

	return render(request, "push_button.html")
	
	
def inventory_type_entry(request):	

	if request.POST:
        			
		part = request.POST.get("inventory_part")
		storage = request.POST.get("inventory_storage")
		qty = request.POST.get("inventory_qty")
		
		request.session['inventory_part'] = part
		request.session['inventory_storage'] = storage
		request.session['inventory_qty'] = qty


		db, cur = db_open()
		
		try:
			sql2 = "SELECT * from tkb_inventory_fixed WHERE Part = '%s' and Storage = '%s'" % (part, storage)
			cur.execute(sql2)
			tmp = cur.fetchall()
			tmp2 = tmp[0]

			return render(request,'done_inventory_fixed.html')
		except:
			cur.execute('''INSERT INTO tkb_inventory_fixed(Part,Storage,Quantity) VALUES(%s,%s,%s)''', (part,storage,qty))
			db.commit()
			return render(request,'done_inventory_fixed.html')
			
		#cur.execute('''INSERT INTO tkb_audits(Type,Part,Op,Department,Description) VALUES(%s,%s,%s,%s,%s)''', (dept,part,op,pl,desc))
		#db.commit()
		db.close()
		
		return render(request,'temp_inventory.html')
		
	else:
		form = inventory_entry_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'entry_fixed.html', {'args':args})