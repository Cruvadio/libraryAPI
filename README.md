# API для работы с библиотекой. 
## Поднятие с помощью docker-compose
~~~bash
docker-compose up -d --build
~~~
## Создвние миграций в базе данных: ##
~~~bash
docker-compose exec web alembic revision --autogenerate -m "Initial revision"
~~~~
~~~bash
docker-compose exex web alembic upgrade head
~~~

Документация к API после сборки находится по адрему localhost:8002/docs
