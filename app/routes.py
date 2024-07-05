"""This file contains routes for the project"""


from flask import Flask

app = FLask(__name__)



@app.route("/")
def home_page():
  return "Welcome!"

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()

@app.route("/auth")
def user_authentication():
  return "<div></div>"

@app.route("/api")
def user_authentication():
  return "<div></div>"

# Registers a users and creates a default organisation Register request body
@app.route("/auth/register", methods=['POST'])
def register_user():
  response_successful = {
    {
    "status": "success",
    "message": "Registration successful",
    "data": {
      "accessToken": "eyJh...",
      "user": {
	      "userId": "string",
	      "firstName": "string",
				"lastName": "string",
				"email": "string",
				"phone": "string",
      }
    }
}
  } 

  response_unsuccessful = {
    "status": "Bad request",
    "message": "Registration unsuccessful",
    "statusCode": 400
}

  return 

# logs in a user. When you log in, you can select an organisation to interact with
@app.route("/auth/login", methods=['POST'])
def login_user():
  response_successful = {
    {
    "status": "success",
    "message": "Login successful",
    "data": {
      "accessToken": "eyJh...",
      "user": {
	      "userId": "string",
	      "firstName": "string",
				"lastName": "string",
				"email": "string",
				"phone": "string",
      }
    }
}
  }

  response_unsuccessful = {
    "status": "Bad request",
    "message": "Authentication failed",
    "statusCode": 401
}

  return 

# a user gets their own record or user record in organisations they belong to or created [PROTECTED].
@app.route("/api/users/:id", methods=['GET'])
def get_users_by_id():
  response_successful = {
		"status": "success",
    "message": "<message>",
    "data": {
      "userId": "string",
      "firstName": "string",
			"lastName": "string",
			"email": "string",
			"phone": "string"
    }
}
  return 

# gets all your organisations the user belongs to or created. 
# If a user is logged in properly, they can get all their organisations.
#  They should not get another user’s organisation [PROTECTED].
@app.route("/api/organizations", methods=['GET'])
def get_organization():
  response_successful = {
    "status": "success",
		"message": "<message>",
    "data": {
      "organisations": [
	      {
		      "orgId": "string",
					"name": "string",
					"description": "string",
	      }
      ]
    }
}

  return 

# the logged in user gets a single organisation record [PROTECTED]
@app.route("/api/organizations/:orgId", methods=['GET'])
def get_organization_by_id():
  response_successful = {
    "status": "success",
		"message": "<message>",
    "data": {
			"orgId": "string", 
			"name": "string",
			"description": "string",
	}
}
  return 

# a user can create their new organisation [PROTECTED].
@app.route("/api/organizations:", methods=['POST'])
def get_organizations():
  return 

# adds a user to a particular organisation
@app.route("/api/organizations/:orgId/users", methods=['POST'])
def get_organization():
  return 

"""
# Endpoint to create an organization
@app.route('/create_organization', methods=['POST'])
def create_organization():
    # Assuming you get the organization data from the request
    org_data = request.get_json()
    
    # Validate and process org_data as needed
    
    # Example response for successful creation
    response_data = {
        "status": "success",
        "message": "Organization created successfully",
        "data": {
            "orgId": "string", 
            "name": "string", 
            "description": "string"
        }
    }
    
    return jsonify(response_data), 201
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
