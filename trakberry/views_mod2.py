from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open
from views_routes import direction
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
import MySQLdb
import time
from django.core.context_processors import csrf
import datetime as dt 
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current6, vacation_set_current5

def hrly_display(request):   # This will return a tuple with hourly prod summary on last hour for each p_cell
    hourly = ['' for x in range(0)]
    ert = ['' for x in range(0)]
    xx = ['' for x in range(0)]
    hourly_all = ['' for x in range(0)]
    red_block = '#ff0000'
    green_block = '#62c12e'
    yellow_block = '#faff2b'
    hhh = 3

    db, cur = db_open()  
    s1 = "SELECT p_cell FROM sc_prod_hr_target"  # Set the p_cell value we'll use to iterate through for each cell
    cur.execute(s1)
    tmp = cur.fetchall()
    p_cell = tmp[0]
    row_ctr = 1
    for i in tmp:
        c1 = 0
        c2 = 0
        pc = i[0]
        try:
                aql = "SELECT MAX(id) FROM sc_prod_hour where p_cell = '%s'" %(pc) # Set the max_id to get p_cell latest entry
                cur.execute(aql)
                tmp3 = cur.fetchall()
                tmp4 = tmp3[0]
                max_id = tmp4[0]
        except:
                route = 'Filed'
        try:
                bql = "Select * From sc_prod_hour where id = '%s'" %(max_id) # Get latest entry for p_cell
                cur.execute(bql)
                tmp3 = cur.fetchall()
                tmp4 = tmp3[0]
                ert.append(tmp4)
                c1 = int((float(tmp4[8])/float(tmp4[7]))*100)  # Calculate the % for Hourly
                c2 = int((float(tmp4[10])/float(tmp4[9]))*100) # Calculate the % for Shift Total
                if c1 > 84:        # Below determins d1 and d2 to signify colour  red, yellow, green
                        d1 = green_block
                elif c1 > 69:
                        d1 = yellow_block
                else:
                        d1 = red_block
                if c2 > 84:
                        d2 = green_block
                elif c2 > 69:
                        d2 = yellow_block
                else:
                        d2 = red_block
                ctr = 0
                s1 = 1
                s2 = 2
                s3 = 0
                s4 = 4
                d11 = 99

                new_line = row_ctr % hhh 

                # new code
                lst = list(tmp4)
                d3 = d2 + ',' + d1
                lst.extend((c2,d2,c1,d1,d3,new_line))
                mst=tuple(lst)
                xx.append(mst)

                row_ctr = row_ctr + 1

        except:
                dummy = 1

    db.close()

    # This is where you return the value 'hourly' which has all the data needed in tuple form
    return render(request,'kiosk/kiosk_test4.html', {'tmpp':xx})	

