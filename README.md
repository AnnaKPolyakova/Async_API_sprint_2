# Проектная работа 5 спринта

Командная работа https://github.com/AnnaKPolyakova/Async_API_sprint_2

Создает индексы person, genre и заполняет данными из бд postgres
(запуск через db_updater.py в отдельном контейнере)
Апи для получения данных из es о фильмах, персонах, жанрах  

Технологии и требования:
```
Python 3.9+
Fast API
```

### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

### Запуск приложения

#### Перед запуском проекта создаем переменные окружения
Создаем в корне .env и добавляем в него необходимые переменные  
Пример в .env.example - для запуска приложения целиком в docker  
Пример в .env.example-local - для запуска приложения локально и частично в docker

#### Запуск проекта полностью в контейнерах docker

* `docker-compose up --build`

Документация по адресу:  
http://0.0.0.0/api/openapi
АПИ:
http://0.0.0.0/api/v1/....


Для остановки контейнера:  
* `docker-compose down --rmi all --volumes`

#### Запуск проекта частично в контейнерах docker (redis и elastic)

* `docker-compose -f docker-compose-local.yml up --build`
* `python src/main.py`
* `python -m etl.db_updater`

Документация по адресу:  
http://0.0.0.0:8000/api/openapi
АПИ:
http://0.0.0.0:8000/api/v1/....

Для остановки контейнера:  
* `docker-compose -f docker-compose-local.yml down --rmi all --volumes`

