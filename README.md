## Environment:
- Python version: 3.7
- Django version: 2.2.16

## Commands

+  install:
```virtualenv env1; source env1/bin/activate; pip install -r requirements.txt;```

+ run:
```source env1/bin/activate; python manage.py makemigrations && python manage.py migrate --run-syncdb && python manage.py runserver 0.0.0.0:8000```

+ test:
```rm -rf unit.xml;source env1/bin/activate; python manage.py test```