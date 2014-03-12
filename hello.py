

import os, logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
#from forms import SelectionForm
from flask import render_template, request
from gameinfo import GameInfo
import urllib2, sys, csv
import xml.dom.minidom
from HTMLParser import HTMLParser
import StringIO
import xml.dom.minidom
from curses.ascii import isprint
import xml.parsers.expat

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLEARDB_DATABASE_URL')

@app.before_first_request
def setup_logging():
    logging.basicConfig(filename='error.log',level=logging.DEBUG)

##    if not app.debug:
##        # In production mode, add log handler to sys.stderr.
##        app.logger.addHandler(logging.StreamHandler())
##        app.logger.setLevel(logging.INFO)

##class Game(db.Model):
##    __tablename__ = 'nba'
##    Q1 = db.Column(db.Integer)
##    Q2 = db.Column(db.Integer)
##    H = db.Column(db.Integer)
##    Q3 = db.Column(db.Integer)
##    Q4 = db.Column(db.Integer)
##    FG = db.Column(db.Integer)

@app.route('/process', methods=['GET', 'POST'])
def processMethod():
    return 'hello'

def trimString(s, findme):
    line = s.find(findme)
    s = s[line:]
    return s

def getText(node):
    rc = ""
        
    if node.nodeType == node.TEXT_NODE:
        rc = rc + node.data
    return rc

def printable(str):
    try:
        return ''.join([c for c in str if ord(c) > 31 or ord(c) == 9])
    except TypeError:
        return ''


def calculateKelly(price, odds, kelly, br, printstr):
    #odds = odds/100.00
    value = ((odds * price) - 1)/(price - 1)
    if ((value * kelly) > .01):
        #myStr = (printstr + str(value * kelly * br * (price-1)))
        val = (value * kelly * br * (price-1))
        myVal = "%.2f" % val
        myStr = printstr + myVal
        return myStr
##        #if '.' in myStr:
##            index = myStr.find('.')
##            #return myStr.substr(0, index+2)
##            return myStr[0:index+2]
##        else:
##            return myStr
    else:
        return ''

def processLine(var):
    myChar = '-'
    if myChar not in var:
        myChar = '+'
    pinny = var.split(myChar)
    if myChar == '-':
        pinny[1] = '-' + pinny[1]
    #print pinny
    return pinny

def calculateOdds(pinny, sign, period, duration, sport, conn):
    #print sport
    if sport == 'ncaab':
        duration = '1H'
    endStr = ''
    beginStr = ''
    if ('.5' in str(pinny) and (sport == 'ncaaf' or sport == 'nfl')):
        pinnyStr = str(pinny).replace('.5', '')
        pinnyFloat = float(pinnyStr)
        endStr = '(fg = ' + str(pinnyFloat - 1) + ' or fg = ' + str(pinnyFloat) + ' or fg = '+ str(pinnyFloat + 1) + ' or fg = ' + str(pinnyFloat + 2) + ');'
    elif (sport == 'ncaaf' or sport == 'nfl'):
        endStr = '(fg = ' + str(pinny - 2) + ' or fg = ' + str(pinny - 1) + ' or fg = '+ str(pinny) + ' or fg = ' + str(pinny + 1) + ' or fg = ' + str(pinny+2) + ');'
    elif ('.5' in str(pinny) and (sport == 'ncaab' or sport == 'nba')):
        pinnyStr = str(pinny).replace('.5', '')
        pinnyFloat = float(pinnyStr)
        endStr = '(fg = ' + str(pinnyFloat - 3) + ' or fg = ' + str(pinnyFloat - 2) + ' or fg = ' + str(pinnyFloat - 1) + ' or fg = ' + str(pinnyFloat) + ' or fg = '+ str(pinnyFloat + 1) + ' or fg = ' + str(pinnyFloat+2)  + ' or fg = ' + str(pinnyFloat+3) + ' or fg = ' + str(pinnyFloat + 4) + ');'
    elif (sport == 'nba' or sport == 'ncaab'):
        endStr = '(fg = ' + str(pinny-4) + ' or fg = ' + str(pinny-3) + ' or fg = ' + str(pinny - 2) + ' or fg = ' + str(pinny - 1) + ' or fg = '+ str(pinny) + ' or fg = ' + str(pinny + 1) + ' or fg = ' + str(pinny+2) + ' or fg = ' + str(pinny+3) + ' or fg = ' + str(pinny+4) + ');'

    
    if ('.5' in period and (sign == '>')):
        tempperiod = period.replace('.5', '')
        beginStr = 'select sum(' + duration + ' ' + sign + ' ' + tempperiod + ')/(count(' + duration + '))'  
    elif ('.5' in period and (sign == '<')):
        beginStr = 'select sum(' + duration + ' ' + sign + ' ' + period + ')/(count(' + duration + '))'  
    else:
        beginStr = 'select sum(' + duration + ' ' + sign + ' ' + period + ')/(count(' + duration + ')' '-sum(' + duration + ' = ' + period + '))'

    finalStr =  beginStr + ' from ' + sport + ' where ' + endStr
    app.logger.debug(finalStr)
    #cur = db.cursor()
    val = conn.execute(finalStr)
    car = val.fetchone()
    #app.logger.debug(val)
    app.logger.debug(car)
    myVal = float(car[0])
    #print myVal
    return myVal

