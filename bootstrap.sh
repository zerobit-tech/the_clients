pip install --upgrade virtualenv
virtualenv venv --python=python3.9
source venv/bin/activate

python -m pip install --upgrade pip
cd sample_project/
pip install -r requirements.txt

cd ..

python setup.py sdist
source venv/bin/activate
cd sample_project/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 9022