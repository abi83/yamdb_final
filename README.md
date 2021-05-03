На русском смотри: [README.ru.md](README.ru.md)

_**YamDB** - a study project, made in small group of students in December 2020. 
It is a service for reviewing and commenting works of fiction, such a lite version of ImDB. API only_

Titles, Reviews and Comments models are done. A Title has relation to one Category and
several Genres. Titles, Reviews and Comments access rules depends on user role: admin, 
moderator or user. Custom user model is implemented: with email registration and JWT Token 
authentication. Managing users allow only for admin.

Project link: http://yamdb.kromm.info/

Dockerfile and docker-compose.yaml files are in source code, for quick deploy.
Fixture commands are also included:
`python manage.py create-users` and `python manage.py populate-titles`

I hope this project would be useful for next generation Yandex.Practicum students and for everyone who studies Python

![main workflow](https://github.com/abi83/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)

Project is temporary running on http://178.154.209.27/api/v1/