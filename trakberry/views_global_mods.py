from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from time import strftime
from datetime import datetime
import MySQLdb
import time

from views_db import db_open

def machine_rates(part,machine):
	if machine == '748': 
		part = '50-0786'
	if machine == '750': 
		part = '50-0786'
	if machine == '749': 
		part = '50-3632'
	if machine == '677': 
		part = '50-3632'	
				
	rate = 0
	machine_list = ['677','748','749','750','614','615','629','620','686','574','756','755']
	part_number = ['50-3632','50-0786']
	# Machine Rates for 1:50-3632  2:50-0786
#	machine_rates = [67,73,76,59,67,73,76,59,72,74,72,74,72,74,72,74,65,66,79,76,65,66,79,76]
#	machine_rates = [54,49,54,49,49,45,55,50,45,45,45,45,45,45,45,45,51,45,51,45,51,45,51,45]
	machine_rates = [54,54,49,49,49,49,25,25,45,45,45,45,45,45,45,45,45,45,51,51,45,45,51,51]
	#machine_rates = [1,2,3,4,5,6,7,8]
	l = len(machine_list)
#	m = len(part_number)
	mc = 0
#	pn = 0
	ctr = 0
	for i in range(0,l):
		if machine == machine_list[i]:
			mc = ctr
			break
		ctr = ctr + 1	
	mc = (mc * 2)
	ctr = 0	
	if part == '50-0786':
			ctr = 1
	
	mc = mc + ctr
	
		
#	ctr = 0	
#	for ii in range(0,m):
#		if part == part_number[ii]:
#			pn = ctr
#		ctr = ctr + 1	
#	z = (mc + (pn * 4))
	rate =  machine_rates[mc]
	#rate = z
	return rate
	#return rate
	
# *******************************************************
# *  Determine Metrics OEE , Availability and Performance
# *******************************************************
def Metric_OEE(t,u,down_time,count,h_rate):

	# Calculate Planned Availability
	#PT = 28800 - down_time
	tu = t-u
	PT = (t-u) - down_time
	A = (PT / float((t-u)))
	A = 1

	# Calculate Performance
	try:
		P = count * (60/float(h_rate))*60
	except:
		P = 0	
	try:
		P = P / float(PT)
	except:
		P = 0
	# Calculate OEE
	OEE = (int((A * P)*1000))/float(10)
	
	# Test Calculations
	#target = (((t-u)*float(h_rate)*8)/float(28800))
	#OEE = (count/float(target))
	

	return OEE

	
def test_machine_rate(request):
	part = '50-0786'
	machine = '677'
	
	rate = machine_rates(part,machine)
	
	return render(request, "done.html", {'Rate':rate})	
