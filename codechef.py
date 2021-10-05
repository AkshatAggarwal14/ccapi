import aiohttp
import asyncio
import random
import json
import time
from bs4 import BeautifulSoup
import re


upsolveHeaders = {
    "Host": "www.codechef.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "|",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}

stalkHeaders = {
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


async def upsolve(handle, limit=50):
    async with aiohttp.ClientSession() as session:
        rurl = f'https://www.codechef.com/users/{handle}'
        async with session.get(rurl, headers=upsolveHeaders) as page:
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            problem_solved_section = soup.find(
                'section', class_='rating-data-section problems-solved')
            try:
                no_solved = problem_solved_section.find_all('h5')
            except:
                return {"response": "Handle not found!"}
            categories = problem_solved_section.find_all('article')
            partially_solved = []
            count = int(re.findall(r'\d+', no_solved[1].text)[0])
            if count != 0:
                for category in categories[1].find_all('p'):
                    if len(partially_solved) >= limit:
                        break
                    # category_name = category.find('strong').text[:-1]
                    for prob in category.find_all('a'):
                        if len(partially_solved) >= limit:
                            break
                        url = prob['href']
                        urlParts = url[1:].split('/')
                        if urlParts[0] == 'status':
                            url = urlParts[1]
                        else:
                            url = urlParts[2]
                        url = 'https://www.codechef.com/' + \
                            url.split(',', 1)[0]
                        partially_solved.append(
                            {'name': prob.text, 'url': url})
            return {"response": partially_solved}


async def stalk(handle, pageLimit, respLimit):
    async with aiohttp.ClientSession() as session:
        ret = []
        for i in range(pageLimit):
            rurl = f'https://www.codechef.com/recent/user?page={i}&user_handle={handle}&_={int(time.time())}'
            async with session.get(rurl, headers=stalkHeaders) as page:
                page = await page.json(content_type=None)
                page = BeautifulSoup(page["content"], 'html.parser')
                rating_table_rows = page.find_all('td')
                a = 0
                for _ in range(int(len(rating_table_rows)/5)):
                    if(len(ret) >= respLimit):
                        return ({"response": ret})
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
                        sid = sid.replace('/viewsolution/', '')
                    except:
                        sid = "1"
                    ret.append({'name': pc, 'time': timeper,
                               'result': res, 'language': lang, 'solution': sid})
                    a += 5
        return ({"response": ret})
