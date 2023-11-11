## INF601VA - Advanced Programming in Python
# Steven Burris
# 11-10-2023
# *Final Project SBurris*
# *Kay's Crochet App*

# *Description*
### With this app, admin can add an item that has title input, description input, image input, price and set choices for example, Like unlike, to vote on in each post
### Users can log in and see the items, vote on the choices, and buy the items
# *Social App Install Instructions*
Please copy the following command in the terminal for all the package downloads needed to run the program:
```
pip install -r requirements.txt
```

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