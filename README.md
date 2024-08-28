Steps to run setup this project:
1. Create virtual env
2. Install all the dependecies which is listed in requiremnts.txt using "pip install -r requiremnts.txt"
3. Than run python manage.py runserver


Steps to build docker images:
1. Install docker desktop or docker cli
2. docker build -t your_django_app .
3. docker run -p 8000:8000 your_django_app
