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


"""
/whitelist/remove
Remove a user
A Owner can remove admins & users
A Admin can remove users
A user Cannot remove people
"""
@app.route('/whitelist/remove', methods=['POST'])
def remove_user_from_whitelist():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the email of the user to be removed and the current user's email from the request body
    data = request.get_json()
    remove_user = data[0]
    current_user = data[1]

    # Get the role of the current user
    current_user_role = None
    for user in whitelist['Whitelist']:
        if user['email'] == current_user['email']:
            if user['owner']:
                current_user_role = 'owner'
                break
            elif user['admin']:
                current_user_role = 'admin'
                break
            break

    remove_user_role = None
    for user in whitelist['Whitelist']:
        if user['email'] == remove_user['email']:
            if user['owner']:
                remove_user_role = 'owner'
                break
            elif user['admin']:
                remove_user_role = 'admin'
                break
            break

    if current_user_role == 'owner' and remove_user_role not in ['owner']:
        pass  # Owners can't remove any user
    if current_user_role == 'admin' and remove_user_role not in ['owner', 'admin']:
        pass  # Admins can remove non-admins
    else:
        return 'Insufficient permissions', 403

    # Find the index of the user to be removed
    index = -1
    for i, user in enumerate(whitelist['Whitelist']):
        if user['email'] == remove_user['email']:
            index = i
            break

    # Check if the user was found
    if index == -1:
        return 'User not found', 404

    # Check if the user is trying to remove themselves
    if remove_user['email'] == current_user['email']:
        return 'Cannot remove self', 403

    # Remove the user from the Whitelist array
    whitelist['Whitelist'].pop(index)

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)
    return 'Success'

"""
/get_jwt
Returns the jwt based on email
"""
@app.route('/get_jwt', methods=['POST'])
def get_jwt():
    # Get the email of the user from the request payload
    email = request.json['email']

    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Look up the user in the whitelist
    user = None
    for users in whitelist['Whitelist']:
        if users['email'] == email:
            user = users
            break

    # If the user was not found in the whitelist, return an error
    if not user:
        return jsonify({'error': 'User not found in whitelist'}), 404

    # Return the JWT for the user to the client
    return jsonify({'jwt': user['jwt']})


"""
/set_jwt
sets the jwt value for the user
"""
@app.route('/set_jwt', methods=['POST'])
def set_jwt():
    # Get the {jwt: jwt_web,email: email} of the user from the request payload
    data = request.get_json()

    jwt_web = data['jwt']
    email = data['email']

    print(jwt_web)
    print(email)

    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Look up the user in the whitelist
    user = None
    for users in whitelist['Whitelist']:
        if users['email'] == email:
            user = users
            break

    # If the user was not found in the whitelist, return an error
    if not user:
        return jsonify({'error': 'User not found in whitelist'}), 404

    # Change the jwt value for the user
    user['jwt'] = jwt_web

    # Save the updated whitelist to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)

    # Return 'Success'
    return 'Success'



if __name__ == '__main__':
    app.run()
