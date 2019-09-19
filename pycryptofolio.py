# This program calculates the total worth of all your coins
# All your coins with their amounts should be put in a file coins.txt. An example file is given in this folder.
# Author: Hamid Mushtaq
import time
import json, requests
import math
import operator
import datetime
import webbrowser, os
import os.path
import locale
from copy import deepcopy

from pycryptofolio.coin import Coin
from pycryptofolio.exchange import Exchange

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

KEY_PATH = 'key.txt'

total = 0.0
total_worth = {}

def get_relevant_info(info, cur):
	coin_info = {}
	coin_info['name'] = info['name']
	coin_info['price'] = info['quote'][cur]['price']
	coin_info['symbol'] = info['symbol']
	coin_info['id'] = info['slug']
	coin_info['change_1h'] = info['quote'][cur]['percent_change_1h']
	coin_info['change_24h'] = info['quote'][cur]['percent_change_24h']

	return coin_info

def get_coins_info(CUR):
	coins = {}

	with open(KEY_PATH, 'r') as f:
		key_path = f.read().strip()

	parameters = {
		'start':'1',
		'limit':'5000',
		'convert':CUR
	}

	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': '%s' % key_path
	}

	session = Session()
	session.headers.update(headers)

	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		for i,coin in enumerate(data['data']):
			try:
				info = get_relevant_info(coin, CUR)
				format_check = "%d. %s, %s, %s -> %g, %g, %g\n" % (i+1, info['name'], info['symbol'], info['id'], info['price'], info['change_1h'], info['change_24h'])
				coins[info['id']] = info
			except:
				print("Exception for coin " + info['name'])
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)

	return coins

def imageStr(coinInfo):
	coinName = coinInfo.split(':')[0]
	if os.path.exists('images/' + coinName + '.png'):
		return " <img src=../images/%s.png alt=\"\" height=24 width=24></img>" % coinName  
	else:
		return ""

def drawProgressBar(val, _1h):
	width_factor = 20 if _1h else 4
	if val < 0:
		width = min(int(abs(val) * width_factor), 100)
		s = "<div class=\"w3-black\"><div class=\"w3-container w3-red w3-center\" style=\"width:%d%%\">%.2f%%</div></div>" % \
			(width, val)
	elif val > 0:
		width = min(int(abs(val) * width_factor), 100)
		s = "<div class=\"w3-black\"><div class=\"w3-container w3-green w3-center\" style=\"width:%d%%\">%.2f%%</div></div>" % \
			(width, val)
	else:
		s = "<div class=\"w3-black\"><div class=\"w3-container w3-green w3-center\" style=\"width:%d%%\">%.2f%%</div></div>" % \
			(0, 0)
			
	return s

def isFloat(s):
	try:
		x = float(s)
		return True
	except ValueError:
		return False
		
filepath = 'coins.txt'
now = datetime.datetime.now()
current_time = now.strftime("%d_%m_%Y-%H_%M")   

if not os.path.isdir('html'):
		os.makedirs('html')
