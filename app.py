from flask import Flask, request, Blueprint, request
from flask_mysqldb import MySQL
from flask import jsonify

# from routes import *
import yaml
import MySQLdb
import collections
import json
app = Flask(__name__)


# from routes import doctors
# import routes.doctors.py


# from routes import routes as review_blueprint

# app.register_blueprint(doctor_routes, url_prefix="/doctors")
# app.register_blueprint(review_routes, url_prefix="/reviews")


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/doctors")

def users():
	if request.method == 'GET': 
	    cur = mysql.connection.cursor()
	    cur.execute('''SELECT * FROM doctor''')
	    doctors = cur.fetchall()

	    # Create our JSON here
	    items = [];
	    for row in doctors:
	    	items.append({'id': row[0], 'name': row[1]})

	    return jsonify(items)

	

@app.route("/doctors/", methods = ['GET', 'POST', 'PATCH', 'DELETE'])

def getAllDoctors():
	#GET

	if request.method == 'GET': 
	    cur = mysql.connection.cursor()
	    cur.execute('''SELECT * FROM doctor''')
	    doctors = cur.fetchall()

	    cur.execute('''SELECT * FROM review''')
	    reviews = cur.fetchall();

	    # Create our JSON here
	    items = [];
	    for row in doctors:
	    	rev = []		
	    	items.append({'id': row[0], 'name': row[1]})
	    	for rowReview in reviews:
	    		if rowReview[2] == row[0]:
	    			rev.append({'id': rowReview[0], 'doctor_id': rowReview[2], 'description': rowReview[1]})
	    	items.append({'reviews': rev})
	    return jsonify(items)

	#POST

	if request.method == 'POST':
		doctor_data = request.get_json(force=True) 
		cur = mysql.connection.cursor()	
		name = doctor_data["doctor"]["name"]
		cur.execute('''INSERT INTO doctor (name) VALUES (%s)''', (name,))
		mysql.connection.commit()
		returnStatement = "ADDED DOCTOR: " + name + "\n"
		return returnStatement


@app.route("/doctors/<id>/", methods = ['GET', 'POST', 'PATCH', 'DELETE'] )
def getDoctorByID(id):
	
	if request.method == 'GET': 
	   cur = mysql.connection.cursor()
	   cur.execute('''SELECT * FROM doctor WHERE id = %s''', id)
	   doctor = cur.fetchall()

	   cur.execute('''SELECT * FROM review WHERE doctor_id = %s''', id)
	   reviews = cur.fetchall();
	   reviewList = []
	   doctorData = []

	   for row in reviews :
	   		d = collections.OrderedDict()
	   		d['id']          = row[0]
	   		d['description'] = row[1]
	   		d['doctor_id']   = row[2]

	   		reviewList.append(d)
	
	   doctorData.append({'name': doctor[0][1], 'id': doctor[0][0], 'review': reviewList})
	   
	   print (doctorData)
	   
	   return jsonify(doctorData)
		

	if request.method == 'DELETE':
	   cur = mysql.connection.cursor() 
	   cur.execute('''DELETE FROM review WHERE doctor_id = %s''', id)
	   cur.execute('''DELETE FROM doctor WHERE id = %s''', id)
	   mysql.connection.commit()

	   return "DELETED\n"
   

@app.route("/doctors/<id>/reviews/", methods = ['GET', 'POST', 'PATCH', 'DELETE'] )
def addReview(id):
	if request.method == 'POST':
		review_data = request.get_json(force=True) 
		cur = mysql.connection.cursor()	
		review = review_data["review"]["description"]
		cur.execute('''INSERT INTO review (review, doctor_id) VALUES (%s, %s)''', (review, id))
		mysql.connection.commit()
		returnStatement = "ADDED Review: " + review + " to Doctor of id: " + id + "\n"
		return returnStatement
	return "No valid request"
	
@app.route("/reviews/")

def getAllReviews():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM doctor''')
    doctors = cur.fetchall()

    cur.execute('''SELECT * FROM review''')
    reviews = cur.fetchall();
    print(reviews)

    # Create our JSON here
    items = [];
    for rowReviews in reviews:
    	rev = []		
    	items.append({'review': rowReviews[1], 'id': rowReviews[0], 'doctor_id': rowReviews[2]})
    	for row in doctors:
    		if row[0] == rowReviews[2]:
    			rev.append({'name': row[1], 'id': row[0]})
    	items.append({'doctor': rev})
    return jsonify(items)




@app.route("/doctors/<id>/reviews/<review_id>/", methods = ['GET', 'POST', 'PATCH', 'DELETE'] )
def getReviewByDoctorID(id, review_id):
	
	if request.method == 'GET':
		print ("review")
		cur = mysql.connection.cursor()
		cur.execute('''SELECT doctor.id, doctor.name, review.id, review.review, review.doctor_id FROM doctor INNER JOIN review on review.doctor_id = doctor.id where review.id = %s and doctor.id = %s''', (review_id, id))
		data = cur.fetchall();
		print(data)
		user_list = []
		doctor = []
		if(len(data) != 0):
			for row in data :
				d = collections.OrderedDict()
				d['id']  			= row[0]
				d['name']   		= row[1]
				
				doctor.append(d)
			user_list.append({'description': data[0][3], 'id': data[0][2], 'doctor': doctor})
			user_list = user_list[0]

		return jsonify(user_list)

	if request.method == 'DELETE':
	   cur = mysql.connection.cursor() 
	   cur.execute('''DELETE FROM review WHERE doctor_id = %s and id = %s''', (id, review_id))
	   mysql.connection.commit()

	   return "DELETED\n"
   



@app.route("/reviews/<id>/", methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def getReviewByID(id):
	
	if request.method == 'GET':
		cur = mysql.connection.cursor()

		cur.execute('''SELECT doctor.id, doctor.name, review.id, review.review, review.doctor_id FROM review INNER JOIN doctor on review.doctor_id = doctor.id where review.id = %s''', id)
		data = cur.fetchall();

		user_list = []
		doctor = []
		if(len(data) != 0):
			for row in data :
				d = collections.OrderedDict()
				d['id']  			= row[0]
				d['name']   		= row[1]
				
				doctor.append(d)
			user_list.append({'description': data[0][3], 'id': data[0][2], 'doctor': doctor})
			print (user_list[0])
			user_list = user_list[0]

		return jsonify(user_list)

	if request.method == 'DELETE':
	   cur = mysql.connection.cursor()
	   
	   cur.execute('''DELETE FROM review WHERE id = %s''', id)
	   mysql.connection.commit()

	   return "DELETED\n"

if __name__ == "__main__":
    app.run(debug=True)

