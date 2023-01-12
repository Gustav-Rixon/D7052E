from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
import uuid
import json
import jwt
import os
import sys
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
# now we can import the module in the parent
# directory.
import tools




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
    new_user = {
        "email": data['target_user_email'],
        "owner": data['owner_web'],
        "admin": data['admin_web'],
        "uuid": str(uuid.uuid4()),
        "jwt": "",
    }
    current_user = data['current_user_email']
    jwt_web = data['jwt_web']

    # Check if the current user is in the Whitelist array
    current_user_found = False
    for user in whitelist['Whitelist']:
        if user['email'] == current_user:
            current_user_found = True
            break
    if not current_user_found:
        return 'Current user not found', 404

    # Check if the current user's JWT matches jwt_web
    if user['jwt'] != jwt_web:
        return 'JWT does not match', 401

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
    remove_user = data['target_user_email']
    current_user = data['current_user_email']
    jwt_web = data['jwt_web']

    # Get the role of the current user
    current_user_role = None
    for user in whitelist['Whitelist']:
        if user['email'] == current_user:
            if user['owner']:
                current_user_role = 'owner'
                break
            elif user['admin']:
                current_user_role = 'admin'
                break
            break

    # Check if the current user's JWT matches jwt_web
    if user['jwt'] != jwt_web:
        return 'JWT does not match', 401

    remove_user_role = None
    for user in whitelist['Whitelist']:
        if user['email'] == remove_user:
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
        if user['email'] == remove_user:
            index = i
            break

    # Check if the user was found
    if index == -1:
        return 'User not found', 404

    # Check if the user is trying to remove themselves
    if remove_user == current_user:
        return 'Cannot remove self', 403

    # Remove the user from the Whitelist array
    whitelist['Whitelist'].pop(index)

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)
    return 'Success'

"""
/whitelist/promote
Owners can promote others to owner and admin
Admins can promote users to admins
Users cant promote anyone
"""
@app.route('/whitelist/promote', methods=['POST'])
def promote_user():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the data for the user to be promoted and the current user from the request body
    data = request.get_json()
    user_to_promote = data['target_user_email']
    current_user = data['current_user_email']
    jwt_web = data['jwt_web']
    owner_web = data["owner_web"]
    admin_web = data['admin_web']

    #JWT authentication
    if user['jwt'] != jwt_web:
        return 'JWT does not match', 401

    # Check if the current user is in the Whitelist array
    current_user_found = False
    for user in whitelist['Whitelist']:
        if user['email'] == current_user:
            current_user_found = True
            break
    if not current_user_found:
        return 'User not found', 404
    
    # Check if the user to be promoted is in the Whitelist array
    user_to_promote_found = False
    for user in whitelist['Whitelist']:
        if user['email'] == user_to_promote:
            user_to_promote_found = True
            break
    if not user_to_promote_found:
        return 'User to promote not found', 404

    # Check if the user to promote already has the permission
    for user in whitelist['Whitelist']:
        if user['email'] == user_to_promote:
            if user['owner'] and not admin_web: # so that u can give admin to a owner
                return 'User is already an owner', 400
            if user['admin'] and not owner_web: # so that u can give owner to a admin
                return 'User is already an admin', 400

    for user in whitelist['Whitelist']:
        if user['email'] == current_user:
            if user['owner'] and owner_web:  
                for user in whitelist['Whitelist']:
                    if user['email'] == user_to_promote:
                        user['owner'] = True
            if user['admin'] and admin_web: 
               for user in whitelist['Whitelist']:
                    if user['email'] == user_to_promote:
                        user['admin'] = True
            else:
                return 'Invalid Permissions', 400

    # Write the updated whitelist back to the file
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f)

    return 'Success'

"""
/whitelist/demote
Owners can demote owners to non owner
Admins can demote admins to non admin
Users cant demote anyone
"""
@app.route('/whitelist/demote', methods=['POST'])
def demote_user():
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the data for the user to be demoted    and the current user from the request body
    data = request.get_json()
    user_to_demote = data['target_user_email']
    current_user = data['current_user_email']
    jwt_web = data['jwt_web']
    owner_web = data["owner_web"]
    admin_web = data['admin_web']

    # Check if the current user is in the Whitelist array
    current_user_found = False
    for user in whitelist['Whitelist']:
        if user['email'] == current_user:
            current_user_found = True
            break
    if not current_user_found:
        return 'User not found', 404
    
    #JWT authentication
    if user['jwt'] != jwt_web:
        return 'JWT does not match', 401

    # Check if the user to be demoted to is in the Whitelist array
    user_to_demote_found = False
    for user in whitelist['Whitelist']:
        if user['email'] == user_to_demote:
            user_to_demote_found = True
            break
    if not user_to_demote_found:
        return 'User to promote not found', 404

    # Check if the user to promote already has the permission
    for user in whitelist['Whitelist']:
        if user['email'] == user_to_demote:
            if user['owner'] and not owner_web: # so that u can give admin to a owner
                return 'User is already an owner', 400
            if user['admin'] and not admin_web: # so that u can give owner to a admin
                return 'User is already an admin', 400

    for user in whitelist['Whitelist']:
        if user['email'] == current_user:
            if user['owner'] and owner_web:  
                for user in whitelist['Whitelist']:
                    if user['email'] == user_to_demote:
                        user['owner'] = False
            if user['admin'] and admin_web: 
               for user in whitelist['Whitelist']:
                    if user['email'] == user_to_demote:
                        user['admin'] = False
            else:
                return 'Invalid Permissions', 400

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
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the email of the user from the request payload
    email = request.json['email']

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
    # Read the contents of the whitelist file
    with open('whitelist.json', 'r') as f:
        whitelist = json.load(f)

    # Get the {jwt: jwt_web,email: email} of the user from the request payload
    data = request.get_json()
    jwt_web = data['jwt']
    email = data['email']

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


"""
/camera/join/<string:ip>
Adds a camera to the cameras.json file and returns you the given id of that camera
"""
@app.route('/camera/join/<string:ip>', methods=["GET"])
def join(ip):
    temp = newpi.Newpi()
    test = temp.joinnet(ip)
    return str(test)

"""
/camera/name/<string:name>/<int:id>
Takes the name and the id of the camera to rename the camera in cameras.json
"""
@app.route('/camera/name/<string:name>/<int:id>', methods=["POST"])
def rename(id, name):
    temp = tools.Tools()
    test = temp.rename(id, name)
    return str(test)

if __name__ == '__main__':
    app.run()
