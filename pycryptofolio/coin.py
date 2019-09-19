import json, requests

class Coin(object):
	coins = {}
	coins_combined = {} # Each coin combined from different exchanges 

	def __init__(self, coin_info, amount, coins_info):
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

		if self.name in coins_info:
			self.price_cur = coins_info[self.name]['price']
			self.worth = self.amount * self.price_cur
			self.change1h = coins_info[self.name]['change_1h']
			self.change24h = coins_info[self.name]['change_24h']
		else:
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