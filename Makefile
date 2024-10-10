env:
	python3 -m venv env && . env/bin/activate
i:
	pip install -r requirements.txt
migration:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
run:
	python3 manage.py runserver
worker:
	python3 manage.py runworker
startapp:
	python manage.py startapp $(name) && mv $(name) apps/$(name)
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
no-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
cru:
	python manage.py createsuperuser --email=goldendevuz@gmail.com --birth_date=2005-01-24
	#make cru email=goldendevuz@gmail.com birth=2005-01-24
	#python manage.py createsuperuser --email $(email) --birth_date=$(birth)