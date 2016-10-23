from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from smtplib import SMTP

import MySQLdb

# Methods for opening database for all and returning db and cur
def db_open():
#	Change host , username , password and db to suit 
	#db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
	db = MySQLdb.connect(host="127.0.0.1",user="dg417",passwd="dg",db='prodrptdb')
	# Uncomment below line to switch to new server PMDS3 and comment above line out
	#db = MySQLdb.connect(host="10.4.1.224",user="dg417",passwd="dg",db='prodrptdb')
	
	cursor = db.cursor()
	return db, cursor
	
def select_test(request):
	table = 'tkb_jobs'
	col1 = 'Description'
	var1 = 'GF6 Input'
	blank = ''
	tmp2 = db_select(table,col1,var1,blank,blank,blank,blank)
	total = tmp2[0]
	return render(request,"test3.html",{'total':total})
	
		
def db_select(table,col1,var1,col2,var2,col3,var3):
	db, cursor = db_open()

#	if col1=='':
	sqlcommand = 'SELECT * FROM '+ table
#	elif col2=='':
#		sqlcommand = '''SELECT * FROM " + table + " where " + col1 + "== '%d'''%(var1)"
#		sqlcommand = "SELECT * FROM tkb_jobs where Description == '%d'" %(var1)

	
	cursor.execute(sqlcommand)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	db.close()
	
	return tmp2
