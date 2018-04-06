from flask import Flask, request, Blueprint
from flask_mysqldb import MySQL
from flask import jsonify

# from routes import *
import yaml
import queries
import MySQLdb
import collections
import json
app = Flask(__name__)


# from routes import doctors
# import routes.doctors.py

from doctors import doctor_routes
from reviews import review_routes
# from routes import routes as review_blueprint

# app.register_blueprint(doctor_routes, url_prefix="/doctors")
# app.register_blueprint(review_routes, url_prefix="/reviews")


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


# app.register_blueprint(routes)

@app.route("/doctors")

def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM doctor''')
    rv = cur.fetchall()

    # Create our JSON here
    items = [];
    for row in rv:
    	items.append({'id': row[0], 'name': row[1]})

    return jsonify(items)

@app.route("/doctors/")

def getAll():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM doctor''')
    rv = cur.fetchall()

    cur.execute('''SELECT * FROM review''')
    reviews = cur.fetchall();

    # Create our JSON here
    items = [];
    for row in rv:
    	rev = []		
    	items.append({'id': row[0], 'name': row[1]})
    	for rowReview in reviews:
    		if rowReview[2] == row[0]:
    			rev.append({'id': rowReview[0], 'doctor_id': rowReview[2], 'description': rowReview[1]})
    	items.append({'reviews': rev})
    return jsonify(items)


@app.route("/doctors/<id>/")
def getDoctorByID(id):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT doctor.id, doctor.name, review.id, review.review, review.doctor_id FROM doctor INNER JOIN review on review.doctor_id = doctor.id where doctor.id = %s''', id)
	data = cur.fetchall();
	print(data)
	user_list = []
	reviews = []
	if(len(data) != 0):
		for row in data :
			d = collections.OrderedDict()
			d['id']  			= row[2]
			d['description']   	= row[3]
			d['doctor_id']  	= row[4]
			reviews.append(d)
		user_list.append({'id': data[0][0], 'name': data[0][1], 'reviews': reviews})
		user_list = user_list[0]

	return jsonify(user_list)
   



if __name__ == "__main__":
    app.run(debug=True)

