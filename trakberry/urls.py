
"""trakberry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""


from django.conf.urls import include, url
from django.contrib import admin


from views2 import main_login, main_login_form, main, main_logout
from views_machinery import machinery
from views_testing import test_display, form_robot_machine_enter, display_robot_machine, machine_list_display, toggletest, test668,create_table_1
from views_tech import tech, job_call, job_close, tech_logout, job_pass, tech_history, tech_recent, tech_map, tech_tech_call, reset_call_route,tech_email_test
#from views_tech import hour_check
from views_transfer import transfer

from mod_simulate import sim
from mod_tracking import edit_part, select_date, select_day, select_datetime, graph_gf6, graph_gf6_report
from mod_test import test_mode
from views_global_mods import test_machine_rate
from views_vacation import vacation_temp, vacation_backup
from views_admin import retrieve
from views_db import db_select
from views_test import place_test, email_test_1
from views_mod1 import table_copy

# *******************************************  Testing Views *******************************************************************************************
from views_email import e_test
from views import fix_time
# ***********************************************************************************************************************************************************


# *******************************************  Main Views *******************************************************************************************
from views import display, db_write, create_table, test, details_session, details_track, reports, test_time, scheduler, inventory, display2, fade_in, fade2
from views import create_test_table, alter_table_name, done, new, graph, graph2, graph3, graph749, graph748, graph750, graph677, ttip,graph_close, display_time, graph_close_snap
from views import graph677_snap, graph748_snap, graph749_snap, graph750_snap, display_initialize, test44, tech_reset
# ***********************************************************************************************************************************************************


# *******************************************  Supervisor Section ********************************************************************************************
from views_supervisor import supervisor_display, supervisor_tech_call,supervisor_elec_call,supervisor_main_call
from views_supervisor import vacation_display_jump, supervisor_edit, sup_close, employee_vac_enter, vacation_display
from views_supervisor import vacation_display_increment, vacation_display_decrement, vacation_edit, vacation_delete
from views_supervisor import employee_vac_enter_init, employee_vac_enter_init2, vacation_month_fix, vacation_display_initial, resetcheck
# ***********************************************************************************************************************************************************


# *******************************************  Employee Section ********************************************************************************************
from views_employee import create_matrix, emp_training_enter, emp_info_enter, emp_info_display, emp_matrix_initialize, create_jobs,emp_info_update_status
from views_employee import job_info_display, job_info_enter,matrix_info_init, matrix_update, fix_shift,matrix_info_display,matrix_info_reload
from views_employee import job_info_update_status, job_info_delete, matrix_job_test, emp_matrix_delete, emp_matrix_rotation_fix
from views_scheduler import current_schedule, set_rotation, rotation_info_display, rotation_update, schedule_set, schedule_set2, schedule_init,schedule_finalize
from views_scheduler import schedule_set2b, schedule_add_job,schedule_set3



# ***********************************************************************************************************************************************************

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    # May 26,2015
    # Path for Test of single direct live tracking and then 
    # link to display.html template
	url(r'^$',main),

    
	url(r'^display/', main), 
	url(r'^main_login/', main_login),
	url(r'^main_login_form/', main_login_form),
	url(r'^display1/', display),
	url(r'^display_initialize/', display_initialize),
	url(r'^display2/', display2),
	url(r'^test6/', test_display),
	url(r'^test668/', test668),
	url(r'^create/', test),
	url(r'^new/', new),
	url(r'^display_time/', display_time),
	
	url(r'^tmr/', test_machine_rate),
	url(r'^fix_shift/', fix_shift),
	
	
	url(r'^fade/', fade_in),
	url(r'^fade2/', fade2),
	url(r'^ttip/', ttip),
	
	
	url(r'^graph_gf6op/get/(?P<index>\d+)/$', graph_gf6),
	url(r'^graph_gf6_report/get/(?P<index>\d+)/$', graph_gf6_report),
	url(r'^graph/', graph),
	url(r'^graph2/', graph2),
	url(r'^graph3/', graph3),
    url(r'^db_write/', db_write),  
	url(r'^sim/', sim),	
	url(r'^test/', test),	
	url(r'^done/', done),
	url(r'^details_session/', details_session),
	url(r'^details_track/', details_track),
	url(r'^main/', main),
	url(r'^tech_reset/', tech_reset),
	url(r'^tech_email_test/', tech_email_test),
	url(r'^main_logout/', main_logout),	
	
	# Reports URL Patterns ***********************************
	url(r'^reports/', select_date),
	url(r'^reports_day/', select_day),
	url(r'^reports_snapshot/', select_datetime),
	# ********************************************************
	
	# Reports URL Patterns for Vacations ***********************************
	url(r'^employee_vacation_enter/', employee_vac_enter),
	url(r'^employee_vacation_enter_init2/', employee_vac_enter_init2),
	url(r'^employee_vacation_enter_init/get/(?P<index>\d+)/$', employee_vac_enter_init),
	url(r'^emp_matrix_rotation_fix/', emp_matrix_rotation_fix),
	url(r'^vacation_display/', vacation_display),
	url(r'^vacation_display_jump/', vacation_display_jump),
	url(r'^vacation_display_increment/', vacation_display_increment),
	url(r'^vacation_display_decrement/', vacation_display_decrement),
	url(r'^vacation_edit/get/(?P<index>\d+)/$', vacation_edit),
	url(r'^vacation_delete/', vacation_delete),
	url(r'^vacation_display_initial/', vacation_display_initial),
	url(r'^vacation_backup/', vacation_backup),
	url(r'^vacation_month_fix/', vacation_month_fix),
	url(r'^resetcheck/', resetcheck),
	# ********************************************************	
	
	url(r'^machinery/', machinery),
	url(r'^test_time/', test_time),
	url(r'^scheduler/', scheduler),
	url(r'^inventory/', inventory),
	url(r'^testdb/', create_test_table),
	url(r'^edit/', edit_part),
	url(r'^create_table_1/', create_table_1),
	url(r'^test44/', test44),
	url(r'^graph_gf6/get/(?P<index>\d+)/$', graph_gf6),
	url(r'^graph749/', graph749),
	url(r'^graph748/', graph748),
	url(r'^graph750/', graph750),
	url(r'^graph677_snap/', graph677_snap),
	url(r'^graph748_snap/', graph748_snap),
	url(r'^graph749_snap/', graph749_snap),
	url(r'^graph750_snap/', graph750_snap),
	url(r'^graph677/', graph677),
	url(r'^graph_close/', graph_close),
	url(r'^graph_close_snap/', graph_close_snap),
	url(r'^test_var/', test_mode),
	url(r'^tech/', tech),
	url(r'^sup/', supervisor_display),
	url(r'^sup_down_tech/', supervisor_tech_call),
	url(r'^sup_close/', sup_close), 
	url(r'^transfer/', transfer),
	url(r'^reset_call_route/', reset_call_route),
	url(r'^sup_down_elec/', supervisor_elec_call),
	url(r'^sup_down_main/', supervisor_main_call),
	#url(r'^sedit/get/(?P<index>\d+)/$', supervisor_edit),
	url(r'^sedit/', supervisor_edit),
	url(r'^alter/', alter_table_name),
	url(r'^tech_logout/', tech_logout),
	url(r'^jcall/get/(?P<index>\d+)/$', job_call),
	url(r'^jclose/get/(?P<index>\d+)/$', job_close),
	url(r'^jpass/get/(?P<index>\d+)/$', job_pass),
	url(r'^tech_history/', tech_history),	
	url(r'^tech_recent/', tech_recent),
	url(r'^tech_tech_call/', tech_tech_call),
    url(r'^tech_map/', tech_map),	
	
	# **************  Employee Section ***************************************
	url(r'^create_matrix/', create_matrix),
	url(r'^create_jobs/', create_jobs),
	url(r'^emp_training_enter/', emp_training_enter),
	url(r'^emp_info_enter/', emp_info_enter),
	url(r'^emp_info_display/', emp_info_display),
	url(r'^emp_matrix_delete/', emp_matrix_delete),
	url(r'^emp_matrix_initialize/', emp_matrix_initialize),
	url(r'^emp_matrix_rotation_fix/', emp_matrix_rotation_fix),
	url(r'^job_info_delete/', job_info_delete),
	url(r'^job_info_display/', job_info_display),
	url(r'^job_info_enter/', job_info_enter),
	url(r'^job_info_update_status/get/(?P<index>\w{0,50})/$', job_info_update_status),
	url(r'^matrix_info_init/', matrix_info_init),
	url(r'^matrix_info_display/', matrix_info_display),
	url(r'^matrix_info_reload/', matrix_info_reload),
	url(r'^training_matrix/get/(?P<index>\d+)/$', matrix_update),
	url(r'^emp_info_delete/get/(?P<index>\w{0,50})/$', emp_info_update_status),
	url(r'^matrix_job_test/', matrix_job_test),
	url(r'^current_schedule/', current_schedule),
	url(r'^set_rotation/', set_rotation),
	url(r'^rotation_info_display/', rotation_info_display),
	url(r'^rotation_matrix/get/(?P<index>\d+)/$', rotation_update),
	                # *******  Scheduling Section   **********
	url(r'^schedule_set/', schedule_set),
	url(r'^schedule_finalize/', schedule_finalize),
	url(r'^schedule_set2b/', schedule_set2b),
	url(r'^schedule_add_job/get/(?P<index>\w{0,50})/$', schedule_add_job),
	
	#url(r'^tech/get/complete/(?P<index>\d+)/$', complete),
	
	
	# ************************************************************************
	
	# **************  Testing Section ***************************************
	
	url(r'^email_test_1/', email_test_1),
	url(r'^form_robot_machine_enter/', form_robot_machine_enter),
	url(r'^display_robot_machine/', display_robot_machine),
	url(r'^machine_list_display/', machine_list_display),
	url(r'^e_test/', e_test),
	url(r'^db_select/', db_select),
	url(r'^place_test/', place_test),
	url(r'^schedule_init/', schedule_init),
	url(r'^schedule_set2/', schedule_set2),
	url(r'^schedule_set3/', schedule_set3),
	url(r'^table_copy/', table_copy),
	# Test for correcting timestamp issues on tracking data
	url(r'^fix_time/', fix_time),
#	url(r'^hour_check/', hour_check),

	
	# ************************************************************************
	# Retrieve Data from ADMIN views for testing
	url(r'^retrieve/', retrieve),
	url(r'^create_table/', create_table),
	
]
 

