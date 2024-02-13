cd django-scian
python setup.py sdist
pip install .
cd ..

python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver