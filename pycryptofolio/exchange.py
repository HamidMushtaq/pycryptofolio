import requests # if its not installed already, install it using "pip install requests"
import json

class Exchange(object):
	def factory(exchange_name):
		exchange_name = exchange_name.lower()
		if exchange_name == "steemit": 
			return Steemit()
	factory = staticmethod(factory)
    
class Steemit(Exchange):
	def __get_steem_per_mvests(self):
		site = 'https://steemdb.com/api/props'
		rj = requests.get(site)
		return rj.json()[0]["steem_per_mvests"]
		
	def __get_user_data(self, user):
		url = 'https://api.steemit.com'
		
		data = {
			"jsonrpc": "2.0",
			"method": "get_accounts",
			"params": [[user]],
			"id": 1
		}
		
		resp = requests.post(url, json=data)
		data = json.loads(resp.content)['result'][0]
		# split()[0] to remove the currency's name
		self.__steem =  float(data['balance'].split()[0])
		self.__sbd = float(data['sbd_balance'].split()[0])
		self.__vests = float(data['vesting_shares'].split()[0])
		
	def getCoinsAmounts(self, key):
		steem_per_mvests = self.__get_steem_per_mvests()
		self.__get_user_data(key)
		
		sp_amount = self.__vests * steem_per_mvests / 1e6
		
		self.coinsAmounts = []
		self.coinsAmounts.append("steem:steemit=%g" % (sp_amount + self.__steem))
		self.coinsAmounts.append("steem-dollars:steemit=%g" % self.__sbd)
		return self.coinsAmounts
 