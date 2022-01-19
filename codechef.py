import random
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


async def upsolve(handle, limit=50, cat=1):
    async with aiohttp.ClientSession() as session:
        rurl = f'https://www.codechef.com/users/{handle}'
        async with session.get(rurl, headers=upsolveHeaders, allow_redirects=False) as page:
            if page.status == 200:
                page = await page.text()
                soup = BeautifulSoup(page, 'html.parser')
                problem_solved_section = soup.find(
                    'section', class_='rating-data-section problems-solved')
                no_solved = problem_solved_section.find_all('h5')
                categories = problem_solved_section.find_all('article')
                partially_solved = []
                count = int(re.findall(r'\d+', no_solved[cat].text)[0])
                if count != 0:
                    for category in categories[cat].find_all('p'):
                        for prob in category.find_all('a'):
                            if cat == 0:
                                partially_solved.append(prob.text)
                            else:
                                partially_solved.append(
                                    {'name': prob.text, 'url': f"https://www.codechef.com/problems/{prob.text}"})
                            if len(partially_solved) >= limit:
                                return {"response": partially_solved}
                return {"response": partially_solved}
            else:
                return {"comment": "Error Occured"}


async def stalk(handle, limit=120):
    async with aiohttp.ClientSession() as session:
        ret = []
        rlimit = limit/12 if limit % 12 == 0 else (limit/12) + 1
        for i in range(int(rlimit)):
            rurl = f'https://www.codechef.com/recent/user?page={i}&user_handle={handle}&_={int(time.time())}'
            async with session.get(rurl, headers=stalkHeaders) as page:
                if page.status == 200:
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
                            sid = sid.replace('/viewsolution/', '')
                        except:
                            sid = "1"
                        ret.append(
                            {'name': pc, 'time': timeper, 'result': res, 'language': lang, 'solution': sid,
                             'link': "https://www.codechef.com/viewsolution/"+sid})
                        if len(ret) >= limit:
                            break
                        a += 5
        return ({"response": ret})


async def gimme(handle, level):
    with open(f"data/{level.lower()}.json", 'r') as f:
        pdata = json.load(f)
    sdata = await upsolve(handle, 1000000, 0)
    solved = []
    try:
        for problem in sdata["response"]:
            solved.append(problem)
    except:
        pass
    recommend = []
    for problem in pdata:
        if problem["id"] not in solved:
            recommend.append(problem)
    chosen = random.choice(recommend)
    chosen["url"] = f"https://www.codechef.com/problems/{chosen['id']}"
    return ({"response": chosen})
