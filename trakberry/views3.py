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
#import pandas

def excel_test(request):
	
	# if needed this assigns mlist to the current path
#	mlist = os.getcwd()
	
	# Change to directory where imported inventory.xlsm is located
#		Use this for local testing
	label_link = '/home/trackberry/file/import1/Inventory/importedxls/'
#		Use this one for actual server
#	label_link = '/home/file/import1/Inventory/importedxls'
	
	sheet = 'INVENTORY SYSTEM.xlsm'
	sheet_name = 'PROSUM REPORT'
	os.chdir(label_link)
	
	book = xlrd.open_workbook(sheet)
	
	#working = book.sheet_by_index(1)
	working = book.sheet_by_name(sheet_name)
	
	a = working.cell(7,7).value
	b = working.cell(7,0).value
	#mlist = book.sheet_names()
	#mlist.encode('ascii','ignore')
	
	#mlist = xl_workbook.nsheets
	
	#unicodedata.normalize('NFKD', mlist).encode('ascii','ignore')
	#mlist = os.listdir('.')
	

	#mlist = 'Done'
	
	
	
#	tx = ' ' + tx
#	if (tx.find('"'))>0:
#		#request.session["test_comment"] = tx
#		#return out(request)
#		ty = list(tx)
#		ta = tx.find('"')
#		tb = tx.rfind('"')
#		ty[ta] = "'"
#		ty[tb] = "'"
#		tc = "".join(ty)
			
	#mlist = mlist + 4


	
	
	return render(request,"test5.html",{'a':a,'b':b})
 

