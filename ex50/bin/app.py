
import web



urls = (
	'/', 'index'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

import urllib
from lxml.html import fromstring





class Game(object):
	team1 = None
	team2 = None
	winner = None
	sprd = None
	
	def __init__(self, team1, team2, sprd):
		self.team1 = team1
		self.team2 = team2
		if sprd.text == 'Ev':
			self.winner = None
			self.sprd = float(0.0)
		elif sprd.text != None:
			self.winner = sprd.text[0]
			self.sprd = float(sprd.text[1:])
		else:
			self.sprd = None
			self.winner =  None
		self.rank =0
		
	def who_wins(self):
		if self.winner == "+":
			return(self.team2)
		if self.winner == "-":
			return(self.team1)
		else:
			return(None)
			
	def printing(self):
		return("#%s Game: %s vs %s Spread: %s Winner: %s" % (self.rank, self.team1, self.team2, self.sprd,self.who_wins()))

class index:
			
	

	
	def GET(self):
		url = 'http://www.oddsshark.com/ncaaf/odds'
		
		content= urllib.urlopen(url).read()
		doc = fromstring(content)
		doc.make_links_absolute(url)	
		spread = doc.xpath("//div[contains(@class, 'op-spread')]")
		
		spread_list = []
		count =0
		for num in spread:
			count+=1
			if count == 1:
				spread_list.append(num)
			elif count == 32:
				count = 0
		
		game_list = []
		switch = 0
		team_temp = None
		team_names =  doc.xpath("//div[contains(@class, 'op-matchup-team')]//text()")
		for team in team_names:
			switch+=1
			if switch == 1:
				team_temp = team
			elif switch == 2:
				switch = 0
				game_list.append(Game(team_temp,team,spread_list[len(game_list)]))
				team_temp = None
				
		game_list.sort(key=lambda game: game.sprd, reverse=False)
		count =0
		for game in game_list: 
			count+=1
			game.rank = count
			
		
		return render.index(game_list)
		
	def POST(self):
		form = web.input(name="Nobody", greet="Hello")
		grt = "%s, %s" % (form.greet, form.name)
		return render.index(greeting = grt)

if __name__ == "__main__":
	app.run()