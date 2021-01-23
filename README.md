# Diana - A Task Assistant

**Diana** aims to help you live a better day by tracking your tasks and helps you have better habits.

## Contribution

All contributions are very **welcomed!**

### Prerequisites

1. Docker

### How to get up and running

0. **_OPTIONALLY_** You can run `pipenv install --dev` in `diana-server/app` to install all python dependencies needed in this project so you can get autocompletion in your IDE -- Requires **python** and **pipenv**
1. create **.env file** in the root directory to hold the environment variables, some of environment variables are
   1. SECRET_KEY
   2. POSTGRES_DB
   3. POSTGRES_USER
   4. POSTGRES_PASSWORD
   5. EMAIL_HOST_USER
   6. EMAIL_HOST_PASSWORD
2. in the root directory run `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`
3. Then run `docker exec -it diana-server_web_1 bash`
4. In the sub-shell run
   1. `python manage.py collectstatic`
   2. `python manage.py migrate`
   3. `python manage.py createsuperuser` follow the instruction to create a new superuser

## Database

This is the way that our database is designed

![Diana db](https://user-images.githubusercontent.com/75932114/105176817-d1bb3280-5b36-11eb-9b13-9a1704f3bf31.png)

## Other links

- [Diana mobile app](https://github.com/softshape-team/diana-mobile)
