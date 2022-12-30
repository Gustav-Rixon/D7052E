from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
import uuid
import json
import jwt
import os

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:5000/*'])

# Load the environment variables from the .env file
load_dotenv()

# Access the environment variables using the os.getenv function
secret_key = os.getenv('SECRET_KEY')
print(secret_key)


"""
/whitelist
Returns the part of the contents within whitelist.json
email: string
owner: bool
admin: bool
"""
@app.route('/whitelist')
def get_whitelist():
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    filtered_whitelist = []
    for item in whitelist['Whitelist']:
        filtered_item = {
            'email': item['email'],
            'owner': item['owner'],
            'admin': item['admin']
        }
        filtered_whitelist.append(filtered_item)

    return jsonify(filtered_whitelist)


""" 
/whitelist/add
Adds a user
a Owner can add another owner and add new admins & new users.
A Admin can add new users
A user cannot add new people.
"""
@app.route('/whitelist/add', methods=['POST'])
def add_user_to_whitelist():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the new user data from the request body
    data = request.get_json()
    new_user = data[0]
    current_user = data[1]

    # Add a UUID to the new_user variable
    new_user['uuid'] = str(uuid.uuid4())

    # Add the jwt variable to the new_user dictionary
    new_user['jwt'] = ""

    # Check if the current user is in the Whitelist array
    current_user_found = False
    for user in whitelist['Whitelist']:
        if user['email'] == current_user['email']:
            current_user_found = True
            break
    if not current_user_found:
        return 'Current user not found', 404

    # Check if the new user is already in the Whitelist array
    for user in whitelist['Whitelist']:
        if user['email'] == new_user['email']:
            return 'Email already exists', 400

    if new_user['owner']:
        if current_user['owner']:
            pass  # Owners can add other owners
        else:
            return 'Invalid Permissions', 400
    if new_user['admin']:
        if current_user['owner'] or current_user['admin']:
            pass  # Owners and admins can add new admins
        else:
            return 'Invalid Permissions', 400

    # Add the new user to the Whitelist array
    whitelist['Whitelist'].append(new_user)

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)

    return 'Success'



@app.route('/whitelist/remove', methods=['POST'])
def remove_user_from_whitelist():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the email of the user to be removed and the current user's email from the request body
    data = request.get_json()
    email = data['email']
    current_user_email = data['current_user_email']
    current_user_role = data['current_user_role']

    # Find the index of the user to be removed
    index = -1
    for i, user in enumerate(whitelist['Whitelist']):
        if user['email'] == email:
            index = i
            break

    # Check if the user was found and if the current user has sufficient permissions
    if index == -1:
        return 'User not found', 404
    elif current_user_email == email:
        return 'Cannot remove self', 403
    elif current_user_role == 'owner':
        pass  # Owners can remove any user
    elif current_user_role == 'admin' and not user['admin']:
        pass  # Admins can remove non-admins
    else:
        return 'Insufficient permissions', 403

    # Remove the user from the Whitelist array
    whitelist['Whitelist'].pop(index)

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)
    return 'Success'


@app.route('/whitelist/promote', methods=['POST'])
def promote_user_to_admin():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the email of the user to be promoted and the current user's role from the request body
    data = request.get_json()
    email = data['email']
    current_user_role = data['current_user_role']

    # Find the index of the user to be promoted
    index = -1
    for i, user in enumerate(whitelist['Whitelist']):
        if user['email'] == email:
            index = i
            break

    # Check if the user was found and if the current user has sufficient permissions
    if index == -1:
        return 'User not found', 404
    elif current_user_role != 'owner':
        return 'Insufficient permissions', 403

    # Promote the user to an admin
    whitelist['Whitelist'][index]['admin'] = True

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)

    return 'Success'


@app.route('/whitelist/demote', methods=['POST'])
def demote_admin_to_user():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the email of the admin to be demoted and the current user's role from the request body
    data = request.get_json()
    email = data['email']
    current_user_role = data['current_user_role']

    # Find the index of the admin to be demoted
    index = -1
    for i, user in enumerate(whitelist['Whitelist']):
        if user['email'] == email:
            index = i
            break

    # Check if the admin was found and if the current user has sufficient permissions
    if index == -1:
        return 'User not found', 404
    elif current_user_role != 'owner':
        return 'Insufficient permissions', 403
    elif not user['admin']:
        return 'User is not an admin', 400

    # Demote the admin to a regular user
    whitelist['Whitelist'][index]['admin'] = False

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)

    return 'Success'


@app.route('/test/edit_json', methods=['POST'])
def edit_json():

    # Get the Request Value
    jwt_token = request.form['jwt']

    try:
        # Decode and verify the JWT using the secret key
        decoded_token = jwt.decode(jwt_token, secret_key, verify=True)
    except jwt.exceptions.DecodeError:
        # The JWT is invalid
        print("The JWT is invalid")
    except jwt.exceptions.ExpiredSignatureError:
        # The JWT has expired
        print("The JWT has expired")
    else:
        # The JWT is valid
        print("The JWT is valid")

    # The decoded token is a dictionary containing the claims of the JWT
    print(decoded_token)

    # Read the requested data
    data = request.get_json()

    # Load the JSON file
    with open('whitelist.json', 'r') as f:
        for item in f:
            if (item['email']) == decoded_token.email:
                return
            if (item['jwt']) == jwt_token:
                return
            if item['owner'] == True:
                return
            if item['admin'] == True:
                return
        json_data = json.load(f)

    # Modify the JSON data
    json_data['key'] = data['new_value']

    # Sending modified data back to the frontend
    with open('whitelist.json', 'w') as f:
        json.dump(json_data, f)

    return 'Json file successfully edited!'


if __name__ == '__main__':
    app.run()
