build:
	pipenv lock -r > requirements.txt
	docker build -t dms:latest .

check:
	safety check
	pylint --django-settings-module=dms.settings dms/*
	bandit -r dms/
	python dms/manage.py check

test:
	coverage run --source=dms dms/manage.py test dms
	coverage report

run:
	python dms/manage.py migrate
	python dms/manage.py runserver
	# docker run --rm -d -p 8000:8000 --name dms dms:latest

push: check test
	git push
