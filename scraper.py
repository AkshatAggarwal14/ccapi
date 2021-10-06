import json
import aiohttp
from bs4 import BeautifulSoup
import asyncio

Headers = {
    "Host": "www.codechef.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}


async def scrape():
    levels = ["school", "easy", "medium", "hard"]
    for level in levels:
        problems = []
        async with aiohttp.ClientSession() as session:
            rurl = f"https://www.codechef.com/problems/{level}"
            async with session.get(rurl, headers=Headers) as page:
                try:
                    page = await page.text()
                    soup = BeautifulSoup(page, 'html.parser')
                    rating_table = soup.find('table', class_='dataTable')
                    rating_table_rows = rating_table.find_all('td')
                    b = 0
                    for _ in range(int(int(len(rating_table_rows))/4)):
                        a = str(rating_table_rows[b].text)
                        a = a.strip()
                        a = a.strip('\n')
                        problems.append(
                            {'name': a, 'id': rating_table_rows[b + 1].text, 'submissions': rating_table_rows[b + 2].text, 'accuracy': rating_table_rows[b + 3].text})
                        b += 4
                except:
                    pass
                with open(f"data/{level}.json", 'w') as f:
                    json.dump(problems, f)
