import aiohttp
import asyncio
import random
import json
import time
from bs4 import BeautifulSoup
import re
async def recent(handle ,limit = 5):
	async with aiohttp.ClientSession() as session:
		#https://www.codechef.com/recent/user?page=undefined&user_handle=mathecodician&_=1633377494809
		headers = {
			"Host": "www.codechef.com",
			"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br",
			"X-Requested-With": "XMLHttpRequest",
			"DNT": "1",
			"Connection": "keep-alive",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Pragma": "no-cache",
			"Cache-Control": "no-cache",
			"TE": "trailers"
			}
		ret=[]
		for i in range(limit):
			rurl = 'https://www.codechef.com/recent/user?page={}&user_handle={}&_={}'.format(i,handle,int(time.time()))
			async with session.get(rurl, headers=headers) as page:
				page = await page.json(content_type=None)
				page = BeautifulSoup(page["content"], 'html.parser')
				rating_table_rows = page.find_all('td')
				
				a = 0
				for _ in range(int(len(rating_table_rows)/5)):
					timesp = rating_table_rows[a].text.split()
					timeper = ' '.join(timesp)
					pc = str(rating_table_rows[a+1].text)
					if str(rating_table_rows[a+2].span['title']) == '':
						res = str(rating_table_rows[a+2].span.text)
					else:
						res = str(rating_table_rows[a+2].span['title'])
					lang = str(rating_table_rows[a+3].text)
					try:
						sid = str(rating_table_rows[a+4].a['href'])
						sid = sid.replace('/viewsolution/','')
					except:
						sid = "1"
					ret.append({'name' : pc, 'time' : timeper, 'result' : res, 'language' : lang, 'solution': sid})
					a = a + 5
		return ({"response" : ret})
#asyncio.run(recent("mathecodician",10))
