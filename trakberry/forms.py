from django import forms


#from django.forms import form_for_model



class entry(forms.Form):
	Mach = forms.CharField()
	
class part_number(forms.Form):
	PartNumber = forms.CharField()
	
class tech_closeForm(forms.Form):
	comment = forms.CharField()	

class tech_passForm(forms.Form):
	comment = forms.CharField()	
	whos = forms.CharField()	
	
class tech_loginForm(forms.Form):
	user = forms.CharField()
	pwd = forms.CharField()		
	
class tech_searchForm(forms.Form):
	machine = forms.CharField()		
	
class report_dateForm(forms.Form):
	start_date = forms.CharField()
	end_date = forms.CharField()

class report_employee_Form(forms.Form):
	date_st = forms.CharField()
	date_en = forms.CharField()	
	employee = forms.CharField()
	shift = forms.CharField()
	Id = forms.CharField()	

class emp_training_form(forms.Form):
	employee = forms.CharField()
	part = forms.CharField()	
	op = forms.CharField()
	machine = forms.CharField()
	level = forms.CharField()	
		
class emp_info_form(forms.Form):
	employee = forms.CharField()
	clock = forms.CharField()	
	shift = forms.CharField()
	
class job_info_form(forms.Form):
	description = forms.CharField()
	OP = forms.CharField()	
	Part = forms.CharField()
	Machine = forms.CharField()
	
class sup_downForm(forms.Form):
	machine = forms.CharField()	
	reason = forms.CharField()	
	priority = forms.CharField()	
	
class sup_dispForm(forms.Form):
	machine = forms.CharField()	
	reason = forms.CharField()	
	priority = forms.CharField()

class sup_closeForm(forms.Form):
	comment = forms.CharField()		

class sup_vac_filterForm(forms.Form):
	shift = forms.CharField()	
	
class login_Form(forms.Form):
	name = forms.CharField()	
	password = forms.CharField()			

class robot_machine_form(forms.Form):
	robot = forms.CharField()
	machine1 = forms.CharField()	
	machine2 = forms.CharField()
	machine3 = forms.CharField()
	machine4 = forms.CharField()
	part = forms.CharField()

class tech_message_Form(forms.Form):
	name = forms.CharField()	
	message = forms.CharField()	

	
	
class toggletest_Form(forms.Form):
	shift = forms.CharField()	

class views_scheduler_selectionForm(forms.Form):
	selection = forms.CharField()

class layered_entry_Form(forms.Form):
	Type = forms.CharField()	
	Part = forms.CharField()	
	Op = forms.CharField()	
	
class maint_closeForm(forms.Form):
	comment = forms.CharField()	

class maint_passForm(forms.Form):
	comment = forms.CharField()	
	whos = forms.CharField()	
	
class maint_loginForm(forms.Form):
	user = forms.CharField()
	pwd = forms.CharField()		
	
class maint_searchForm(forms.Form):
	machine = forms.CharField()	
