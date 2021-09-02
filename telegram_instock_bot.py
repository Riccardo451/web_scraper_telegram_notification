#!/usr/bin/python3
# -*- coding: utf-8 -*-

# on raspberry run: sudo apt-get install libxslt1-dev libxml2
import random
from time import sleep
import schedule
import requests

from bs4 import BeautifulSoup
import lxml
import cchardet
import telebot

#debug library with snakeviz    /home/pi/gpu_scraper/gpu_single.py
#import cProfile

################# replace here with your data ##################################

telegram_bot_key = " telegram bot api number here "
my_ids = [122345678, 122345678]


keyword = "Comprar ya"    # Word to be checked
keyword2  = "Añadir a la cesta"

sleeptime = 1

# urls to be checked
url1 = "https://www.ldlc.com/es-es/ficha/PB84665477.html" # 3060ti founder
url2 = "https://www.ldlc.com/es-es/ficha/PB84531252.html" # 3070
url3 = "https://www.ldlc.com/es-es/ficha/PB84665477.html" # 3080
all_urls = [url1,url2,url3]

messaggio1 = '!!! GPU 3060Ti Founder DISPONIBILE !!!'
messaggio2 = '!!! GPU 3070 Founder DISPONIBILE !!!'
messaggio3 = '!!! GPU 3080 Founder DISPONIBILE !!!'
messaggi = [messaggio1, messaggio2, messaggio3]

#################################################################################
#################################################################################



bot = telebot.TeleBot(telegram_bot_key, threaded=False)

headers0 = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'}
headers1 = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.72'}
headers2 = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
headers3 = {"User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'}
headers4 = {"User-Agent": 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
headers5 = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
headers6 = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36'}
headers7 = {"User-Agent": 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
headers8 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15'}
headers9 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'}
allHeaders = [headers0, headers1, headers2, headers3, headers4, headers5, headers6, headers7, headers8, headers9]


def double_check(link):
	global gpu
	global counter
	gpu = False
	counter = 0
	try:
		response = requests.get(link, headers=random.choice(allHeaders))
		
		soup = BeautifulSoup(response.text, "lxml")

		if str(soup).find(keyword) == -1:
		    gpu = False
		    sleep(sleeptime)
		else:
			if str(soup).find(keyword) == -1:
				gpu = False
				sleep(sleeptime)
			else:
				gpu = True
				counter += 1

	except:
		None
	return gpu

def alive():
	message1 = 'Bot Alive'
	for my_id in my_ids:
		bot.send_message(my_id, message1)

 

if __name__ == '__main__':

	# Every day at 10am or 10:00 time alive() is called. 
	#schedule.every().day.at("10:00").do(alive)	
	schedule.every().day.at("22:00").do(alive)

	while True:
		
		schedule.run_pending() 

		for url, messaggio in zip(all_urls, messaggi):
			message = messaggio + "\n" + url1
			double_check(url)
			if gpu == True:

				for my_id in my_ids:
					try:
						bot.send_message(my_id, message)
						sleep(sleeptime)
					except:
						None
				if counter >= 3:
						sleep(60)
						counter = 0