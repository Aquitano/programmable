# social_app

It is recommended to use a virtual environment.

Then the requirements in the requirements.txt can be installed using the command:
```
pip install -r requirements.txt
```

Then you need to run the migrations to set up the sqlite database:
```
python manage.py migrate
```

Additionally, you can add an admin user:
```
python manage.py createsuperuser
```
With this user you can access the [admin page](http://localhost:8000/admin) that is provided by django.