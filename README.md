# Social Media API
> **Welcome to the Social Media API** 

###### The API allows users to create profiles, follow other users, create and view posts, manage likes and comments, and perform basic social media actions.

## Key Features

* **Authentication:** Users undergo secure registration and login processes, receiving JWTs for authenticated access.
* **User Profile Management:** Users can create and update their profiles, incorporating details such as profile pictures, bios, and other relevant information.
* **Follow/Unfollow System:** Establish connections by following and unfollowing other users. Track the list of followers and those being followed.
* **Post Creation and Retrieval:** Users can craft text-based posts and optionally attach images. Retrieve personal posts and those from followed users.
* **Likes and Comments:** Users have the option to like and unlike posts, view their liked posts, and engage with comments on posts.
* **Scheduled Post Creation:** Schedule post creation using Celery, allowing users to select the time for post publication.
* **API Permissions:** Strictly enforce permissions, ensuring that only authenticated users can create posts, like content, and follow/unfollow users. Users retain control over their own posts, comments, and profiles.
* **API Documentation:** Thorough documentation, available through the Swagger UI, provides clear instructions on each endpoint. Sample API requests and responses are included.
## DB structure 

![DB structure](DB-structure.png)

## Installation
### Using GitHub

- Ensure you have `Python 3` installed.
- Install `PostgreSQL` and create db.
- Clone repository to your local machine and change working directory:

```bash
git clone https://github.com/o-davydova/Social-Media-API
cd Social-Media-API
```
- Create venv & Activate it:
`python3 -m venv venv`
`source venv/Scripts/activate`

- Install requirements:
`pip install -r requirements.txt`

- Create new Postgres DB & User
- Set required data:
```
set DJANGO_SECRET_KEY=<your secret key>
set DJANGO_DEBUG=<your debug value>
set DJANGO_ALLOWED_HOSTS=<your allowed hosts>

set POSTGRES_ENGINE=<your Postgres engine>
set POSTGRES_HOST=<your Postgres host>
set POSTGRES_DB=<your Postgres database>
set POSTGRES_USER=<your Postgres user>
set POSTGRES_PASSWORD=<your Postgres password>

set CELERY_BROKER=<your Celery broker URL>
set CELERY_BACKEND=<your Celery result backend>
```
- Run migrations:`python manage.py migrate`
- Run Redis Server: `docker run -d -p 6379:6379 redis`
- Run Celery worker for task handling: `celery -A social_media worker -l INFO`
- Run app: `python manage.py runserver`

### Run with docker

`Docker` should be installed.

```
docker-compose build
docker-compose up
```

## Getting access
- create a user via **/api/user/register**
- get access token via **/api/user/token**
