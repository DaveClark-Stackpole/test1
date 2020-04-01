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
