from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

class Pessoa(db.Model):
	__tablename__	= 'pessoa'
	_id				= db.Column(db.Integer, primary_key=True, autoincrement=True)
	name			= db.Column(db.String(100))
	email			= db.Column(db.String(100))
	birthDate		= db.Column(db.String(10))

	def __init__(self, name, email, birthDate):
		self.name		= name
		self.email		= email
		self.birthDate	= birthDate
	
	def json(self):
		return ({
			'id':			self._id,
			'name':			self.name,
			'email':		self.email,
			'birthDate':	self.birthDate
		})

with app.app_context():
	db.create_all()


@app.route('/pessoa', methods=['POST'])
def createNew():
	requestJson	= request.get_json()

	if requestJson['name'] and requestJson['email'] and requestJson['birthDate']:
		newPerson = Pessoa(
			requestJson['name'], 
			requestJson['email'],
			requestJson['birthDate'])

		db.session.add(newPerson)
		db.session.commit()

	return readAll()


@app.route('/pessoa/<int:id>', methods=['GET'])
def readById(id):
	try:
		personQuery	= Pessoa.query.filter_by(_id=id).first()
		return (jsonify(personQuery.json()))
	except:
		return(jsonify([]))


@app.route('/pessoa/<int:id>', methods=['PUT'])
def updateById(id):
	personQuery	= Pessoa.query.filter_by(_id=id).first()
	requestJson	= request.get_json()

	if requestJson['name'] and requestJson['email'] and requestJson['birthDate']:
		personQuery.name		= requestJson['name']
		personQuery.email		= requestJson['email']
		personQuery.birthDate	= requestJson['birthDate']
		db.session.commit()

	return (readAll())


@app.route('/pessoa/<int:id>', methods=['DELETE'])
def deleteById(id):
	try:
		personQuery	= Pessoa.query.filter_by(_id=id).first()
		db.session.delete(personQuery)
		db.session.commit()
	except:
		return readAll()

	return readAll()


@app.route('/pessoas', methods=['GET'])
def readAll():
	personQuery	= Pessoa.query.all()
	personJson	= []

	for person in personQuery:
		personJson.append(person.json())

	return (jsonify(personJson))


if __name__ == "__main__":
	app.run(port=5000, host="localhost")
