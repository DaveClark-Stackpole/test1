from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import MySQLdb
import time


def hyphon_fix(tx):
    tps = list(tx)
    if (tx.find("'"))>0:
        ty = list(tx)
        ta = tx.find("'")
        ty[ta] = ""
        tc = "".join(ty)
    else:
        tc = tx

    return tc

def multi_name_breakdown(n):
    nm = []
    tx = n
    if (tx.find("|"))>0:
        while True:
            len_tx = len(tx)
            ty = list(tx)
            ta = tx.find("|")
            ta = ta - 1
            lft = tx[:ta]
            nm.append(lft)
            ta = ta + 3
            ta_right = len_tx - ta
            tx = tx[-ta_right:]
            len_tx = len(tx)
            if (tx.find("|"))<0:
                break
        nm.append(tx)
    return nm


def index_template(request, index):
	page1 = request.session["page_edit"]
	request.session["current_index"] = index
	db, cur = db_set(request)
	if page1 == 'user login':
		sql1 = "SELECT * FROM tkb_logins where Id='%s'" % (index)
		cur.execute(sql1)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		tmp3 = tmp2[0]
		t = generate_string(tmp3, tec)

		sql = ('update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' %(t, index))
		cur.execute(sql)
		db.commit()
	db.close()

	return maint(request)
