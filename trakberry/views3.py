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
import xlrd


def excel_test(request):
	
	# if needed this assigns mlist to the current path
#	mlist = os.getcwd()
	
	# Change to directory where imported inventory.xlsm is located
	label_link = '/home/file/import1/Inventory/importedxls'
	os.chdir(label_link)
	
	
	
	mlist = os.listdir('.')
	

	#mlist = 'Done'
	return render(request,"test5.html",{'list':mlist})
 

