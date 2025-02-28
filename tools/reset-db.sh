rm -r src/instance migrations
flask --app src/app db init
flask --app src/app db migrate
flask --app src/app db upgrade