from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from views_routes import direction
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
import MySQLdb
import time
from django.core.context_processors import csrf
import datetime as dt 
from views_vacation import vacation_temp, vacation_set_current7, vacation_set_current6, vacation_set_current5

def hrly_display(request):   # This will return a tuple with hourly prod summary on last hour for each p_cell
    hourly = ['' for x in range(0)]
    hourly_var = ['' for x in range(0)]
    ert = ['' for x in range(0)]
    xx = ['' for x in range(0)]
    hourly_all = ['' for x in range(0)]
    request.session["local_toggle"] = "/trakberry"
    red_block = '#ff0000'
    green_block = '#62c12e'
    yellow_block = '#faff2b'
    grey_block = '#a5a4a4'
	
	# Set the toggle for Net/Local
 #   try:
	#    if request.session["local_switch"] == 1:
     #              request.session["local_toggle"] = ""
    #else:
#			request.session["local_toggle"] = "/trakberry"
#	except:
#		request.session["local_toggle"] = "/trakberry"
		

    hhh = 3

    current_first, shift1, shift2, shift3, hour_curr  = vacation_set_current7()

    db, cur = db_set(request)  
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
                hourly_var.append(str(tmp4[4]))
                if int(tmp4[6]) != (hour_curr-1):
                        d1 = grey_block 
                        c1 = '---'
                if (str(tmp4[4])) != str(current_first):
                        d2 = grey_block
                        d1 = grey_block
                        c1 = '---'
                        c2 = '---'
                elif (tmp4[5]) != shift1:
                        if (tmp4[5]) != shift2:
                                if (tmp4[5]) != shift3:
                                        d2 = grey_block
                                        d1 = grey_block
                                        c1 = '---'
                                        c2 = '---'

                new_line = row_ctr % hhh # uses Mod of hhh to determine how many on a line.   hhh is the number on a line

                #yyt = vacation_set_current6(tmp[4])

                # new code
                lst = list(tmp4)
                d3 = d2 + ' 60%,' + d1 + ' 40%' # combines the two colors together to d3 format 
                lst.extend((c2,d2,c1,d1,d3,new_line,tmp[4]))
                mst=tuple(lst)
                xx.append(mst)

#                yyt = vacation_set_current6(tmp[4])
#                xx.append(yyt)



                row_ctr = row_ctr + 1

        except:
                dummy = 1

    db.close()

    current_first, shift1, shift2, shift3, hour_curr  = vacation_set_current7()
    request.session["variableA"] = current_first
    request.session["variableB"] = shift1
    request.session["variableC"] = shift2
    request.session["variableD"] = hourly_var
    request.session["variableE"] = hour_curr

    # This is where you return the value 'hourly' which has all the data needed in tuple form
    return render(request,'production/hrly_display.html', {'tmpp':xx})	



