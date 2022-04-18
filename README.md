# Book List
## General info
Django project, where you can add books to your own library/ list.
How to fill your list:

* import books using external api (google books api) - you just
have to choose title, author or ISBN
to be searched.
* create them yourself with validation included.

Data are stored in postgres db. Whole project is build on docker.


Whole project is available on heroku, 
[click here](http://book-list-martyna.herokuapp.com/books/list/).


## Setup
To run app:
```
$ make build
```
To recreate docker image:
```
$ make recreate
```

In order to run migrations:
```
$ make migrate
```

To create super user in a running container:
```
$ make super
```

To check logs for app:
```
$ make logs_app
```

To check logs for database:
```
$ make logs_db
```

To find stylistic errors:
```
$ make lint
```

When container is running, documentation generated by 
swagger is available. But when it comes to rest there is only one endpoint.

[click here](http://localhost:8000/docs/).