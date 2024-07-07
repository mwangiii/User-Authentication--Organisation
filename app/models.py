from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)



class Organisation(db.Model):
    __tablename__ = 'organisations'
    orgid = db.Column(db.String, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class UserOrganisation(db.Model):
    __tablename__ = 'userorganisation'
    userid = db.Column(db.String, db.ForeignKey('users.userid'), primary_key=True)
    orgid = db.Column(db.String, db.ForeignKey('organisations.orgid'), primary_key=True)

# def get_organizations():
#     try:
#         # Query all organizations from the database
#         organizations = Organization.query.all()

#         # Convert organizations to JSON format
#         organizations_list = []
#         for org in organizations:
#             organizations_list.append({
#                 'id': org.id,
#                 'name': org.name,
#                 'description': org.description,
#                 # Add more fields as needed
#             })

#         # Return JSON response with organizations data
#         return jsonify(organizations_list), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500