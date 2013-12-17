# -*- coding: utf-8 -*-

'''
Frisst eine Rundendefinition aus Tournaman als XML-Datei und spuckt dann mithilfe eines pptx-Templates eine Präsentation für die Runde aus. Für die Motion kann eine weitere pptx-Präsentation übergeben werden, die dann dort eingebaut wird.
'''

import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--round_no', dest='round_no', action='store', type=int,
                   help='Rundennummer')
parser.add_argument('--venue_file', dest='venue_file', action='store',
                   help='Definition der Venues im Tournaman-def-Format')
parser.add_argument('--team_file', dest='team_file', action='store',
                   help='Definition der Teams im Tournaman-XML-Format')
parser.add_argument('--adjucator_file', dest='adjucator_file', action='store',
                   help='Definition der Juroren im Tournaman-XML-Format')
parser.add_argument('--round_file', dest='round_file', action='store',
                   help='Definition der Turnierrunde im Tournaman-XML-Format')
parser.add_argument('--pptx_template', dest='pptx_template', action='store',
                   help='Präsentations-Template im pptx-Format')
parser.add_argument('--output', dest='output', action='store', default='test.pptx', help='Ausgabe-Dateiname')

args = parser.parse_args()

round_no   = args.round_no
venue_file = args.venue_file
team_file  = args.team_file
adjucator_file = args.adjucator_file
round_file = args.round_file
output = args.output

pptx_template = args.pptx_template

#Einlesen Daten aus XML

import tournaman

venue_db = tournaman.parse_venue_def(venue_file)
team_db  = tournaman.parse_team_xml(team_file)
adjud_db = tournaman.parse_adjucator_xml(adjucator_file)
rnd = tournaman.parse_debates_xml(round_file, team_db, adjud_db, venue_db)

from pptx import Presentation

import re

prs = Presentation(pptx_template)

replacements = {
                "m": rnd.motion,
                "r": str(round_no),
                "v1": rnd.debates[0].venue.name,
                "v2": rnd.debates[1].venue.name,
                "v3": rnd.debates[2].venue.name,
                "og1": rnd.debates[0].og.name,
                "og2": rnd.debates[1].og.name,
                "og3": rnd.debates[2].og.name,
                "oo1": rnd.debates[0].oo.name,
                "oo2": rnd.debates[1].oo.name,
                "oo3": rnd.debates[2].oo.name,
                "cg1": rnd.debates[0].cg.name,
                "cg2": rnd.debates[1].cg.name,
                "cg3": rnd.debates[2].cg.name,
                "co1": rnd.debates[0].co.name,
                "co2": rnd.debates[1].co.name,
                "co3": rnd.debates[2].co.name,
                "j1":"\n".join(adjud.name for adjud in rnd.debates[0].adjuds),
                "j2":"\n".join(adjud.name for adjud in rnd.debates[1].adjuds),
                "j3":"\n".join(adjud.name for adjud in rnd.debates[2].adjuds)
                }

def do_repl(match):
    name = match.groups(1)[0]
    return replacements[name]

for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_textframe:
            continue
        for paragraph in shape.textframe.paragraphs:
            for run in paragraph.runs:     
                run.text = re.sub(r"#([a-z0-9]+)", do_repl, run.text)

prs.save(output)