def calculatePrice(var):
    price = 1.0
    if var[0] == '-':
        tempVar = var.strip('-')
        tempPrice = float(tempVar)
        addMe = 100.00/tempPrice
        price = price + addMe
    else:
        tempVar = float(var)
        tempPrice = tempVar/100.00
        price = price + tempPrice

    #print price
    return price

def getGames(games, id, theClass, elements, k):
    if ((theClass == 'eventLine-book-value ') and (id == (('eventLineBook-') + (k) + ('-19-o-3')))):
        b = elements.getElementsByTagName('b')
        if (b[0].firstChild is not None):
            games[k].dimeso = printable(b[0].firstChild.nodeValue)
    if ((theClass == 'eventLine-book-value ') and (id == (('eventLineBook-') + (k) + ('-93-o-3')))):
        b = elements.getElementsByTagName('b')
        if (b[0].firstChild  is not None):
            games[k].bmo = printable(b[0].firstChild.nodeValue)
    if ((theClass == 'eventLine-book-value ') and (id == (('eventLineBook-') + (k) + ('-238-o-3')))):
        b = elements.getElementsByTagName('b')
        if (b[0].firstChild  is not None):
            games[k].pinnyo = printable(b[0].firstChild.nodeValue)
    if ((theClass == 'eventLine-book-value ') and (id == (('eventLineBook-') + (k) + ('-19-u-3')))):
        b = elements.getElementsByTagName('b')
        if (b[0].firstChild  is not None):
            games[k].dimesu = printable(b[0].firstChild.nodeValue)
    if ((theClass == 'eventLine-book-value ') and (id == (('eventLineBook-') + (k) + ('-93-u-3')))):
        b = elements.getElementsByTagName('b') 
        if (b[0].firstChild  is not None):
            games[k].bmu = printable(b[0].firstChild.nodeValue)
    if ((theClass == 'eventLine-book-value ') and (id == (('eventLineBook-') + (k) + ('-238-u-3')))):
        b = elements.getElementsByTagName('b')
        if (b[0].firstChild  is not None):
            games[k].pinnyu = printable(b[0].firstChild.nodeValue)





def parseWebsite(doc):
    games = {}
    reflist = doc.getElementsByTagName('div')
    for subelement in reflist:
        attr = subelement.getAttribute('id')
        if 'holder-' in attr:
            gameno = attr.strip('holder-')
        attr2 = subelement.getAttribute('class')
        if (attr2 == 'eventLine  status-scheduled ' or attr2 == 'eventLine odd status-scheduled '):
            games[gameno] =  GameInfo()

    for k, v in games.items():
        for elements in reflist:
            attrs1 = elements.getAttribute('id')
            if attrs1 == k:
                for e in elements.childNodes:
                    attrs2 = e.getAttribute('class')
                    if attrs2 == 'el-div eventLine-team':
                        for d in e.childNodes:
                            attrs3 = d.getAttribute('class')
                            if attrs3 == 'eventLine-value':
                                for f in d.childNodes:
                                    attrs4 = f.getAttribute('class')
                                    if (attrs4 == 'team-name'):
                                        if games[k].team1 == '':
                                            games[k].team1 = printable(f.firstChild.nodeValue)
                                        else:
                                            games[k].team2 = printable(f.firstChild.nodeValue)




    for k1, v1 in games.items():
        for elements2 in reflist:
            id = elements2.getAttribute('id')
            theClass = elements2.getAttribute('class')
            getGames(games, id, theClass, elements2, k1)


    for k1, v1 in games.items():
       games[k1].printcsv()
