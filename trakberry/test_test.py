from django.shortcuts import render_to_response
#from math import trunc
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render

from django.http import HttpResponse
from views_db import db_open, db_set
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from smtplib import SMTP
import MySQLdb

#ADD THIS FOR ACKNOWLEDGEMENT


# Methods for opening database for all and returning db and cur
def db_open():
#	Change host , username , password and db to suit 
    db = MySQLdb.connect(host="localhost",user="weclouduser",passwd="benny6868",db='wecloud')
    cursor = db.cursor()
    return db, cursor
	
	
	
	
	# THEN 
def start(request):

  db, cursor = db_set(request)
  cursor.execute("""DROP TABLE IF EXISTS pr_downtime1""")
  cursor.execute("""CREATE TABLE IF NOT EXISTS pr_downtime1(Id INT PRIMARY KEY AUTO_INCREMENT,mid INT(10), machinenum CHAR(30), problem CHAR(30), priority CHAR(30), whoisonit CHAR(30), called4helptime DATETIME DEFAULT NULL)""")
  db.commit()
  db.close()
  return render(request,'done.html')	

def table_mod1(request):

  db, cursor = db_set(request)
  # cursor.execute("""DROP TABLE IF EXISTS tkb_test1""")
  # cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_test1(Id INT PRIMARY KEY AUTO_INCREMENT, First INT(10), Second CHAR(30) DEFAULT 'Unused', Date1 DATETIME DEFAULT NULL)""")
  # 
  # cursor.execute("Alter Table sc_production1 DROP Column low_production")  # Drop a Column
  # db.commit()
  # Below will test for a variable and if it doesn't exist then make the column with a value assigned
  x = 0
  # try:
  #   sql = "SELECT * FROM sc_production1 where low_production = '%d'" % (x)
  #   cursor.execute(sql)
  #   tmp = cursor.fetchall()
  # except:
  #   cursor.execute("Alter Table sc_production1 ADD low_production INT Default 0")
  #   db.commit()

  # try:
  #   sql = "SELECT * FROM sc_production1 where manual_sent = '%d'" % (x)
  #   cursor.execute(sql)
  #   tmp = cursor.fetchall()
  # except:
  #   cursor.execute("Alter Table sc_production1 ADD manual_sent INT Default 1")
  #   db.commit()


  cursor.execute("Alter Table sc_production1 DROP Column low_production")  # Drop a Column
  cursor.execute("Alter Table sc_production1 DROP Column manual_sent")  # Drop a Column
  db.commit()

  # # cursor.execute("Alter Table tkb_test1 ADD Third Char(30) DEFAULT NULL")  # Add a Column
  # cursor.execute("Alter Table tkb_test1 ADD Third Boolean Default 0")
  # db.commit()
  db.close()

  return render(request,'done_test.html')	