html_fname = 'html/coinstable_%s.html' % current_time
f = open(html_fname, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body bgcolor=lavender>\n')
table_style="""
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
#cointable {
	font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
	border-collapse: collapse;
	background-color: white;
	width: 100%;
}

#cointable td, #cointable th {
	border: 1px solid #ddd;
	padding: 8px;
}

#cointable tr:nth-child(even){background-color: whitesmoke;}

#cointable th {
	padding-top: 12px;
	padding-bottom: 12px;
	text-align: left;
	background-color: darkblue;
	color: white;
}

h2 {
	font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
}

.green_cell {
	color: limegreen;
}
.red_cell {
	color: red;
}
colored_span {
	color: darkblue 
}
</style>"""
f.write(table_style + '\n')

with open(filepath) as fp:  
		lines = fp.readlines()

print("Gathering all the necessary information...")

for line in lines:
	x = line.split('=')
	if line[0] == '#' or (len(x) < 2):
		continue
	coin_info = x[0].strip()
	coin_name = coin_info.split(':')[0].strip()
	if coin_info.lower() == "currency":
		CURRENCY = x[1].strip().upper()
		coins_info = get_coins_info(CURRENCY)
		continue
	
	coin_amount = x[1].strip()
	if coin_amount[0] != '@':
		coin = Coin(coin_info, float(coin_amount), coins_info)
		if Coin.contextListIsEmpty(coin.context):
			total_worth[coin.context] = 0.0
		Coin.addCoin(coin.context, coin)
		Coin.addCoinCombined(coin.name, coin)
		total_worth[coin.context] = total_worth[coin.context] + coin.worth
		total = total + coin.worth
	else:
		exchange_key = coin_amount[1:]
		exchange_name = coin_info
		print ("EXCHANGE NAME = " + exchange_name + ", EXCHANGE_KEY = " + exchange_key)
		obj = Exchange.factory(exchange_name)
		coins_amounts = obj.getCoinsAmounts(exchange_key)
		for e in coins_amounts:
			x = e.split('=')
			coin_info = x[0]
			coin_name = coin_info.split(':')[0]
			coin_amount = x[1]
			coin = Coin(coin_info, float(coin_amount), CURRENCY)
			if Coin.contextListIsEmpty(coin.context):
				total_worth[coin.context] = 0.0
			Coin.addCoin(coin.context, coin)
			Coin.addCoinCombined(coin.name, coin)
			total_worth[coin.context] = total_worth[coin.context] + coin.worth
			total = total + coin.worth
		
coins = Coin.getCoins()
coins_combined = Coin.getCoinsCombined()

def drawRow(i, coin):
	name = "<a href=\"https://coinmarketcap.com/currencies/%s/\" target=\"_blank\">%s</a>" % (coin.name.lower(), coin.name.upper())
	f.write('<tr>\n')
	if (coin.price_cur != 0):
		price = "%.4f %s (%0.8f BTC)" % (coin.price_cur, CURRENCY.upper(), coin.price_cur / coins_info['bitcoin']['price'])
		amount = "%g" % coin.amount
		worth = "%0.2f %s (%0.4f BTC)" % (coin.worth, CURRENCY.upper(), coin.worth / coins_info['bitcoin']['price'])
		change1h_td = "<td>" + drawProgressBar(coin.change1h, True) + "</td>"
		change24h_td = "<td>" + drawProgressBar(coin.change24h, False) + "</td>"
		# Changes with respect to BTC
		change1h_wrt_btc = coin.change1h - coins_info['bitcoin']['change_1h']
		change24h_wrt_btc = coin.change24h - coins_info['bitcoin']['change_24h']
		change1h_wrt_btc_td = "<td>" + drawProgressBar(change1h_wrt_btc, True) + "</td>"
		change24h_wrt_btc_td = "<td>" + drawProgressBar(change24h_wrt_btc, False) + "</td>"
		f.write("\t<td>%d. %s %s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t%s\n \t%s\n \t%s\n \t%s\n" % \
			(i, imageStr(coin.name), name, amount, worth, price, change1h_td, change1h_wrt_btc_td, change24h_td, change24h_wrt_btc_td))
	else:
		price = "This coin doesn't exist" 
		amount = "%0.4f" % coin.amount
		worth = "-" 
		change = "<td>-</td>"
		f.write("\t<td>%d. %s %s</td>\n  \t<td>%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t%s\n \t%s\n \t%s\n \t%s\n" % \
			(i, imageStr(coin.name), name, amount, worth, price, change, change, change, change))
	f.write('</tr>\n')

def drawTable(context):
	sorted_coins = sorted(coins[context], key=operator.attrgetter('worth'), reverse=True)

	f.write('<h2>Total worth %s = <colored_span>%.2f %s (%.4f BTC)</colored_span></h2>\n' % \
		("for rest" if context == "other" else "at " + context, total_worth[context], CURRENCY.upper(), total_worth[context] / coins_info['bitcoin']['price']))

	i = 0
	f.write('<table id = cointable>\n<tr>\n\t<th>Coin</th>\n \t<th>Amount</th>\n \t<th>Worth</th> \t<th>Price</th>\n \t<th>Change in 1 hour</th>\n \t<th>Change in 1 hour w.r.t BTC</th>\n \t<th>Change in 24 hours</th>\n \t<th>Change in 24 hours w.r.t BTC</th>\n \n')
	for coin in sorted_coins:
		i = i + 1
		drawRow(i, coin)
	f.write('</table>\n\n<br/>\n')
		
def drawCombinedTable():
	coins_dict = {}
	
	# coins_combined -> (coin_name, [coin at bittrex, coin at bitfinex ...] etc)
	for coin_name in coins_combined:
		total_amount = 0.0
		coin_list = coins_combined[coin_name]
		coin = deepcopy(coin_list[0])
		for c in coin_list:
			total_amount = total_amount + c.amount
		coin.amount = total_amount
		coin.worth = coin.amount * coin.price_cur
		coins_dict[coin_name] = coin
	
	i = 0
	f.write('<table id = cointable>\n<tr>\n\t<th>Coin</th>\n \t<th>Amount</th>\n \t<th>Worth</th> \t<th>Price</th>\n \t<th>Change in 1 hour</th>\n \t<th>Change in 1 hour w.r.t BTC</th>\n \t<th>Change in 24 hours</th>\n \t<th>Change in 24 hours w.r.t BTC</th>\n \n')
	sorted_coins = sorted(coins_dict.items(), key=lambda x: x[1].worth, reverse=True)
	for x in sorted_coins:
		i = i + 1
		coin = x[1]
		drawRow(i, coin)
	f.write('</table>\n<br/>\n')

print("Generating the html file " + html_fname + "...")
f.write('<h2>Total worth = <colored_span>%.2f %s (%.4f BTC)</colored_span></h2>\n' % (total, CURRENCY, total / coins_info['bitcoin']['price']))
sorted_total_worth = sorted(total_worth.items(), key=operator.itemgetter(1), reverse=True)
drawCombinedTable()
for e in sorted_total_worth:
	drawTable(e[0])
f.write('</body>\n</html>\n')

f.close()
print ("Opening the html file " + html_fname)
webbrowser.open('file://' + os.path.realpath(html_fname))