##        for thestr in wr:
##            app.logger.debug(thestr)

    return games
 

def gettheGames(myform, duration):
    dimesbr = float(myform['dimesbr'])
    bmbr = float(myform['bkbr'])
    kelly = float(myform['kelly'])/100
    sport = myform['sport']
    

    if sport == 'nfl':
        urlsport = 'nfl-football/'
        seasonId = '119'
    if sport == 'ncaaf':
        urlsport = 'college-football/'
        seasonId = '124'
    if sport == 'nba':
        urlsport = 'nba-basketball/'
        seasonId = '170'
    if sport == 'ncaab':
        urlsport = 'ncaa-basketball/'
        seasonId = '191'

    if duration == 'H':
        urlduration = '1st-half/'
    if duration == '1Q':
        urlduration = '1st-quarter/'
    if duration == '2Q':
        urlduration = '2nd-quarter/'
    if duration == '3Q':
        urlduration = '3rd-quarter/'
    if duration == '4Q':
        urlduration = '4th-quarter/'
    if duration == 'FG':
        urlduration = 'full-game/'
        if sport == 'ncaab':
            urlduration = ''


    app.logger.debug(urlsport)
    app.logger.debug(urlduration)


    f = urllib2.urlopen('http://www.sbrforum.com/betting-odds/' + urlsport + 'totals/' + urlduration)
    s = f.read()
    s = trimString(s, '   _SEASONID = ' + seasonId + ';</script>')
    s = trimString(s, '<div')
    #index = s.index('<script language=')
    #s = s[0:index-17]
    buf = StringIO.StringIO(s)

    myLine = '<?xml version="1.0" ?>\n' + buf.readline()
    test = StringIO.StringIO(myLine)
    doc = xml.dom.minidom.parse(test)
    
    games = parseWebsite(doc)
    return games
    #for game in games:
#        app.logger.debug('game is ' + (str(game.team1)))
                         
 #   app.logger.debug('A value for debugging')
    
    #return str(games[0].team1)
def processFGline(var):
    myChar = '-'
    if myChar not in var:
        myChar = '+'
    pinny = var.split(myChar)
    #print pinny
    return float(pinny[0])

