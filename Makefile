mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser

dumpdata:
	python3 manage.py dumpdata --indent=2 apps.Product > products.json