import json, requests

class Coin(object):
	coins = {}
	coins_combined = {} # Each coin combined from different exchanges 

	def __init__(self, coin_info, amount, currency):
		self.context = "other"
		coin_and_context = coin_info.split(':')
		
		self.name = coin_and_context[0].strip()
		self.amount = amount
		
		if len(coin_and_context) > 1:
			self.context = coin_and_context[1].strip()
		if self.context not in Coin.coins:
			Coin.coins[self.context] = []
	
		if self.name not in Coin.coins_combined:
			Coin.coins_combined[self.name] = []
			
		try:
			req_str = 'https://api.coinmarketcap.com/v1/ticker/' + self.name + '/?convert=' + currency
			rj = requests.get(req_str).json()[0]
			self.price_cur = float(rj["price_" + currency])
			self.worth = self.amount * self.price_cur
			self.change1h = float(rj["percent_change_1h"])
			self.change24h = float(rj["percent_change_24h"])
		except:
			self.price_cur = 0
			self.worth = 0
			self.change1h = 0
			self.change24h = 0
			
	@classmethod
	def addCoin(cls, context, coin):
		cls.coins[coin.context].append(coin)
		
	@classmethod
	def addCoinCombined(cls, name, coin):
		cls.coins_combined[name].append(coin)
	
	@classmethod
	def getCoins(cls):
		return cls.coins
	
	@classmethod
	def getCoinsCombined(cls):
		return cls.coins_combined

	@classmethod
	def contextListIsEmpty(cls, context):
		return not Coin.coins[context]