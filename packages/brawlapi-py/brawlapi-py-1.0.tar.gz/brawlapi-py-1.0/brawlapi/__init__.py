try:
	import requests
	import json
except:
	import os
	for module in ['requests', 'json']:
		os.system(f"pip install {module}")

class Errors():
	class AuthorizationError(Exception):
		pass
		
class BrawlApi():
	def __init__(self):
		self.headers = {}
		self.api_url = "https://api.brawlapi.com/v1/"
		self.api_url_2 = "https://api.brawlstars.com/v1/"
		self.errors = Errors()
	#core
	def BrawlSession(self, token: str):
		self.headers = {
		"Authorization":f"Bearer {token}",
		"User-Agent": "brawlstats/v4.1.0 (Python 3.8)",
		"Accept-Encoding": "gzip"
		}
	def get_content(self, arg: str, content=None, api_mode=1):
		if self.headers != {}:
				if api_mode ==1:
					api_url_mode = self.api_url
				elif api_mode ==2:
					api_url_mode = self.api_url_2
				if content != None:
					request = requests.get(f"{api_url_mode}{arg}/{content}", self.headers)
					
				else:
						request = requests.get(f"{api_url_mode}{arg}", self.headers)
						
				if request.status_code == 200:
					return request.json()
				elif request.status_code == 403:
					return 403
		else:
			raise self.errors.AuthorizationError("Please authorization using your token!")
	def get_all_methods(self):
		return {"Core_methods":["BrawlSession(token: str)","get_content(arg, content=None,api_mode=1)","get_all_methods()"],"BrawlifyApi_methods":["get_events(rec_trophies=None: str)","get_brawlers(brawler_id=None: [int, str])","get_maps(map_id=None: [int, str], rec_trophies=None: str)","get_gamemodes(gamemode_id=None: [int, str])","get_icons()","get_clublog(tag: str)"],"BrawlstatsApi_methods":["get_profile/get_player(tag: str)","get_club(tag: str)","get_club_members(tag: str)","get_battle_log(tag: str)","get_rankings(ranking: str, region='global',limit: int = 200, brawler_id=None: [str, int])"]}
	#brawlify api
	def get_events(self, rec_trophies=None):
		if rec_trophies != None:
			if rec_trophies in ["0-299","300-599","600+"]:
				return self.get_content("events", rec_trophies)
			else:
				return {"err_code":403,"desc":"Bad arguments! Select the arguments from the list: 0-299,300-599,600+"}
		else:
			return self.get_content("events")
	def get_brawlers(self, brawler_id=None):
		if brawler_id != None:
			request = self.get_content("brawlers", brawler_id)
			if request == 403:
				return {"err_code":403,"desc":"Bad arguments! Bad brawler id!"}
			else:
				return request
		else:
			return self.get_content("brawlers")
	def get_maps(self, map_id=None, rec_trophies=None):
		if map_id != None:
			if rec_trophies !=None:
				if rec_trophies in ["0-299","300-599","600+"]:
					request = self.get_content("maps", f"{map_id}/{rec_trophies}")
					if request == 403:
						return {"err_code":403,"desc":"Bad arguments! Bad map id!"}
					else:
						return request
				else:
					return {"err_code":403,"desc":"Bad arguments! Select the arguments from the list: 0-299,300-599,600+"}
			else:
				request = self.get_content("maps", map_id)
				if request == 403:
					return {"err_code":403,"desc":"Bad arguments! Bad map id!"}
				else:
					return request
		else:
			return self.get_content("maps")
	def get_gamemodes(self, gamemode_id=None):
		if gamemode_id != None:
			request = self.get_content("gamemodes", gamemode_id)
			if request == 403:
				return {"err_code":403,"desc":"Bad arguments! Bad gamemode id!"}
			else:
				return request
		else:
			return self.get_content("gamemodes")
	def get_icons(self):
		return self.get_content("icons")
	def get_clublog(self, tag):
		request = self.get_content("clublog", tag.strip("#"))
		if request == 403:
			return {"err_code":404,"desc":"Please check club tag! Warning! Not all clubs are tracked."}
		else:
			return request
	#brawlstats api
	def get_player(self, tag: str):
		tag = "#" + tag.replace("#","")
		request = self.get_content("players",tag.replace("#","%23").upper(),api_mode=2)
		if request == None:
			return {"err_code":404,"desc":"Please check tag!"}
		elif request == 403:
			raise self.errors.AuthorizationError("Wrong token!")
		else:
			return request
	get_profile = get_player
	def get_club(self, tag: str):
		tag = "#" + tag.replace("#","")
		request = self.get_content("clubs",tag.replace("#","%23").upper(),api_mode=2)
		if request == None:
			return {"err_code":404,"desc":"Please check club tag!"}
		elif request == 403:
			raise self.errors.AuthorizationError("Wrong token!")
		else:
			return request
	def get_club_members(self, tag: str):
		tag = "#" + tag.replace("#","")
		request = self.get_content("clubs",tag.replace("#","%23").upper() + "/members",api_mode=2)
		if request == None:
			return {"err_code":404,"desc":"Please check club tag!"}
		elif request == 403:
			raise self.errors.AuthorizationError("Wrong token!")
		else:
			return request
	def get_battle_log(self, tag):
		tag = "#" + tag.replace("#","")
		request = self.get_content("players",tag.replace("#","%23").upper() + "/battlelog",api_mode=2)
		if request == None:
			return {"err_code":404,"desc":"Please check tag!"}
		elif request == 403:
			raise self.errors.AuthorizationError("Wrong token!")
		else:
			return request
	def get_rankings(self, ranking, region="global",limit: int = 200, brawler_id=None):
		if ranking in ["players", "clubs", "brawlers"]:
			if 0 < limit <= 200:
				if ranking == "brawlers":
					request = self.get_content("rankings",f"{region}/{ranking}/{brawler_id}/?limit={limit}", api_mode=2)
					if request == None:
						return {"err_code":403,"desc":"Bad arguments! Bad brawler id!"}
					else:
						return request
				else:
					return self.get_content("rankings",f"{region}/{ranking}/?limit={limit}", api_mode=2)
			else:
				return {"err_code":403,"desc":"Bad arguments! Make sure limit is between 1 and 200."}
		else:
			return {"err_code":403,"desc":"Bad arguments! Select the arguments from the list: players, clubs, brawlers"}