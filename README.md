# Feer-Club
Manage Them Beers

## Getting started

- Install python3
- `pip install -r requirements.txt`
- `cd feer_club/`
- `python manage.py runserver`
- `python manage.py createsuperuser` to create a user
- Go to `http://127.0.0.1:8000/admin` for admin page
- Go to `http://127.0.0.1:8000/feer` for beers! Cheers!

### Seeding the Database
The `feer` app has fixtures for a number of models in the `fixtures` directory in the `feer` app. Load these using `python manage.py loaddata <fixture>`.
