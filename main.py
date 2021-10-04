from flask import Flask, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
from details_soup import UserData, UsernameError
import grequests
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import approute as ap
import os
import json

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

def check(handle):
	url = "https://www.codechef.com/users/" + handle
	r = requests.head(url)
	sc = r.status_code
	return (sc == 200)

def problemscrape(level):
	url = 'https://www.codechef.com/problems/' + level
	eas = []
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	rating_table = soup.find('table', class_='dataTable')
	rating_table_rows = rating_table.find_all('td')
	b = 0
	for _ in range(int(int(len(rating_table_rows))/4)):
		a = str(rating_table_rows[b].text)
		a = a.strip()
		a = a.strip('\n')
		eas.append({'name' : a, 'id' : rating_table_rows[b + 1].text, 'submissions' : rating_table_rows[b + 2].text, 'accuracy' : rating_table_rows[b + 3].text})
		b += 4
	return eas

@app.route("/")
def home():
	return render_template('home.html')
@app.route("/rating", methods=['GET'])
def getrnk():
	if 'handle' in request.args:
		handle = (request.args['handle'])
	else:
		return {'status': 200, 'message': 'Username missing'}
	if check(handle):
		return ap.rnk(handle)
	else:
		return {'status': 200, 'message': 'Invalid Username'}

@app.route("/contest", methods=['GET'])
def getcdg():
	if 'handle' in request.args:
		handle = (request.args['handle'])
	else:
		return {'status': 200, 'message': 'Username missing'}
	if check(handle):
		return ap.cdg(handle)
	else:
		return {'status': 200, 'message': 'Invalid Username'}
	

@app.route("/ranking", methods=['GET'])
def getcrdg():
	if 'handle' in request.args:
		handle = (request.args['handle'])
	else:
		return {'status': 200, 'message': 'Username missing'}

	if check(handle):
		return ap.crdg(handle)
	else:
		return {'status': 200, 'message': 'Invalid Username'}
	

@app.route("/problem", methods=['GET'])
def getpsg():
	if 'handle' in request.args:
		handle = (request.args['handle'])
	else:
		return {'status': 200, 'message': 'Username missing'}
	if check(handle):
		return ap.psg(handle)
	else:
		return {'status': 200, 'message': 'Invalid Username'}


@app.route("/recent", methods=['GET'])
def getrec():
	if 'handle' in request.args:
		handle = (request.args['handle'])
	else:
		return {'status': 200, 'message': 'Username missing'}
	if check(handle):
		return ap.rec(handle)
	else:
		return {'status': 200, 'message': 'Invalid Username'}


@app.route("/submission", methods=['GET'])
def getsg():
	if 'handle' in request.args:
		handle = (request.args['handle'])
	else:
		return {'status': 200, 'message': 'Username missing'}
	if check(handle):
		return ap.sg(handle)
	else:
		return {'status': 200, 'message': 'Invalid Username'}

@app.route("/problemset")
def pscrape():
	try:
		if os.path.getsize("problemset.json") > 1:
			with open('problemset.json', 'r', encoding='utf-8') as f:
				jdata = json.load(f)
			return jdata
		else:
			problems = {'status' : 200, 'school': problemscrape("school"), 'easy': problemscrape("easy"), 'medium': problemscrape("medium"), 'hard': problemscrape("hard"), 'challenge': problemscrape("challenge"), 'extcontest': problemscrape("extcontest")}
			with open('problemset.json', 'w', encoding='utf-8') as f:
				json.dump(problems, f, ensure_ascii=False, indent=4)
			return problems
	except:
		problems = {'status' : 200, 'school': problemscrape("school"), 'easy': problemscrape("easy"), 'medium': problemscrape("medium"), 'hard': problemscrape("hard"), 'challenge': problemscrape("challenge"), 'extcontest': problemscrape("extcontest")}
		with open('problemset.json', 'w', encoding='utf-8') as f:
			json.dump(problems, f, ensure_ascii=False, indent=4)
		return problems


class Details(Resource):
	def get(self, username):

		user_data = UserData(username)

		try:
			return user_data.get_details()
		except UsernameError:
			return {'status': 200, 'message': 'Invalid username'}


api.add_resource(Details,'/all/<string:username>')

@app.errorhandler(404)
def invalid_route(e):
	return {'status': 404, 'message': 'Not Found'}
@app.errorhandler(500)
def internal_error(e):
	return {"status": 500, "message": "Internal Server Error. Administrator Has Been Informed. Please Try Back Later"}

if __name__ == '__main__':
	app.run()
