from flask import Flask, request, jsonify, render_template, redirect, url_for
import json

app = Flask(__name__)

@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		data = request.form
		username=data['username']
		#if welcomeLogin(data['username']):
		str=username+'/'+'read'
		return redirect(url_for('read', user=username))
		#else:
		#print("Error")
		#return render_template('error.html')
	
@app.route("/features", methods=['GET'])
def features():
	if request.method == 'GET':
		return render_template('features.html')

@app.route("/advanced", methods=['GET'])
def advanced():
	if request.method == 'GET':
		return render_template('advanced.html')

@app.route("/statistics", methods=['GET'])
def statistics():
	if request.method == 'GET':
		return render_template('statistics.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('welcome.html')
	elif request.method == 'POST':
		data = request.form
		username = data['username']
		welcomeRegister(data['username'])
		return redirect(url_for('read', user=username))
		

#@app.route("/<user>/read", methods=['GET', 'POST'])
#def read(user):
#	if request.method == 'GET':
#		return render_template('read.html')
#	elif request.method == 'POST':
#		book_data, book_category = readNew(user, request.form['book_name'])
#		return render_template('readAns.html', user=user, book_data=book_data, book_category=book_category)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3800, debug=True, threaded=True)