# pycryptofolio
Add the amount of all your coins in file coins.txt (Example file given), and then just run the python script pycrptofolio.py. 

### Format to be used in coins.txt
1. All lines starting with # are ignored. So, you can put comments in such lines.
2. At the top, put the fiat currency you want to see the worth in. The format of that is `currency=currency_symbol`. 
For example, `currency=gbp` would show worth in British pound.
3. To get all the coins from an exchange/site, the format is `exchange_name = @read_key`. At this moment, only reading all coins from 
steemit are supported.
4. To list amount of a coin without exchange name, use the format `coin_name = amount`. If the coin is in an exchange, use the format 
`coin_name:exchange_name = amount`.
