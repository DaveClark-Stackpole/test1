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

import uuid

def test_mac(request):
    request.session["Mac_Address"] = (hex(uuid.getnode()))
    return render(request,'done_test8.html')



