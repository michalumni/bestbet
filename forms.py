from flask.ext.wtf import Form
from wtforms.fields import IntegerField, SubmitField, SelectField

class SelectionForm(Form):
  sport = SelectField(u'Sport', choices=[('ncaab', 'College Basketball'), ('nba', 'NBA')]) 
  dimesbr = IntegerField("5dimes Bankroll")
  bmbr = IntegerField("Bookmaker Bankroll")
  kelly = IntegerField("Percentage Kelly criterion")
  submit = SubmitField("Process")
