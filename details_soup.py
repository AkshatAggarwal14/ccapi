import json
import re
# DO NOT import this after requests
import grequests
import requests
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

class UsernameError(Exception):
	pass

class UserData:
	def __init__(self, username=None):
		self.__username = username

	def update_username(self, username):
		self.__username = username

	def __codechef(self):
		url = 'https://www.codechef.com/users/{}'.format(self.__username)
		driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver" )
		options = Options()
		options.binary_location = "/app/.apt/usr/bin/google-chrome"
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		driver.get(url)
		driver.implicitly_wait(10)
		soup = driver.page_source
		soup = BeautifulSoup(soup, "html.parser")
		page = requests.get(url)
		driver.quit()
		try:
			rating = soup.find('div', class_='rating-number').text
		except AttributeError:
			raise UsernameError('User not Found')

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
			
		def contests_details_get():
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

			return [long_challenge, cook_off, lunch_time]

		def contest_rating_details_get():
			start_ind = page.text.find('[', page.text.find('all_rating'))
			end_ind = page.text.find(']', start_ind) + 1

			next_opening_brack = page.text.find('[', start_ind + 1)
			while next_opening_brack < end_ind:
				end_ind = page.text.find(']', end_ind + 1) + 1
				next_opening_brack = page.text.find('[', next_opening_brack + 1)

			all_rating = json.loads(page.text[start_ind: end_ind])
			for rating_contest in all_rating:
				rating_contest.pop('color')

			return all_rating

		def problems_solved_get():
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

			return fully_solved, partially_solved

		def user_details_get():
			header_containers = soup.find_all('header')
			name = header_containers[1].find('h1', class_="h2-style").text

			return {'name': name, 'username': self.__username}
			
		def submission_get():
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
				return {'AC': int(valdict["solutions_accepted"]), 'WA': int(valdict["wrong_answers"]), 'TLE': int(valdict["time_limit_exceeded"]), 'RTE': int(valdict["runtime_error"]), 'CE': int(valdict["compile_error"]), 'PAC': int(valdict["solutions_partially_accepted"])}
			except KeyError:
				return {'AC': int(valdict["solutions_accepted"]), 'WA': int(valdict["wrong_answers"]), 'TLE': int(valdict["time_limit_exceeded"]), 'RTE': int(valdict["runtime_error"]), 'CE': int(valdict["compile_error"])}
			
		def recent():
			rating_table = soup.find('table', class_='dataTable')
			rating_table_rows = rating_table.find_all('td')
			ret=[]
			a = 0
			for i in range(int(len(rating_table_rows)/5)):
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
			return ret

		full, partial = problems_solved_get()

		try:
			details = {'status': 200, 'rating': int(rating), 'stars': stars, 'highest_rating': int(highest_rating),
				   'global_rank': global_rank, 'country_rank': country_rank,
				   'user_details': user_details_get(), 'submissions': submission_get(), 'recent': recent(), 'contests': contests_details_get(),
				   'contest_ratings': contest_rating_details_get(), 'fully_solved': full, 'partially_solved': partial}
		except Exception as e:
			return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}
		
		return details
		
	def get_details(self):
		return self.__codechef()
		
