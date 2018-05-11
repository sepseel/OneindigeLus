#!/home/sepseel/anaconda3/bin/python
##!/usr/bin/env python

from infinity import OneindigeLus
import cgitb
import cgi
import json

# geef meer informatie weer bij een request,
# zoals error boodschappen
cgitb.enable()

def new_game(size=5):
    """
    start een niew spel met de opgegeven grootte
    """
    game = OneindigeLus([9, 12, 12, 6, 10, 13, 13, 5, 3, 3, 9, 3], 4, 0)
    print(json.dumps(game.state()))

def do_move(status, zin, rij, kol):
    """
    maakt een zet op de opgegeven status met de gegeven kleur,
    en geeft de nieuwe status trug
    """
    status = json.loads(status)
    status["score"] += 1
    game = OneindigeLus(status["tegels"], status["kol"], status["score"])
    game.draai(rij, kol, zin)
    print(json.dumps(game.state()))

def parse_query():
    """
    vertaald de query naar een uitvoerbare functie, 
    en voert deze uit
    """
    parameters = cgi.FieldStorage()
    func = parameters.getvalue('func')
    if func == 'new_game':
        return new_game()
    elif func == 'do_move':
        staat = parameters.getvalue('state')
        zin = parameters.getvalue('zin')
        rij = parameters.getvalue('rij')
        kol = parameters.getvalue('kol')
        return do_move(staat, zin, int(rij), int(kol))

def print_bord(status):
    """
    print het spelbord uit naar de console 
    (voor debugging)
    """
    for lijn in status['board']:
        print(lijn)

print("Content-type: text/json\nAccess-Control-Allow-Origin: *\n")
parse_query()
