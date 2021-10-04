import grequests
import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def rnk(username):
	try:
		url = 'https://www.codechef.com/users/{}'.format(username)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header_containers = soup.find_all('header')
		name = header_containers[1].find('h1', class_="h2-style").text
		try:
			rating = soup.find('div', class_='rating-number').text
		except AttributeError:
			return {'status': 200, 'message': 'Invalid username'}
		stars = soup.find('span', class_='rating')
		if stars:
			stars = stars.text
		highest_rating_container = soup.find('div', class_='rating-header')
		highest_rating = highest_rating_container.find_next('small').text.split()[-1].rstrip(')')
		rating_ranks_container = soup.find('div', class_='rating-ranks')
		rating_ranks = rating_ranks_container.find_all('a')
		global_rank = rating_ranks[0].strong.text
		country_rank = rating_ranks[1].strong.text

		try:
			global_rank = int(global_rank)
		except ValueError:
			global_rank = global_rank
		try:
			country_rank = int(country_rank)
		except ValueError:
			country_rank = country_rank	
		return {'status': 200, 'name': name, 'username': username,
				'rating': int(rating), 'stars': stars, 'highest_rating': int(highest_rating),
				'global_rank': global_rank, 'country_rank': country_rank}
	except:
		return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}




def cdg(username):
	try:
		url = 'https://www.codechef.com/users/{}'.format(username)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header_containers = soup.find_all('header')
		name = header_containers[1].find('h1', class_="h2-style").text
		rating_table = soup.find('table', class_='rating-table')
		rating_table_rows = rating_table.find_all('td')
		'''Can add ranking url to contests'''
		
		try:
			long_challenge = {'name': 'Long Challenge', 'rating': int(rating_table_rows[1].text),
							  'global_rank': int(rating_table_rows[2].a.hx.text),
							  'country_rank': int(rating_table_rows[3].a.hx.text)}

		except ValueError:
			long_challenge = {'name': 'Long Challenge', 'rating': int(rating_table_rows[1].text),
						  'global_rank': rating_table_rows[2].a.hx.text,
						  'country_rank': rating_table_rows[3].a.hx.text}

		try:
			cook_off = {'name': 'Cook-off',
						'rating': int(rating_table_rows[5].text),
						'global_rank': int(rating_table_rows[6].a.hx.text),
						'country_rank': int(rating_table_rows[7].a.hx.text)}
		except ValueError:
			cook_off = {'name': 'Cook-off',
						'rating': int(rating_table_rows[5].text),
						'global_rank': rating_table_rows[6].a.hx.text,
						'country_rank': rating_table_rows[7].a.hx.text}

		try:
			lunch_time = {'name': 'Lunch Time', 'rating': int(rating_table_rows[9].text),
						  'global_rank': int(rating_table_rows[10].a.hx.text),
						  'country_rank': int(rating_table_rows[11].a.hx.text)}

		except ValueError:
			lunch_time = {'name': 'Lunch Time', 'rating': int(rating_table_rows[9].text),
						  'global_rank': rating_table_rows[10].a.hx.text,
						  'country_rank': rating_table_rows[11].a.hx.text}

		return {'status': 200, 'name': name, 'username': username,'contests' : [long_challenge, cook_off, lunch_time]}
	except:
		return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}


def crdg(username):
	try:
		url = 'https://www.codechef.com/users/{}'.format(username)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header_containers = soup.find_all('header')
		name = header_containers[1].find('h1', class_="h2-style").text
		start_ind = page.text.find('[', page.text.find('all_rating'))
		end_ind = page.text.find(']', start_ind) + 1
		next_opening_brack = page.text.find('[', start_ind + 1)
		while next_opening_brack < end_ind:
			end_ind = page.text.find(']', end_ind + 1) + 1
			next_opening_brack = page.text.find('[', next_opening_brack + 1)
		
		all_rating = json.loads(page.text[start_ind: end_ind])
		for rating_contest in all_rating:
			rating_contest.pop('color')
		return {'status': 200, 'name': name, 'username': username,'contest_ratings' : all_rating}
	except:
		return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}


def psg(username):
	try:
		url = 'https://www.codechef.com/users/{}'.format(username)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header_containers = soup.find_all('header')
		name = header_containers[1].find('h1', class_="h2-style").text
		problem_solved_section = soup.find('section', class_='rating-data-section problems-solved')
		no_solved = problem_solved_section.find_all('h5')
		categories = problem_solved_section.find_all('article')
		fully_solved = {'count': int(re.findall(r'\d+', no_solved[0].text)[0])}

		if fully_solved['count'] != 0:
			for category in categories[0].find_all('p'):
				category_name = category.find('strong').text[:-1]
				fully_solved[category_name] = []

				for prob in category.find_all('a'):
					fully_solved[category_name].append({'name': prob.text,
														'link': 'https://www.codechef.com' + prob['href']})

		partially_solved = {'count': int(re.findall(r'\d+', no_solved[1].text)[0])}
		if partially_solved['count'] != 0:
			for category in categories[1].find_all('p'):
				category_name = category.find('strong').text[:-1]
				partially_solved[category_name] = []

				for prob in category.find_all('a'):
					partially_solved[category_name].append({'name': prob.text,
															'link': 'https://www.codechef.com' + prob['href']})

		return {'status': 200, 'name': name, 'username': username, 'fully_solved': fully_solved, 'partially_solved': partially_solved }
	except:
		return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}

		
