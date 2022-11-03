# StudentResultSaverWeb
A system to save and display results of students. Hopefully the final version this time.
The system is web based this time and made with the framework Django.


-Command line:
cd website
cd ..

-Activate virtual environment without relaunch
.env/Scripts/Activate.ps1

-To create Django project:
django-admin startproject website

-To run server type in terminal:
py manage.py runserver

-To create django-app:
py manage.py startapp main

-To update (commit) database:
py manage.py migrate

-To stage database changes:
py manage.py makemigrations main

-Get into manual manager control:
py manage.py shell

-My admin is "John_admin" (standard password)
python manage.py createsuperuser John_admin
http://127.0.0.1:8000/admin/




-Better jinja-html add in settings.json (makes html a bit worse...):
"files.associations": {"*.html": "jinja-html"}

-Fix annoying sql-error in pylint. In file .pylintrc:
ignored-classes=SQLObject,Registrant,scoped_session