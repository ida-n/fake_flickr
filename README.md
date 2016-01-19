# README #

### What is this repository for? ###

Django exercise app for sharing funny Pics

### Dependencies ###

This app was built using:
* python 3.5.1
* Django==1.9.1
* Pillow
* django-registration-redux


### How to set up ###
This application is developed with python 3.5.1 and Django 1.9.1     
https://www.python.org/downloads/release/python-351/   
https://docs.djangoproject.com/en/1.9/releases/1.9/
It is recommended that you start by creating a new ``virtualenv``. 
```
pip install virtualenv # install virtualenv
virtualenv venv # Create virtualenv
source venv/bin/activate # Active virtualenv on linux
source venv\scripts\activate # Active virtualenv on windows
```
Following links can help you set up:    
http://docs.python-guide.org/en/latest/dev/virtualenvs/    
https://docs.python.org/3/library/venv.html

Clone this repository
```
clone https://github.com/inakhostin/fake_flickr.git
```

Install the requirements by running:
```
pip install -r requirements.txt 
```
Create you database tables by running:
```
#!python

python manage.py migrate
```
Create and admin user by running:
```
#!python

python manage.py createsuperuser
```
Start your local server by running:
```
#!python

python manage.py runserver
```
This will start a development server at http://127.0.0.1:8000/

Navigate to http://127.0.0.1:8000/faker to access the faker app    
Navigate to http://127.0.0.1:8000/admin to access the admin app
