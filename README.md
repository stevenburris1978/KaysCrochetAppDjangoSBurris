## INF601VA - Advanced Programming in Python
# Steven Burris
# 11-10-2023
# *Final Project SBurris*
# *Kay's Crochet App*

# Github commits to Main Branch instead of Master at: 
[Gituhb](https://github.com/stevenburris1978/KaysCrochetAppDjangoSBurris/tree/main)
# The code for Kay's Crochet works without being changed both locally and through Heroku to the domain:
[Kay's Crochet](https://www.kayscrochet.us)
# *Description*
### With this app, admin can add an item that has title input, description input, image input, and price; and get customer orders emailed to them and sent to the django admin Customer_order table.
### Admin cam also add item choices for users to vote on for future crochet items to be made. 
### Users can log in and see the items, like the items, vote on the choices, buy the items, and get an invoice to their saved email.

# API, Platform
This app uses the Stripe API for payments.
This app uses AWS (Amazon S3) to store media files.
This app uses the Heroku platform for production to deploy to [Kay's Crochet](https://www.kayscrochet.us).

# *Social App Install Instructions*
Please copy the following command in the terminal for all the package downloads needed to run the program:
```
pip install -r requirements.txt
```
# How to set up these .env variables - they need to be in a .env root directory with your keys and email server info for local development to work.
DJANGO_SECRET_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
DJANGO_EMAIL_HOST=
DJANGO_EMAIL_HOST_USER=
DJANGO_EMAIL_HOST_PASSWORD=
DJANGO_EMAIL_PORT=
DJANGO_EMAIL_USE_TLS=
# How to set up database
(this will create any SQL entries that need to go into the database)
```
python manage.py makemigrations kayscrochetapp
```
(this will show tables created)
```
python manage.py sqlmigrate kayscrochetapp 0001
```
(this will apply the migrations)
```
python manage.py migrate
```

# How to create the main admin user
(this will create the administrator login to log into Kay's Crochet App administration page)
```
python manage.py createsuperuser
```

# Then start app
```
python manage.py runserver
``` 
and go to [ app home page](http://127.0.0.1:8000)

# This is the link to go to the admin page to add, edit, and delete the Social App post items
Administration url : [Administration url](http://127.0.0.1:8000/admin)