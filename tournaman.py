# -*- coding: utf-8 -*-

# Copyright 2013 by Fabian Hachenberg http://github.com/fHachenberg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Representation of Tournaman XML data as Python classes
'''

__author__ = "Fabian Hachenberg"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley",
                    "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rob Knight"
__email__ = "rob@spot.colorado.edu"
__status__ = "Production"

class Team(object):
    def __init__(self, **args):
        self.name = args['name']
        self.id   = args['id']

class Participant(object):
    def __init__(self, **args):
        self.name = args['name']

class Speaker(Participant):
    def __init__(self, **args):
        Participant.__init__(self, **args)

class Adjucator(Participant):
    def __init__(self, **args):
        Participant.__init__(self, **args)

class Venue(object):
    def __init__(self, **args):
        self.id = args['id']
        self.name = args['name']

class Debate(object):
    def __init__(self, **args):
        self.og = args['og']
        self.cg = args['cg']
        self.oo = args['oo']
        self.co = args['co']
        self.venue = args['venue']
        self.adjuds = [] 

class Round(object):
    def __init__(self, **args):
        #self.index = args['index']
        self.motion = args['motion']
        self.debates = args['debates']

from lxml import etree

def parse_team_xml(filename):
    tree =etree.parse(filename)
    branch = tree.getroot()
    branch_name = branch.attrib['name']
    teams_tags = branch.findall("team")
    teams = {}
    for team_tag in teams_tags:
        name = team_tag.attrib['name']
        index = int(team_tag.attrib['ident'])
        teams[index] = Team(name=name, id=index)
    return teams

def parse_adjucator_xml(filename):
    tree =etree.parse(filename)
    adjudicators = tree.getroot()
    adjuds = {}
    adjuds_tags = adjudicators.findall("adjud")
    for adjud_tag in adjuds_tags:
        name = adjud_tag.attrib['name']
        institutions = [adjud_tag.attrib['home']]
        id = int(adjud_tag.attrib['id'])
        adjuds[id] = Adjucator(name=name)
    return adjuds

import re

def parse_venue_def(filename):
    venues = {}

    f = open(filename, "rb")
    for line in f:
        match = re.search(r"^([0-9]+)\s(.+)$", line)
        assert match != None
        venue_index_str, venue_name = match.groups(1)
        venue_index = int(venue_index_str)
        venues[venue_index] = Venue(name=venue_name, id=venue_index)
    return venues   

def parse_debates_xml(filename, team_db, adjuds_db, venue_db):
    tree =etree.parse(filename)
    rnd_tag = tree.getroot()
    motion_tag = rnd_tag.find("motion")
    debates_tags = rnd_tag.findall("debate")
    debates = []
    for debate_tag in debates_tags:
        venue_id = int(debate_tag.attrib['venue'])
        venue = venue_db[venue_id]
        teams_tags = debate_tag.findall("team")
        teams = {}
        #in tournaman xml files, the order of the team entries defines the
        #positions in the debate. The order is as following
        positions = ["og", "oo", "cg", "co"]
        for i, team_tag in enumerate(teams_tags):            
            team_id = int(team_tag.attrib['id'])
            teams[positions[i]] = team_db[team_id]
        debate = Debate(venue=venue, **teams)
        debates.append(debate)
    adjucators = rnd_tag.find("adjudicators")
    pair_tags = adjucators.findall("pair")
    for pair_tag in pair_tags:
        adjucator_id = int(pair_tag.attrib['adj'])
        adjucator = adjuds_db[adjucator_id]
        venue_id = int(pair_tag.attrib['venue'])
        debate = filter(lambda d: d.venue.id == venue_id, debates)[0]        
        debate.adjuds.append(adjucator)
    rnd = Round(motion=motion_tag.text, debates=debates) #index=1, 
    return rnd
        
