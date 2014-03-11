
# -*- coding: utf-8 -*-
class GameInfo():
    team1 = ''
    team2 = ''
    dimeso = ''
    dimesu = ''
    bmo = ''
    bmu = ''
    pinnyo = ''
    pinnyu = ''

        #def __init__(self):
    #self.teams[:] = []

 
    def printcsv(self):
        self.team1 = self.team1.replace(u'\xa0', '')
        self.team2 = self.team2.replace(u'\xa0', '')
        
        self.dimeso = self.dimeso.replace(u'½', '.5 ')
        self.dimeso = self.dimeso.replace(u'\xa0', '')
        self.dimesu = self.dimesu.replace(u'\xa0', '')
        self.dimesu = self.dimesu.replace(u'½', '.5 ')
        self.bmo = self.bmo.replace(u'\xa0', '')
        self.bmo = self.bmo.replace(u'½', '.5 ')
        self.bmu = self.bmu.replace(u'\xa0', '')
        self.bmu = self.bmu.replace(u'½', '.5 ')
        self.pinnyo = self.pinnyo.replace(u'\xa0', '')
        self.pinnyo = self.pinnyo.replace(u'½', '.5 ')
        self.pinnyu = self.pinnyu.replace(u'\xa0', '')
        self.pinnyu = self.pinnyu.replace(u'½', '.5 ')
        #self.printme()
        #return [printable(self.team1), (self.team2), 
        #return ( [(self.team1), (self.team2), (self.dimeso), (self.dimesu), (self.bmo), (self.bmu), (self.pinnyo), (self.pinnyu)])
    def printme(self):
        print self.team1
        print self.team2
        print self.dimeso
        print self.dimesu
        print self.bmo
        print self.bmu
        print self.pinnyo
        print self.pinnyu
