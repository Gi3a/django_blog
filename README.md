# django_blog
blog on django/python

[ Use 'python manage.py runserver' to start ]

1) django-admin startproject Project | # Creating project

2) python manage.py startapp core | # Creating app (core)

3) python manage.py migrate | # First migration (creating sqllite db3)

----------------------------------------------------------------------------

4) python manage.py createsuperuser | # Creating User Admin, password 123456

5) python manage.py makemigrations core | # When created model => makemigrations

6) python manage.py migrate core | # Then we migrate it
