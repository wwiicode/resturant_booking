# set virtual environment
run `pipenv shell`

then `pipenv install`


# Connect the Little Lemon back-end to MySQL
mysql.server start
(just hit 'enter' for password)

# once inside mysql, you can check existed user registered
SELECT user, host FROM mysql.user;

# test the booking funciton
run `python manage.py runserver` to spin up the Django app
hover over to booking to test functionality of the /book/ API