def sg(username):
	url = 'https://www.codechef.com/users/{}'.format(username)
	#driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver" )
	driver = webdriver.Chrome()
	options = Options()
	#options.binary_location = "/app/.apt/usr/bin/google-chrome"
	options.add_argument('--headless') #background task; don't open a window
	options.add_argument('--disable-gpu')
	options.add_argument('--no-sandbox')#I copied this, so IDK?
	options.add_argument('--disable-dev-shm-usage')#this too
	driver.get(url)# set browser to use this page
	driver.implicitly_wait(10) # let the scripts load
	soup = driver.page_source #copy from chrome process to your python instance
	soup = BeautifulSoup(soup, "html.parser")
	driver.quit()
	header_containers = soup.find_all('header')
	name = header_containers[1].find('h1', class_="h2-style").text
	valdict = {}
	one = soup.find('g', class_='highcharts-label highcharts-data-label highcharts-data-label-color-0')
	vone = one.tspan.text.replace(one.tspan.tspan.text,'')
	sone = soup.find('g', class_='highcharts-legend-item highcharts-pie-series highcharts-color-0').text
	
	two = soup.find('g', class_='highcharts-label highcharts-data-label highcharts-data-label-color-1')
	vtwo = two.tspan.text.replace(two.tspan.tspan.text,'')
	stwo = soup.find('g', class_='highcharts-legend-item highcharts-pie-series highcharts-color-1').text

	thr = soup.find('g', class_='highcharts-label highcharts-data-label highcharts-data-label-color-2')
	vthr = thr.tspan.text.replace(thr.tspan.tspan.text,'')
	sthr = soup.find('g', class_='highcharts-legend-item highcharts-pie-series highcharts-color-2').text

	fou = soup.find('g', class_='highcharts-label highcharts-data-label highcharts-data-label-color-3')
	vfou = fou.tspan.text.replace(fou.tspan.tspan.text,'')
	sfou = soup.find('g', class_='highcharts-legend-item highcharts-pie-series highcharts-color-3').text
		
	fiv = soup.find('g', class_='highcharts-label highcharts-data-label highcharts-data-label-color-4')
	vfiv = fiv.tspan.text.replace(fiv.tspan.tspan.text,'')
	sfiv = soup.find('g', class_='highcharts-legend-item highcharts-pie-series highcharts-color-4').text
			
	six = soup.find('g', class_='highcharts-label highcharts-data-label highcharts-data-label-color-5')
	vsix = six.tspan.text.replace(six.tspan.tspan.text,'')
	ssix = soup.find('g', class_='highcharts-legend-item highcharts-pie-series highcharts-color-5').text
	
	if (sone.find('solutions_partially_accepted') != -1):
		sone = 'solutions_partially_accepted'
	if (stwo.find('solutions_partially_accepted') != -1):
		stwo = 'solutions_partially_accepted'
	if (sthr.find('solutions_partially_accepted') != -1):
		sthr = 'solutions_partially_accepted'
	if (sfou.find('solutions_partially_accepted') != -1):
		sfou = 'solutions_partially_accepted'
	if (sfiv.find('solutions_partially_accepted') != -1):
		sfiv = 'solutions_partially_accepted'
	if (ssix.find('solutions_partially_accepted') != -1):
		ssix = 'solutions_partially_accepted'
	valdict.update({sone: vone})
	valdict.update({stwo: vtwo})
	valdict.update({sthr: vthr})
	valdict.update({sfou: vfou})
	valdict.update({sfiv: vfiv})
	valdict.update({ssix: vsix})

	try:
		sub = {'AC': int(valdict["solutions_accepted"]), 'WA': int(valdict["wrong_answers"]), 'TLE': int(valdict["time_limit_exceeded"]), 'RTE': int(valdict["runtime_error"]), 'CE': int(valdict["compile_error"]), 'PAC': int(valdict["solutions_partially_accepted"])}
	except KeyError:
		sub = {'AC': int(valdict["solutions_accepted"]), 'WA': int(valdict["wrong_answers"]), 'TLE': int(valdict["time_limit_exceeded"]), 'RTE': int(valdict["runtime_error"]), 'CE': int(valdict["compile_error"])}
	try:
		return {'status': 200, 'name': name, 'username': username,'submissions' : sub}
	except:
		return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}
			
def rec(username):
	url = 'https://www.codechef.com/users/{}'.format(username)
	#driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver" )
	driver = webdriver.Chrome()
	options = Options()
	#options.binary_location = "/app/.apt/usr/bin/google-chrome"
	options.add_argument('--headless') #background task; don't open a window
	options.add_argument('--disable-gpu')
	options.add_argument('--no-sandbox')#I copied this, so IDK?
	options.add_argument('--disable-dev-shm-usage')#this too
	driver.get(url)# set browser to use this page
	driver.implicitly_wait(10) # let the scripts load
	soup = driver.page_source #copy from chrome process to your python instance
	soup = BeautifulSoup(soup, "html.parser")
	driver.quit()
	header_containers = soup.find_all('header')
	name = header_containers[1].find('h1', class_="h2-style").text
	rating_table = soup.find('table', class_='dataTable')
	rating_table_rows = rating_table.find_all('td')
	ret=[]
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
	try:
		return {'status': 200, 'name': name, 'username': username,'recent' : ret}
	except:
		return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}