def processGames(games, finalGames, myform):
    #parse input form
    dimesbr = float(myform['dimesbr'])
    bmbr = float(myform['bkbr'])
    kelly = float(myform['kelly'])/100
    sport = myform['sport']
    duration = myform['Interval']

    #setup the db
    engine = db.create_engine('mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98')
    conn = engine.connect()
    finalStr = '<html>'
    finalStr = finalStr + '<div style=\"text-align: center;\">' + '<title> Best Bets </title>'
    finalStr = finalStr + '<link rel=\"stylesheet\" href=\"//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css\">'
    finalStr = finalStr + '<h1>' + duration + ' Bets' + '</h1>' + '</div>'
    for k1, v1 in games.items():
        finalStr = finalStr + '<table border=\"1\">'
        finalStr = finalStr + '<th>' + finalGames[k1].team1 + ' vs ' + finalGames[k1].team2 + '</th>'
        fgi = finalGames.items()
        pinnyo = finalGames[k1].pinnyo
        if (pinnyo != ''):
            #finalStr = finalStr  + ' ' + finalGames[k1].team1 + ' ' +  pinnyo + '<br/>'
            pinny = processFGline(pinnyo)
            if games[k1].dimeso != '':
                var = processLine(games[k1].dimeso)
                price = calculatePrice(var[1])
                odds = calculateOdds(pinny, '>', var[0], duration, sport, conn)
                value = calculateKelly(price, odds, kelly, dimesbr, '5dimes over ')
                if value != '':
                    finalStr =  finalStr + '<tr bgcolor=\"green\"><td>' + value + '</td></tr>'
            if games[k1].bmo != '':
                var = processLine(games[k1].bmo)
                price = calculatePrice(var[1])
                odds = calculateOdds(pinny, '>', var[0], duration, sport, conn)
                value = calculateKelly(price, odds, kelly, bmbr, 'Bookmaker over ')
                if value != '':
                    finalStr =  finalStr + '<tr bgcolor=\"green\"><td>' + value + '</td></tr>'
            if games[k1].dimesu != '':
                var = processLine(games[k1].dimesu)
                price = calculatePrice(var[1])
                odds = calculateOdds(pinny, '<', var[0], duration, sport, conn)
                value = calculateKelly(price, odds, kelly, dimesbr, '5dimes under ')
                if value != '':
                    finalStr =  finalStr + '<tr bgcolor=\"red\"><td>' + value + '</td></tr>'
            if games[k1].bmu != '':
                var = processLine(games[k1].bmu)
                price = calculatePrice(var[1])
                odds = calculateOdds(pinny, '<', var[0], duration, sport, conn)
                value = calculateKelly(price, odds, kelly, dimesbr, 'Bookmaker under ')
                if value != '':
                    finalStr =  finalStr + '<tr bgcolor=\"red\"><td>' + value + '</td></tr>'
    
        #finalStr = finalStr + 'hello'bgcolor="#FF0000"

        finalStr = finalStr + '</table><br/><br/>'
        
    #result = db.engine.execute( '''select 2Q from nba where 1Q=45 and fg=205''')
    #result = result.fetchone()

    finalStr = finalStr + '</html>'
    return finalStr

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def validateForm(myform):

    dimesbr = (myform['dimesbr'])
    if not is_number(dimesbr):
        return 'Please enter a number for 5 dimes bankroll'
    else:
        j = float(dimesbr)
        if j < 0:
            return 'Please enter a positive number for 5 dimes bankroll'


    
    bmbr = myform['bkbr']
    if not is_number(bmbr):
        return 'Please enter a number for Bookmaker bankroll'
    else:
        j = float(bmbr)
        if j < 0:
            return 'Please enter a positive number for Bookmaker bankroll'


    
    kelly = myform['kelly']
    if not is_number(kelly):
        return 'Please enter a number for Kelly Criterion'
    else:
        j = float(kelly)
        if j > 100 or j < 0:
            return 'Please enter a number between 0-100 for Kelly Criterion'



    

    sport = myform['sport']

    duration = myform['Interval']
    if duration != '1Q' and duration != '2Q' and duration != '3Q' and duration != '4Q' and duration != 'H':
        return 'Please Enter 1Q, 2Q, H, 3Q or 4Q for Interval'

    if sport == 'ncaab' and duration != 'H':
        return 'Interval needs to be H for college basketball'
    
    return ''

@app.route('/', methods=['GET', 'POST'])
def hello():

    error = ''
    if (request.method == 'GET'):
        return render_template('index.html', error=error)
    else:
        myform = request.form
        error = validateForm(myform)
        if (error != ''):
            app.logger.debug('error is ' + error)
            
            return render_template('index.html', error=error)
        duration = myform['Interval']
        #assume all input is valid lets process
        try:
            games = gettheGames(myform, duration)
        except xml.parsers.expat.ExpatError:
            error = 'NBA games started, please select different sport'
            return render_template('index2.html', error=error)
        duration = 'FG'
        finalGames = gettheGames(myform, duration)
        return processGames(games, finalGames, myform)
        
        #logging.basicConfig(filename='error.log',level=logging.DEBUG)

#    if 
    #sess = db.create_engine('mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98')
    #myconn = db.connect()
    #result = db.engine.execute( '''select 2Q from nba where 1Q=45 and fg=205''')
    #result = result.fetchone()
    #for row in result:
    #    return str(row)
    
    #return 'hello world'
    #engine = create_engine('mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98')
    #conn = engine.connect()
    #result = conn.execute('select * from nba')
    #for row in result:
        #return row
    
    #return conn
##    myNba = SQLAlchemy.Table('nba', metadata,
##                             SQLAlchemy.Column('1Q', Integer),
##                             SQLAlchemy.Column('2Q', Integer),
##                             SQLAlchemy.Column('H', Integer),
##                             SQLAhchemy.Column('3Q', Integer),
##                             SQLAlchemy.Column('4Q', Integer),
##                             SQLAlchemy.Column('FG', Integer)
##                             )
    
    #return 'Hello World!111'


