from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5,vacation_set_current6
from trakberry.views_vacation import vacation_1
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
import decimal
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open
from views_mod1 import kiosk_lastpart_find
from datetime import datetime
import json


def barcode_initial(request):
  db, cur = db_open()
  sql = "SELECT max(scrap) FROM barcode"
  cur.execute(sql)
  tmp2 = cur.fetchall()
  tmp3 = tmp2[0]
  max_stamp = tmp3[0]

  sql = "SELECT * from barcode where scrap = '%s'" %(tmp3[0])
  cur.execute(sql)
  tmp2 = cur.fetchall()
  request.session["barcode1"] = tmp2[0][2]
  skid = tmp2[0][3] 
  part = tmp2[0][4]
  request.session["barcode_skid"] = skid
  request.session["barcode_part"] = part 

  request.session["route_1"] = 'barcode_input'
  return direction(request)


def barcode_input(request):
    request.session["local_toggle"]="/trakberry"

    part = request.session["barcode_part"]
    db, cur = db_open()
    sql = "SELECT * FROM barcode"
    cur.execute(sql)
    tmp2 = cur.fetchall()


    if request.POST:
        bc1 = request.POST.get("barcode")
        request.session["barcode"] = bc1
        request.session["barcode_part_number"] = bc1[-4:]
        request.session["route_1"] = 'barcode_check'
        return direction(request)
    else:
		form = kiosk_dispForm1()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request,"kiosk/barcode_input.html",{'args':args})

def barcode_reset(request):
  b = 0
  a = '0'
  db, cur = db_open()

  sql = "SELECT max(scrap) FROM barcode"
  cur.execute(sql)
  tmp2 = cur.fetchall()
  tmp3 = tmp2[0]
  max_stamp = tmp3[0]
  max_stamp = max_stamp + 1


  cur.execute('''INSERT INTO barcode(asset_num,scrap,part) VALUES(%s,%s,%s)''', (a,max_stamp,b))
  db.commit()
  request.session["route_1"] = 'barcode_initial'
  return direction(request)


def barcode_check(request):
    bar1 = request.session["barcode"]
    bar1=str(bar1)
    stamp = time.time()
    db, cur = db_open()
 #   try:
    
    mql = "SELECT * FROM barcode WHERE asset_num = '%s'" %(bar1)
    cur.execute(mql)
    tmp2 = cur.fetchall()
    try:
     tmp3=tmp2[0]
     tmp4=tmp3[0]
     timestamp = tmp3[2]
     d = vacation_1(timestamp)
     request.session["alert_time"] = d
     return render(request,"barcode_alert.html")

    except:
      dummy = 1

    part = request.session["barcode_part"]
    part = part + 1
    cur.execute('''INSERT INTO barcode(asset_num,scrap,part) VALUES(%s,%s,%s)''', (bar1,stamp,part))
    db.commit()
    
    request.session["bar1"] = bar1
    
    request.session["barcode_part"] = part

    db.close()

    part_num = request.session["barcode_part_number"]

    if part_num == "5401" and part == 144:
      return render(request,"barcode_complete.html")
    if part_num == "5399" and part == 40:
      return render(request,"barcode_complete.html")
    if part_num == "5404" and part == 120:
      return render(request,"barcode_complete.html")


    return render(request,"barcode_ok.html")
    
    request.session["route_1"] = 'barcode_input'
    return direction(request)