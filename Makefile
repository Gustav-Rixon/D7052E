# Makefile tasks

# https://superuser.com/questions/370575/how-to-run-make-file-from-any-directory

build:
	cd frontend/ && npm install

start:
	cd frontend/ && npm run start

stop:
	cd frontend/ && npm run stop

flask:
	cd backend/flask/ && python3 app.py

