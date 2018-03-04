class Exchange(object):
	def factory(exchange_name):
		exchange_name = exchange_name.lower()
		if exchange_name == "steemit": 
			return Steemit()
	factory = staticmethod(factory)
    
class Steemit(Exchange):
	def getCoinsAmounts(self, key):
		self.coinsAmounts = []
		self.coinsAmounts.append("steem:steemit=782.3")
		self.coinsAmounts.append("steem-dollars:steemit=32.5")
		return self.coinsAmounts
 