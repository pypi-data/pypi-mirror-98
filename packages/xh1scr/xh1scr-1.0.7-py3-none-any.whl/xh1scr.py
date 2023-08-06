import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
global loop
loop = asyncio.get_event_loop()
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.400'}
class AsyncTok():
	async def run(acc):
		global accsx
		global soup
		accsx = []
		if type(acc) == list:
			for accs in acc:
				async with aiohttp.ClientSession() as session:
					async with session.get('http://tiktok.com/@%s?lang=en' % accs) as response:
						html = await response.text()
						soup = BeautifulSoup(html,'lxml')
						accsx.append(soup)
			soup = None
			return(accsx)
		else:
			async with aiohttp.ClientSession() as session:
					async with session.get('http://tiktok.com/@%s?lang=en' % acc) as response:
						html = await response.text()
						soup = BeautifulSoup(html,'lxml')
						accsx = None
						return(soup)
	async def status():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('h2','share-desc mt10')
					if parse.text == 'No bio yet.':
						parse = None
					else:
						stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('h2','share-desc mt10')
				if parse.text == 'No bio yet.':
					stats = None
				else:
					stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def nickname():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('h1','share-sub-title')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('h1','share-sub-title')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def following():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('strong',title='Following')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('strong',title='Following')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def followers():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('strong',title='Followers')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('strong',title='Followers')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def likes():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('strong',title='Likes')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('strong',title='Likes')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
	async def getavatar():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find_all('img')
					stats = parse[-1].get('src')
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find_all('img')
				stats = parse[-1].get('src')
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
class TikTok():
	def run(acc):
		global accsz
		global soupz
		accsz = []
		if type(acc) == list:
			for accsz in acc:
				session = requests.Session()
				url = ('http://tiktok.com/@%s?lang=en' % accs)
				html = session.get(url,headers=headers)
				soupz = BeautifulSoup(html.text,'lxml')
				accsz.append(soupz)
			soupz = None
			return(accsz)
		else:
			session = requests.Session()
			url = 'http://tiktok.com/@%s?lang=en' % acc
			html = session.get(url,headers=headers)
			soupz = BeautifulSoup(html.text,'lxml')
			accsz = None
			return(soupz)
	def status():
		global accsz
		global soupz
		res = []
		if soupz == None:
			for soupz in accsz:
				try:
					parse = soupz.find('h2','share-desc mt10')
					if parse.text == 'No bio yet.':
						parse = None
					else:
						stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soupz = None
			return(res)
		else:
			try:
				parse = soupz.find('h2','share-desc mt10')
				if parse.text == 'No bio yet.':
					stats = None
				else:
					stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	def nickname():
		global accsz
		global soupz
		res = []
		if soupz == None:
			for soupz in accsz:
				try:
					parse = soupz.find('h1','share-sub-title')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soupz = None
			return(res)
		else:
			try:
				parse = soupz.find('h1','share-sub-title')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	def following():
		global accsz
		global soupz
		res = []
		if soupz == None:
			for soupz in accsz:
				try:
					parse = soupz.find('strong',title='Following')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soupz = None
			return(res)
		else:
			try:
				parse = soupz.find('strong',title='Following')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	def followers():
		global accsz
		global soupz
		res = []
		if soupz == None:
			for soupz in accsz:
				try:
					parse = soupz.find('strong',title='Followers')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soupz = None
			return(res)
		else:
			try:
				parse = soupz.find('strong',title='Followers')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	def likes():
		global accsz
		global soupz
		res = []
		if soupz == None:
			for soupz in accsz:
				try:
					parse = soupz.find('strong',title='Likes')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soupz = None
			return(res)
		else:
			try:
				parse = soupz.find('strong',title='Likes')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
	def getavatar():
		global accsz
		global soupz
		res = []
		if soupz == None:
			for soupz in accsz:
				try:
					parse = soupz.find_all('img')
					stats = parse[-1].get('src')
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soupz = None
			return(res)
		else:
			try:
				parse = soupz.find_all('img')
				stats = parse[-1].get('src')
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')			

