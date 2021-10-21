This is for a Flask backend which has no db.

1. Install dependencies:
```pipenv install --dev -r dev-requirements.txt --python=python3 && pipenv install -r requirements.txt```
1. Create a .ENV file based on the example with proper settings for your
   development environment.
1. Get into your pipenv (```pipenv shell```) and run your flask app (```flask run```).

If you add any python dependencies to your pipfiles, you'll need to regenerate your requirements.txt before deployment.
   You can do this by running ```pipenv lock -r > requirements.txt```

If problems arise, try deleting .venv and repeating ```pipenv install...``` etc.

## Deploy to Heroku

1. Create a new project on Heroku
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)
1. Run ```heroku login```
1. Login to the heroku container registry: ```heroku container:login```
1. Push your docker container to heroku from the root directory of your project.
   (This will build the dockerfile and push the image to your heroku container registry.)

   ```heroku container:push web -a {NAME_OF_HEROKU_APP}```
1. Release your docker container to heroku via

   ```heroku container:release web -a {NAME_OF_HEROKU_APP}```
1. Under Settings find "Config Vars" and add any additional/secret/apikey .env variables.
1. Run
```docker system prune -a -f```
in order to keep things from getting bloated.
[From @chrishakos:
"You're also probably on an AWS ec2 via heroku which also needs the occasional apt-get clean and ```apt-get autoremove```."]
